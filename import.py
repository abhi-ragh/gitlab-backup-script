import os
import requests
import time

from projects import projects, headers

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
        

def import_projects(path, name):
    print("\nStarting Import")
    
    project_name = name.split(".")[0]
    
    data = {
        "path": project_name
    }
        
    delete_project(project_name)

    try:
        files = { "file": open(path, "rb") }
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
        return path, dir_list[choice]
    
    return get_file_path(path)
    

def main():
    print("Select File to Import")
    
    path = os.getcwd() + "/Backups"
    path, name = get_file_path(path)
    
    if path and name:
        import_projects(path, name)
    else:
        print("No file was selected")

if __name__ == "__main__":
    main()
