import setuptools

with open("README.md", "rb") as fh:
    long_description = fh.read()

setuptools.setup(
    name="selenide",
    version="0.0.1",
    author="aquichita",
    author_email="chaochao.wu@outlook.com",
    description="Realization of UI automated testing wheels by selenium.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aquichita/selenide",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
