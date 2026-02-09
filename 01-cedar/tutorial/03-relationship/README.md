# Relationship-Based Access Control Exercise

This exercise demonstrates implementing relationship-based access control using Cedar, where access is determined by relationships between entities (like ownership and department membership).

## Files
- `rel.cedar`: Cedar policy file
- `rel.cedarschema`: Cedar schema file
- `rel.cedarentities.json`: Entity definitions including relationships
- `rel.py`: Python implementation
- `test_rel.py`: Test cases

## Exercise

The first test case is already implemented and passing:
- Alice has full access (view, edit, delete) to her own photo "VacationPhoto94.jpg"
- Bob has full access (view, edit, delete) to his own photo "Portrait.jpg"

Your task is to implement the following access control rules:
- Charlie (in the same department as Alice) should be able to view "VacationPhoto94.jpg"
- Charlie should not be able to edit or delete "VacationPhoto94.jpg"
- Bob (in a different department) should not be able to view, edit, or delete "VacationPhoto94.jpg"

## Running the Tests
```bash
pytest test_rel.py -v
```

## Hint
You'll need to only edit the policy:
* https://www.cedarpolicy.com/en/tutorial/abac-pt2