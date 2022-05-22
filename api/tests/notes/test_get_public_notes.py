import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User
from src.utils.note import create_note
from tests.auth.utils import check_auth_error
from tests.graphql.get_public_notes import GET_PUBLIC_NOTES_QUERY
from tests.utils import GraphQLClient


@pytest.fixture
async def create_test_notes(
    database_session: AsyncSession, user: User, another_user: User
):
    notes_data = [
        ('id', 'first', False, user),
        ('id', 'second', True, user),
        ('id', 'third', True, user),
        ('id', 'fourth', False, another_user),
        ('id', 'fifth', False, user),
        ('id', 'sixth', False, another_user),
        ('id', 'seventh', True, user),
        ('id', 'eighths', False, another_user),
        ('id', 'ninths', False, another_user),
        ('id', 'tenth', True, another_user),
        ('id', 'the last one', False, user),
    ]

    for i, (_, title, privacy, owner) in enumerate(notes_data):
        note = await database_session.run_sync(
            create_note,
            title=title,
            content='content',
            tags=[],
            link='',
            is_private=privacy,
            user=owner,
        )
        notes_data[i] = (note.id, title, privacy, owner)

    await database_session.close()

    return notes_data


async def test_get_public_notes_default_args(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    create_test_notes: list[tuple[str, str, bool, User]],
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=GET_PUBLIC_NOTES_QUERY,
        variables={},
        token=token,
    )
    assert data is not None
    assert data['getPublicNotes']['__typename'] == 'NoteConnection'


async def test_get_public_notes_success_type(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    create_test_notes: list[tuple[str, str, bool, User]],
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=GET_PUBLIC_NOTES_QUERY,
        variables={},
        token=token,
    )
    assert data is not None
    assert data['getPublicNotes']['__typename'] == 'NoteConnection'


async def test_get_public_notes_length(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    create_test_notes: list[tuple[str, str, bool, User]],
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=GET_PUBLIC_NOTES_QUERY,
        variables={'first': 3},
        token=token,
    )
    assert data is not None

    assert len(data['getPublicNotes']['edges']) == 3


async def test_get_public_notes_after(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    create_test_notes: list[tuple[str, str, bool, User]],
):
    token, _ = token_user

    (pub_id_1, _, _, _), (pub_id_2, _, _, _) = [
        note for note in create_test_notes if note[2] == False
    ][:2]

    data, _ = await graphql_client.get_request_data(
        query=GET_PUBLIC_NOTES_QUERY,
        variables={'after': pub_id_2},
        token=token,
    )
    assert data is not None

    edges = data['getPublicNotes']['edges']
    received_ids = [edge['node']['id'] for edge in edges]
    assert len(edges) == 5
    assert pub_id_1 not in received_ids
    assert pub_id_2 not in received_ids


async def test_get_public_notes_length_after(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    create_test_notes: list[tuple[str, str, bool, User]],
):
    token, _ = token_user

    public_ids = [note[0] for note in create_test_notes if note[2] == False]

    data, _ = await graphql_client.get_request_data(
        query=GET_PUBLIC_NOTES_QUERY,
        variables={
            'first': 2,
            'after': public_ids[1],
        },
        token=token,
    )
    assert data is not None

    edges = data['getPublicNotes']['edges']
    received_ids = [edge['node']['id'] for edge in edges]
    assert len(edges) == 2
    assert public_ids[0] not in received_ids
    assert public_ids[1] not in received_ids
    assert public_ids[2] in received_ids
    assert public_ids[3] in received_ids


async def test_get_public_notes_no_private_shown(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    create_test_notes: list[tuple[str, str, bool, User]],
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=GET_PUBLIC_NOTES_QUERY,
        variables={},
        token=token,
    )
    assert data is not None

    edges = data['getPublicNotes']['edges']
    received_privacy = [edge['node']['isPrivate'] for edge in edges]
    assert all(is_private == False for is_private in received_privacy)


async def test_get_public_notes_different_users(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    create_test_notes: list[tuple[str, str, bool, User]],
    user: User,
    another_user: User,
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=GET_PUBLIC_NOTES_QUERY,
        variables={},
        token=token,
    )
    assert data is not None

    edges = data['getPublicNotes']['edges']
    received_usernames = [edge['node']['user']['username'] for edge in edges]
    assert user.username in received_usernames
    assert another_user.username in received_usernames


async def test_get_public_notes_end_cursor(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    create_test_notes: list[tuple[str, str, bool, User]],
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=GET_PUBLIC_NOTES_QUERY,
        variables={'first': 3, 'after': None},
        token=token,
    )
    assert data is not None
    page_info = data['getPublicNotes']['pageInfo']
    end_cursor = page_info['endCursor']
    edges1 = data['getPublicNotes']['edges']
    received_ids = [edge['node']['id'] for edge in edges1]

    data, _ = await graphql_client.get_request_data(
        query=GET_PUBLIC_NOTES_QUERY,
        variables={'first': 4, 'after': end_cursor},
        token=token,
    )
    assert data is not None
    edges2 = data['getPublicNotes']['edges']
    received_ids += [edge['node']['id'] for edge in edges2]

    public_ids = [note[0] for note in create_test_notes if note[2] == False]
    assert received_ids == public_ids


