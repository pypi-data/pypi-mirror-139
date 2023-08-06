#!/usr/bin/python3
"""lets you choose an account from bitwarden-cli and gives the password to your clipboard"""

import os
import subprocess
import shutil
from . import cli, utils, vault

KEY_FILE_NAME = "bitwarden_session_key.txt"
if "XDG_CACHE_HOME" in os.environ:
    KEY_PATH = f"{os.getenv('XDG_CACHE_HOME')}/{KEY_FILE_NAME}"
else:
    KEY_PATH = f"{os.getenv('HOME')}/.cache/{KEY_FILE_NAME}"
# color is necessary to hide the password
DMENU_COLOR = "#AAA"
DELIM = " - "
NOTE_MARK = "[NOTE]"
BITWARDEN_LOGIN_CODE = 1
BITWARDEN_NOTES_CODE = 2


def get_sess_key():
    if not os.path.exists(KEY_PATH):
        sess_key = vault.get_new_key(DMENU_COLOR)
        # create the file
        with open(KEY_PATH, "w") as file:
            file.write(sess_key)
        # r/w permissions for the file owner
        # noone else gets permissions
        os.chmod(KEY_PATH, 0o600)
    else:
        # load session key from file
        with open(KEY_PATH, "r") as file:
            sess_key = file.readline()
    return sess_key

def make_prompt(args):
    prompt_items = []
    if args.want_password is True:
        prompt_items += ["Passwords"]
    if args.want_username is True:
        prompt_items += ["Usernames"]
    if args.want_note is True:
        prompt_items += ["Notes"]

    prompt = ", ".join(prompt_items) + " :"
    return prompt

def format_names(login_items: list) -> str:
    name_list = []
    for acc in login_items:
        if acc['type'] == 1:
            name_list += [f"{acc['name']}{DELIM}{acc['login']['username']}"]
        else:
            name_list += [f"{acc['name']}{DELIM}{NOTE_MARK}"]

    return "\n".join(name_list)

def get_items(sess_key: str) -> list:
    try:
        # try to use loaded sess key
        items_list = vault.get_items(sess_key)
    except subprocess.TimeoutExpired:
        # try again with new key
        sess_key = vault.get_new_key(DMENU_COLOR)
        # note the new key
        with open(KEY_PATH, "w") as file:
            file.write(sess_key)
        try:
            items_list = vault.get_items(sess_key)
        except subprocess.TimeoutExpired:
            utils.notify("Something went wrong")
            exit(1)
    return items_list

def get_desired_types(args) -> list:
    desired_types = []
    if args.want_username is True or args.want_password is True:
        desired_types += [BITWARDEN_LOGIN_CODE]
    if args.want_note is True:
        desired_types += [BITWARDEN_NOTES_CODE]
    return desired_types

def get_desired_info_from_match(args, match) -> str:
    """args specify what information to get, match holds the information"""
    if match["type"] == BITWARDEN_LOGIN_CODE:
        if args.want_username:
            res = match['login']['username']
        else:
            res = match['login']['password']
    elif match["type"] == BITWARDEN_NOTES_CODE:
        res = match['notes']
    else:
        msg = "Unknown match type"
        utils.notify(msg)
        raise Exception(msg)
    return res

def main():
    # assert all required programs are in $PATH
    assert shutil.which("dmenu") is not None, "You have to install dmenu first, here is the link https://tools.suckless.org/dmenu/"
    assert shutil.which("bw") is not None, "You have to install Bitwarden CLI first, here is the link https://bitwarden.com/help/article/cli/"

    args = cli.create_parser().parse_args()

    assert args.want_username is False or args.want_password is False, "You can't get username and password at the same time"
    assert args.want_username is True or args.want_password is True or args.want_note is True, "Select at least one option"

    sess_key = get_sess_key()
    items_list = get_items(sess_key)

    # filter logins or notes
    desired_types = get_desired_types(args)
    filtered_items = filter(lambda x: x["type"] in desired_types, items_list)

    # choose with dmenu
    prompt = make_prompt(args)
    names = format_names(filtered_items)
    dmenu_choose_item_process = subprocess.run(["dmenu", "-i", "-p", prompt],
                                               input=names.encode("UTF-8"), stdout=subprocess.PIPE, check=True)
    # remove \n
    name, username = dmenu_choose_item_process.stdout.decode(
        "UTF-8")[:-1].split(DELIM)
    # find selected item
    was_found = False
    for item in filtered_items:
        if item['name'] == name and ((item["type"] == BITWARDEN_LOGIN_CODE and item['login']['username'] == username) or item["type"] == BITWARDEN_NOTES_CODE):
            final_match = item
            was_found = True
            break

    assert was_found == True, "Your query was not found. Something went wrong."

    res = get_desired_info_from_match(args, final_match)
    # copy to clipboard
    utils.copy_to_clipboard(res)


if __name__ == "__main__":
    main()
