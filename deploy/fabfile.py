#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/chivitc1/pytdd'


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))


def _get_latest_source(source_folder):
    '''
    either do a git clone if it’s a fresh deploy, or we do a
    git fetch + git reset --hard if a previous version of the code is already there; the
    equivalent of the git pull we used when we did it manually, but with the reset --
    hard to force overwriting any local changes.
    :param source_folder:
    :return:
    '''
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % (source_folder, ))
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))

        '''
        Fabric’s local command runs a command on your local machine—it’s just a
        wrapper around subprocess.Popen really, but it’s quite convenient. Here we cap‐
        ture the output from that git log invocation to get the ID of the current commit
        that’s on your local PC. That means the server will end up with whatever code is
        currently checked out on your machine (as long as you’ve pushed it up to the server).
        '''
    current_commit = local("git log -n 1 --format=%H", capture=True)

    '''blow away any current changes in
    the server’s code directory.'''
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))


def _update_settings(source_folder, site_name):
    '''
    update settings file, to set the ALLOWED_HOSTS and DEBUG variables, and to
    create a new SECRET_KEY
    :param source_folder:
    :param site_name:
    :return:
    '''
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS = .+$',
        'ALLOWED_HOSTS = ["%s"]' % (site_name,))

    '''
    Django uses SECRET_KEY for some of its crypto—things like cookies and CSRF
    protection. It’s good practice to make sure the secret key on the server is different
    from the one in your source code repo, because that code might be visible to
    strangers. This section will generate a new key to import into settings, if there
    isn’t one there already (once you have a secret key, it should stay the same
    between deploys)
    '''
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, 'SECRET_KEY = "%s"' % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('python3 -m venv %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (virtualenv_folder, source_folder))


def _update_database(source_folder):
    # The --noinput removes any interactive yes/no confirmations that Fabric would find hard to deal with
    run(
        'cd %s/ && ../virtualenv/bin/python manage.py migrate --noinput' % (source_folder,)
    )


def _update_static_files(source_folder):
    run(
        'cd %s/ && ../virtualenv/bin/python manage.py collectstatic --noinput' % (source_folder,)
    )


def deploy():
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)