def import_projects(id):
    print("\nStarting Import")
    data = {
        "path":f"{projects[id]}_{date.today()}.tar.gz"
    }
    print("Waiting for Import to finish")
    try:abhiragh0/portfolio_2025-10-28.tar.gz
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
        print(response.json())abhiragh0/portfolio_2025-10-28.tar.gz
    
def main():
    for id in projects.keys():
        export_projects(id)

if __name__ == "__main__":
    main()
