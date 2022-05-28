import os
from secrets import token_bytes
from tempfile import NamedTemporaryFile
from typing import IO, Any, Generator

import pytest
from httpx import AsyncClient

from src.config import Configuration
from src.db.models import User
from src.utils.file_upload import get_image_mime_type


async def send_file(
    client: AsyncClient,
    file_path: str,
    token: str,
    content_type: str | None = None,
) -> tuple[dict[str, Any] | None, list[dict[str, Any]] | None]:
    payload = {
        'operations': (
            '{"query": "mutation ($newUsername: String, $newProfileColor: String,'
            ' $newProfilePicture: Upload) {editAccount(newUsername: $newUsername,'
            ' newProfileColor: $newProfileColor,newProfilePicture: $newProfilePicture)'
            ' {__typename ... on EditAccountSuccess {account {email username'
            ' profileColor profilePictureFilename}}... on ValidationError {fields'
            ' {field details}}... on RequestValueError{details}}}","variables": {'
            ' "newProfilePicture": 123 }}'
        ),
        'map': '{"0": ["variables.newProfilePicture"]}',
    }

    _, filename = os.path.split(file_path)
    _, _, extension = filename.rpartition('.')
    if content_type is None:
        content_type = get_image_mime_type(extension)
    files = [('0', (filename, open(file_path, 'rb'), content_type))]

    headers = {'Authorization': f'Bearer {token}'}

    response = await client.post(
        url='/graphql', data=payload, files=files, headers=headers
    )

    assert response.status_code == 200
    response_json = response.json()
    data = response_json.get('data')
    errors = response_json.get('errors')
    return data, errors


def file_exists(uploaded_file_name: str, config: Configuration) -> bool:
    upload_path = config.file_upload.upload_path
    uploaded_path = os.path.join(upload_path, uploaded_file_name)
    return os.path.exists(uploaded_path)


def identifiers_are_same(
    compared: bytes, uploaded_file_name: str, config: Configuration
) -> bool:
    try:
        compared_identifier = compared[:32]

        upload_path = config.file_upload.upload_path
        uploaded_path = os.path.join(upload_path, uploaded_file_name)
        with open(uploaded_path, 'rb') as f:
            uploaded_file_identifier = f.read(32)

        return compared_identifier == uploaded_file_identifier
    except FileNotFoundError:
        return False


def files_are_same(
    temp_file: IO[bytes], uploaded_file_name: str, config: Configuration
) -> bool:
    temp_file.seek(0)
    temp_file_identifier = temp_file.read(32)
    return identifiers_are_same(temp_file_identifier, uploaded_file_name, config)


def check_good_response(
    data: dict[str, Any] | None,
    errors: list[dict[str, Any]] | None,
    temp_file: IO[bytes],
    config: Configuration,
):
    assert data is not None
    assert errors is None

    uploaded_file_name = data['editAccount']['account']['profilePictureFilename']
    assert file_exists(uploaded_file_name, config)
    assert files_are_same(temp_file, uploaded_file_name, config)


def check_bad_response(
    data: dict[str, Any] | None, errors: list[dict[str, Any]] | None, error_message: str
):
    assert data is not None
    assert errors is None

    assert data['editAccount']['__typename'] == 'RequestValueError'
    assert data['editAccount']['details'] == error_message


def temp_file(
    extension: str, size_bytes: int, test_config: Configuration
) -> Generator[IO[bytes], None, None]:
    temp_file = NamedTemporaryFile(
        'a+b', suffix=f'.{extension}', dir=test_config.file_upload.upload_path
    )
    temp_file.write(token_bytes(32))  # Unique identifier for this file
    temp_file.write(b'\x00' * (size_bytes - 32))
    temp_file.seek(0)

    yield temp_file

    temp_file.close()


@pytest.fixture(name='temp_file', scope='function')
def temp_file_fixture(request, test_config: Configuration) -> IO[bytes]:
    extension: str = request.param[0]
    size_bytes: int = request.param[1]
    return temp_file(extension, size_bytes, test_config).__next__()


@pytest.mark.parametrize('temp_file', [('png', 1024)], indirect=True)
async def test_valid_image_upload(
    client: AsyncClient,
    token_user: tuple[str, User],
    test_config: Configuration,
    temp_file: IO[bytes],
):
    token, _ = token_user
    data, errors = await send_file(client, temp_file.name, token)
    check_good_response(data, errors, temp_file, test_config)


def get_extension_test_factory(
    extension: str,
    should_fail: bool,
    client: AsyncClient,
    token_user: tuple[str, User],
    test_config: Configuration,
):
    async def test_extension_upload():
        file = temp_file(extension, 1024, test_config).__next__()

        token, _ = token_user
        data, errors = await send_file(
            client, file.name, token, content_type='image/jpeg'
        )

        if should_fail:
            check_bad_response(data, errors, 'Only images are allowed')
        else:
            check_good_response(data, errors, file, test_config)

    return test_extension_upload


@pytest.mark.parametrize('temp_file', [('png', 1024 * 1024 * 16)], indirect=True)
async def test_big_but_not_too_big_upload(
    client: AsyncClient,
    token_user: tuple[str, User],
    test_config: Configuration,
    temp_file: IO[bytes],
):
    token, _ = token_user
    data, errors = await send_file(client, temp_file.name, token)
    check_good_response(data, errors, temp_file, test_config)


@pytest.mark.parametrize('temp_file', [('png', 1024 * 1024 * 16 + 1)], indirect=True)
async def test_too_big_upload(
    client: AsyncClient,
    token_user: tuple[str, User],
    temp_file: IO[bytes],
):
    token, _ = token_user
    data, errors = await send_file(client, temp_file.name, token)
    check_bad_response(data, errors, "Uploaded file size can't be larger than 16MB")


async def test_good_file_extensions(
    client: AsyncClient, token_user: tuple[str, User], test_config: Configuration
):
    for extension in test_config.file_upload.allowed_extensions:
        test = get_extension_test_factory(
            extension, False, client, token_user, test_config
        )
        await test()


async def test_bad_file_extensions(
    client: AsyncClient, token_user: tuple[str, User], test_config: Configuration
):
    bad_extensions = ['txt', 'xml', 'pdf', 'bmp']
    for extension in bad_extensions:
        test = get_extension_test_factory(
            extension, True, client, token_user, test_config
        )
        await test()


@pytest.mark.parametrize('temp_file', [('png', 1024)], indirect=True)
async def test_bad_mime_type_upload(
    client: AsyncClient,
    token_user: tuple[str, User],
    temp_file: IO[bytes],
):
    token, _ = token_user
    data, errors = await send_file(
        client, temp_file.name, token, content_type='application/javascript'
    )
    check_bad_response(data, errors, 'Uploaded file must have type image/*')


@pytest.mark.parametrize('temp_file', [('webp', 1024)], indirect=True)
async def test_view_uploaded_file(
    client: AsyncClient,
    token_user: tuple[str, User],
    test_config: Configuration,
    temp_file: IO[bytes],
):
    token, _ = token_user
    data, _ = await send_file(client, temp_file.name, token)
    assert data is not None
    uploaded_file_name = data['editAccount']['account']['profilePictureFilename']

    response = await client.get(f'/uploads/{uploaded_file_name}')
    assert response.status_code == 200

    headers = response.headers
    assert headers['content-length'] == '1024'
    assert headers['content-type'] == get_image_mime_type('webp')

    content = response.content
    assert identifiers_are_same(content, uploaded_file_name, test_config)
