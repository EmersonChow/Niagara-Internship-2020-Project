import csv 

def createPDQDict(filename: str) -> dict:
    """
        Parameters:
        filename: name of csv file with PDQ data
        Returns:
        dict with serial numbers as key and 
        [Name, OSName, SystemFamily, ADDisplayName, BiosAssetTag, CurrentUser]
        as value
    """
    fullFile = "csvContainer/" + filename
    with open(fullFile, 'r', newline = "") as f:
        reader = csv.reader(f)
        PDQdict = {}
        for row in reader:
            if(row[4]) != "": #ignore empty serial number rows
                x = row[1:4] #ignore the first column, computer id kinda pointless though may let us skip a sort in SQL
                x.extend(row[5:7])
                currentUser = row[7]
                if "NIAGARAWATER\\" in currentUser:
                    splitByBackslash = currentUser.split("\\")
                    splitBySpace = splitByBackslash[1].split(" ")
                    x.append(splitBySpace[0])
                else:
                    x.append(currentUser)
                PDQdict[row[4]] = x         #overwrites the duplicates (most recently added version used)
        if "SerialNumber" in PDQdict.keys():
            PDQdict.pop("SerialNumber") #remove column names from the dict
        if "" in PDQdict.keys():
            PDQdict.pop("")
        return PDQdict

def createPeopleDict(filename:str) -> dict:
    """
        Parameters:
        filename: name of csv file with people
        Returns:
        dict with ExternalAccountUID in str as key and [oid,dept,location] in ints
    """
    fullFile = "csvContainer/" + filename
    with open(fullFile, 'r', newline = "") as f:
        reader = csv.reader(f)
        peopleDict = {}
        for row in reader:
            if row[3] == "NULL":
                row[3] = row[3].lower()
            if row[4] == "NULL":
                row[4] = row[4].lower()
            x = [row[0],row[3], row[4]] #[oid, department, location]
            peopleDict[row[5]] = x #ExternalAccountUID
        if "ExternalAccountUID" in peopleDict.keys():
            peopleDict.pop("ExternalAccountUID") #remove row that contains titles
        if "" in  peopleDict.keys():
            peopleDict.pop("")
        return peopleDict

def createAdDict(filename:str) -> dict:
    """
        Paramters:
        filename: name of csv file with Active Directory info
        Returns:
        dict with sAMAccount as key and objectSid as value
    """
    fullFile = "csvContainer/" + filename 
    with open(fullFile, 'r', newline = "") as f:
        reader = csv.reader(f)
        aDDict = {}
        for row in reader:
            if len(row) == 2: #escape the first line of form #TYPE Selected.Microsoft.ActiveDirectory.Management.ADUser
                aDDict[row[0]] = row[1] #row[0] holds sAMAccountUID, row[1] holds objectSid
        if "" in aDDict.keys():
            aDDict.pop("") #Remove the empty key
        if "sAMAccountName" in aDDict.keys():
            aDDict.pop("sAMAccountName") #remove the column name key
        return aDDict