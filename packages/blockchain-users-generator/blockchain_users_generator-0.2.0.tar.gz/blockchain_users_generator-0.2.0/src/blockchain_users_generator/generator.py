from . import models

import names
import uuid
import random
import hashlib

def generate_user():
  blockchain_info = models.blockchain.generate_blockchain_info()
  first_name = names.get_first_name()
  last_name = names.get_last_name()
  return models.User(
    uuid              =  uuid.uuid4().hex,
    first_name        =  first_name,
    last_name         =  last_name,
    full_name         =  first_name + " " + last_name,
    age               =  random.randint(1, 101),
    username          =  (first_name + last_name).lower() + str(random.randint(100, 9999)),
    password          =  hashlib.md5(uuid.uuid4().hex.encode()).digest().hex(),
    gender            =  models.user.get_random_user_gender(),
    country_info      =  models.country.get_random_country(),
    blockchain_info   =  blockchain_info,
  )

def generate(number_of_users):
  users = []
  for _ in range(0, number_of_users):
    user = generate_user()
    users.append(user)
  return users