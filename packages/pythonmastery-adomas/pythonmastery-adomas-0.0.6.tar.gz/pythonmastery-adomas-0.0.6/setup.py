from setuptools import setup, find_packages

VERSION = "0.0.6"
DESCRIPTION = "Python Mastery"

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

# LONG_DESCRIPTION = 'Python Mastery @ Turing College'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="pythonmastery-adomas",
    version=VERSION,
    author="Adomas Valiukevicius",
    author_email="<adomasval08@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    test_suite = 'tests',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
)
