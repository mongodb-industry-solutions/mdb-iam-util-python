from setuptools import setup, find_packages # type: ignore

setup(
    name="role-rectifier",
    version="0.1.0",
    description="A Python package for MongoDB role rectification",
    author="Tu Nombre",
    author_email="tuemail@example.com",
    packages=find_packages(),
    install_requires=["pymongo"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
