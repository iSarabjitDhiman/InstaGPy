import pickle
import requests
import os
import instagpy as instagram
from . import config


def generate_new_session(path=None):
    insta = instagram.InstaGPy()
    insta.login(show_saved_sessions=False, save_session=False)
    if insta.logged_in:
        try:
            filename = insta.me['username']
        except:
            filename = None
        return save_session(session=insta.session, filename=filename, path=path)
    raise Exception("Couldn't LogIn, Try again...")


def create_session_directory(path=None, directory_name=None):
    if path is None:
        path = os.getcwd()
    if directory_name is None:
        directory_name = config.SESSION_DIRECTORY
    directory = os.path.join(path, directory_name)
    if not os.path.exists(directory):
        os.mkdir(directory)
    return directory


def show_saved_sessions(path=None):
    if path is None:
        path = create_session_directory()
    all_files = [f"{count}. {file}" for count, file in enumerate(
        os.listdir(path), start=1) if file.endswith(".pkl")]
    all_files.append(
        f"{len(os.listdir(path))+1}. Login with a New Account.")
    for file in all_files:
        print(os.path.splitext(file)[0])
    file_number = int(
        input("\nChoose a Number to Load an Exising Session : ").strip())
    if file_number != len(os.listdir(path))+1:
        filename = os.listdir(path)[file_number-1]
    else:
        path, filename = generate_new_session(path)
    return path, filename


def save_session(session=None, filename=None, path=None):
    if session is None or not isinstance(session, requests.Session):
        raise TypeError(f'{session} is not a requests Session Object...')
    if filename is None:
        try:
            filename = session.cookies['ds_user_id']
        except:
            filename = str(
                input("Enter Username/Account Name to Save the Session : ")).strip()
    if path is None:
        path = create_session_directory()
    filename = f"{filename}.pkl"
    file_path = os.path.join(path, filename)
    with open(file_path, "wb") as file:
        pickle.dump([session.headers, session.cookies], file)
    return path, filename


def load_session(filename=None, path=None, session=None):
    if filename is None:
        path, filename = show_saved_sessions()
    if path is None:
        path = create_session_directory()
    if not filename.endswith("pkl"):
        filename = f"{filename}.pkl"
    filename = os.path.join(path, filename)
    if not os.path.exists(filename):
        raise Exception("Couldn't find any session file for this user.")

    with open(filename, "rb") as file:
        headers, cookies = pickle.load(file)
    if session is not None:
        session.headers = headers
        session.cookies = cookies
        return
    return session


if __name__ == "__main__":
    create_session_directory()
