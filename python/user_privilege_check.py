from pymongo import MongoClient
from pprint import pprint


# Function that gets all the roles that the specific user has
def get_user_roles(uri, username):
    """
    Connects to the MongoDB instance specified by `uri` and retrieves all roles
    for `username` across all databases.
    
    Parameters:
    uri (str): MongoDB connection URI
    username (str): The username for whom to find roles
    
    Returns:
    dict: A dictionary with database names as keys and lists of role documents as values
    """
    
    client = MongoClient(uri)
    roles_info = {}
    
    try:
        # Get a list of all databases
        databases = client.list_database_names()
        
        # Iterate over each database
        for db_name in databases:
           try:
                db = client[db_name]
                user_info = db.command("usersInfo", username)
                
                if user_info.get('users'):
                    user_roles = user_info['users'][0].get('roles', [])
                    roles_info[db_name] = user_roles
           except Exception as e:
               pass
    finally:
        # Always close the client connection
        client.close()
    return roles_info

# Function to get privileges of a specific custom role
def get_privileges_of_custom_role(uri, role_name):
    # Connect to MongoDB
    client = MongoClient(uri)
    # Access the 'admin' database where user and role metadata is stored
    admin_db = client['admin']
    role_info = admin_db.command('rolesInfo', role_name, showPrivileges=True, showBuiltinRoles=True)
    print(f"Privileges for role '{role_name}':")
    for role in role_info.get('roles', []):
        for privilege in role.get('privileges', []):
            print(f"  - Resource: {privilege.get('resource')}")
            print(f"  - Actions: {privilege.get('actions')}")


# Find custom role in a list of data with a similar structure:
'''
{'admin': [{'db': 'admin', 'minFcv': '', 'role': 'PowerSyncCustomRole'},
           {'db': 'admin', 'minFcv': '', 'role': 'read'},
           {'db': 'admin',
            'minFcv': '',
            'role': 'xgen-readWriteAtopsmanager.bigdata'},
           {'db': 'opsmanager', 'minFcv': '', 'role': 'dbAdmin'},
           {'db': 'sample_mflix', 'minFcv': '', 'role': 'dbAdmin'},
           {'db': 'sample_mflix', 'minFcv': '', 'role': 'readWrite'}]}
'''
def find_custom_roles(role_data):
    """
    Identify custom roles from the provided role data.
    
    Parameters:
    role_data (dict): A dictionary where keys are database names and values are lists of role dicts.
    
    Returns:
    list: A list of custom role names
    """
    # Define the set of MongoDB built-in roles
    built_in_roles = {
        'read', 'readWrite', 'dbAdmin', 'dbOwner', 'userAdmin', 'clusterAdmin', 'clusterManager',
        'clusterMonitor', 'hostManager', 'backup', 'restore', 'readAnyDatabase', 'readWriteAnyDatabase',
        'userAdminAnyDatabase', 'dbAdminAnyDatabase', 'root'
    }
    
    custom_roles = []
    # Iterate over each database in the role data
    for roles in role_data.values():
        # Check each role in the list
        for role in roles:
            role_name = role.get('role')
            # Check if role is neither a built-in nor starts with 'xgen'
            if role_name not in built_in_roles and not role_name.startswith('xgen'):
                custom_roles.append(role_name)
    
    return custom_roles


# Call the functions
connection_string = ""  # Replace with your connection string
user_name = "" # Replace with your username
#Add a custom user role to be able to see the roles of a concrete user
print("Check all the roles that a user has in all the databases:\n")
user_roles = get_user_roles(connection_string, user_name)
pprint(user_roles)
print("-----------------------------------------\n")
print("Find custom roles\n")
custom_roles=find_custom_roles(user_roles)
print("The custom roles:", custom_roles, "\n")
print("-----------------------------------------\n")
# Check the privileges of all the custom roles a user has
for custom_role in custom_roles:
    get_privileges_of_custom_role(connection_string, custom_role)
