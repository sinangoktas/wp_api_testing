import pdb

from automation_code.src.utilities.db_utility import DBUtility
import random

class CustomersDAO(object):

    def __init__(self):
        self.db_utility = DBUtility()


    def get_customer_by_email(self, email):

        sql = f'''SELECT * FROM {self.db_utility.database}.{self.db_utility.table_prefix}_users 
                  WHERE user_email = '{email}';'''

        res_sql = self.db_utility.execute_select(sql)
        return res_sql


    def get_random_customer_from_db(self, qty=1):

        sql = f'''SELECT * FROM {self.db_utility.database}.{self.db_utility.table_prefix}_users 
                 ORDER BY id DESC LIMIT 1000;'''

        res_sql = self.db_utility.execute_select(sql)
        return random.sample(res_sql, int(qty))


    def get_customer_by_id(self, id):

        sql = f'''SELECT * FROM {self.db_utility.database}.{self.db_utility.table_prefix}_wc_customer_lookup 
                  WHERE user_id = '{id}';'''

        res_sql = self.db_utility.execute_select(sql)
        return res_sql


    def get_customer_table_data(self, table, id_attr, id):

        sql = f'''SELECT * FROM {self.db_utility.database}.{self.db_utility.table_prefix}_{table}
                  WHERE {id_attr} = {id};'''

        return self.db_utility.execute_select(sql)
