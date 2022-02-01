from sys import argv
import os
import hashlib
import datetime
import time
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import schedule
import urllib
import getpass

def CheckConnection():
    try:
        urllib.request.urlopen("http://172.217.14.228")
        return True
    except Exception:
        return False

def MailIt(SendersEMail,SendersPassword,RecieversMail,FilePath,MailContent):

    if not CheckConnection():
        print("CHECK NETWORK CONNECTION AT YOUR END")
        return 0

    sr=re.search(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$",RecieversMail)
    if sr==None:
        print("Enter Valid email")
        return

    if not os.path.exists(FilePath):
        print(f"\'{FilePath}\' Path doesn\'t exist")
        print("Returning...Without Mailing")
        return

    msg=MIMEMultipart("alternative")
    msg["Subject"]="DUPLICATE FILE LOGS"
    msg["From"]=SendersEMail
    msg["To"]=RecieversMail

    msg.attach(MIMEText(MailContent,"plain"));

    with open(FilePath,"rb") as attachment:
        file=MIMEBase("application","octet-stream")
        file.set_payload(attachment.read())

        encoders.encode_base64(file)
        file.add_header("Content-Disposition",f"attachment; filename={os.path.basename(FilePath)}")
        msg.attach(file)
    try:
        start=time.time()
        Vsmtp=smtplib.SMTP("smtp.gmail.com",587)
        Vsmtp.connect("smtp.gmail.com",587)
        Vsmtp.ehlo()
        Vsmtp.starttls()
        Vsmtp.ehlo()
        Vsmtp.login(SendersEMail,SendersPassword)
        Vsmtp.sendmail(SendersEMail,RecieversMail,msg.as_string());
        print(f"Mailing SESSION TOOK {time.time()-start} secs")
    except Exception as e:
        print(e)
    finally:
        Vsmtp.quit()



def get_checksum(filepath,blocksize=1024):
    if not os.path.exists(filepath):
        print("CheckSum cant be detected for invalid file path")
        return None
    md=hashlib.md5()
    with open(filepath,"rb") as fd:
        data=fd.read(blocksize)
        while(len(data)>0):
            md.update(data)
            data=fd.read(blocksize)
    return md.hexdigest()

def createLog(dirname="PyLogDir"):
    fname=f"DuplicateFileLog_{time.time()}.log"
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    fpath=os.path.join(dirname,fname)
    return fpath


def RemoveDuplicate(MainDirPath,logDir="DuplicateFileLOG"):
    if((not os.path.exists(MainDirPath)) or (not os.path.isdir(MainDirPath))):
        print(f"ERROR LOCATING DIRECTORY \'{MainDirPath}\' TO REMOVE DUPLICATE FILES")
        print("SESSION ABORTED")
        exit()
    if not os.path.isabs(MainDirPath):
        MainDirPath=os.path.abspath(MainDirPath)
    try:
        file_hashes=set()
        LogFilePath=createLog(logDir)
        fd=open(LogFilePath,"w")
        fd.write("*"*80)
        fd.write(f"\nDuplicates Deleted from directory \'{MainDirPath}\' on [{datetime.datetime.now()}]\n")
        fd.write("*"*80)
        starttime=time.time()
        ScanStarted=(datetime.datetime.now()).strftime("%H:%M:%S")
        NumberOfFileScanned=0
        NumberOfDuplicateFound=0
        for (dirpath,_,filename) in os.walk(MainDirPath):
            for fname in filename:
                NumberOfFileScanned+=1
                fpath=os.path.join(dirpath,fname);
                key=get_checksum(fpath)
                if(key not in file_hashes):
                    file_hashes.add(key);
                else:
                    NumberOfDuplicateFound+=1
                    os.remove(fpath)
                    fd.write("\n"+os.path.basename(fpath))
        TotalTime=time.time()-starttime;
        print(f"Deletion of Duplicate files done in {TotalTime} sec")
    except Exception as e:
        print(e)
    finally:
        fd.close()
        Statistics=f"Starting time of scanning:{ScanStarted}\nTotal Time Required:{TotalTime}\nTotal Number of files scanned:{NumberOfFileScanned}\nTotal Number of duplicates found:{NumberOfDuplicateFound}\n"
        return LogFilePath,Statistics

def WholeTask(DirectoryPath,SendersEmail,SendersPassword,RecieversEmail):
    LogFilePath,Statistics=RemoveDuplicate(DirectoryPath)
    MailIt(SendersEmail,SendersPassword,RecieversEmail,LogFilePath,Statistics)


def main():
    print("*"*40)
    print("Duplicate_File_Remover")
    print("*"*40)

    if((len(argv)>4) or (len(argv)<2)):
        print("ERROR:Invalid number of arguments")
        print("Note:Use -u flag for usage\nNote:Use -h flag for Help")
        exit()
    if(len(argv)==2):
        if(argv[1]=="-u"):
            print("USAGE: Script used to Delete Duplicate files from directory dpecified in first_argument and schedule it for time interval mentioned in second_arg and this deleted files info to email mentioned in third_arg")
            exit()
        if(argv[1]=="-h"):
            print("HELP:script_name first_arg second_arg third_arg")
            print("first_arg:Directory_name or Path for Directory")
            print("second_arg:Value for time interval in minutes eg. 50 ,60")
            print("third_arg:Email Address of receiver to receive email")
            exit()
        else:
            print("Provide appropriate flag")
            exit()
    if(len(argv)==3):
        print("Enter third_argument i.e Email-address of reciever")
        exit()
    if(len(argv)==4):
        TimeInterval=float(argv[2])
        if(TimeInterval<10.0):
            print("WARNING:Provide TimeInterval More than 10 min. System may Crash after a while")
        SenderEmail=input("\nEnter Senders Email Id : ")
        SenderPassword=getpass.getpass(prompt="Enter Senders Password(No Echo): ")
        print("Task scheduling..")
        WholeTask(argv[1],SenderEmail,SenderPassword,argv[3])
        schedule.every(TimeInterval).minutes.do(WholeTask,argv[1],SenderEmail,SenderPassword,argv[3]);
        
        while(True):
            schedule.run_pending()
            time.sleep(1)

if __name__=="__main__":
    main()