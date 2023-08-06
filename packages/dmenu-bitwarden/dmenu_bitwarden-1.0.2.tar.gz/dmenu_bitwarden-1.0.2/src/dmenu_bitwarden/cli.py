#!/usr/bin/env python3
"""module to parse the command-line options"""

import argparse

def create_parser():
    """parse command-line options"""
    parser = argparse.ArgumentParser(description='Default behavior is to copy selected password or note content to clipboard')
    parser.add_argument('-u', '--username', help="Get username to clipboard instead. (notes are excluded)", default=False, action="store_true", dest="want_username")
    parser.add_argument('-p', '--password', help='Get passwords to clipboard (notes are excluded)', default=False, action="store_true", dest="want_password")
    parser.add_argument('-n', '--notes', help='Get notes content to clipboard (logins are excluded)', default=False, action="store_true", dest="want_note")
    return parser
