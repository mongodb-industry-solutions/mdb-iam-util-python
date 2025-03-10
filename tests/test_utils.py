from src.utils import findCustomRoles

def test_findCustomRoles():
    roleData = {
        "admin": [
            {"role": "customRole1", "db": "admin"},
            {"role": "read", "db": "admin"},
        ]
    }

    result = findCustomRoles(roleData)

    assert "customRole1" in result
    assert "read" not in result
