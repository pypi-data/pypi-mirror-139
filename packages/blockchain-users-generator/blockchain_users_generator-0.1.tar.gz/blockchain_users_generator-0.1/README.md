# Generate random users with blockchain information included

## Installation

```
pip install blockchain_users_generator
```

## Example of use

```
from blockchain_users_generator import generator as blockchain_users_generator
users  = blockchain_users_generator.generate(1000)
users_dict = [user.to_dict() for user in users]

print("\n\n------model------\n", users[0])
print("\n\n------dict-------\n", users_dict[0])
```
