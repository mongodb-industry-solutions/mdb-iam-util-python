# MongoDB IAM Utils
This repository is for checking access privileges for MongoDB configured users.

In order to run the python code, follow the below step:
1. Install the necessary Python packages, by executing the below command: 

    ```shell
    pip install -r requirements.txt 
    ```

Role Rectifier is a Python package that helps manage and validate user roles and privileges in MongoDB databases. It allows developers to:

- ✅ Retrieve all roles assigned to a user across multiple databases.
- ✅ Identify custom roles (excluding built-in roles).
- ✅ Retrieve detailed privileges of specific roles.
- ✅ Verify missing and extra permissions for a given list of required permissions.

This package is designed for system administrators, DevOps engineers, and developers who manage MongoDB access control and want to ensure role consistency and security.

## 📌 Installation

```sh
pip install user-access-checks
``` 

Alternatively, install it directly from the source:

```sh
git clone https://github.com/mongodb-industry-solutions/user-access-checks.git
cd user-access-checks
mv .env.example .env
pip install -r requirements.txt
```
## 🔬 Test
Run tests using pytest:
```sh
pytest
``` 
or with Make 
```sh
make test
``` 

## 🛠 Usage Example
1. Connect to MongoDB and Retrieve User Roles
```python
from src.mongo_role_manager import MongoRoleManager

# Replace with your MongoDB connection string
connectionString = "mongodb+srv://myuser:itpassword@solutionsassurance.n0kts.mongodb.net/?retryWrites=true&w=majority&appName=SolutionsAssurance"

# Create the role manager instance
roleManager = MongoRoleManager(connectionString)

# Get user roles
userRoles = roleManager.getUserRoles()

print(userRoles)
```


## 🚀 Verify Missing & Extra Permissions
```python

requiredPermissions = [
    "search",
    "read",
    "find",
    "insert",
    "update",
    "remove",
    "collMod",
]

permissions = roleManager.verifyPermissions(requiredPermissions)

## over-privileged
print("Extra Permissions:", permissions["extra"])

## under-privilidged
print("Missing Permissions:", permissions["missing"])

## required permissions
print("Valid Permissions:", permissions["present"])
```