from setuptools import setup

# gets the long description from the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# sets up the pypi package
setup(
    name="interactions-cooldowns",  # package name on pypi, also install name for pip
    version="1.0.4",  # this is the version of the extension
    description="description",  # the short description of the extension
    long_description=long_description,  # the long description of the extension, taken from README.md
    long_description_content_type="text/markdown",
    url="https://github.com/dontbanmeplz/interactions-cooldowns",  # put your github repo link here
    author="dontbanmeplz",  # pypi username
    author_email="example@email.domain",  # pypi email
    license="MIT",  # change/choose a license here, dont forget to change LICENSE file
    packages=["interactions.ext.cooldowns"],
    classifiers=[  # change this according to pypi
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "discord-py-interactions>=4.0.2"  # the version of discord-py-interactions you depend on
    ],  # you can add more dependencies here
)
