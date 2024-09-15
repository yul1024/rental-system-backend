import datetime
import os
from PIL import Image
import io
import qrcode

from model import *
from Mapper import *


class ProductService:
    def __init__(self):
        self.productMapper = ProductMapper()

    def insert_product(self, product: Product):
        return self.productMapper.insert_product(product)

    def delete_product(self, product: Product):
        self.productMapper.delete_product(product)

    def update_product(self, product: Product):
        self.productMapper.update_product(product)

    def query_product(self, product: Product):
        return self.productMapper.query_product(product)

    def query_product_by_cate(self, cate):
        return self.productMapper.query_product_by_cate(cate)


class PhotographerService:
    def __init__(self):
        self.photographerMapper = PhotographerMapper()

    def insert_photographer(self, photographer: Photographer):
        self.photographerMapper.insert_photographer(photographer)

    def delete_photographer(self, photographer: Photographer):
        self.photographerMapper.delete_photographer(photographer)

    def update_photographer(self, photographer: Photographer):
        self.photographerMapper.update_photographer(photographer)

    def query_photographer(self, photographer: Photographer):
        return self.photographerMapper.query_photographer(photographer)


class OrderService:
    def __init__(self):
        self.orderMapper = OrderMapper()
        self.orderDetailMapper = OrderDetailMapper()

    def insert_order(self, order: Order):
        self.orderMapper.insert_order(order)

    def delete_order(self, order: Order):
        # 需要修改，删除订单前，要先把订单明细中的订单全部删除。
        self.orderDetailMapper.delete_orderDetail_by_order(order.idx)
        self.orderMapper.delete_order(order)

    def update_order(self, order: Order):
        # 为了安全，修改订单信息最好不要修改订单时间。修改订单时间需要删除订单，然后重新下订单。
        self.orderMapper.update_order(order)

    def query_order(self, order: Order):
        return self.orderMapper.query_order(order)


class OrderDetailService:
    def __init__(self):
        self.orderDetailMapper = OrderDetailMapper()
        self.searchService = SearchService()

    def insert_orderDetail(self, orderDetail: OrderDetail):
        # 添加商品前，需要检查商品是否可添加。
        start_date, end_date = self.get_order_duration(orderDetail)
        search = {'method': 'date', 'idx': f'{orderDetail.product_idx}', 'cate': f'{orderDetail.cate}', 'start_date': f'{start_date}',
                  'end_date': f'{end_date}'}
        search = Search(**search)
        search_result = self.searchService.search_by_date(search)
        product_list = [order[f'{Cate[orderDetail.cate].value}Id'] for order in search_result]
        if orderDetail.product_idx in product_list:
            self.orderDetailMapper.insert_orderDetail(orderDetail)
            return "添加成功"
        return "添加失败"

    def delete_orderDetail(self, orderDetail: OrderDetail):
        self.orderDetailMapper.delete_orderDetail(orderDetail)

    def update_orderDetail(self, orderDetail: OrderDetail):
        self.orderDetailMapper.update_orderDetail(orderDetail)

    def query_orderDetail(self, orderDetail: OrderDetail):
        return self.orderDetailMapper.query_orderDetail(orderDetail)

    def get_order_duration(self, orderDetail: OrderDetail):
        res = self.orderDetailMapper.query_order(orderDetail)
        return res[0]['StartDate'].strftime('%Y-%m-%d'), res[0]['EndDate'].strftime('%Y-%m-%d')

    def query_orderDetail_by_order(self, order_idx):
        return self.orderDetailMapper.query_orderDetail_by_idx(order_idx)

    def delete_orderDetail_by_order(self, order_idx):
        self.orderDetailMapper.delete_orderDetail_by_order(order_idx)


