import pytest
import os

from src import MongoRoleManager

db_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")
db_host = os.environ.get("DB_HOST")

connectionString = f"mongodb+srv://{db_username}:{db_password}@{db_host}/?retryWrites=true&w=majority&appName=SolutionsAssurance"


@pytest.fixture
def roleManager():
    return MongoRoleManager(connectionString)


def test_verifyPermissions(roleManager):
    requiredPermissions = [
        "search",
        "read",
        "find",
        "insert",
        "update",
        "remove",
        "collMod",
    ]

    res = roleManager.verifyPermissions(requiredPermissions)

    assert isinstance(res["extra"], list)
    assert isinstance(res["missing"], list)
    assert isinstance(res["present"], list)

    assert sorted(res["missing"]) == sorted(["search", "read"])
    assert sorted(res["present"]) == sorted(
        ["find", "insert", "update", "remove", "collMod"]
    )
    assert len(res["extra"]) > 5
