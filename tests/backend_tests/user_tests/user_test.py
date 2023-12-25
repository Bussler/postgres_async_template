import pytest

from backend_tests import DummyUser, PostgresTestClient


@pytest.mark.asyncio
async def test_greeting():
    client = PostgresTestClient()
    greeting = await DummyUser.greet(client)
    assert greeting["greeting"] == "Hello, user!"


@pytest.mark.asyncio
async def test_create_user():
    client = PostgresTestClient()
    user = DummyUser.generate()
    created_user = await user.create_user(client)
    assert created_user["name"] == user.name
    assert created_user["surname"] == user.surname


@pytest.mark.asyncio
async def test_get_user():
    client = PostgresTestClient()
    user = DummyUser.generate()
    created_user = await user.create_user(client)
    fetched_users = await DummyUser.get_user(user.name, user.surname, client)

    assert len(fetched_users) >= 1

    for fuser in fetched_users:
        assert fuser["name"] == user.name
        assert fuser["surname"] == user.surname
