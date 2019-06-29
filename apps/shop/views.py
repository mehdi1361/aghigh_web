import json
import requests

from django.http import JsonResponse, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render, redirect, reverse
from django.conf import settings

from apps.main.views import BaseViewClass, page_permission_denied_view


class ProductsIndex(BaseViewClass):
    def get(self, request):
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/product/slider",
            headers=self.get_http_header(request),
            params=self.add_pagination_param(request, {})
        )
        self.is_auth_valid(request, get_res)
        try:
            sliders = get_res.json()
        except:
            sliders = []

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/product/special_category",
            headers=self.get_http_header(request),
        )

        self.is_auth_valid(request, get_res)
        try:
            special_categories = get_res.json()
        except:
            special_categories = []

        return render(
            request=request,
            template_name="apps/shop/index.html",
            context={
                "sliders": sliders,
                "special_categories": special_categories,
            }
        )


class Basket(BaseViewClass):
    def get(self, request):
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/basket/",
            headers=self.get_http_header(request),
        )
        self.is_auth_valid(request, get_res)
        try:
            basket_resp = get_res.json()
        except:
            basket_resp = []

        return render(
            request=request,
            template_name="apps/shop/basket.html",
            context={
                "results": basket_resp,
            }
        )

    def post(self, request):
        get_res = requests.post(
            url=settings.SERVER_FULL_URL + "/api/v1/basket/",
            headers=self.get_http_header(request),
            data={'product': request.POST.get('product_id')}
        )
        self.is_auth_valid(request, get_res)

        if get_res.status_code == 201:
            message = "success"
        else:
            message = "error"

        return JsonResponse({"message": message})


class DeleteBasket(BaseViewClass):
    def post(self, request):
        get_res = requests.post(
            url=settings.SERVER_FULL_URL + "/api/v1/basket/delete/",
            headers=self.get_http_header(request),
            data={'product': request.POST.get('product_id')}
        )
        self.is_auth_valid(request, get_res)

        if get_res.status_code == 200:
            message = "success"
        else:
            message = "error"

        return JsonResponse({"message": message})


class Payment(BaseViewClass):
    def get(self, request):
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/shop/payment_methods/",
            headers=self.get_http_header(request),
        )
        payment_methods = get_res.json()

        return render(
            request=request,
            context={'payment_methods': payment_methods},
            template_name="apps/shop/payment.html",
        )

    def post(self, request):
        payment_method = request.POST.get('payment_method')
        role_accepted = request.POST.get('role_accepted')
        context = {
            'error': True,
        }
        if payment_method and role_accepted == 'true':
            get_res = requests.post(
                url=settings.SERVER_FULL_URL + "/api/v1/invoice/",
                headers=self.get_http_header(request),
                data={
                    "payment_method": payment_method,
                }
            )
            if get_res.status_code == 200:
                context['error'] = False
                context['url'] = get_res.json()['url']
                context['order_code'] = get_res.json()['order_code']

        return JsonResponse(context)


class SingleInvoice(BaseViewClass):
    def get(self, request):
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/invoice/" + request.GET.get('code'),
            headers=self.get_http_header(request),
        )

        self.is_auth_valid(request, get_res)
        try:
            invoice = get_res.json()
        except:
            invoice = {}

        return render(
            request=request,
            template_name="apps/shop/single_invoice.html",
            context={
                'invoice': invoice,
                'error': False
            }
        )


class Invoice(BaseViewClass):
    def get(self, request):
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/invoice/",
            headers=self.get_http_header(request),
            params=self.add_pagination_param(request, {})
        )

        self.is_auth_valid(request, get_res)
        try:
            invoices = get_res.json()
        except:
            invoices = []

        pagination_data = self.return_pagination(response=invoices, page=request.GET.get('page', 1))

        return render(
            request=request,
            template_name="apps/shop/invoices.html",
            context={
                'invoices': invoices,
                'pagination_data': pagination_data
            }
        )


class Final(BaseViewClass):
    def get(self, request):
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/invoice/" + request.GET.get('code'),
            headers=self.get_http_header(request),
        )

        self.is_auth_valid(request, get_res)
        try:
            invoice = get_res.json()
        except:
            invoice = {}

        return render(
            request=request,
            template_name="apps/shop/final.html",
            context={
                'invoice': invoice,
                'error': False
            }
        )


class SubCategory(BaseViewClass):
    def get(self, request, category_id):
        categories = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/product_manager/" + str(
                category_id) + "/sub_categories/",
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, categories)

        context = {
            "categories": categories.json(),
            "success": True
        }

        return JsonResponse(context)


