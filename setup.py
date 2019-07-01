import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='IPASS-repo-denbergvanthijs',
    version="2019.07.1.2",
    author="Thijs van den Berg",
    author_email="denbergvanthijs@gmail.com",
    description='IPASS eindproject 2018 - 2019',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/denbergvanthijs/IPASS-repo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
