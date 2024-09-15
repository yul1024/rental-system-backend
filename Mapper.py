import yaml
import datetime

import pymysql
from pymysql import cursors

from model import *


class Mapper:
    def __init__(self):
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        self.conn = pymysql.connect(
            host=config.get('host'),
            port=config.get('port'),
            user=config.get('user'),
            password=config.get('password'),
            database=config.get('database'),
            cursorclass=cursors.DictCursor,
        )
        self.cursor = self.conn.cursor()


class ProductMapper(Mapper):
    def __init__(self):
        super().__init__()

    def insert_product(self, product: Product):
        table = Cate[product.cate].value
        sql = f"""
            INSERT INTO {table} ({table}Name, {table}Count, {table}Info)
            VALUES ('{product.name}', {product.count}, '{product.info}');
        """
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.lastrowid

    def delete_product(self, product):
        table = Cate[product.cate].value
        sql = f"""
            DELETE FROM {table}
            WHERE {table}Id = {product.idx};
        """
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def update_product(self, product):
        table = Cate[product.cate].value
        sql = f"""
            UPDATE {table}
            SET {table}Name = '{product.name}', {table}Count = {product.count}, {table}Info = '{product.info}'
            WHERE {table}Id = {product.idx};
        """
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def query_product(self, product):
        table = Cate[product.cate].value
        sql = f"""
            SELECT *
            FROM {table}
        """
        print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        # self.conn.commit()

    def query_product_by_cate(self, cate):
        table = Cate[cate].value
        sql = f"""
            SELECT *
            FROM {table}
        """
        print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result


class PhotographerMapper(Mapper):
    def __init__(self):
        super().__init__()

    def insert_photographer(self, photographer):
        table = Cate[photographer.cate].value
        sql = f"""
                    INSERT INTO {table} ({table}Name, {table}Info)
                    VALUES ('{photographer.name}', '{photographer.info}');
                """
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def delete_photographer(self, photographer):
        table = Cate[photographer.cate].value
        sql = f"""
                    DELETE FROM {table}
                    WHERE {table}Id = {photographer.idx};
                """
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def update_photographer(self, photographer):
        table = Cate[photographer.cate].value
        sql = f"""
                    UPDATE {table}
                    SET {table}Name = '{photographer.name}', {table}Info = '{photographer.info}'
                    WHERE {table}Id = {photographer.idx};
                """
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def query_photographer(self, photographer):
        table = Cate[photographer.cate].value
        sql = f"""
                    SELECT *
                    FROM {table}
                """
        print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        # self.conn.commit()


class OrderMapper(Mapper):
    def __init__(self):
        super().__init__()

    def insert_order(self, order):
        table = 'Order'
        sql = f"""
            INSERT INTO `{table}` ({table}Name, StartDate, EndDate, {table}Info)
            VALUES ('{order.name}', '{order.start_date}', '{order.end_date}', '{order.info}');
        """
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def delete_order(self, order):
        # 需要修改，删除订单前，要先把订单明细中的订单全部删除。
        table = 'Order'
        sql = f"""
            DELETE FROM `{table}`
            WHERE {table}Id = {order.idx};
        """
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def update_order(self, order):
        # 为了安全，修改订单信息最好不要修改订单时间。修改订单时间需要删除订单，然后重新下订单。
        table = 'Order'
        sql = f"""
            UPDATE `{table}`
            SET {table}Name = '{order.name}', StartDate = '{order.startDate}', EndDate = '{order.endDate}', {table}Info = '{order.info}'
            WHERE {table}Id = {order.idx};
        """
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def query_order(self, order):
        table = 'Order'
        sql = f"""
            SELECT *
            FROM `{table}`;
        """
        print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        # print(type(result[0]['StartDate']))
        return result


