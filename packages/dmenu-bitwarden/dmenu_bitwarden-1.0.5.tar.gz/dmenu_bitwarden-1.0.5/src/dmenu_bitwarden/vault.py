#!/usr/bin/env python3
"""module for working with the bitwarden vault"""

import subprocess
import re
import json
from . import utils


def get_new_key(dmenu_color: str) -> str:
    """asks user for password (wrong password -> exit(1))"""
    m = subprocess.run(["dmenu", "-p", "Password:", "-nb", dmenu_color, "-nf", dmenu_color],
                       input=b"", stdout=subprocess.PIPE, check=True)
    # get password and remove trailing \n
    pswd = m.stdout[:-1]
    # unlock vault
    g = subprocess.run(["bw", "unlock", pswd],
                       stdout=subprocess.PIPE, text=True)
    if g.returncode == 0:
        # sucessfully opened the vault
        out = g.stdout
        # find sess key in output
        regex = re.compile(
            r"^\$ export BW_SESSION=\"(.*?)\"", re.MULTILINE)
        res = re.search(regex, out)
        sess_key = res.group(1)
        return sess_key
    else:
        # incorrect password
        utils.notify("Incorrect password")
        exit(1)


def get_items(key: str) -> list:
    """get items from vault using session key"""
    cmd_out = subprocess.run(["bw", "list", "items", "--session", key],
                          stdout=subprocess.PIPE, text=True, timeout=2, check=True).stdout
    # ignore err mess
    i = cmd_out.find("[")
    cmd_out = cmd_out[i:]
    # parse json content
    items = json.loads(cmd_out)
    return items
