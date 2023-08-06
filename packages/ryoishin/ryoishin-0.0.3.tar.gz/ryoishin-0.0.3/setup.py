import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ryoishin", # Replace with your own username
    version="0.0.3",
    author="ryoishin",
    author_email="ryoishincoder@gmail.com",
    description="A small info about ryoishin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ryoishin/ryoishin-pypi",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
