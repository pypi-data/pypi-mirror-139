from dataclasses import dataclass

from oso_cloud import Oso


@dataclass
class User:
    id: str


@dataclass
class Organization:
    id: str


@dataclass
class Repository:
    id: str
    parent: Organization


oso = Oso("http://localhost:8080")

bob = User("bob")
acme = Organization("acme")
anvil = Repository("anvil", acme)

# oso.add_role(bob, "owner", acme)
# oso.add_relation(anvil, "parent", acme)
# oso.delete_role(bob, "maintainer", anvil)
# oso.delete_relation(anvil, "parent", acme)

print(f'{oso.authorize(bob, "read", anvil)=}')

print(f'{oso.list(bob, "read", "Repository")=}')
