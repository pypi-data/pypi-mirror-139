from dataclasses import dataclass
from . import blockchain, country
import random
from dataclasses import asdict

genders = ["female", "male"]

@dataclass
class User:
  uuid:             str
  first_name:       str
  last_name:        str
  full_name:        str
  username:         str = None
  password:         str = None
  gender:           str = None
  country_info:     country.CountryInfo = None
  blockchain_info:  blockchain.BlockchainInfo = None
  def to_dict(self):
    return asdict(self)
def get_random_user_gender():
  return random.choice(genders)