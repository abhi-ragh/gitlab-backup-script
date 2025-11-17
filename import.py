import os
import requests
import time
import boto3

from projects import projects, headers

s3 = boto3.client("s3")
BUCKET = "repo-backup-abhiragh"

def delete_project(project_name):
    try:
        response = requests.delete(f"https://gitlab.com/api/v4/projects/abhiragh0%2F{project_name}",headers=headers)
        if response.status_code == 202:
            print("Previous Repo Deleted.\nProceeding with the Import")
        elif response.status_code == 404:
            print("No Previous Repo Found.\nProceeding with the Import")
        else:
            print(response)
    except Exception as e:
        print("Error:", e)
        

def import_projects(path, name, data, files):
    print("\nStarting Import")
    
    data = data
        
    delete_project(name)

    try:
        files = files
        response = requests.post(
            "https://gitlab.com/api/v4/projects/import",
            headers=headers,
            files=files,
            data=data
        )

        if response.status_code != 201:
            print("Import request failed:")
            print(response.text)
            return

        print("Waiting for Import to finish")
        
        project_id = response.json()["id"]

        attempts = 0
        while True:
            time.sleep(5)
            attempts += 1
            status = requests.get(
                f"https://gitlab.com/api/v4/projects/{project_id}/import",
                headers=headers,
            )
            if status.json()["import_status"] == "finished":
                print("Import Successful\n")
                return

            if attempts >= 30: 
                print("Timed Out")
                return

    except Exception as e:
        print("Error:", e)

def get_file_path(path):
    dir_list = os.listdir(path)
    for i in dir_list:
        print(dir_list.index(i),":",i)
    
    choice = int(input("Enter Folder Number: "))
    path = path +"/"+dir_list[choice]
    
    if dir_list[choice].endswith((".tar.gz",)) == True:
        return path, dir_list[choice].split(".")[0]
    
    return get_file_path(path)
    
def get_s3_file_path(Prefix):
    resp = s3.list_objects_v2(
        Bucket=BUCKET,
        Prefix=Prefix,
        Delimiter="/"
    )

    prefix = []
    
    try:
        for i in resp['CommonPrefixes']:
            prefix.append(i['Prefix'])    
            print(prefix.index(i['Prefix']),":",i['Prefix'])
    except:
        for i in resp['Contents']:
            prefix.append(i['Key'])    
            print(prefix.index(i['Key']),":",i['Key'])

    choice = int(input("Enter a Option Number: "))
    
    if prefix[choice].endswith((".tar.gz",)) == True:
        return prefix[choice], prefix[choice].split("/")[-1].replace(".tar.gz","")
    
    return get_s3_file_path(prefix[choice])
    

def main():
    print("Select File to Import")
    ch = int(input("1. Local Storage\n2. S3 Storage\nChoose: "))
    
    if ch==1:
        path = os.getcwd() + "/Backups"
        path, name = get_file_path(path)
        data = {
            "path": name
        }
        files = { "file": open(path, "rb") }

    elif ch==2:
        path, name = get_s3_file_path("Backups/")
        obj = s3.get_object(Bucket=BUCKET, Key=path)
        file_bytes = obj["Body"].read()
        files = {
            "file": (name + ".tar.gz", file_bytes)
        }
        data = {
            "path": name
        }

    
    if path and name:
        import_projects(path, name, data, files)
    else:
        print("No file was selected")

if __name__ == "__main__":
    main()
