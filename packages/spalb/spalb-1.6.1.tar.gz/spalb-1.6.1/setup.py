import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spalb", # Replace with your own username
    version="1.6.1",
    author="Sirapob and Siriwimon ",
    author_email="16630.mnr@gmail.com",
    description="This package can solve single product assembly line balancing problem",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    project_urls={
            "Documentation": "https://spalb.github.io/documentation/",       
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    install_requires= [],
    python_requires='>=3.7',
)


