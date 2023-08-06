import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='dmenu_bitwarden',
    version='1.0.7',
    author="Patrik Trefil",
    author_email="patrik.trefil@gmail.com",
    url="https://gitlab.com/patriktrefil/dmenu-bitwarden",
    project_urls={
        "Bug Tracker": "https://gitlab.com/patriktrefil/dmenu-bitwarden/-/issues",
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        'pyperclip'
    ],
    package_dir={"": "src"},
    data_files=[("man/man1", ["docs/_build/man/bitwardendmenu.1"])]
)
