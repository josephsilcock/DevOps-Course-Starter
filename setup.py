import os
import shutil

if shutil.which("poetry") is None:
    os.system("wget -o install_poetry.py https://install.python-poetry.org")
    f = open("install_poetry.py").read()
    code = compile(f, "install_poetry.py", 'exec')
    exec(code)

os.system("poetry install")
shutil.copy(".env.template", ".env")
os.system("poetry run flask run")