class SingleProduct(BaseViewClass):
    def get(self, request, product_id):
        product_id = self.decode_id(product_id)
        if not product_id:
            return HttpResponseNotFound()

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/product/" + str(product_id),
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, get_res)

        if get_res.status_code == 403:
            return page_permission_denied_view(self.request)
        elif get_res.status_code == 404:
            return redirect(reverse('products'))
        elif get_res.status_code != 200:
            return HttpResponseNotFound()

        product_data = get_res.json()

        comments_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/product_comment/" + str(product_id) + "/product",
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, comments_res)

        context = {
            "product": product_data,
            # "comments": comments,
            # "params": _params
        }

        return render(
            request=request,
            context=context,
            template_name="apps/shop/single.html"
        )


class SingleTestProduct(BaseViewClass):
    def get(self, request):
        return render(
            request=request,
            context={},
            template_name="apps/shop/single_test.html"
        )


class BannerManager(BaseViewClass):
    def get(self, request):
        return render(
            request=request,
            template_name="apps/shop/banner_manager.html",
            context={}
        )


class SimpleBankPage(BaseViewClass):
    def get(self, request):
        return render(
            request=request,
            template_name="apps/shop/banner_manager.html",
            context={}
        )


class ProductsListManager(BaseViewClass):
    def get(self, request):
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/product_manager/",
            headers=self.get_http_header(request),
            params=self.add_pagination_param(request, {})
        )

        self.is_auth_valid(request, get_res)
        try:
            product_resp = get_res.json()
        except:
            product_resp = []

        pagination_data = self.return_pagination(response=product_resp, page=request.GET.get('page', 1))

        return render(
            request=request,
            template_name="apps/shop/product_list_manager.html",
            context={
                "pagination_data": pagination_data,
                "products": product_resp,
            }
        )


class ShopManagerIndex(BaseViewClass):
    def get(self, request):
        return render(
            request=request,
            template_name="apps/shop/product_index_manager.html",
            context={}
        )


class LoadFieldSampleForm(BaseViewClass):
    def post(self, request):
        context = {
            "message": "error"
        }

        sample_form = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/product_manager/sample_form",
            headers=self.get_http_header(request),
            params={"id": request.POST.get('sample_form_id')}
        )

        self.is_auth_valid(request, sample_form)
        if sample_form.status_code == 200:
            context["message"] = "success"
            context["sample_form"] = sample_form.json()

        return JsonResponse(context)


