from typing import Any
from httpx import AsyncClient, Response


class GraphQLClient:
    def __init__(self, client: AsyncClient):
        self.client = client

    async def make_request(
        self,
        query: str,
        token: str | None = None,
    ) -> Response:
        headers = {}
        if token is not None:
            headers['Authorization'] = f'Bearer {token}'

        response = await self.client.post(
            '/graphql',
            json={'query': query},
            headers=headers,
        )

        return response
