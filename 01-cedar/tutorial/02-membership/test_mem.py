from cedarpy import Decision
from mem import checkAccess

def test_alice_and_bob():
    """Test Bob's access (member of both vacationPhotoJudges and juniorPhotographerJudges)."""
    assert checkAccess("Bob", "view", "vacationPhoto94.jpg") == Decision.Allow
    assert checkAccess("Bob", "view", "juniorPhotographerPhoto.jpg") == Decision.Allow
    
    assert checkAccess("Alice", "view", "juniorPhotographerPhoto.jpg") == Decision.Allow
    assert checkAccess("Alice", "view", "vacationPhoto94.jpg") == Decision.Deny

    assert checkAccess("Rando", "view", "genericPhoto.jpg") == Decision.Deny
    assert checkAccess("Rando", "view", "vacationPhoto94.jpg") == Decision.Deny
    assert checkAccess("Rando", "view", "juniorPhotographerPhoto.jpg") == Decision.Deny 


def test_eve_access():
    """Test Eve's access (member of PhotographyJudge)."""
    assert checkAccess("Eve", "view", "genericPhoto.jpg") == Decision.Allow
    assert checkAccess("Eve", "view", "vacationPhoto94.jpg") == Decision.Deny
    assert checkAccess("Eve", "view", "juniorPhotographerPhoto.jpg") == Decision.Deny

def test_group_parents():
    assert checkAccess("Alice", "view", "genericPhoto.jpg") == Decision.Allow  # Through PhotographyJudge parent role
    assert checkAccess("Bob", "view", "genericPhoto.jpg") == Decision.Allow  # Through PhotographyJudge parent role
