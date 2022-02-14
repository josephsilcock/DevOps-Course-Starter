import os
import shutil
import ssl
import requests

gcontext = ssl.SSLContext()
if shutil.which("poetry") is None:
    code = compile(requests.get("https://install.python-poetry.org").content, "install_poetry.py", 'exec')
    exec(code)

os.system("poetry install")
shutil.copy(".env.template", ".env")
os.system("poetry run flask run")
