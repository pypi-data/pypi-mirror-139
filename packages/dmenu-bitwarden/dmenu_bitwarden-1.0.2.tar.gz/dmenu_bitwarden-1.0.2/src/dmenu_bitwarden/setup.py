if __name__ == "__main__":
    import setuptools

    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="dmenu-bitwarden-patrik.trefil",  # Replace with your own username
        version="1.0.0",
        author="Patrik Trefil",
        author_email="patrik@patriktrefil.com",
        description="Python script to copy password from Bitwarden to clipboard using dmenu",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://gitlab.com/patrik.trefil/dmenu-bitwarden",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GPLv3",
            "Operating System :: Linux",
        ],
        python_requires='>=3.8',
        data_files = [('man/man1', ['docs/_build/man/bitwardendmenu.1'])],
    )
