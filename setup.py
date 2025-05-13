from setuptools import setup, find_packages  # type: ignore

setup(
    name="mongodb-solution-assurance-iam-util",
    version="0.1.3",
    description="A collection of utilities focused on streamlining MongoDB security",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="MongoDB Solutions Assurance Team",
    author_email="solution.assurance@mongodb.com",
    license="Apache Software",
    url="https://github.com/mongodb-industry-solutions/mdb-iam-util-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    # include_package_data=True,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["pymongo"],
    python_requires=">=3.7",
    extra_require={"dev": ["pytest>=7.0", "twine>=4.0.2"]},
)
