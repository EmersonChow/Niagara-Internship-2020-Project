from csvContainer.csvConverter import createPDQDict
from csvContainer.csvConverter import createPeopleDict
from csvContainer.csvConverter import createAdDict
import credentialHandler
import retrieveFromCMDB
import modifyPerson
from datetime import datetime 

#Checklist before running:
#   Updated "New Report.csv", "cgPeopleF.csv",  "All Resources.csv", "userObjectSidShort.csv" in csvContainer folder
#       Get New Report.csv by running SQL script (from PDQ SQL Query.txt) in PDQ new sql report
#       Get cgPeopleF.csv from Carlos Gomez (running another SQL Query)
#       Get userObjectSidShort.csv by running the powershell script from Jack
#       DELETE GARBAGE (clears bad inputs in system)
#       Get All Resources.csv by exporting from (#This information has been omitted)
#           NOTE: Views MUST be set to critical,name,type, description,location,CI #,Asset Tag
#                   AND in that order


#Extras for future reference in case someone wants to use this script to run more than just classic workstations
        
        #ResourceType 42 = Base Case - just lists workstation
        #ResourceType 111 = Windows 10
        #Resource Type 109 = Windows 8
        #Resource Type 100 = Windows 7
        #86 = Mac OS X
        #41 = Windows XP Professional
        #33 = Copier
        #5 = Linux
        #30 = Printer
        #37 = Windows Server

def resourceTypeSelector(osName:str) -> int:
    """
        Parameters:
            osName (str): osName field from PDQ export
        Return:
            int: resourceTypeNumber
    """
    if "Windows 10" in osName:
        return 111
    elif "Windows 8" in osName:
        return 109
    elif "Windows 7" in osName:
        return 100
    elif "Mac OS X" in osName:
        return 86
    elif "Windows XP" in osName:
        return 41
    else:
        return 42

def payloadMaker(body: str, pdqInput: [], sNum: str, personExists: bool, peopleInput: [int]) -> str:
    """ 
        Parameters:
        body(str): payload string
        pdqInput([]): PDQdict field values 
        sNum(str): serialNumber
        personExists (bool): whether or not person found in cgPeople/currentUser listed
        peopleInput([int]): peopleDict field values
        
        Return:
        A string containing the payload
    """

    payload = body + f'\
        \r\n   "Field(#This information has been omitted)": "{pdqInput[0]}", \
        \r\n   "Field(#This information has been omitted)": {resourceTypeSelector(pdqInput[1])},\
        \r\n   "Field(#This information has been omitted)": "{pdqInput[2]}",\
        \r\n   "Field(#This information has been omitted)": "{sNum}"\
        '
    if pdqInput[4] != "":
        payload += f',\r\n   "Field(#This information has been omitted)":"{pdqInput[4]}"'
    else:
        payload += f',\r\n    "Field(#This information has been omitted)": "No Asset Information"'
    
    if personExists:
        payload += f'\
        ,\r\n   "Field(#This information has been omitted)":{peopleInput[0]},\
        \r\n   "Field(#This information has been omitted)":{peopleInput[1]},\
        \r\n   "Field(#This information has been omitted)":{peopleInput[2]}\
        '
    return payload

def changeChecker(item:dict, pdqInput: [], peopleInput:[],personExists) -> bool:
    """
    Checks if item has had any changes before calling update api on it
    Parameters: 
    item (dict): dict 0 returned from serial number search
    pdqInput([]) : information to be entered (#This information has been omitted)
    peopleInput([]): information about person (#This information has been omitted)
    Returns:
    True if there is a difference
    False otherwise
    """
    assetData = pdqInput[4]
    if pdqInput[4] == "":
        assetData = "No Asset Information"
    resourceData = resourceTypeSelector(pdqInput[1])
    if personExists:
        allParts = ["Field(#This information has been omitted)"]
        fullList = [pdqInput[0]]
        fullList.append(resourceData)
        fullList.append(pdqInput[2])
        fullList.append(assetData)
        fullList += peopleInput
        fieldsAndAnswers = zip(allParts, fullList)
        for field, answer in fieldsAndAnswers:
            if(str(item[field])) != str(answer):
                return True
        return False
    else:
        allParts = ["Field(#This information has been omitted)"]
        pdqInputFixed = [pdqInput[0]]
        pdqInputFixed.append(resourceData)
        pdqInputFixed.append(pdqInput[2])
        pdqInputFixed.append(assetData)
        fieldsAndAnswers = zip(allParts, pdqInputFixed)
        for field, answer in fieldsAndAnswers:
            if(str(item[field])) != str(answer):
                return True
        return False


if __name__ == "__main__":
    startTime = datetime.now()
    #login session id
    sID = credentialHandler.login()

    #Create PDQ dictionary from the csv file
    PDQdict = createPDQDict("Short New Report.csv")


    #Create People dictionary from the csv file
    peopleDict = createPeopleDict("cgPeopleF.csv")

    #Create Active Directory dictionary from the csv file
    adDict = createAdDict("userObjectSidShort.csv")
    
    #test error log
    log = []

    for key in PDQdict.keys():
        #for every serial number, call the api for the view.
        item = retrieveFromCMDB.allResourcesViewFilteredBySerialNumber(sID,key)
        #payloads are practically the same, you just need eTag for updating

        #currentUser
        currentUser = PDQdict[key][5] #currentUser field
        
        adId = ""
        personInfo = []
        exists = False 

        #get the active directory identifying id if it exists
        if currentUser in adDict.keys():
            adId = adDict[currentUser]
        
        #
        if adId != "":
            if adId in peopleDict.keys():
                personInfo = peopleDict[adId]
        
        if personInfo != []:
            exists = True
        

        if len(item.keys()) != 0:
            #Means it exists; update
            if changeChecker(item,PDQdict[key],personInfo,exists):
                #if there is a difference, then call update api
                payload = f'{{\r\n    "Field(#This information has been omitted)": {item["Field(#This information has been omitted)"]},'
                finishedPayload = payloadMaker(payload, PDQdict[key], key, exists, personInfo)
                finishedPayload += f'}}\r\n'
                try:
                    #the update api has trouble if the data already exists as it should be in cg
                    updatedPerson = modifyPerson.updatePerson(sID,item["Field(#This information has been omitted)"], finishedPayload) 
                except:
                    log.append(key) 

        else:
            #if it doesn't; create a person
            payload = f'{{\r\n    "Field(#This information has been omitted)": 0,'
            finishedPayload = payloadMaker(payload, PDQdict[key], key, exists, personInfo)
            finishedPayload += f'}}\r\n'
            try:
                #print(finishedPayload)
                createdPersonOID = modifyPerson.createPerson(sID,finishedPayload)
            except:
                log.append("Create Person Error. Serial Number: " + str(key))

    #write errors to error.txt
    with open("error.txt", 'w') as f:
        for error in log:
            f.write(str(error) + "\n")
    print(log)
    #logout so no one else can use the sID
    credentialHandler.logout(sID)
    endTime = datetime.now()
    print("Total time is: " + str(endTime - startTime))

