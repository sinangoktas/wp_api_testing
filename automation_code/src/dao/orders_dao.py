from automation_code.src.utilities.db_utility import DBUtility

class OrdersDAO(object):

    def __init__(self):
        self.db_utility = DBUtility()


    def get_order_table_data(self, table, id_attr, id):

        sql = f'''SELECT * FROM {self.db_utility.database}.{self.db_utility.table_prefix}_{table}
                  WHERE {id_attr} = {id};'''
        return self.db_utility.execute_select(sql)