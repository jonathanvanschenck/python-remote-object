import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="remote-object",
    version="0.2.3",
    author="Jonathan D B Van Schenck",
    author_email="vanschej@oregonstate.edu",
    description="A TCP-based server/client library for making method calls from a client to a python object on the server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonathanvanschenck/python-remote-object",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
