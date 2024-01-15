from setuptools import setup

VERSION = "0.1.14"
SHORT_DESCRIPTION = "InstaGPy is an Instagram Unofficial API to extract data from Instargam Profiles. Scrape data from user's profile like username, userid, bio, email, phone, followers/followings list, profile media, account_type, etc."

with open("requirements.txt") as file:
    dependencies = file.read().splitlines()
with open("README.md", "r") as file:
    DESCRIPTION = file.read()


setup(
    name="instagpy",
    version=VERSION,
    description=SHORT_DESCRIPTION,
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Sarabjit Dhiman",
    author_email="hello@sarabjitdhiman.com",
    license="MIT",
    url="https://github.com/iSarabjitDhiman/InstaGPy",
    packages=["instagpy"],
    keywords=["instagpy", "instagram scraper", "instagram email scraper",
              "insta data extraction", "instagram api", "instagram python"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
    ],
    install_requires=dependencies,
    python_requires=">=3"
)
