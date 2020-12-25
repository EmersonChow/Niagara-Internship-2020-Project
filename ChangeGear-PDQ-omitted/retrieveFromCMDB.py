import requests

def getIndividual(sID: str, oID: str) -> dict :
    """takes session id and oid, returns all data about the corresponding person in a dict"""
    url = "Niagara's API call + OID(#This information has been omitted)" + oID
    headers = {
        'sessionId' : sID
    }
    response = requests.get(url,headers = headers)
    if(response.status_code == 200):
        if len(response.json()) >0:
            return response.json()[0]
    else:
        print("Error has occurred, http response status code: " + response.status_code + " returned.")

def allResourcesViewFilteredBySerialNumber(sID:str, serialN:str) -> dict:
    """takes session id and serial number, returns all data corresponding to that entry in a dict"""
    url = "#Niagara's API call +filter (#This information has been omitted) = '" + serialN + "'"
    headers = {
    'sessionid': sID
    }

    response = requests.request("GET", url, headers=headers)
    if(response.status_code == 200):
        if len(response.json()) > 0:
            #further research has revealed that search by serial number does not give the full view
            #it takes first returned instance of that serial number(I believe it means the oldest based on CI#)
            #and does a search on that one's CI number for the full view
            firstMatch = response.json()[0]
            return getIndividual(sID,str(firstMatch["Field(This information has been omitted)"]))

        else:
            return {}
    else:
        print("Error has occurred, http response status code: " + response.status_code + " returned.")

