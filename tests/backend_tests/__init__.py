import json
import os

from aiohttp import ClientSession
from faker import Faker

SERVER_URL = "http://localhost:8001"
API_URL = f"{SERVER_URL}/api"


class PostgresTestClient:
    def __init__(self):
        self.session = ClientSession(SERVER_URL)


FAKE = Faker()


class DummyUser:
    prefix: str = "/api/user"

    def __init__(self, name: str, surname: str):
        self.name = name
        self.surname = surname

    @classmethod
    def generate(cls) -> "DummyUser":
        return cls(FAKE.first_name(), FAKE.last_name())

    @classmethod
    async def greet(cls, client: PostgresTestClient, desired_status: int = 200):
        async with client.session.get(f"{cls.prefix}/greeting") as resp:
            assert resp.status == desired_status
            return await resp.json()

    async def create_user(self, client: PostgresTestClient, desired_status: int = 200):
        async with client.session.post(
            f"{self.prefix}/create",
            params={"name": self.name, "surname": self.surname},
        ) as resp:
            assert resp.status == desired_status
            return await resp.json()

    @classmethod
    async def get_user(
        cls,
        name: str,
        surname: str,
        client: PostgresTestClient,
        desired_status: int = 200,
    ):
        async with client.session.get(
            f"{cls.prefix}",
            params={"name": name, "surname": surname},
        ) as resp:
            assert resp.status == desired_status
            return await resp.json()
