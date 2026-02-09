from cedarpy import is_authorized, AuthzResult, Decision
import os

#Change into this directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('disc.cedar', 'r') as file:
    policies: str = file.read()

with open('disc.cedarschema', 'r') as file:
    schema: str = file.read()

# Not needed for discretionary policies
entities: list = [ ]

def accessPhoto(user, photo, action):
    request = {
        "principal": f'User::"{user}"',
        "action": f'Action::"{action}"',
        "resource": f'Photo::"{photo}"',
        "context": {}
    }

    print(f"Request: {request}")
    authz_result: AuthzResult = is_authorized(request, policies, entities, schema)
    print(authz_result.decision)
    return authz_result.decision

