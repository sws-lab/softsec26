from cedarpy import Decision
from rel import checkAccess

def test_owner_based_access():
    """Test owner-based access control."""
    # Test Alice's access to her own photo
    assert checkAccess("alice", "view", "VacationPhoto94.jpg") == Decision.Allow
    assert checkAccess("alice", "edit", "VacationPhoto94.jpg") == Decision.Allow
    assert checkAccess("alice", "delete", "VacationPhoto94.jpg") == Decision.Allow
    
    # Test Bob's access to his own photo
    assert checkAccess("bob", "view", "Portrait.jpg") == Decision.Allow
    assert checkAccess("bob", "edit", "Portrait.jpg") == Decision.Allow
    assert checkAccess("bob", "delete", "Portrait.jpg") == Decision.Allow

def test_department_based_access():
    """Test department-based access control."""
    # Test Charlie's access to photos in same department
    assert checkAccess("charlie", "view", "VacationPhoto94.jpg") == Decision.Allow  # Same dept
    assert checkAccess("charlie", "edit", "VacationPhoto94.jpg") == Decision.Deny    # Different dept, no edit
    assert checkAccess("charlie", "delete", "VacationPhoto94.jpg") == Decision.Deny  # Different dept, no delete

    # Test Bob's access to Alice's photo (different owner and department)
    assert checkAccess("bob", "view", "VacationPhoto94.jpg") == Decision.Deny
    assert checkAccess("bob", "edit", "VacationPhoto94.jpg") == Decision.Deny
    assert checkAccess("bob", "delete", "VacationPhoto94.jpg") == Decision.Deny 