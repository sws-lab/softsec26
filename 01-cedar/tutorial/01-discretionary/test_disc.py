from cedarpy import Decision
from disc import accessPhoto

def test_initial_permissions():
    """Test initial permissions where Alice can update VacationPhoto94.jpg."""
    assert accessPhoto("alice", "VacationPhoto94.jpg", "update") == Decision.Allow

def test_add_bob_permissions():
    """Test adding permissions for Bob to update Portrait.jpg."""
    assert accessPhoto("bob", "Portrait.jpg", "view") == Decision.Allow

def test_add_view_delete_permissions_for_alice():
    """Test adding view and delete permissions for Alice on VacationPhoto94.jpg."""
    assert accessPhoto("alice", "VacationPhoto94.jpg", "view") == Decision.Allow
    assert accessPhoto("alice", "VacationPhoto94.jpg", "delete") == Decision.Allow
    # Make sure Bob doesn't have any permissions
    assert accessPhoto("bob", "Portrait.jpg", "update") == Decision.Deny
    assert accessPhoto("bob", "Portrait.jpg", "delete") == Decision.Deny
    assert accessPhoto("bob", "VacationPhoto94.jpg", "update") == Decision.Deny
    assert accessPhoto("bob", "VacationPhoto94.jpg", "view") == Decision.Deny
    assert accessPhoto("bob", "VacationPhoto94.jpg", "delete") == Decision.Deny 