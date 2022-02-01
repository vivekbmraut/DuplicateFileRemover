# Duplicate File Remover<br>
This is python(Cython) script which removes duplicate files for every time interval that user mentions from given directory and places the names of removed directory in log file which will be emailed to user<br><br>

## SetUp<br>
### Steps
1. Ensure you have python.exe installed, if not then go through [this_link](https://www.python.org/downloads/) and do the whole setup
2. If python setup is completed then you have to install schedule module by command<br>
`pip install schedule `
3. Clone this repository


## Script Execution<br>
1. Run the file named DuplicateFileRemover.py by following command<br>
` python DocumentFileRemover first-arg second-arg third-arg`<br>
- *first-arg*:It Represents your path to Directory from where you want to delete duplicates
- *second-arg*:It Represents time interval, this script runs continuously and every time interval it would delete duplicate from given directory and will email you to email address given in third-arg 
- *third-arg*:It Represents email-address, this email-address will recieve a log file which contains filenames which were duplicate<br>
2. After this script will prompt to enter email address of sender and password before entering credentials be sure you have enabled access of third party app for your email address
- for google its mostly goes by enabling less secure app in account settings


### * REMEMBER THIS WILL RUN CONTINUOUSLY AND WILL MAIL LOG FILE EVERY TIME INTERVAL YOU MENTIONED *
### * STOP EXECUTION BY KEYBOARD INTERRUPT CTRL+C*