# Membership-Based Access Control Exercise

This exercise demonstrates implementing role-based access control (RBAC) using Cedar, where access is determined by group memberships and hierarchical roles.

## Files
- `mem.cedar`: Cedar policy file
- `mem.cedarschema`: Cedar schema file
- `mem.cedarentities.json`: Entity definitions including group memberships
- `mem.py`: Python implementation
- `test_mem.py`: Test cases

## Exercise

The first test case is already implemented and passing:
- Bob (member of both `vacationPhotoJudges` and `juniorPhotographerJudges`) can view both "vacationPhoto94.jpg" and "juniorPhotographerPhoto.jpg"
- Alice (member of `juniorPhotographerJudges`) should be able to view "juniorPhotographerPhoto.jpg", but Alice should not be able to view "vacationPhoto94.jpg"
- Rando (not a member of any groups) cannot view any photos

Your task is to implement the following access control rules:

1. Add a new user Eve and a new group `PhotographyJudge` (yes, it's Photo, Photographer, and Photography!):
   - Eve should be a member of `PhotographyJudge`.
   - Members of `PhotographyJudge` should be able to view "genericPhoto.jpg"
   - Eve should not be able to view "vacationPhoto94.jpg" or "juniorPhotographerPhoto.jpg"

2. Implement role hierarchy:
   - `PhotographyJudge` should be a parent role
   - Members of child roles (like `vacationPhotoJudges` and `juniorPhotographerJudges`) should inherit access to "genericPhoto.jpg"

## Running the Tests
```bash
pytest test_mem.py -v
```

## Hint
You'll need add one rule for the new group in the policies file, but most work is with the entities (`mem.cedarentities.json`).
* https://www.cedarpolicy.com/en/tutorial/rbac