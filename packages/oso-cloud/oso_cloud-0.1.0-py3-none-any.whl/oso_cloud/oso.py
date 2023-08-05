import json
from typing import Tuple

import requests


def extract_type_and_id(obj) -> Tuple[str, str]:
    if not hasattr(obj, "__dict__"):
        raise TypeError(f"Expected an instance of a class but received: {obj}")
    if not hasattr(obj, "id"):
        raise TypeError(f"Expected {obj} to have an 'id' attribute")
    return (obj.__class__.__name__, obj.id)


def to_params(role_or_relation, from_type, from_id, name, to_type, to_id):
    from_name = "resource" if role_or_relation == "role" else "from"
    to_name = "actor" if role_or_relation == "role" else "to"
    return {
        from_name + "_id": str(from_id),
        from_name + "_type": from_type,
        role_or_relation: name,
        to_name + "_id": str(to_id),
        to_name + "_type": to_type,
    }


class Oso:
    def __init__(self, service_url="http://localhost:8080"):
        self.service_url = service_url

    def _handle_result(self, result):
        if not result.ok:
            code, text = result.status_code, result.text
            msg = f"Got unexpected error from Oso Service: {code}\n{text}"
            raise Exception(msg)
        try:
            return result.json()
        except json.decoder.JSONDecodeError:
            return result.text

    def authorize(self, actor, action, resource):
        actor_type, actor_id = extract_type_and_id(actor)
        resource_type, resource_id = extract_type_and_id(resource)
        result = requests.post(
            f"{self.service_url}/authorize",
            json={
                "actor_type": actor_type,
                "actor_id": str(actor_id),
                "action": action,
                "resource_type": resource_type,
                "resource_id": str(resource_id),
            },
        )
        allowed = self._handle_result(result)["allowed"]
        return allowed

    def list(self, actor, action, resource_type):
        actor_type, actor_id = extract_type_and_id(actor)
        result = requests.post(
            f"{self.service_url}/list",
            json={
                "actor_type": actor_type,
                "actor_id": str(actor_id),
                "action": action,
                "resource_type": resource_type,
            },
        )
        results = self._handle_result(result)["results"]
        return results

    def _add_role_or_relation(self, role_or_relation, from_, name, to):
        from_type, from_id = extract_type_and_id(from_)
        to_type, to_id = extract_type_and_id(to)
        params = to_params(role_or_relation, from_type, from_id, name, to_type, to_id)
        result = requests.post(f"{self.service_url}/{role_or_relation}s", json=params)
        return self._handle_result(result)

    def _delete_role_or_relation(self, role_or_relation, from_, name, to):
        from_type, from_id = extract_type_and_id(from_)
        to_type, to_id = extract_type_and_id(to)
        params = to_params(role_or_relation, from_type, from_id, name, to_type, to_id)
        result = requests.delete(f"{self.service_url}/{role_or_relation}s", json=params)
        return self._handle_result(result)

    def add_role(self, actor, role_name, resource):
        return self._add_role_or_relation("role", resource, role_name, actor)

    def add_relation(self, subject, name, object):
        return self._add_role_or_relation("relation", subject, name, object)

    def delete_role(self, actor, role_name, resource):
        return self._delete_role_or_relation("role", resource, role_name, actor)

    def delete_relation(self, subject, name, object):
        return self._delete_role_or_relation("relation", subject, name, object)

    def get_roles(self, resource=None, role=None, actor=None):
        params = {}
        if actor:
            actor_type, actor_id = extract_type_and_id(actor)
            params["actor_type"] = actor_type
            params["actor_id"] = actor_id
        if resource:
            resource_type, resource_id = extract_type_and_id(resource)
            params["resource_type"] = resource_type
            params["resource_id"] = resource_id
        if role:
            params["role"] = role
        result = requests.get(f"{self.service_url}/roles", params=params)
        return self._handle_result(result)
