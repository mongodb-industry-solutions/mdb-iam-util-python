from pymongo import MongoClient
from typing import Dict, List, Dict, Set
import re

"""
Class to manage MongoDB user roles and permissions.
"""

class MongoRoleManager:
    """
    Initializes MongoRoleManager with a MongoDB connection URI.

    @param {str} uri - MongoDB connection string.
    """

    def __init__(self, uri: str):
        self.uri = uri
        self.client = None
        self.username, self.password = self.extractCredentials(uri)

    """
    Extracts the username and password from a MongoDB connection string.

    @param {str} uri - MongoDB connection string.
    @return {(str, str)} - A tuple containing (username, password) or (None, None) if not found.
    """

    def extractCredentials(self, uri: str) -> (str, str):  # type: ignore
        match = re.search(r"mongodb\+srv://([^:]+):([^@]+)@", uri)
        if match:
            return match.group(1), match.group(2)
        return None, None

    """
    Establishes a MongoDB connection.
    """

    def connect(self):
        if not self.client:
            self.client = MongoClient(self.uri)

    """
    Closes the MongoDB connection.
    """

    def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None

    """
    Retrieves all roles assigned to a user across all databases.

    @param {str} [username] - (Optional) The username to fetch roles for. If not provided, the username will be extracted from the URI.
    @return {List[str]} - Dictionary with database names as keys and lists of role documents as values.
    """

    def getUserRoles(self, username: str = None) -> List[str]:

        self.connect()
        rolesInfo = {}

        username = username or self.username
        if not username:
            raise ValueError(
                "Username must be provided or extracted from the connection string."
            )

        try:
            databases = self.client.list_database_names()

            for dbName in databases:
                try:
                    db = self.client[dbName]
                    userInfo = db.command("usersInfo", username)

                    if userInfo.get("users"):
                        userRoles = userInfo["users"][0].get("roles", [])
                        rolesInfo[dbName] = userRoles
                except Exception:
                    pass  # Ignore databases where the user does not exist
        finally:
            self.disconnect()

        if "admin" in rolesInfo and isinstance(rolesInfo["admin"], list):
            return list(
                set(
                    [
                        item["role"]
                        for item in rolesInfo["admin"]
                        if isinstance(item, dict) and "role" in item
                    ]
                )
            )
        else:
            return []

    """
    Retrieves the privileges of a specific role.

    @param {str} roleName - The role name.
    @return {List[str]} - List of privileges associated with the role.
    """

    def getPrivilegesOfRole(self, roleName: str) -> List[str]:
        self.connect()
        privileges = set()  # Use this type to eliminate duplicate values

        try:
            adminDb = self.client["admin"]
            roleInfo = adminDb.command(
                "rolesInfo", roleName, showPrivileges=True, showBuiltinRoles=True
            )

            roles = roleInfo.get("roles", [])
            if roles and isinstance(roles, list):
                for role in roles:
                    for privilege in role.get("privileges", []):
                        actions = privilege.get("actions", [])
                        if actions and isinstance(actions, list):
                            privileges.update(
                                actions
                            )  # Using update to add multiple elements at a time

        except Exception as e:
            print(f"Error inesperado: {e}")

        finally:
            self.disconnect()

        return list(privileges)

    """
    Verifies which permissions are missing, present or extra in a given set of roles.

    @param {List[str]} requiredPermissions - List of required permissions to compare against.
    @param {List[str]} [roleNames] - Optional list of role names to check.
    @return {Dict[str, List[str]]} - JSON-style dictionary with 'extra', 'missing' and 'present' permissions.
    """

    def verifyPermissions(
        self, requiredPermissions: List[str], roleNames: List[str] = None
    ) -> Dict[str, List[str]]:
        try:
            if roleNames is None:
                roleNames = self.getUserRoles()

            # Use a set for efficient permission storage and lookup
            currentPermissions: Set[str] = set()

            # Fetch permissions for each role and update the set
            for role in roleNames:
                currentPermissions.update(self.getPrivilegesOfRole(role))

            # Convert required permissions to a set for efficient set operations
            requiredPermissionsSet: Set[str] = set(requiredPermissions)

            # Calculate extra, missing, and present permissions using set operations
            extraPermissions: List[str] = list(
                currentPermissions - requiredPermissionsSet
            )
            missingPermissions: List[str] = list(
                requiredPermissionsSet - currentPermissions
            )
            presentPermissions: List[str] = list(
                requiredPermissionsSet.intersection(currentPermissions)
            )

            return {
                "extra": extraPermissions,
                "missing": missingPermissions,
                "present": presentPermissions,
            }

        except Exception as e:
            # Log the error for debugging purposes (consider using a logging library)
            print(f"Unexpected error: {e}")
            return {
                "extra": [],
                "missing": [],
                "present": [],
            }  # Return empty lists in case of error.
