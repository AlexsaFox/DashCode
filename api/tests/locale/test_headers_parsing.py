from src.db.models import User
from tests.utils import GraphQLClient
from tests.locale.utils import check_localization


async def test_order(graphql_client: GraphQLClient, user: User):
    header = 'en-US;q=0.5, ru-RU;q=1'
    await check_localization(
        graphql_client, user, header, 'Пользователь с указанными данными не был найден'
    )


async def test_wildcart(graphql_client: GraphQLClient, user: User):
    header = '*;q=1, ru;q=0.5'
    await check_localization(
        graphql_client, user, header, 'Unable to find user with provided credentials'
    )


async def test_no_quality(graphql_client: GraphQLClient, user: User):
    header = 'ru-RU, en-US'
    await check_localization(
        graphql_client, user, header, 'Пользователь с указанными данными не был найден'
    )


async def test_non_existing_locale(graphql_client: GraphQLClient, user: User):
    header = 'xx-XX;q=1, ru;q=0.001'
    await check_localization(
        graphql_client, user, header, 'Пользователь с указанными данными не был найден'
    )


async def test_fallback_locale(graphql_client: GraphQLClient, user: User):
    header = 'xx-XX;q=1, yy;q=0.001'
    await check_localization(
        graphql_client, user, header, 'Unable to find user with provided credentials'
    )


async def test_bad_header(graphql_client: GraphQLClient, user: User):
    header = 'B;A,D;-HE=,,aD;q=0.1er,'
    await check_localization(
        graphql_client, user, header, 'Unable to find user with provided credentials'
    )
