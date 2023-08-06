## Disclaimer

Although I belive this program is safe, You should use this program at Your own risk.

## Installation

Note: This program has been tested only on Linux.

[Dmenu](https://tools.suckless.org/dmenu/) and [python3](https://www.python.org/) are required to run this program.
The program communicates with the user using `notify-send`, which should be available on Your system.

You also need the [official CLI of Bitwarden](https://bitwarden.com/help/article/cli/). **You should
log in on Your own first**, especially if You use any form of 2-Factor Authentification (`bw login`).

You can install the package via pip using the following command:

```
$ pip install dmenu-bitwarden
```

## Usage

```
$ python -m dmenu-bitwarden
```

Password prompt should appear. After you put in Your password you can choose the account for which
you want your password. The selected password will be copied to your clipboard.

I recommend You bind this to a keyboard shortcut, e.g., `super + p`. (recommended [Hotkey daemon](https://github.com/baskerville/shkd))

## Documentation

You can find the documentation [here](https://patriktrefil.gitlab.io/dmenu-bitwarden)
