from typing import Dict, List

BUILT_IN_ROLES = {
    "read",
    "readWrite",
    "dbAdmin",
    "dbOwner",
    "userAdmin",
    "clusterAdmin",
    "clusterManager",
    "clusterMonitor",
    "hostManager",
    "backup",
    "restore",
    "readAnyDatabase",
    "readWriteAnyDatabase",
    "userAdminAnyDatabase",
    "dbAdminAnyDatabase",
    "root",
}


def findCustomRoles(roleData: Dict[str, List[dict]]) -> List[str]:
    """
    Identify custom roles from the provided role data.

    :param roleData: Dictionary where keys are database names and values are lists of role dicts.
    :return: A list of custom role names.
    """
    customRoles = []

    for roles in roleData.values():
        for role in roles:
            roleName = role.get("role")
            if (
                roleName
                and roleName not in BUILT_IN_ROLES
                and not roleName.startswith("xgen")
            ):
                customRoles.append(roleName)

    return customRoles
