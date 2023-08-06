import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygooglechat",
    version="0.3",
    author="moonseoklee",
    author_email="winnyiee@korea.ac.kr",
    description="Easy Googlechat Handler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moonseoklee/pygooglechat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