class SearchService:
    def __init__(self):
        self.searchMapper = SearchMapper()
        self.productService = ProductService()

    def search_by_product(self, search: Search):
        """根据当前商品，返回可用时间段。"""
        # return self.searchMapper.search(search)
        exist_order = self.searchMapper.search(search)
        return self.remain_date(search, exist_order)

    def search_by_date(self, search: Search):
        """根据当前时间段，返回已用商品。"""
        # return self.searchMapper.search(search)
        # 根据具体搜索对象，修改搜索日期区间。
        padding = self.get_padding(search)
        search.start_date = (datetime.datetime.strptime(search.start_date, '%Y-%m-%d').date() - datetime.timedelta(days=padding)).strftime('%Y-%m-%d')
        search.end_date = (datetime.datetime.strptime(search.end_date, '%Y-%m-%d').date() + datetime.timedelta(days=padding)).strftime('%Y-%m-%d')
        exit_order = self.searchMapper.search(search)
        return self.remain_product(search, exit_order)

    def remain_date(self, search: Search, exist_order):
        # 确定日期区间。
        left_date = datetime.datetime.strptime(search.start_date, '%Y-%m-%d').date()
        right_date = datetime.datetime.strptime(search.end_date, '%Y-%m-%d').date()
        # 列举出区间的每一天。
        date = {left_date + datetime.timedelta(days=x): False for x in range(0, (right_date - left_date).days + 1)}
        # 这里设置了隔订单的时间间隔，只有当对象为摄影师时没有间隔。
        padding = self.get_padding(search)
        for order in exist_order:
            for x in range(0 - padding, (order['EndDate'] - order['StartDate']).days + 1 + padding):
                # 填写当前订单中目标商品所占用的时间，填写为订单ID。
                date[order['StartDate'] + datetime.timedelta(days=x)] = order['OrderId']
        return date

    def ordered_product(self, search: Search, exist_order):
        # 这里设置了隔订单的时间间隔，只有当对象为摄影师时没有间隔。
        padding = self.get_padding(search)
        # 确定时间区间
        left_date = datetime.datetime.strptime(search.start_date, '%Y-%m-%d').date() - datetime.timedelta(days=padding)
        right_date = datetime.datetime.strptime(search.end_date, '%Y-%m-%d').date() + datetime.timedelta(days=padding)
        res = []
        for order in exist_order:
            if left_date <= order['StartDate'] <= right_date or left_date <= order['EndDate'] <= right_date:
                res.append(order)
        return res

    def remain_product(self, search: Search, exist_order):
        product_list = self.productService.query_product_by_cate(search.cate)
        used_product_list = self.ordered_product(search, exist_order)
        for order in used_product_list:
            for product in product_list:
                if product[f'{Cate[search.cate].value}Id'] == order['ProductId']:
                    product_list.remove(product)
        return product_list

    def get_padding(self, search: Search):
        """标准化返回多个订单之间的时间间隔，之后可以修改。"""
        if search.cate == Cate.photographer.value:
            # 当搜索对象是摄影师
            return 0
        else:
            # 当搜索对象是一般商品
            return 4


class QrcodeService:
    def __init__(self):
        self.qrcodeMapper = QrcodeMapper()
        if not os.path.exists("picture"):
            os.mkdir("picture")

    def get_picture(self, idx):
        # 根据图片的id返回图片
        picture_path = self.qrcodeMapper.query_path(idx)[0]['PicturePath']
        # picture_path = "picture/1.png"
        print(picture_path)
        img = Image.open(picture_path)
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)
        return img_byte_array

    def get_picture_list(self, cate, idx):
        picture_list = self.qrcodeMapper.query_picture_list(cate, idx)
        product_info = self.qrcodeMapper.query_product(cate, idx)[0]
        product_info['picture_list'] = picture_list
        return product_info

    def get_qrcode(self, url):
        img = qrcode.make(url)
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)
        return img_byte_array


class PictureService:
    def __init__(self):
        self.pictureMapper = PictureMapper()
        if not os.path.exists("picture"):
            os.mkdir("picture")

    def insert_picture(self, file, cate, idx, info):
        picture_idx = self.pictureMapper.insert_picture(cate, idx, info)
        picture_path = self.pictureMapper.save_picture(file, picture_idx)
        self.pictureMapper.update_picture_path(picture_idx, picture_path)


class TestService:
    def __init__(self):
        self.testMapper = TestMapper()

    def test(self):
        return self.testMapper.test()


if __name__ == '__main__':
    pass

