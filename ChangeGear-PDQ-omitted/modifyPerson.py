import requests
def deleteItem(sID: str, oID: str) -> str:
    """takes session id and oID as str and deletes individual. Returns a message regarding http status.
    200 if person is deleted, other if error. NOTE: This does not mean the item cannot be found via OID, IT STILL
    EXISTS WITHIN CHANGEGEAR!!!"""
    oID = str(oID) #just in case it was in int
    url = "Niagara's API call + oid(#This information has been omitted)" + oID

    payload = {}
    headers = {
    'sessionid': sID
    }
    response = requests.request("DELETE", url, headers=headers, data = payload)

    if(response.status_code == 200):
        print("Succesfully deleted item with OID: " + oID)
    else:
        print("There was a problem deleteing item with OID: " + oID + ". Http Status Code: " + response.status_code)


def createPerson(sID: str, body: str) -> str:
    """takes session id and payload as str and creates individual. Returns the person's OID in str
    
    Sample Payload:
    payload = " (#This information has been omitted)"

    """

    url = "Niagara's API call  (#This information has been omitted)"

    headers = {
      'sessionid': sID,
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data = body)
    return str(response.json()["ID"])


def updatePerson(sID: str, oID: str, body: str) -> dict:
    """takes session id, oid, and things to update (including an tag number) and returns the updated person.
    Sample payload: payload = "(#This information has been omitted)" """
    oID = str(oID) #just in case it was in int
    url = "Niagara's API call +(#This information has been omitted)" + oID

    
    headers = {
    'sessionid': sID,
    'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data = body)
    return response.json()[0]