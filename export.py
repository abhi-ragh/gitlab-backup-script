import os 
import requests
import time 
import boto3
from datetime import date

from projects import projects,headers

directory_name = f"{date.today()}"

s3 = boto3.client("s3")
BUCKET = "repo-backup-abhiragh"

try:
    os.mkdir(f"Backups/{directory_name}")
    print(f"Directory {directory_name} created Successfully")
except FileExistsError:
    print(f"Directory {directory_name} Already Exists")
except PermissionError:
    print(f"Unable to create Directory {directory_name}: Permission Denied")
except Exception as e:
    print(f"An error '{e}' Happened")

def export_projects(id):
    print(f"\nCURRENT PROJECT: {id}")
    response = requests.post(f"https://gitlab.com/api/v4/projects/abhiragh0%2F{id}/export", headers=headers)
    
    if response.json()["message"] == "202 Accepted":
        print("Export Request Sent!")
    else:
        print("Export Request Failed to Sent")
        print(response.json())
        exit()

    print("Waiting The Export to Finish")
    
    while True:
        time.sleep(10) # sleep to make sure to not spam the api 
        Check = 1      # Check to make sure the while loop doesnt continue forever 
        response = requests.get(f"https://gitlab.com/api/v4/projects/abhiragh0%2F{id}/export", headers=headers)   
        if response.json()["export_status"] == "finished":
            response = requests.get(f"https://gitlab.com/api/v4/projects/abhiragh0%2F{id}/export/download", headers=headers)
            try:
                with open(f"Backups/{directory_name}/{id}.tar.gz", 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192): 
                        f.write(chunk)
            except Exception as e:
                print(f"Error '{e}' Occured")
            break
        Check += 1 
        if Check >= 30:
            print("Timed Out")
            exit()
    
    print(f"{id} Export Downloaded")
        
    path = f"Backups/{directory_name}/{id}.tar.gz"
    s3.upload_file(path, BUCKET, path)
    
    print(f"{id} was uploaded to S3 Storage")

def retention_check():
    print("Start Retention Check")
    no_of_backups = len(os.listdir(os.getcwd() + "/Backups"))
    if no_of_backups >= 7:
        oldest_dir = min(os.listdir(os.getcwd()+"/Backups"))
        print("Deleting Backup Older than 7 days from Local Storage.")
        os.remove(oldest_dir)   

def main():
    for id in projects:
        export_projects(id)
    retention_check()
    

if __name__ == "__main__":
    main()
