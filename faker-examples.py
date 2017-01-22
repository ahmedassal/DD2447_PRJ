import networkx as nx
from networkx.utils import uniform_sequence
import matplotlib.pyplot as plt
from faker import Factory


# fake = Factory.create()
fake = Factory.create("en_US")
print(fake.name())

print(fake.city())

# names
print(fake.last_name_male())

print(fake.name_female())

print(fake.prefix_male())

print(fake.prefix())

print(fake.name())

print(fake.suffix_female())

print(fake.name_male())

print(fake.first_name())

print(fake.suffix_male())

print(fake.suffix())

print(fake.first_name_male())

print(fake.first_name_female())

print(fake.last_name_female())

print(fake.last_name())

print(fake.prefix_female())

# addresses
# fake("city")

for i in range(10):
    print(fake.city())


# ----------------------------------------------------------------------
def create_fake_cities(fake):
  """"""
  stuff = ["email", "bs", "address",
           "city", "state",
           "paragraph"]
  for item in stuff:
    print
    "%s = %s" % (item, getattr(fake, item)())


if __name__ == "__main__":
  fake = Factory.create()
  create_fake_stuff(fake)