import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="virhunter",
    version="1.0.0",
    author="Grigorii sukhorukov",
    author_email="grsukhorukov@gmail.com ",
    description="A virus identifier for High Throughput Sequencing datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cbib/virhunter",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)