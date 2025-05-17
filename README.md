# MongoDB IAM Utilities for Python
This repository is a utility project focused on streamlining IAM processes for MongoDB, leveraging the native driver (Python in this case), with the understanding that similar projects could be developed for other platforms. Its goal is to simplify and accelerate security-related tasks, making IAM management more efficient.

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/mongodb-industry-solutions/mdb-iam-util-python)

iam-util (Role Rectifier) is a Python package that helps manage and validate user roles and privileges in MongoDB databases. It allows developers to:

- ✅ Retrieve all roles assigned to a user across multiple databases.
- ✅ Identify custom roles (excluding built-in roles).
- ✅ Retrieve detailed privileges of specific roles.
- ✅ Verify missing and extra permissions for a given list of required permissions.

This package is designed for system administrators, DevOps engineers, and developers who manage MongoDB access control and want to ensure role consistency and security.

## 📌 Installation

```sh
pip install mongodb-solution-assurance-iam-util
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
Connect to MongoDB and Retrieve User Roles

```python
import os
from dotenv import load_dotenv  # Import dotenv to load environment variables
from mongodb_solution_assurance_iam_util import MongoRoleManager  # Import the custom role manager

# Load environment variables from the `.env` file
# This ensures sensitive values (like credentials) are not hardcoded in the script.
load_dotenv()

# Create the MongoDB connection string using environment variables
db_username = os.environ.get("DB_USERNAME")  # Retrieve the database username
db_password = os.environ.get("DB_PASSWORD")  # Retrieve the database password
db_host = os.environ.get("DB_HOST")          # Retrieve the database host
db_cluster = os.environ.get("DB_CLUSTER")    # Retrieve the cluster name

# Format the connection string required for MongoDB
connectionString = f"mongodb+srv://{db_username}:{db_password}@{db_host}/?retryWrites=true&w=majority&appName={db_cluster}"

def main():
    """
    Main function to handle MongoDB role permissions verification.
    """
    # Print the connection string for debugging purposes (optional and for testing purpose only).
    print("Connection string:", connectionString)
    # --------------------------------
    # OUTPUT:
    # Connection string: mongodb+srv://<username>:<password>@<host>/?retryWrites=true&w=majority&appName=<cluster>

    # Define the list of required permissions that need to be verified
    required_permissions = [
        "search",   # Permission to search documents
        "read",     # Permission to read documents
        "find",     # Permission to find documents based on a query
        "insert",   # Permission to insert new documents
        "update",   # Permission to update existing documents
        "remove",   # Permission to remove documents
        "collMod",  # Permission to modify collections
    ]

    # Initialize the MongoRoleManager with the connection string
    role_manager = MongoRoleManager(connectionString)

    # Verify that the necessary permissions are available for the database
    res = role_manager.verifyPermissions(required_permissions)

    # Print the verification result to the console
    print("--------------------------------")
    print(res)
    # --------------------------------
    # OUTPUT:
    # {
    #     'extra': ['viewRole', 'dropCollection', 'killAnyCursor', 'analyze'],
    #     'missing': ['search', 'read'],
    #     'present': ['remove', 'update', 'find', 'insert', 'collMod']
    # }

    # Get user roles
    userRoles = role_manager.getUserRoles()

    # Print the list of roles associated with the user in the connection string
    print("--------------------------------")
    print(userRoles)
    # OUTPUT:
    # --------------------------------
    # ['readWrite', 'read', 'PowerSyncCustomRole']

# Ensure the script runs only when executed directly (not imported as a module)
if __name__ == "__main__":
    main()
```
This code snippet establishes a connection to a MongoDB database using a constructed connection string, then utilizes a `MongoRoleManager` instance to retrieve the roles assigned to the authenticated user. It serves to programmatically access and display the user's role-based access control within the MongoDB environment, facilitating security audits and role management.


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

permissions = role_manager.verifyPermissions(requiredPermissions)

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

## 🔗 Available Plugins
- [MongoDB IAM Utilities for Node.Js](https://github.com/mongodb-industry-solutions/mdb-iam-util-node), get more details also at [NPM package link](https://www.npmjs.com/package/@mongodb-solution-assurance/iam-util)
- [MongoDB IAM Utilities for Python](https://github.com/mongodb-industry-solutions/mdb-iam-util-python), get more details also at [PYPI package link](https://pypi.org/project/mongodb-solution-assurance-iam-util)
- Additional plugins for Java, .NET, and Go (Coming Soon)

## 🔗 Demo Apps
- [MongoDB Security Utilities for IAM Remediation](https://github.com/mongodb-industry-solutions/mdb-iam-util-demo)