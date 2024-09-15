from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
import io

from model import *
from Service import ProductService, PhotographerService, OrderService, OrderDetailService, SearchService, QrcodeService, PictureService, TestService


productService = ProductService()
photographerService = PhotographerService()
orderService = OrderService()
orderDetailService = OrderDetailService()
searchService = SearchService()
qrcodeService = QrcodeService()
pictureService = PictureService()
testService = TestService()

app = FastAPI()


@app.post("/product")
def product(product: Product):
    if product.method == Method.insert.name:
        return productService.insert_product(product)
    elif product.method == Method.delete.name:
        productService.delete_product(product)
    elif product.method == Method.update.name:
        productService.update_product(product)
    elif product.method == Method.query.name:
        return productService.query_product(product)


@app.post("/photographer")
def photographer(photographer: Photographer):
    if photographer.method == Method.insert.name:
        photographerService.insert_photographer(photographer)
    elif photographer.method == Method.delete.name:
        photographerService.delete_photographer(photographer)
    elif photographer.method == Method.update.name:
        photographerService.update_photographer(photographer)
    elif photographer.method == Method.query.name:
        return photographerService.query_photographer(photographer)


@app.post("/order/list")
def order(order: Order):
    if order.method == Method.insert.name:
        orderService.insert_order(order)
    elif order.method == Method.delete.name:
        orderService.delete_order(order)
    elif order.method == Method.update.name:
        orderService.update_order(order)
    elif order.method == Method.query.name:
        return orderService.query_order(order)


@app.post("/order/detail")
def orderDetail(orderDetail: OrderDetail):
    if orderDetail.method == Method.insert.name:
        return orderDetailService.insert_orderDetail(orderDetail)
    elif orderDetail.method == Method.delete.name:
        orderDetailService.delete_orderDetail(orderDetail)
    elif orderDetail.method == Method.update.name:
        orderDetailService.update_orderDetail(orderDetail)
    elif orderDetail.method == Method.query.name:
        return orderDetailService.query_orderDetail(orderDetail)


@app.post("/search")
def search(search: Search):
    if search.method == 'product':
        return searchService.search_by_product(search)
    elif search.method == 'date':
        return searchService.search_by_date(search)


@app.get("/qrcode/{content}")
def qrcode(content: str, cate: str = None, idx: int = None):
    if content == 'json':
        # 这里的idx指的是商品的编号
        return qrcodeService.get_picture_list(cate, idx)
    elif content == 'picture':
        # 这里的idx指的是图像的编号
        img_byte_array = qrcodeService.get_picture(idx)
        return StreamingResponse(io.BytesIO(img_byte_array.read()), media_type="image/png")
    elif content == 'qrcode':
        # 这里的idx指的是商品的编号
        base_url = "localhost"
        url = f"http://{base_url}:8000/qrcode/qrcode?cate={cate}&idx={idx}"
        print(url)
        img_byte_array = qrcodeService.get_qrcode(url)
        return StreamingResponse(io.BytesIO(img_byte_array.read()), media_type="image/png")


@app.post("/upload")
def upload(file: UploadFile = File(...), cate: str = Form(...), idx: int = Form(...), info: str = Form(...)):
    pictureService.insert_picture(file, cate, idx, info)


# @app.get("/test")
# def test():
#     return testService.test()
