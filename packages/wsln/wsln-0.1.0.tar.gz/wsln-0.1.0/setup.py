import setuptools

setuptools.setup(
    name = "wsln",
    version = "0.1.0",
    description = "Understand the Semantics of Text",
    author = "gajanlee",
    index_url = "https://github.com/gajanlee/W-SLN",
    author_email = "lee_jiazh@163.com",
    install_requires = ["nltk", "tqdm"],
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    package_data = {
        "wsln": ["patterns/patterns.json"],
    },
)