class ProductsInsertManager(BaseViewClass):
    def get(self, request):
        context = {}
        product_id = request.GET.get("id")
        if product_id:
            product = requests.get(
                url=settings.SERVER_FULL_URL + "/api/v1/product_manager/" + product_id,
                headers=self.get_http_header(request),
            )
            if product.status_code == 200:
                context["product"] = product.json()
                context["product"]["sample_form_fields"] = json.dumps(context["product"].get('sample_form_fields', "[]"))

            else:
                return HttpResponseNotFound()
            if context["product"]['category']:
                get_res = requests.get(
                    url=settings.SERVER_FULL_URL + "/api/v1/product_manager/" + str(context["product"]['category']['parent']['id']) + "/sub_categories/",
                    headers=self.get_http_header(request)
                )
                context['sub_categories'] = get_res.json()

        categories = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/product_manager/categories",
            headers=self.get_http_header(request),
        )

        self.is_auth_valid(request, categories)
        if categories.status_code == 200:
            context["categories"] = categories.json()

        sample_forms = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/product_manager/sample_forms",
            headers=self.get_http_header(request),
        )
        self.is_auth_valid(request, sample_forms)
        if sample_forms.status_code == 200:
            context["sample_forms"] = sample_forms.json()

        return render(
            request=request,
            template_name="apps/shop/product_insert_manager.html",
            context=context
        )

    def post(self, request):
        headers = self.get_http_header(request).copy()

        post_req, post_files, errors = self.cleaned_data(request)
        product_id = ""
        message = ""

        if not errors:
            if request.POST.get("product_id", False):
                _req = self.update_product(headers, post_files, post_req, request)
                message = "update"
                if _req.status_code != 200:
                    errors = ['اطلاعات ارسالی اشتباه می باشد.']
                else:
                    product_id = _req.json()["id"]
            else:
                _req = self.insert_product(headers, post_files, post_req, request)
                message = "insert"

                if _req.status_code != 201:
                    errors = ['اطلاعات ارسالی اشتباه می باشد.']
                else:
                    product_id = _req.json()["id"]

        return JsonResponse({"errors": errors, 'product_id': product_id, 'message': message})

    def insert_product(self, headers, post_files, post_req, request):
        _res = requests.post(
            url=settings.SERVER_FULL_URL + "/api/v1/product_manager/",
            data=post_req, files=post_files, headers=headers
        )
        self.is_auth_valid(request, _res)
        return _res

    def update_product(self, headers, post_files, post_req, request):
        deleted_images = []
        deleted_files = []
        product_id = request.POST.get('product_id')

        if not product_id:
            return False

        for _id in request.POST.get("deleted_images", '').split(','):
            try:
                deleted_images.append(int(_id))
            except:
                continue
        for _id in request.POST.get("deleted_files", '').split(','):
            try:
                deleted_files.append(int(_id))
            except:
                continue

        post_req["deleted_images"] = json.dumps(deleted_images)
        post_req["deleted_files"] = json.dumps(deleted_files)
        post_req["product_id"] = product_id

        _res = requests.post(
            url=settings.SERVER_FULL_URL + "/api/v1/product_manager/update/",
            data=post_req, files=post_files, headers=headers
        )
        self.is_auth_valid(request, _res)
        return _res

    @staticmethod
    def cleaned_data(request):
        data = request.POST
        errors = []
        title = data.get('title') if data.get('title') else errors.append("عنوان نباید خالی باشد.")
        published = data.get('published') if data.get('published') else errors.append('وضعیت محصول مشخص نیست.')
        description = data.get('description') if data.get('description') else errors.append('توضیحات مشخص نیست.')
        gender = data.get('gender') if data.get('gender') else errors.append('جنسیت مشخص نیست.')
        category = data.get('category') if data.get('category') else errors.append('دسته مشخص نیست.')

        status_price = data.get('status_price')
        price = data.get('price')

        if not status_price and not price:
            errors.append('قیمت را وارد کنید.')

        status_discount = data.get('status_discount')
        discount = data.get('discount')
        if status_discount == "on" and not discount:
            errors.append('تخفیف را وارد کنید.')

        is_free = True if status_price == "on" else False

        if is_free:
            price = 0
            discount = 0
            status_discount = False
            link_buy_direct = ""
        else:

            link_buy_direct = data.get('link_buy_direct')
            if link_buy_direct:
                if not (link_buy_direct.startswith("http://") and link_buy_direct.startswith("http://")):
                    link_buy_direct = "http://" + link_buy_direct

        sample_form = data.get('sample_form')

        for_student = True if data.get('for_student') == 'on' else False
        for_teacher = True if data.get('for_teacher') == 'on' else False

        is_digital = 0
        seller_name = data.get('seller_name')

        post_req = {
            "title": title,
            "published": published,
            "gender": gender,
            "description": description,
            "price": price,
            "has_discount": True if status_discount == "on" else False,
            "is_free": True if status_price == "on" else False,
            "discount": discount,
            "sample_form": sample_form,
            "category": category,
            "is_digital": is_digital,
            "seller_name": seller_name,
            "link_buy_direct": link_buy_direct,
            "for_student": for_student,
            "for_teacher": for_teacher
        }

        # for field in list(post_req):
        #     if post_req[field] == "":
        #         post_req.pop(field)

        sample_forms = []
        for post_item in data:
            if str(post_item).lower().find("sample_forms") > -1 and data[post_item]:
                sample_forms.append({
                    "id": int(post_item.split('sample_forms')[-1]),
                    "value": data.get(post_item)
                })

        post_req["sample_forms[]"] = json.dumps(sample_forms)

        post_files = []
        for file_item in request.FILES.getlist("images[]"):
            post_files.append(
                ('images[]', (file_item.name, file_item.file.read(), file_item.content_type))
            )
        for file_item in request.FILES.getlist("files[]"):
            post_files.append(
                ('files[]', (file_item.name, file_item.file.read(), file_item.content_type))
            )

        return post_req, post_files, errors


class SearchProduct(BaseViewClass):
    def get(self, request):

        price = request.GET.get("price", None)
        order = request.GET.get("order", None)
        text = request.GET.get("text", None)
        category = request.GET.get("category", None)
        has_discount = request.GET.get("has_discount", None)

        params = dict(
            text=text,
            points=price,
            order=order,
            category=category,
            has_discount=1 if has_discount == "on" else 0,
        )

        if price:
            price_data = price.split(",")
            params["price_start"] = int(float(price_data[0]))
            params["price_end"] = int(float(price_data[1]))

        query_params = {}

        for key in params:
            if params[key] is not None and params[key] is not '':
                query_params[key] = params[key]

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/product/search",
            headers=self.get_http_header(request),
            params=self.add_pagination_param(request, query_params)
        )
        self.is_auth_valid(request, get_res)
        try:
            product_resp = get_res.json()
        except:
            product_resp = []

        pagination_data = self.return_pagination(response=product_resp, page=request.GET.get('page', 1))
        context = {
            "products": product_resp,
            "pagination_data": pagination_data,
            "categories": [],
            "query_params": params
        }

        categories = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/product_manager/categories",
            headers=self.get_http_header(request),
        )

        self.is_auth_valid(request, categories)
        if categories.status_code == 200:
            context["categories"] = categories.json()

        return render(
            request=request,
            context=context,
            template_name="apps/shop/search.html",
        )


class ProductsDeleteManager(BaseViewClass):
    def get(self, request):
        get_res = requests.post(
            url=settings.SERVER_FULL_URL + "/api/v1/product_manager/delete/",
            headers=self.get_http_header(request),
            data={'product_id': request.GET.get('id')}
        )
        self.is_auth_valid(request, get_res)
        return redirect(reverse('product_list_manager'))
