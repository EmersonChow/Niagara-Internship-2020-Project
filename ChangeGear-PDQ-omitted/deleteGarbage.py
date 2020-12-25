from modifyPerson import deleteItem
import csv
import credentialHandler

def deleteGarbage(sID: str, filename: str):
    fullFile = "csvContainer/" + filename
    with open(fullFile, 'r', newline = "") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "" and row[2] == "" and row[3] == "" and row[4] == "":
                deleteItem(sID, row[5])


#This says: if the file is being run, then do this; if it is imported then these lines won't run
if __name__ == "__main__":
    sId = credentialHandler.login()
    deleteGarbage(sId, "All Resources.csv") #change based on your naming for all resources.csv
    credentialHandler.logout(sId)
