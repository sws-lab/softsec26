from cedarpy import is_authorized, AuthzResult, Decision
import os
import json

# Change into this directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Read Cedar policy file
with open('rel.cedar', 'r') as file:
    policies: str = file.read()

# Read Cedar schema file
with open('rel.cedarschema', 'r') as file:
    schema: str = file.read()

# Read entities file
with open('rel.cedarentities.json', 'r') as file:
    entities: str = file.read()

def checkAccess(user, action, resource):
    """Check if a user has permission to perform an action on a resource."""
    request = {
        "principal": f'User::"{user}"',
        "action": f'Action::"{action}"',
        "resource": f'Photo::"{resource}"',
        "context": {}
    }

    print(f"Request: {request}")
    authz_result: AuthzResult = is_authorized(request, policies, entities, schema)
    print(f"Decision: {authz_result.decision}")
    return authz_result.decision 