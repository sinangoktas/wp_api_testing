API_HOSTS = {
    "test": "http://wordpress.local/wp-json/wc/v3/",
    "dev": "",
    "prod": ""
}

DB_HOST = {
    'machine1': {
              "test": {"host": "localhost",
                       "database": "local",
                       "table_prefix": "wp_",
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
    'machine2': {
              "test": {"host": "localhost",
                       "database": "local",
                       "table_prefix": "wp_",
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
}