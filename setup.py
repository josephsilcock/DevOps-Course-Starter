import os
import shutil

if shutil.which("poetry") is None:
    os.system("curl -o install_poetry.py https://install.python-poetry.org")
    f = open("install_poetry.py").read()
    os.remove("install_poetry.py")
    code = compile(f, "install_poetry.py", 'exec')
    exec(code)

os.system("poetry install")
shutil.copy(".env.template", ".env")
os.system("poetry run flask run")
