import setuptools

long_description = open("README.md").read()
required = ["requests>=2.27.1", "boto3>=1.20.38"] # Comma seperated dependent libraries name

setuptools.setup(
    name="Labii sdk",
    version="1.0", # eg:1.0.0
    author="Labii Inc.",
    author_email="developer@labii.com",
    license="GNU GPLv3",
    description="An SDK for the Labii ELN & LIMS platform (https://www.labii.com) that provides interaction with the Labii API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/labii-dev/labii-sdk",
    packages = ['labii_sdk'],
    # project_urls is optional
    project_urls={
        "Bug Tracker": "https://gitlab.com/labii-dev/labii-sdk/-/issues?sort=created_date&state=opened",
    },
    key_words="Labii, Labii ELN & LIMS, ELN, LIMS, SDK, Electronic Lab Notebook, Laboratory Information Management System",
    install_requires=required,
    #packages=setuptools.find_packages(where="labii"),
    python_requires=">=3.8",
)
