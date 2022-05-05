from src.db.models import User
from tests.utils import GraphQLClient
from tests.locale.utils import check_localization


async def test_english_localization(graphql_client: GraphQLClient, user: User):
    await check_localization(
        graphql_client, user, 'en', 'Unable to find user with provided credentials'
    )


async def test_non_english_localization(graphql_client: GraphQLClient, user: User):
    await check_localization(
        graphql_client, user, 'ru', 'Пользователь с указанными данными не был найден'
    )