async def test_get_public_notes_start_cursor(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    create_test_notes: list[tuple[str, str, bool, User]],
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=GET_PUBLIC_NOTES_QUERY,
        variables={},
        token=token,
    )
    assert data is not None
    page_info = data['getPublicNotes']['pageInfo']
    edges = data['getPublicNotes']['edges']
    assert page_info['startCursor'] == edges[0]['cursor']


async def test_get_public_notes_has_next_page_true(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    create_test_notes: list[tuple[str, str, bool, User]],
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=GET_PUBLIC_NOTES_QUERY,
        variables={'first': 6},
        token=token,
    )
    assert data is not None
    page_info = data['getPublicNotes']['pageInfo']
    assert page_info['hasNextPage']


async def test_get_public_notes_has_next_page_false(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    create_test_notes: list[tuple[str, str, bool, User]],
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=GET_PUBLIC_NOTES_QUERY,
        variables={'first': 7},
        token=token,
    )
    assert data is not None
    page_info = data['getPublicNotes']['pageInfo']
    assert not page_info['hasNextPage']


async def test_get_public_notes_after_last_note(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    create_test_notes: list[tuple[str, str, bool, User]],
):
    token, _ = token_user

    public_ids = [note[0] for note in create_test_notes if note[2] == False]

    data, _ = await graphql_client.get_request_data(
        query=GET_PUBLIC_NOTES_QUERY,
        variables={'after': public_ids[-1]},
        token=token,
    )
    assert data is not None
    page_info = data['getPublicNotes']['pageInfo']
    edges = data['getPublicNotes']['edges']

    assert page_info == {
        'hasNextPage': False,
        'startCursor': None,
        'endCursor': None,
    }
    assert len(edges) == 0


async def test_get_public_notes_requested_zero_elements_from_start(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    create_test_notes: list[tuple[str, str, bool, User]],
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=GET_PUBLIC_NOTES_QUERY,
        variables={'first': 0},
        token=token,
    )
    assert data is not None
    page_info = data['getPublicNotes']['pageInfo']
    edges = data['getPublicNotes']['edges']

    assert page_info == {
        'hasNextPage': True,
        'startCursor': None,
        'endCursor': None,
    }
    assert len(edges) == 0


async def test_get_public_notes_requested_zero_elements_from_middle(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    create_test_notes: list[tuple[str, str, bool, User]],
):
    token, _ = token_user

    public_ids = [note[0] for note in create_test_notes if note[2] == False]

    data, _ = await graphql_client.get_request_data(
        query=GET_PUBLIC_NOTES_QUERY,
        variables={'first': 0, 'after': public_ids[2]},
        token=token,
    )
    assert data is not None
    page_info = data['getPublicNotes']['pageInfo']
    edges = data['getPublicNotes']['edges']

    assert page_info == {
        'hasNextPage': True,
        'startCursor': None,
        'endCursor': None,
    }
    assert len(edges) == 0


async def test_get_public_notes_requested_zero_elements_from_last(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    create_test_notes: list[tuple[str, str, bool, User]],
):
    token, _ = token_user

    public_ids = [note[0] for note in create_test_notes if note[2] == False]

    data, _ = await graphql_client.get_request_data(
        query=GET_PUBLIC_NOTES_QUERY,
        variables={'first': 0, 'after': public_ids[-1]},
        token=token,
    )
    assert data is not None
    page_info = data['getPublicNotes']['pageInfo']
    edges = data['getPublicNotes']['edges']

    assert page_info == {
        'hasNextPage': False,
        'startCursor': None,
        'endCursor': None,
    }
    assert len(edges) == 0


async def test_get_public_notes_no_notes_created(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=GET_PUBLIC_NOTES_QUERY,
        variables={'first': 7},
        token=token,
    )
    assert data is not None
    page_info = data['getPublicNotes']['pageInfo']
    edges = data['getPublicNotes']['edges']

    assert page_info == {
        'hasNextPage': False,
        'startCursor': None,
        'endCursor': None,
    }
    assert len(edges) == 0


async def test_get_public_notes_after_private_note(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    create_test_notes: list[tuple[str, str, bool, User]],
):
    token, _ = token_user

    private_ids = [note[0] for note in create_test_notes if note[2] == True]

    data, _ = await graphql_client.get_request_data(
        query=GET_PUBLIC_NOTES_QUERY,
        variables={'after': private_ids[0]},
        token=token,
    )
    assert data is not None
    assert data['getPublicNotes']['__typename'] == 'RequestValueError'
    assert data['getPublicNotes']['details'] == 'Unable to find a note with provided id'


async def test_get_public_notes_invalid_cursor(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    create_test_notes: list[tuple[str, str, bool, User]],
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=GET_PUBLIC_NOTES_QUERY,
        variables={'after': 'invalid-note'},
        token=token,
    )
    assert data is not None
    assert data['getPublicNotes']['__typename'] == 'RequestValueError'
    assert data['getPublicNotes']['details'] == 'Unable to find a note with provided id'


async def test_get_public_notes_no_auth(
    graphql_client: GraphQLClient,
    create_test_notes: list[tuple[str, str, bool, User]],
):
    data, errors = await graphql_client.get_request_data(
        query=GET_PUBLIC_NOTES_QUERY,
        variables={},
    )
    check_auth_error(data, errors)
