import os  
import shutil  
from setuptools import setup, find_packages  
  
# Constants  
MODULE_VERSION = "0.1.4"  
MODULE_NAME = "mongodb_solution_assurance_iam_util"  # Package name  
PUBLISH_DIR = "publish"  # Temporary directory for staging files  
SRC_DIR = "src"  # Source directory  
  
# Function to prepare the publish directory  
def prepare_publish_directory(src_dir: str, publish_dir: str, module_name: str):  
    """  
    Copies the contents of the source directory to the publish directory under the module name.  
    Excludes unnecessary files like `__pycache__`.  
  
    :param src_dir: Path to the source directory.  
    :param publish_dir: Path to the temporary publish directory.  
    :param module_name: Name of the module (used as a subdirectory in publish).  
    """  
    print(f"Preparing publish directory... (src={src_dir}, publish={publish_dir}, module={module_name})")  
  
    # Step 1: Check if the source directory exists  
    if not os.path.exists(src_dir):  
        print(f"ERROR: Source directory '{src_dir}' does not exist.")  
        return  
  
    # Step 2: Remove the publish directory if it already exists  
    if os.path.exists(publish_dir):  
        print(f"Removing existing publish directory: {publish_dir}")  
        shutil.rmtree(publish_dir)  
  
    # Step 3: Create the publish directory  
    os.makedirs(publish_dir, exist_ok=True)  
    print(f"Created publish directory: {publish_dir}")  
  
    # Step 4: Define the module directory inside the publish directory  
    module_dir = os.path.join(publish_dir, module_name)  
  
    # Step 5: Copy files from src to publish/module_name  
    for root, dirs, files in os.walk(src_dir):  
        # Remove `__pycache__` directories  
        dirs[:] = [d for d in dirs if d != "__pycache__"]  
  
        # Calculate the relative path and destination  
        relative_path = os.path.relpath(root, src_dir)  
        dest_dir = os.path.join(module_dir, relative_path)  
  
        # Create necessary directories  
        os.makedirs(dest_dir, exist_ok=True)  
        print(f"Created directory: {dest_dir}")  
  
        # Copy valid files  
        for file in files:  
            src_file = os.path.join(root, file)  
            dest_file = os.path.join(dest_dir, file)  
            shutil.copy(src_file, dest_file)  
            print(f"Copied file: {src_file} -> {dest_file}")  
  
  
# Prepare the publish directory  
prepare_publish_directory(SRC_DIR, PUBLISH_DIR, MODULE_NAME)  
  
print("------- Starting Setup Process -------")  
  
# Setup configuration  
setup(  
    name=MODULE_NAME,  # Name of your PyPI package  
    version=MODULE_VERSION,  
    description="A collection of utilities focused on streamlining MongoDB security",  
    long_description=open("README.md", encoding="utf-8").read(),  
    long_description_content_type="text/markdown",  
    author="MongoDB Solutions Assurance Team",  
    author_email="solution.assurance@mongodb.com",  
    license="Apache-2.0", 
    url="https://github.com/mongodb-industry-solutions/mdb-iam-util-python",  
    classifiers=[  
        "Programming Language :: Python :: 3",  
        "License :: OSI Approved :: Apache Software License",   
        "Operating System :: OS Independent",  
        "Topic :: Database",  
        "Topic :: Security",  
        "Intended Audience :: Developers",  
        "Intended Audience :: System Administrators",  
    ],  
    keywords="mongodb security iam role manager permissions pymongo",  
    packages=find_packages(where=PUBLISH_DIR),  # Packages detected in the publish directory  
    package_dir={"": PUBLISH_DIR},  # Declare the publish directory as the source  
    install_requires=["pymongo"],  
    python_requires=">=3.7",  
    extras_require={  
        "dev": ["pytest>=7.0", "twine>=4.0.2"],  
    },  
)  
  
print("------- Setup Process Completed -------")  
  
# Clean up the publish directory after packaging  
if os.path.exists(PUBLISH_DIR):  
    print(f"Cleaning up publish directory: {PUBLISH_DIR}")  
    shutil.rmtree(PUBLISH_DIR)  
  
print("------- End of Script -------")  
