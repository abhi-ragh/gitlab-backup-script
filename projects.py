import os 
from dotenv import load_dotenv, dotenv_values
load_dotenv()

projects = ['portfolio','dent-ai','docker-pratice'] #project paths here, not id 

headers = {
    'Private-Token':os.getenv("gitlabtoken")
}
