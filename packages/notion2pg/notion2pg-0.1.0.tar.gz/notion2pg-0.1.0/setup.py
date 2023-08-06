# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['notion2pg']
install_requires = \
['httpx', 'psycopg']

entry_points = \
{'console_scripts': ['notion2pg = notion2pg:main']}

setup_kwargs = {
    'name': 'notion2pg',
    'version': '0.1.0',
    'description': 'Import Notion databases to PostgreSQL tables',
    'long_description': 'notion2pg - Import Notion databases to PostgreSQL tables\n========================================================\n\nWhen a system built with Notion_ databases reaches a sufficient scale, the need\nfor business intelligence arises. This requires extracting data from Notion and\nloading it into a relational database.\n\nThe original author didn\'t find a convenient, off-the-shelf solution for this.\nServices offering synchronization from Notion to a relational database rely on\nclunky automations and involve manual configuration.\n\nThus notion2pg was born.\n\nIt does exactly one thing: convert any Notion database to a PostgreSQL table.\nIt requires zero configuration. You made changes in Notion? No worries, just\nre-run notion2pg to refresh the table definition and its content.\n\n.. _Notion: https://www.notion.so/\n.. _PostgreSQL: https://www.postgresql.org/\n\nWhile notion2pg is currently alpha software, it imported successfully complex\ndatabases with dozens of columns and thousands of rows. There\'s a fair chance\nthat it will handle any human-sized Notion database.\n\nQuick start\n-----------\n\n1. `Create a Notion integration`_.\n\n   .. _Create a Notion integration: https://www.notion.so/my-integrations\n\n2. Share a Notion database with your integration, as well as related databases.\n\n3. Create a PostgreSQL database e.g.:\n\n   .. code-block:: shell-session\n\n      $ createuser notion\n      $ createdb notion -O notion\n\n4. Install notion2pg (requires Python ≥ 3.8):\n\n   .. code-block:: shell-session\n\n      $ pip install notion2pg\n\n5. Set Notion and PostgreSQL credentials as environment variables e.g.:\n\n   .. code-block:: shell-session\n\n      $ export NOTION_TOKEN=secret_...\n      $ export POSTGRESQL_DSN="dbname=notion user=notion"\n\n6. Import your database e.g.:\n\n   .. code-block:: shell-session\n\n      $ notion2pg <database_id> <table_name>\n\n   where ``<database_id>`` can be found in the URL of your database — it\'s a\n   UUID like ``858611286a7d43a197c7c0ddcc7d5a4f`` and ``<table_name>`` is any\n   valid PostgreSQL table name.\n\nCommand line options\n--------------------\n\n``--drop-existing``\n~~~~~~~~~~~~~~~~~~~\n\nDrop the PostgreSQL table if it exists. This is useful if you want to import a\ntable repeatedly, overwriting any previous version.\n\n``--versioned``\n~~~~~~~~~~~~~~~\n\nAppend a timestamp to the name of the PostgreSQL table. Then, create a view\npointing to that table, so it can still be queried under ``<table name>``. This\nis useful if you want to import a table a repeatedly, but would rather keep\nprevious versions around.\n\nFAQ\n---\n\n**Why is my relation or rollup field empty?**\n\nYour integration must have access not only to the table that you\'re importing,\nbut also to every table involved in a relation or a rollup.\n\nLimitations\n-----------\n\n* The order of columns in the table isn\'t preserved. This information isn\'t\n  available in the API of Notion.\n* Rollups "Show original" and "Show unique values" are ignored. Import the\n  related table and join it in your queries instead.\n* Properties of type "people" are imported as the person ID, which is probably\n  not the most useful representation.\n* Every import is a full copy. Given that Notion\'s API isn\'t particularly fast,\n  the practical limit is around 10,000 rows.\n\nChangelog\n---------\n\n0.1\n~~~\n\n* Initial public release.\n',
    'author': 'Aymeric Augustin',
    'author_email': 'aymeric.augustin@fractalideas.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aaugustin/notion2pg',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
