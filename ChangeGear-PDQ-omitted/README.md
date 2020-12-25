#Integration of ChangeGear (IT service manager) and PDQ (systems management tool)
Sending data from one database to another and clearing bad inputs. 

Secondary program: Delete Garbage clears bad inputs left in ChangeGear.

Original Approach: CSV file transfer information
Secondary Approach: Use Oracle's Integration Cloud (OIC) to perform integration based on a timed basis (Rejected by department managers due to perceived time constraints)

Final Approach - uses 3 csv files for data and calls the changegear api to upload the info to the database. Csv files need to be "manually" acquired through SQL scripts & powershell scripts - some of which is included here. 

Manual entry: 6min 48s/item
integration speed: 11s/item
time savings: 6min 37s/item
Current item count: 3298
Estimated savings ~363 hours, 40min, 7.06 seconds/run (future runs should be faster for both the manual integration as well as the automated approach - manual inputter knows more and automated doesn't have to input all information, just check if it is touched.)




Code Written during: June 2020-Auguest 2020
Folder approved to be made public by manager: Jack Kaylor 9/1/2020. (with certain omissions to hide secure information)
12/24/2020 Omissions made for security and replaced on github in public folder. 