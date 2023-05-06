from automation_code.src.utilities.db_utility import DBUtility
import random

class ProductsDAO(object):

    def __init__(self):
        self.db_helper = DBUtility()

    def get_random_product_from_db(self, qty=1):

        sql = f'''SELECT * FROM {self.db_helper.database}.{self.db_helper.table_prefix}_posts 
                  WHERE post_type = "product" LIMIT 5000;'''
        res_sql = self.db_helper.execute_select(sql)

        return random.sample(res_sql, int(qty))

    def get_product_by_id(self, product_id):

        sql = f'''SELECT * FROM {self.db_helper.database}.{self.db_helper.table_prefix}_posts 
                  WHERE ID = {product_id};'''

        return self.db_helper.execute_select(sql)

    def get_products_created_after_given_date(self, _date):

        sql = f'''SELECT * FROM {self.db_helper.database}.{self.db_helper.table_prefix}_posts 
                  WHERE post_type = "product" AND post_date > "{_date}" 
                  LIMIT 10000;'''

        return self.db_helper.execute_select(sql)

    # LINE 35 and 44 "{self.db_helper.table_prefix} post meta" is this right?

    def get_random_products_that_are_not_on_sale(self, qty=1):

        sql = f"""SELECT * FROM {self.db_helper.database}.{self.db_helper.table_prefix}_posts WHERE post_type = 'product' AND id NOT IN 
                    (SELECT post_id FROM {self.db_helper.database}.{self.db_helper.table_prefix} post meta WHERE `meta_key`="_sale_price");"""

        res_sql = self.db_helper.execute_select(sql)

        return random.sample(res_sql, int(qty))

    def get_random_products_that_are_on_sale(self, qty=1):

        sql = f"""SELECT * FROM {self.db_helper.database}.{self.db_helper.table_prefix}_posts WHERE post_type = 'product' AND id IN 
                    (SELECT post_id FROM {self.db_helper.database}.{self.db_helper.table_prefix} post meta WHERE `meta_key`="_sale_price");"""

        res_sql = self.db_helper.execute_select(sql)

        return random.sample(res_sql, int(qty))