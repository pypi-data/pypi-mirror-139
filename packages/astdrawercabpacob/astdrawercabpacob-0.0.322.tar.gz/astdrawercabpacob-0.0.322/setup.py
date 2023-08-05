import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="astdrawercabpacob",
    version="0.0.322",
    author="Cabpacob",
    author_email="Cabpacob@github.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cabpacob/advanced_python/hw_1",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['astdrawercabpacob'],
    install_requires=[
        "networkx==2.5.1",
        "astunparse==1.6.3",
        "pydot==1.4.2"
    ],
    python_requires=">=3.6",
)
