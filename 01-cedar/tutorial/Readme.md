# Cedar Tutorial Exercises

This repository contains a series of exercises from [the Cedar Policy tutorial](https://www.cedarpolicy.com/en/tutorial), adapted for running with cedar-py. The instructions are on [the course website](https://courses.cs.ut.ee/2025/softsec/spring/Main/Cedar).

## Exercises

1. **[Discretionary Access Control](01-discretionary)**
   - Basic permission management
   - Granting and revoking access
   - Testing with `pytest 01-discretionary/`

2. **[Group Membership](02-membership/)**
   - Role-based access control
   - Group hierarchies
   - Testing with `pytest 02-membership/`

3. **[Relationship-Based Access](03-relationship/)**
   - Attribute-based access control
   - Department-based permissions
   - Testing with `pytest 03-relationship/`

## Running Tests

To run all tests:
```bash
pytest
```

Initially, this should pass 3 tests, and fail 5, as the exercises are incomplete. Your goal is to make all tests pass.

To run tests for a specific exercise:
```bash
pytest 01-discretionary/  # For discretionary access control
pytest 02-membership/    # For group membership
pytest 03-relationship/  # For relationship-based access
```

## Dependencies

- Python 3.13+
- pytest
- cedarpy

Install dependencies with:
```bash
pip install -r requirements.txt
```
