from pymongo import MongoClient
from typing import Dict, List, Any
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
        self.username, self.password = self._extract_credentials(uri)

    """
    Extracts the username and password from a MongoDB connection string.

    @param {str} uri - MongoDB connection string.
    @return {(str, str)} - A tuple containing (username, password) or (None, None) if not found.
    """
    def _extract_credentials(self, uri: str) -> (str, str): # type: ignore
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

    @param {str} username - (Optional) The username to fetch roles for. If not provided, the username will be extracted from the URI.
    @return {Dict[str, List[Dict[str, Any]]]} - Dictionary with database names as keys and lists of role documents as values.
    """
    def getUserRoles(self, username: str = None) -> Dict[str, List[Dict[str, Any]]]:

        self.connect()
        rolesInfo = {}

        username = username or self.username
        if not username:
            raise ValueError("Username must be provided or extracted from the connection string.")

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

        return rolesInfo

    """
    Retrieves the privileges of a specific role.

    @param {str} roleName - The role name.
    @return {List[Dict[str, Any]]} - List of privileges associated with the role.
    """
    def getPrivilegesOfRole(self, roleName: str) -> List[Dict[str, Any]]:

        self.connect()
        privileges = []

        try:
            adminDb = self.client["admin"]
            roleInfo = adminDb.command("rolesInfo", roleName, showPrivileges=True)

            for role in roleInfo.get("roles", []):
                privileges.extend(role.get("privileges", []))
        finally:
            self.disconnect()

        return privileges
    
    """
    Verifies which permissions are missing or extra in a given set of roles.

    @param {List[str]} roleNames - List of role names to check.
    @param {List[Dict[str, Any]]} requiredPermissions - List of required permissions to compare against.
    @return {Dict[str, List[Dict[str, Any]]]} - JSON-style dictionary with 'extraPermissions' and 'missingPermissions'.
    """
    def verifyPermissions(self, roleNames: List[str], requiredPermissions: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:

        currentPermissions = set()
        for role in roleNames:
            currentPermissions.update(tuple(p.items()) for p in self.getPrivilegesOfRole(role))

        requiredPermissionsSet = set(tuple(p.items()) for p in requiredPermissions)

        return {
            "extraPermissions": [dict(p) for p in currentPermissions - requiredPermissionsSet],
            "missingPermissions": [dict(p) for p in requiredPermissionsSet - currentPermissions],
        }
