from setuptools import setup, find_packages # type: ignore

setup(
    name="role-rectifier",
    version="0.1.0",
    description="A Python package for MongoDB role rectification",
    author="MongoDB Solutions Assurance Team",
    author_email="solution-assurance@mongodb.com",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=["pymongo"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
