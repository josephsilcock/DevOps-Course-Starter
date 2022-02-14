import os
import shutil

# Install Poetry
if shutil.which("poetry") is None:
    os.system("curl -o install_poetry.py https://install.python-poetry.org")
    install_poetry_file = open("install_poetry.py").read().replace("sys.exit(main())", "main()")
    os.remove("install_poetry.py")
    code = compile(install_poetry_file, "install_poetry.py", 'exec')
    exec(code)

# Install Dependencies
os.system("poetry install")

# Create .env
if not os.path.exists(".env"):
    env_file = open(".env.template").read()
    env_file = env_file.replace("secret-key", input("What is the secret key? "))
    env_file = env_file.replace("trello-key", input("What is the trello key? "))
    env_file = env_file.replace("trello-token", input("What is the trello token? "))
    env_file = env_file.replace("trello-board-id", input("What is the trello board id? "))

    with open(".env", "w+") as f:
        print(env_file, file=f)

# Start App
os.system("poetry run flask run")
