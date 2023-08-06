from setuptools import setup, find_packages

setup(
    name="blockchainer",
    version="0.0.6",
    author="Shoaib Wani",
    description="An interface to help you make your own blockchain",
    package_dir={"":"src"},
    packages=find_packages(where="src"),
    install_requires=["fastecdsa"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.4",
)