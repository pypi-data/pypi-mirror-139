#!/usr/bin/env python3
"""utility functions"""

import subprocess
import pyperclip


def notify(text: str) -> None:
    """notify user about an event"""
    subprocess.run(["notify-send", text, ], check=True)

def copy_to_clipboard(text: str) -> None:
    """copy text to user's clipboard"""
    pyperclip.copy(text)
