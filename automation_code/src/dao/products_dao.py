from automation_code.src.utilities.db_utility import DBUtility
import random

class ProductsDAO(object):

    def __init__(self):
        self.db_utility = DBUtility()

    def get_random_product_from_db(self, table, qty=1):

        sql = f'''SELECT * FROM {self.db_utility.database}.{self.db_utility.table_prefix}_{table} WHERE post_type = "product" LIMIT 1000;'''
        res_sql = self.db_utility.execute_select(sql)
        return random.sample(res_sql, int(qty))


    def get_product_table_data(self, table, attr, value):

        sql = f'''SELECT * FROM {self.db_utility.database}.{self.db_utility.table_prefix}_{table}
                  WHERE {attr} = {value};'''

        return self.db_utility.execute_select(sql)


    def get_products_created_after_given_date(self, _date):

        sql = f'''SELECT * FROM {self.db_utility.database}.{self.db_utility.table_prefix}_posts 
                  WHERE post_type = "product" AND post_date > "{_date}" 
                  LIMIT 10000;'''

        return self.db_utility.execute_select(sql)


    def get_random_products_that_are_not_on_sale(self, qty=1):

        sql = f"""SELECT * FROM {self.db_utility.database}.{self.db_utility.table_prefix}_posts WHERE post_type = 'product' AND id NOT IN 
                    (SELECT post_id FROM {self.db_utility.database}.{self.db_utility.table_prefix}_postmeta WHERE `meta_key`="_sale_price");"""

        res_sql = self.db_utility.execute_select(sql)

        return random.sample(res_sql, int(qty))


    def get_random_products_that_are_on_sale(self, qty=1):

        sql = f"""SELECT * FROM {self.db_utility.database}.{self.db_utility.table_prefix}_posts WHERE post_type = 'product' AND id IN 
                    (SELECT post_id FROM {self.db_utility.database}.{self.db_utility.table_prefix}_postmeta WHERE `meta_key`="_sale_price");"""

        res_sql = self.db_utility.execute_select(sql)

        return random.sample(res_sql, int(qty))