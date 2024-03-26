from automation_code.src.utilities.db_utility import DBUtility

class OrdersDAO(object):

    def __init__(self):
        self.db_utility = DBUtility()


    def get_random_order_from_db(self, table, qty=1):

        sql = f'''SELECT * FROM {self.db_utility.database}.{self.db_utility.table_prefix}_{table} LIMIT 1000;'''

        res_sql = self.db_utility.execute_select(sql)

        return random.sample(res_sql, int(qty))


    def get_order_table_data(self, table, attr, value):

        sql = f'''SELECT * FROM {self.db_utility.database}.{self.db_utility.table_prefix}_{table}
                  WHERE {attr} = {value};'''

        return self.db_utility.execute_select(sql)