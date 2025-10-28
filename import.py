import os 
import requests
import time 
from datetime import date
import tkinter as tk
from tkinter import filedialog

from projects import projects,headers

def import_projects(path, name):
    print("\nStarting Import")
    data = {
        "path": name
    }
    print("Waiting for Import to finish")
    try:
        files = { "file": open(path, 'rb') }
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
    

def get_file_path():

    root = tk.Tk()
    root.withdraw() 
    
    print("Opening file dialog...")
    file_path = filedialog.askopenfilename()
    
    root.destroy()
    
    if file_path:  
        file_name = os.path.basename(file_path)
        return file_path, file_name
    else:
        return None, None

def main():
    
    print("Select File to Import")
    
    path, name = get_file_path()

    if path and name:
        import_projects(path, name)

    else:
        print("\nNo file was selected (dialog was canceled).")


if __name__ == "__main__":
    main()
