import os
import requests
import time
import tkinter as tk
from tkinter import filedialog

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

def get_file_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()

    if file_path:
        return file_path, os.path.basename(file_path)
    return None, None

def main():
    print("Select File to Import")
    
    path, name = get_file_path()
    if path and name:
        import_projects(path, name)
    else:
        print("No file was selected")

if __name__ == "__main__":
    main()
