from . import models
from datetime import datetime

import names
import uuid
import random
import hashlib

now = datetime.now()

days_in_month = [
  31,
  28,
  31,
  30,
  31,
  30,
  31,
  31,
  30,
  31,
  30,
  31,
]


def generate_user():
  blockchain_info = models.blockchain.generate_blockchain_info()
  first_name = names.get_first_name()
  last_name = names.get_last_name()
  year = random.randint(1945, now.year)
  month = random.randint(1, 12)
  day = random.randint(1, days_in_month[month - 1])
  birthday = datetime(year, month, day)
  if birthday > now:
    birthday.replace(year=birthday.year - 1)
  age = int((now - birthday).days/365)
  anual_income = random.randint(1, 200)*1000 if age > 18 else 0
  return models.User(
    uuid              =  uuid.uuid4().hex,
    first_name        =  first_name,
    last_name         =  last_name,
    full_name         =  first_name + " " + last_name,
    birthday          =  birthday,
    age               =  age,
    anual_income      =  anual_income,
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