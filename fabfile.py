import os

from tools.fablib import *

"""
Base configuration
"""
env.project_name = 'oneliner'
env.database_password = ''
env.site_media_prefix = "static"
env.path = '/home/newsapps/sites/%(project_name)s' % env
env.env_path = '/home/newsapps/.virtualenvs/%(project_name)s' % env
env.repo_path = '%(path)s' % env
env.repository_url = ""

# Varnish cache servers to purge
env.cache_servers = []

# Setup celery
env.use_celery = False


# Environments
def production():
    """
    Work on production environment
    """
    env.settings = 'production'
    env.hosts = [
        os.environ['ONELINER_PROD_HOST'],
    ]

    env.roledefs = {
        'app': [
            os.environ['ONELINER_PROD_HOST'],
        ],
        'admin': [
            os.environ['ONELINER_PROD_HOST'],
        ]
    }

    env.user = 'newsapps'
    env.site_domain = 'oneliner.inn.org'

    env.db_root_user = os.environ['MYSQL_PRODUCTION_ROOT_USER']
    env.db_root_pass = os.environ['MYSQL_PRODUCTION_ROOT_PASSWORD']
    env.db_type = 'mysql'
    env.db_host = 'localhost'
    env.database_password = os.environ['ONELINER_PROD_DB_PASSWORD']

    env.django_settings_module = '%(project_name)s.settings' % env


def staging():
    """
    Work on staging environment
    """
    env.settings = 'staging'
    env.hosts = []

    env.roledefs = {
        'app': [],
        'worker': [],
        'admin': []
    }

    env.user = 'newsapps'

    env.s3_bucket = ''
    env.site_domain = ''

    env.db_root_user = ''
    env.db_root_pass = ''
    env.db_type = 'mysql'
    env.db_host = ''
    env.database_password = ''

    env.django_settings_module = '%(project_name)s.staging_settings' % env
