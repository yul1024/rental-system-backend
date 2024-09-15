from enum import Enum
from pydantic import BaseModel


class Method(Enum):
    """这里是数据库相关的操作"""
    insert = 'insert'
    delete = 'delete'
    update = 'update'
    query = 'query'


class Cate(Enum):
    """这里是进行操作的数据表"""
    male = 'MaleProduct'
    female = 'FemaleProduct'
    acc = 'AccProduct'
    photographer = 'Photographer'
    order = 'Order'
    order_detail = 'OrderDetail'


class Product(BaseModel):
    """产品字段"""
    method: str
    cate: str
    idx: int = None
    name: str = None
    count: int = None
    info: str = None


class Photographer(BaseModel):
    """摄影师字段"""
    method: str
    cate: str = 'photographer'
    idx: int = None
    name: str = None
    info: str = None


class Order(BaseModel):
    """订单字段"""
    method: str
    idx: int = None
    name: str = None
    start_date: str = None
    end_date: str = None
    # photographer_id: str = None
    # count: int = None
    info: str = None
    # order_detail: []


class OrderDetail(BaseModel):
    """订单明细字段"""
    method: str
    idx: int = None
    order_idx: int = None
    cate: str = None
    product_idx: int = None
    info: str = None


class Search(BaseModel):
    """
    查询字段
    method需要是 'product' 或 'date'
    必须指定搜索的类别
    必须指定搜索的起始和结束时间，即使不同的查询方法的实际操作是不同的。
    """
    method: str
    cate: str
    idx: int = None
    start_date: str
    end_date: str

