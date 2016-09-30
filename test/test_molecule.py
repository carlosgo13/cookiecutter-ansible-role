import pytest
import sys
import os
import shutil
from subprocess import call
from cookiecutter.main import cookiecutter


playbook_setup_commands = ['pip install -r requirements.txt']
playbook_setup_success = 0
playbook_test_command = "molecule test"
playbook_test_success = 0


@pytest.mark.parametrize('role_name', ['tree'])
def test_role_name(role_name):
    last_dir = os.path.curdir
    project_name="ansible-role-{0}".format(role_name)
    test_dir = project_name 
    try:
        shutil.rmtree(test_dir, ignore_errors=True)
        cookiecutter(
                '.', 
                no_input=True, 
                overwrite_if_exists=True,
                extra_context={'role_name': role_name, 'project_name': project_name})
        for command in playbook_setup_commands:
            assert call(command.split()) == playbook_setup_success
        os.chdir(test_dir)
        assert call(playbook_test_command.split()) == playbook_test_success
    finally:
        os.chdir(last_dir)
        shutil.rmtree(test_dir, ignore_errors=True)