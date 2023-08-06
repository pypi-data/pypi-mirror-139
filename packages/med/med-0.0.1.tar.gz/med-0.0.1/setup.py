

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="med",
    version="v0.0.1",

    author="Maggie",
    author_email="bechmanel@gmail.com",
    description="Django project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mag1i/med.git",
    project_urls={
        "Bug Tracker": "https://github.com/mag1i/med.git/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.9",
    scripts=["manage.py"],
)