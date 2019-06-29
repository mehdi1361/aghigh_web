from django.conf.urls import url
from apps.shop.views import (
    ShopManagerIndex,
    ProductsListManager,
    ProductsInsertManager,
    LoadFieldSampleForm,
    ProductsIndex,
    Basket,
    Payment,
    SingleProduct,
    Final,
    SearchProduct,
    DeleteBasket,
    SingleInvoice,
    Invoice,
    ProductsDeleteManager,
    BannerManager,
    SingleTestProduct,
    SubCategory
)


urlpatterns = [
    url(r'^$', ProductsIndex.as_view(), name='products'),
    url(r'^basket/$', Basket.as_view(), name='shopping_basket'),
    url(r'^delete_basket/$', DeleteBasket.as_view(), name='delete_basket'),
    url(r'^payment/$', Payment.as_view(), name='shopping_payment'),
    url(r'^final/$', Final.as_view(), name='shopping_final'),
    url(r'^invoice/$', Invoice.as_view(), name='shopping_invoice'),
    url(r'^single_invoice/$', SingleInvoice.as_view(), name='single_invoice'),
    url(r'^search/$', SearchProduct.as_view(), name='search_product'),
    url(r'^(?P<product_id>[\w\d-]+)$', SingleProduct.as_view(), name='single_product'),
    url(r'^test_shop/$', SingleTestProduct.as_view(), name='test_shop'),

    url(r'^manager/$', ShopManagerIndex.as_view(), name='product_index_manager'),
    url(r'^manager/products$', ProductsListManager.as_view(), name='product_list_manager'),
    url(r'^manager/products/insert$', ProductsInsertManager.as_view(), name='product_insert_manager'),
    url(r'^manager/products/delete', ProductsDeleteManager.as_view(), name='product_delete_manager'),
    url(r'^manager/products/sample_form', LoadFieldSampleForm.as_view(), name='load_sample_form_field'),

    url(r'sub/category/(?P<category_id>[\w\d-]+)$', SubCategory.as_view(), name='sub_category'),

    url(r'^manager/banner$', BannerManager.as_view(), name='banner_manager'),
    url(r'^simple_bank$', BannerManager.as_view(), name='simple_bank'),

]
