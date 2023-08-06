import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-reddit",
    version="1.0.1",
    author="KING7077",
    author_email="sram2007india@gmail.com",
    description="Reddit and python, made simple.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    install_requires=['aiohttp', 'requests'],
    keywords=['python', 'reddit', 'py-reddit',
              'async-py-reddit', 'python-reddit'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
