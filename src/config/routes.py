from flask import Blueprint, request, render_template, make_response, redirect
from src.utils.page_extractor import PageExtractor
from src.controllers.product_controller import ProductController


main_page = Blueprint("main_page", __name__, template_folder="templates")
controller = ProductController()

@main_page.route("/", methods=["GET", "POST"])
def submit_url():
    if request.method == "GET":
        return render_template("form.html")
    else:
        extractor = PageExtractor(request.form['product_url'])
        
        processing = extractor.extract_page()
        
        # save result into db
        get_product = controller.find_by_product_id(processing['source_product_id'])
        
        if get_product['code'] == 500:
            return redirect('/')

        if get_product['code'] == 200:
            product_id = get_product['data']['id']
            result = controller.update(product_id, processing)
            pid = result['data']['id']
        else:
            result = controller.create(processing)
            pid = result['data']['id']

        if result['status']:
            return redirect(f"/product/{pid}")
        else:
            return redirect('/')

@main_page.route("/product", methods=["GET"])
def data_product():
    products = controller.find_all()

    return render_template("list.html", data=products['data'])

@main_page.route("/product/<product_id>", methods=["GET"])
def detail(product_id):
    product = controller.find_by_id(product_id)

    return render_template("detail.html", data=product['data'])