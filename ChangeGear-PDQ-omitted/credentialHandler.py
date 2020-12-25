import requests

def login() -> str:
  """returns the sessionId in str format"""

  url = "Niagara API url (This information has been omitted)"

  payload = "{\r\n   \"Field(#This information has been omitted)\"\r\n}\r\n"
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data = payload)

  return response.json()["sessionId"]


def logout(sID: str): 
  """Takes sessionid, prints status message depending on if logout successful"""
  url = "Niagara API url (This information has been omitted)"
  headers = {
    'sessionId' : sID
  }
  response2 = requests.post(url, headers = headers)
  if(response2.status_code == 200):
    print("Successfully logged out.")
  else:
    print("There was a problem logging out. HTTP error code: " + str(response2.status_code))

