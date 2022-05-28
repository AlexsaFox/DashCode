from src.db.models import User
from tests.locale.utils import check_localization
from tests.utils import GraphQLClient


async def test_english_localization(graphql_client: GraphQLClient, user: User):
    await check_localization(
        graphql_client, user, 'en', 'Unable to find user with provided credentials'
    )


async def test_non_english_localization(graphql_client: GraphQLClient, user: User):
    await check_localization(
        graphql_client,
        user,
        'ru',
        'Не удалось найти пользователя с предоставленными учетными данными',
    )
