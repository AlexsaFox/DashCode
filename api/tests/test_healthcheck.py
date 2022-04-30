from httpx import AsyncClient


async def test_ping(client: AsyncClient) -> None:
    response = await client.get('/ping')

    assert response.status_code == 200
    assert response.json() == 'pong'
