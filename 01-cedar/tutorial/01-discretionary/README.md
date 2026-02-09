# Discretionary Access Control Exercise

This exercise demonstrates implementing discretionary access control (DAC) using Cedar. In DAC, the owner of a resource can grant or revoke access permissions to other users.

## Files
- `disc.cedar`: Cedar policy file
- `disc.cedarschema`: Cedar schema file
- `disc.py`: Python implementation
- `test_disc.py`: Test cases

## Exercise

The first test case is already implemented and passing:
- Alice can update "VacationPhoto94.jpg"

Your task is to implement the following access control rules:

1. Add permissions for Bob:
   - Bob should be able to view "Portrait.jpg"

2. Add view and delete permissions for Alice:
   - Alice should be able to view and delete "VacationPhoto94.jpg"
   - Bob should not have any permissions on "VacationPhoto94.jpg"

## Running the Tests
```bash
pytest test_disc.py -v
```

## Hint
You'll only need to modify the Cedar policy file (`disc.cedar`) to implement these access control rules. 
* https://www.cedarpolicy.com/en/tutorial/policy-structure
* https://www.cedarpolicy.com/en/tutorial/sets