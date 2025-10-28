import os 
from dotenv import load_dotenv, dotenv_values
load_dotenv()

projects = {
    '72990278':'portfolio', # id:project-name
    '74623144':'dent-ai',
    '72906451':'DockerPractice'
}

headers = {
    'Private-Token':os.getenv("gitlabtoken")
}