class OrderDetailMapper(Mapper):
    def __init__(self):
        super().__init__()

    def insert_orderDetail(self, orderDetail):
        table = 'OrderDetail'
        sql = f"""
            INSERT INTO {table} (OrderId, Cate, ProductId, {table}Info)
            VALUES ({orderDetail.order_idx}, '{orderDetail.cate}', {orderDetail.product_idx}, '{orderDetail.info}');
        """
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def delete_orderDetail(self, orderDetail):
        table = 'OrderDetail'
        sql = f"""
            DELETE FROM `{table}`
            WHERE {table}Id = {orderDetail.idx};
        """
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def update_orderDetail(self, orderDetail):
        table = 'OrderDetail'
        sql = f"""
            UPDATE `{table}`
            SET OrderId = {orderDetail.order_idx}, Cate = '{orderDetail.cate}', ProductId = {orderDetail.product_idx}, {table}Info = '{orderDetail.info}'
            WHERE {table}Id = {orderDetail.idx};
        """
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def query_orderDetail(self, orderDetail):
        table = 'OrderDetail'
        sql = f"""
            SELECT *
            FROM `{table}`;
        """
        print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def query_orderDetail_by_idx(self, order_idx):
        table = 'OrderDetail'
        sql = f"""
            SELECT *
            FROM `{table}`
            WHERE OrderId = {order_idx};
        """
        print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def delete_orderDetail_by_order(self, order_idx):
        table = 'OrderDetail'
        sql = f"""
            DELETE FROM `{table}`
            WHERE OrderId = {order_idx};
        """
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def query_order(self, orderDetail):
        table = 'Order'
        sql = f"""
            SELECT StartDate, EndDate
            FROM `{table}`
            WHERE OrderId = {orderDetail.order_idx};
        """
        print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result


class SearchMapper(Mapper):
    def __init__(self):
        super().__init__()

    def search_by_product(self, search):
        table = Cate[search.cate].value
        sql = f"""
            SELECT *
            FROM `order`
                JOIN orderDetail ON order.OrderId = orderDetail.orderId
                JOIN {table} ON orderDetail.ProductId = {table}.{table}Id
            WHERE {table}Id = {search.idx};
        """
        print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def search_by_date(self, search):
        table = Cate[search.cate].value
        sql = f"""
            SELECT *
            FROM `order`
                JOIN orderDetail ON order.OrderId = orderDetail.orderId
                JOIN {table} ON orderDetail.ProductId = {table}.{table}Id
             WHERE order.EndDate>{search.start_date} OR order.EndDate<{search.end_date};
        """
        print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def search(self, search):
        """查询无论怎样都需要有开始和结束时间，但是不一定指定具体商品。"""
        table = Cate[search.cate].value
        condition = f"AND orderDetail.ProductId = {search.idx}" if search.method == 'product' else ""
        sql = f"""
            SELECT *
            FROM `order`
                JOIN orderDetail ON order.OrderId = orderDetail.orderId
                JOIN {table} ON orderDetail.ProductId = {table}.{table}Id
             WHERE ((order.StartDate BETWEEN '{search.start_date}' AND '{search.end_date}')
                OR (order.EndDate BETWEEN '{search.start_date}' AND '{search.end_date}'))
                {condition};
        """
        print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result


class QrcodeMapper(Mapper):
    def __init__(self):
        super().__init__()

    def query_path(self, idx):
        table = 'Picture'
        sql = f"""
            SELECT PicturePath
            FROM `{table}`
            WHERE PictureId = {idx};
        """
        print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def query_picture_list(self, cate, idx):
        table = 'Picture'
        sql = f"""
            SELECT PictureId
            FROM `{table}`
            WHERE Cate = '{cate}' AND Id = {idx};
        """
        print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return [v['PictureId'] for v in result]

    def query_product(self, cate, idx):
        table = Cate[cate].value
        sql = f"""
            SELECT *
            FROM `{table}`
            WHERE {table}Id = {idx};
        """
        print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result


class PictureMapper(Mapper):
    def __init__(self):
        super().__init__()

    def insert_picture(self, cate, idx, info):
        # 保存图片相关信息
        table = 'Picture'
        sql = f"""
            INSERT INTO `{table}` (Cate, Id, Info)
            VALUES ('{cate}', {idx}, '{info}');
        """
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.lastrowid

    def save_picture(self, file, picture_idx):
        picture_path = f"pictures/{picture_idx}.png"
        with open(picture_path, 'wb') as f:
            f.write(file.file.read())
        return picture_path

    def update_picture_path(self, picture_idx, picture_path):
        table = 'Picture'
        sql = f"""
            UPDATE `{table}`
            SET PicturePath = '{picture_path}'
            WHERE PictureId = {picture_idx};
        """
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()


class TestMapper(Mapper):
    def __init__(self):
        super().__init__()

    def test(self):
        # sql = f"""
        #     SHOW TABLE STATUS LIKE 'Picture';
        # """
        # print(sql)
        # self.cursor.execute(sql)
        # result = self.cursor.fetchall()
        # return result
        return self.cursor.lastrowid


if __name__ == '__main__':
    pass
