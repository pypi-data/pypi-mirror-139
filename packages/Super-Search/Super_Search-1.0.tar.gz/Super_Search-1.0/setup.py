import setuptools


with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="Super_Search",
    version="1.0",
    author="Rayshawn Levy",
    author_email="rayshawnlevy3@gmail.com",
    description="A command-line utility for system searches.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "susearch"},
    packages=setuptools.find_packages(where="susearch"),
    python_requires=">=3.8",
)
