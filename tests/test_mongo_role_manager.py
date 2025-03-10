import pytest
from src.mongo_role_manager import MongoRoleManager

connectionString = "mongodb+srv://dorottya:passwordone@solutionsassurance.n0kts.mongodb.net/?retryWrites=true&w=majority&appName=SolutionsAssurance"


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
