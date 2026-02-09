import os
from cedarpy import is_authorized, AuthzResult, Decision
from typing import Optional
import json

# Load Cedar schema and policies
with open('schema.cedarschema', 'r') as f:
    SCHEMA = f.read()

with open('policies.cedar', 'r') as f:
    POLICIES = f.read()

with open('groups.cedarentities.json', 'r') as f:
    GROUPS = json.load(f)

def get_user_entity(user) -> dict:
    """Convert a User model instance to a Cedar entity."""
    group = "Admin" if user.is_admin else "User"
    return {
        "uid": {"__entity": {"type": "User", "id": str(user.id)}},
        "attrs": {
            "isMinor": user.is_minor()
        },
        "parents": [
            {"__entity": {"type": "Group", "id": group}}
        ]
    }

def get_photo_entity(photo) -> dict:
    """Convert an Image model instance to a Cedar entity."""
    return {
        "uid": {"__entity": {"type": "Photo", "id": str(photo.id)}},
        "attrs": {
            "isPublic": photo.is_public,
            "isExplicit": photo.is_explicit,
            "owner": {"__entity": {"type": "User", "id": str(photo.user_id)}}
        },
        "parents": []
    }

def check_authorization(user, action: str, photo) -> bool:
    """
    Check if a user is authorized to perform an action on a photo.
    
    Args:
        user: The User model instance or None for anonymous users
        action: The action to check ("view" or "delete")
        photo: The Image model instance
    
    Returns:
        bool: True if authorized, False otherwise
    """
    # Create the authorization request
    request = {
        "principal": f'User::"{user.id}"',
        "action": f'Action::"{action}"',
        "resource": f'Photo::"{photo.id}"',
        "context": {
            "authenticated": user.is_authenticated
        }
    }
    
    entities = [
        get_user_entity(user),
        get_photo_entity(photo),
    ] + GROUPS
    
    # Check authorization
    result: AuthzResult = is_authorized(request, POLICIES, entities, SCHEMA)
    print("=== Authorization Request ===")
    print(json.dumps(request, indent=2))
    print("Decision: " + str(result.decision)) 
    print("Reasons: " + str(result.diagnostics.reasons))
    return result.allowed 