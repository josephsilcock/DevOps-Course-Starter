import argparse
import os
import shutil


def main(use_production: bool):
    # Install Poetry
    if shutil.which("poetry") is None:
        os.system("curl -o install_poetry.py https://install.python-poetry.org")
        install_poetry_file = open("install_poetry.py").read().replace("sys.exit(main())", "main()")
        os.remove("install_poetry.py")
        exec(compile(install_poetry_file, "install_poetry.py", "exec"))

    # Install Dependencies
    os.system("poetry install")

    # Create .env
    if not os.path.exists(".env"):
        env_file = open(".env.template").read()
        env_file = env_file.replace("secret-key", input("What is the secret key? "))
        env_file = env_file.replace("db-name", input("What is the Database name? "))
        env_file = env_file.replace("mongodb-connection-string", input("MongoDB connection string? "))

        with open(".env", "w+") as f:
            print(env_file, file=f)

    # Start App
    if use_production:
        os.system('poetry run gunicorn --bind 0.0.0.0:80 "wsgi:run()" --logfile ~/todoapp.log')
    else:
        os.system("poetry run flask run")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup the To Do App")
    parser.add_argument(
        "-p",
        "--production",
        action="store_true",
        help="If set, set up the production server. Otherwise, setup the development server",
    )
    args = parser.parse_args()
    main(args.production)
