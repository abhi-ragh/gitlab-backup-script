import os 
import requests
import time 
from datetime import date
from dotenv import load_dotenv, dotenv_values
load_dotenv()

headers = {
    'Private-Token':os.getenv("gitlabtoken")
}

directory_name = f"{date.today()}"
try:
    os.mkdir(directory_name)
    print(f"Directory {directory_name} created Successfully")
except FileExistsError:
    print(f"Directory {directory_name} Already Exists")
except PermissionError:
    print(f"Unable to create Directory {directory_name}: Permission Denied")
except Exception as e:
    print(f"An error '{e}' Happened")
 
projects = {
    '72990278':'portfolio', # id:project-name
    '74623144':'dent-ai',
    '72906451':'DockerPractice'
}

def export_projects(id):
    print(f"\nCURRENT PROJECT: {projects[id]}")
    response = requests.post(f"https://gitlab.com/api/v4/projects/{id}/export", headers=headers)
    
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
        response = requests.get(f"https://gitlab.com/api/v4/projects/{id}/export", headers=headers)   
        if response.json()["export_status"] == "finished":
            response = requests.get(f"https://gitlab.com/api/v4/projects/{id}/export/download", headers=headers)
            try:
                with open(f"{directory_name}/{projects[id]}_backup.tar.gz", 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192): 
                        f.write(chunk)
            except Exception as e:
                print(f"Error '{e}' Occured")
            break
        Check += 1 
        if Check >= 30:
            print("Timed Out")
            exit()
            
    print(f"{projects[id]} Export Downloaded")
    import_projects(id)
    
def import_projects(id):
    print("\nStarting Import")
    data = {
        "path":f"{projects[id]}_{date.today()}.tar.gz"
    }
    print("Waiting for Import to finish")
    try:
        files = { "file": open(f"{directory_name}/{projects[id]}_backup.tar.gz", 'rb') }
        response = requests.post(f"https://gitlab.com/api/v4/projects/import", headers=headers, files=files, data=data)
        new_project_id = response.json()["id"]
        
        while response.json()["import_status"] != "finished":
            time.sleep(10)
            Check = 1   
            response = requests.get(f"https://gitlab.com/api/v4/projects/{new_project_id}/import", headers=headers)
            Check += 1 
            if Check >= 30:
                print("Timed Out")
                exit()        
        
        print("Import Successful\n")
    except Exception as e:
        print(response.json())
    
def main():
    for id in projects.keys():
        export_projects(id)

if __name__ == "__main__":
    main()
