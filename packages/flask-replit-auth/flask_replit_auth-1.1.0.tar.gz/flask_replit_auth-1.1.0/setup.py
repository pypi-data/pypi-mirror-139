import setuptools

with open("README.md", "r") as fhandle:
    long_description = fhandle.read()

setuptools.setup(
    name="flask_replit_auth",
    version="1.1.0",
    author="EpicCodeWizard",
    author_email="epiccodewizard@gmail.com",
    description="Brings replit auth to flask.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://replit.com/@EpicCodeWizard/flaskreplitauth",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'flask'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
