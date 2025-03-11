# MongoDB IAM Utils
This repository is a utility project focused on streamlining IAM processes for MongoDB, leveraging the native driver (Python in this case), with the understanding that similar projects could be developed for other platforms. Its goal is to simplify and accelerate security-related tasks, making IAM management more efficient.


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
from src import MongoRoleManager

# Replace with your MongoDB connection string data
dbUsername = "db_username"
dbPassword = "db_password"
dbHost = "mydb.kts.mongodb.net"
dbApp = "MyLocalApp"

connectionString = f"mongodb+srv://{dbUsername}:{dbPassword}@{dbHost}/?retryWrites=true&w=majority&appName={dbApp}"

# Create the role manager instance
roleManager = MongoRoleManager(connectionString)

# Get user roles
userRoles = roleManager.getUserRoles()

print(userRoles)
```


## 🚀 Verify Missing & Extra Permissions
Checking access privileges for the user defined in the connection string of the previous example:

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

## required-privileged
print("Valid Permissions:", permissions["present"])
```

The provided code snippet demonstrates how to effectively verify and manage user permissions within a MongoDB environment. Utilizing the `verifyPermissions` method, it compares a list of `requiredPermissions` against the actual privileges granted to the user, as determined by their assigned roles. 

This process then categorizes permissions into three distinct groups: 
- **Extra Permissions:** highlights any privileges exceeding the required set, indicating potential over-privileging.
- **Missing Permissions:** identifies necessary permissions that are absent, revealing under-privileging.
- **Valid Permissions:** confirms the required privileges that are correctly assigned. 

This functionality allows for precise auditing and adjustment of user access, ensuring adherence to security best practices and minimizing risks associated with excessive or insufficient permissions.