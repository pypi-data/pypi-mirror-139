import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("CHANGELOG.md", "r", encoding="utf-8") as fh:
    changelog_file = fh.read()

setuptools.setup(
    name="py-reddit",
    version="1.1.3",
    author="KING7077",
    author_email="sram2007india@gmail.com",
    description="Reddit and python, made simple.",
    long_description=long_description+'\n\n'+changelog_file,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    install_requires=['aiohttp', 'requests'],
    keywords=['python', 'reddit', 'py-reddit',
              'async-py-reddit', 'python-reddit'],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
