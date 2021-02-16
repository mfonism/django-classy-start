import pathlib
import random
import shlex
import string
from unittest import mock

import pytest

from classy_start.file_contents import (
    auth_user_model_file_content,
    auth_user_admin_file_content,
)
from classy_start.paths import APP_TEMPLATES_DIR, PROJECT_TEMPLATES_DIR
from classy_start.start import (
    start_app,
    start_project,
    follow_up_start_project,
    rename_file,
    create_accounts_app,
    write_file,
)


def test_start_app(fake_process):

    fake_process.keep_last_process(True)
    fake_process.register_subprocess([fake_process.any()])

    start_app('appify')

    count = fake_process.call_count(
        shlex.split(f'django-admin startapp appify --template "{APP_TEMPLATES_DIR!s}"')
    )
    assert count == 1


@mock.patch('classy_start.start.follow_up_start_project')
def test_start_project(mock_follow_up, fake_process):

    fake_process.keep_last_process(True)
    fake_process.register_subprocess([fake_process.any()])

    start_project('projectible', '.')

    count = fake_process.call_count(
        shlex.split(
            f'django-admin startproject projectible . --template "{PROJECT_TEMPLATES_DIR!s}"'
        )
    )
    assert count == 1

    mock_follow_up.assert_called_once_with('projectible', '.')


@mock.patch('pathlib.Path.resolve')
@mock.patch('classy_start.start.rename_file')
@mock.patch('classy_start.start.create_accounts_app')
def test_follow_up_start_project(
    mock_create_accounts_app, mock_rename_file, _mock_resolve
):
    '''
    Assert that ~.follow_up_start_project() calls ~.rename_file() the correct number of
    times and with the correct arguments. And that it also calls
    ~.create_accounts_app() with the correct arguments.
    '''
    follow_up_start_project('projectible')

    assert mock_rename_file.call_count == 3
    mock_rename_file.assert_has_calls(
        [
            mock.call('secrets.py', '.env', base_dir=pathlib.Path('projectible')),
            mock.call(
                'gitignore.py', '.gitignore', base_dir=pathlib.Path('projectible')
            ),
            mock.call(
                'requirements.py',
                'requirements.txt',
                base_dir=pathlib.Path('projectible'),
            ),
        ]
    )
    mock_create_accounts_app.assert_called_once_with(pathlib.Path('projectible'))

    # reset the **all used** mocks
    mock_rename_file.reset_mock()
    mock_create_accounts_app.reset_mock()

    follow_up_start_project('projectible', pathlib.Path('.'))

    assert mock_rename_file.call_count == 3
    mock_rename_file.assert_has_calls(
        [
            mock.call('secrets.py', '.env', base_dir=pathlib.Path('.')),
            mock.call('gitignore.py', '.gitignore', base_dir=pathlib.Path('.')),
            mock.call(
                'requirements.py', 'requirements.txt', base_dir=pathlib.Path('.'),
            ),
        ]
    )
    mock_create_accounts_app.assert_called_once_with(pathlib.Path('.'))


@mock.patch('pathlib.Path.rename')
def test_rename_file(mock_rename):
    '''
    Assert that ~.rename_file() calls pathlib.Path.rename with the correct target.
    '''
    base_dir = pathlib.Path('.') / 'projectible'
    rename_file('old_name', 'new_name', base_dir)

    mock_rename.assert_called_once_with(base_dir / 'new_name')


@pytest.mark.parametrize(
    'manage_dir', [pathlib.Path('.'), pathlib.Path('.') / 'projectible']
)
@mock.patch('pathlib.Path.mkdir')
@mock.patch('classy_start.start.start_app')
@mock.patch('classy_start.start.write_file')
def test_create_accounts_app(mock_write_file, mock_start_app, _mock_mkdir, manage_dir):
    '''
    Assert that ~.create_accoung_app() calls ~.start_app() with the
    correct arguments. And that it calls pathlib.Path.write_text the
    correct number of times and with the correct arguments.
    '''
    create_accounts_app(manage_dir)

    accounts_app_dir = manage_dir / 'accounts'
    model_file = accounts_app_dir / 'models.py'
    admin_file = accounts_app_dir / 'admin.py'

    mock_start_app.assert_called_once_with('accounts', accounts_app_dir)

    assert mock_write_file.call_count == 2
    assert mock_write_file.has_calls(
        [
            mock.call(model_file, auth_user_model_file_content,),
            mock.call(admin_file, auth_user_admin_file_content,),
        ]
    )


@mock.patch('pathlib.Path.touch')
@mock.patch('pathlib.Path.write_text')
def test_write_file(mock_write_text, mock_touch):
    file = pathlib.Path('project') / 'app' / 'an_app_file.py'
    content = ''.join(random.sample(string.printable, 64))

    write_file(file, content)

    mock_touch.assert_called_once()
    mock_write_text.assert_called_once_with(content)
