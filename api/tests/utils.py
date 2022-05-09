from typing import Any

from httpx import AsyncClient, Response


class GraphQLClient:
    def __init__(self, client: AsyncClient):
        self.client = client

    async def make_request(
        self,
        query: str,
        variables: dict[str, Any] | None = None,
        token: str | None = None,
        lang_header: str = 'en',
    ) -> Response:
        headers = {'Accept-Language': lang_header}
        if token is not None:
            headers['Authorization'] = f'Bearer {token}'

        response = await self.client.post(
            '/graphql',
            json={'query': query, 'variables': variables},
            headers=headers,
        )

        return response

    async def get_request_data(
        self,
        query: str,
        variables: dict[str, Any] | None = None,
        token: str | None = None,
        lang_header: str = 'en',
    ) -> tuple[dict[str, Any] | None, list[dict[str, Any]] | None]:
        response = await self.make_request(query, variables, token, lang_header)
        assert response.status_code == 200

        response_json = response.json()
        data = response_json.get('data')
        errors = response_json.get('errors')
        return data, errors
