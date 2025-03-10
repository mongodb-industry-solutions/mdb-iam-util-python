import pytest
from src.mongo_role_manager import MongoRoleManager


@pytest.fixture
def roleManager():
    return MongoRoleManager("mongodb://localhost:27017")


def test_verifyPermissions(roleManager):
    roleNames = ["readWriteRole"]
    requiredPermissions = [
        {"resource": {"db": "test", "collection": ""}, "actions": ["find"]}
    ]

    extra, missing = roleManager.verifyPermissions(roleNames, requiredPermissions)

    assert isinstance(extra, list)
    assert isinstance(missing, list)
