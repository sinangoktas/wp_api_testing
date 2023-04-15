from automation_code.src.utilities.db_utility import DBUtility

class OrdersDAO(object):

    def __init__(self):
        self.db_utility = DBUtility()

    def get_order_lines_by_order_id(self, order_id):
        sql = f'''SELECT * FROM {self.db_utility.database}.{self.db_utility.table_prefix}woocommerce_order_items 
                  WHERE order_id = {order_id};'''
        return self.db_utility.execute_select(sql)

    def get_order_items_details(self, order_item_id):
        sql = f'''SELECT * FROM {self.db_utility.database}.{self.db_utility.table_prefix}woocommerce_order_itemmeta 
                  WHERE order_item_id = {order_item_id};'''
        rs_sql = self.db_utility.execute_select(sql)
        line_details = dict()
        for meta in rs_sql:
            line_details[meta['meta_key']] = meta['meta_value']

        return line_details