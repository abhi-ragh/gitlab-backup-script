import os 
import requests
import time 
from datetime import date

from projects import projects,headers

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
                with open(f"{directory_name}/{projects[id]}_{date.today()}.tar.gz", 'wb') as f:
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
    
def main():
    for id in projects.keys():
        export_projects(id)

if __name__ == "__main__":
    main()
