API_HOSTS = {
    "test": "http://wordpress.local/wp-json/wc/v3/",
    "dev": "",
    "prod": ""
}

DB_HOST = {
    'machine1': {
              "test": {"host": "localhost",
                       "database": "local",
                       "table_prefix": "wp",
                       "socket": "/home/sinangoktas/.config/Local/run/R6sTeUhet/mysql/mysqld.sock",
                       "port": 3306
                       },
              "dev": {
                  "host": "",
                  "database": "",
                  "table_prefix": "",
                  "socket": None,
                  "port": 3306
              },
              "prod": {
                  "host": "",
                  "database": "",
                  "table_prefix": "",
                  "socket": None,
                  "port": 3306
              }
            },
    'docker': {
              "test": {"host": "host.docker.internal",
                       "database": "local",
                       "table_prefix": "wp",
                       "socket": None,
                       "port": 3306
                       },
              "dev": {
                  "host": "",
                  "database": "",
                  "table_prefix": "wp",
                  "socket": None,
                  "port": 3306
              },
              "prod": {
                  "host": "",
                  "database": "",
                  "table_prefix": "wp",
                  "socket": None,
                  "port": 3306
              }
            },
}