import credentialHandler
import modifyPerson
import retrieveFromCMDB
import unittest
from csvContainer import csvConverter
from integrate import payloadMaker


class TestCredentialHandler(unittest.TestCase):
    def testLogin(self):
        sID = credentialHandler.login()
        self.assertNotEqual(sID,None)
    
    def testLogout(self):
        sID = credentialHandler.login()
        self.assertEqual(type(credentialHandler.logout(sID)), type(None))

class TestCsvConverter(unittest.TestCase):
    def testCreatePDQDictType(self):
        myPDQdict = csvConverter.createPDQDict("New Report.csv")
        self.assertEqual(type(myPDQdict),dict)

    def testCreatePDQDictKey(self):
        myPDQdict = csvConverter.createPDQDict("New Report.csv")
        self.assertEqual(myPDQdict[#This information has been omitted])

class TestRetrieveFromCMDB(unittest.TestCase):
    def testGetIndividual(self):
        sID = credentialHandler.login()
        personDict = retrieveFromCMDB.getIndividual(sID, "#This information has been omitted")
        self.assertEqual(type(personDict), dict, msg="This may fail if user: ASALGADOLT was removed. Double check before ignoring.")
        credentialHandler.logout(sID)

    def testGetSerialNumber(self):
        sID = credentialHandler.login()
        personDict = retrieveFromCMDB.allResourcesViewFilteredBySerialNumber(sID, "#This information has been omitted")
        self.assertEqual(type(personDict), dict, msg="This may fail if user: ASALGADOLT was removed. Double check before ignoring.")
        credentialHandler.logout(sID)

class TestModifyPerson(unittest.TestCase):

    def testCreateModifyDeleteItem(self):
        sID = credentialHandler.login()
        first_pdq_list = [#This information has been omitted"]
        first_people_list = [#This information has been omitted]
        serial_number = "#This information has been omitted"
        my_str = f'{{'
        exists = True 
        payload = payloadMaker(my_str,first_pdq_list, serial_number, exists, first_people_list,)
        payload += f'}}'
        oID = modifyPerson.createPerson(sID,payload)
        #Check that individual was created
        self.assertNotEqual(retrieveFromCMDB.getIndividual(sID, oID), None)
        thisDict = retrieveFromCMDB.getIndividual(sID, oID)
        eTag = thisDict["Field(This information has been omitted)"]
        name = "myNewName"


        payload = f'{{\r\n    "Field(This information has been omitted)": {eTag}, \r\n    "Field(This information has been omitted)": "{name}"}}'

        newPerson = modifyPerson.updatePerson(sID, oID, payload)
        #check that it was not deleted
        self.assertEqual(newPerson["Field(This information has been omitted)"], 1)
        self.assertNotEqual(retrieveFromCMDB.getIndividual(sID, oID), None)

        #Check that eTag got incremented - meaning that there was an update performed
        personDict = retrieveFromCMDB.getIndividual(sID, oID)
        self.assertEqual(personDict["Field(This information has been omitted)"], eTag+1)

        modifyPerson.deleteItem(sID, oID)
        #check that it is deleted
        self.assertEqual(retrieveFromCMDB.getIndividual(sID,oID)["IsDeleted"],True)
        credentialHandler.logout(sID)
        


if __name__ == "__main__":
    unittest.main()
