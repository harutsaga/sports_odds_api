# fetch swagger yaml and convert it into md file using widdershins
import sys
import os
import json
import glob

from requests import get  


def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)

download('http://localhost:8000/swagger.yaml', 'swagger.yaml')
os.system("widdershins --omitBody true --omitHeader true --theme darkula --language_tabs shell:Shell --yaml --useBodyName true --code false --summary --language_tabs 'python:Python' --html false swagger.yaml -o swagger.md")