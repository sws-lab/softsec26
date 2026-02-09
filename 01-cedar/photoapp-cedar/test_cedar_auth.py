import pytest
from datetime import date
from app import User, Image, GuestUser
from cedar_auth import check_authorization

class MockUser(User):
    def __init__(self, id, is_admin=False, birthday=None):
        self.id = id
        self.is_admin = is_admin
        self.birthday = birthday or date(1990, 1, 1)

class MockGuestUser(GuestUser):
    def __init__(self):
        super().__init__()

class MockPhoto:
    def __init__(self, id, user_id, is_public=False, is_explicit=False):
        self.id = id
        self.user_id = user_id
        self.is_public = is_public
        self.is_explicit = is_explicit

def test_public_photo_access():
    """Test that any user can view public photos"""
    # Create a public photo
    photo = MockPhoto(id=1, user_id=1, is_public=True, is_explicit=False)
    
    # Test with regular user
    user = MockUser(id=2)
    assert check_authorization(user, "view", photo) == True
    
    # Test with admin
    admin = MockUser(id=3, is_admin=True)
    assert check_authorization(admin, "view", photo) == True
    
    # Test with guest user
    guest = GuestUser()
    assert check_authorization(guest, "view", photo) == True

def test_private_photo_access():
    """Test that users can only view their own private photos"""
    # Create a private photo
    photo = MockPhoto(id=1, user_id=1, is_public=False, is_explicit=False)
    
    # Owner should be able to view
    owner = MockUser(id=1)
    assert check_authorization(owner, "view", photo) == True
    
    # Other user should not be able to view
    other_user = MockUser(id=2)
    assert check_authorization(other_user, "view", photo) == False
    
    # Admin should not be able to view private photos
    admin = MockUser(id=3, is_admin=True)
    assert check_authorization(admin, "view", photo) == False

def test_explicit_content_restrictions():
    """Test that minors cannot view explicit content"""
    # Create an explicit photo
    photo = MockPhoto(id=1, user_id=1, is_public=True, is_explicit=True)
    
    # Minor user should not be able to view
    minor = MockUser(id=2, birthday=date(2010, 1, 1))
    assert check_authorization(minor, "view", photo) == False
    
    # Adult user should be able to view
    adult = MockUser(id=3, birthday=date(1990, 1, 1))
    assert check_authorization(adult, "view", photo) == True
    
    # Guest user (considered minor) should not be able to view
    guest = GuestUser()
    assert check_authorization(guest, "view", photo) == False

def test_photo_deletion_permissions():
    """Test photo deletion permissions"""
    # Create a public photo
    public_photo = MockPhoto(id=1, user_id=1, is_public=True, is_explicit=False)
    
    # Owner should be able to delete
    owner = MockUser(id=1)
    assert check_authorization(owner, "delete", public_photo) == True
    
    # Admin should be able to delete public photos
    admin = MockUser(id=3, is_admin=True)
    assert check_authorization(admin, "delete", public_photo) == True
    
    # Other user should not be able to delete
    other_user = MockUser(id=2)
    assert check_authorization(other_user, "delete", public_photo) == False
    
    # Test private photo deletion
    private_photo = MockPhoto(id=2, user_id=1, is_public=False, is_explicit=False)
    
    # Owner should be able to delete their private photo
    assert check_authorization(owner, "delete", private_photo) == True
    
    # Admin should not be able to delete private photos
    assert check_authorization(admin, "delete", private_photo) == False

def test_toggle_visibility_permissions():
    """Test visibility toggle permissions"""
    photo = MockPhoto(id=1, user_id=1, is_public=False, is_explicit=False)
    
    # Owner should be able to toggle visibility
    owner = MockUser(id=1)
    assert check_authorization(owner, "toggle", photo) == True
    
    # Admin should not be able to toggle visibility
    admin = MockUser(id=3, is_admin=True)
    assert check_authorization(admin, "toggle", photo) == False
    
    # Other user should not be able to toggle visibility
    other_user = MockUser(id=2)
    assert check_authorization(other_user, "toggle", photo) == False

def test_non_authenticated_user_access():
    """Test that non-authenticated users can only view public, non-explicit photos"""
    # Create a public, non-explicit photo
    public_safe_photo = MockPhoto(id=1, user_id=1, is_public=True, is_explicit=False)
    
    # Create a public, explicit photo
    public_explicit_photo = MockPhoto(id=2, user_id=1, is_public=True, is_explicit=True)
    
    # Create a private photo
    private_photo = MockPhoto(id=3, user_id=1, is_public=False, is_explicit=False)
    
    # Create a non-authenticated user
    non_auth_user = MockGuestUser()
    
    # Non-authenticated user should be able to view public, non-explicit photos
    assert check_authorization(non_auth_user, "view", public_safe_photo) == True
    
    # Non-authenticated user should not be able to view explicit photos
    assert check_authorization(non_auth_user, "view", public_explicit_photo) == False
    
    # Non-authenticated user should not be able to view private photos
    assert check_authorization(non_auth_user, "view", private_photo) == False
    
    # Non-authenticated user should not be able to delete any photos
    assert check_authorization(non_auth_user, "delete", public_safe_photo) == False
    assert check_authorization(non_auth_user, "delete", private_photo) == False
    
    # Non-authenticated user should not be able to toggle visibility
    assert check_authorization(non_auth_user, "toggle", public_safe_photo) == False 