from django.urls import path 
from . import views


app_name = 'kwetuTrade'

urlpatterns = [
    path("api/", views.api_list, name="api_list"),
    path("<str:classification>/list/", views.products_list, name="products_list"),
    path("add-new/<str:classification>/product/", views.create_product, name="create_product"),
    path("update/<str:classification>/product/<str:pk>/", views.update_product, name="update_product"),
    path("<str:classification>/product/detail/<str:pk>/", views.detail_product, name="detail_product"),
    path("delete/<str:classification>/product/<str:pk>/", views.delete_product, name="delete_product"),
    path("<str:classification>/products/list/users/", views.products_list_to_users, name="products_list_to_users"),


    path("coffee/product/weights/", views.coffee_weights, name="coffee_weights"),
    path("coffee/product/<str:pk>/add/weight/", views.add_coffee_weight, name="add_coffee_weight"),
    path("coffee/product/update/weight/<str:pk>/", views.update_coffee_weight, name="update_coffee_weight"),
    path("coffee/product/delete/weight/<str:pk>/", views.delete_coffee_weight, name="delete_coffee_weight"),
    path("coffee/product/<str:pk>/weights/", views.coffee_weights_list, name="coffee_weights_list"),


    path("<str:classification>/product/shipping/list/", views.product_shipping_fees_list, name="product_shipping_fees_list"),
    path("<str:classification>/product/<str:pk>/shipping/list/", views.single_product_shipping_fee_list, name="single_product_shipping_fee_list"),
    path("add/<str:classification>/product/<str:pk>/shipping-fee/", views.add_shipping_fee, name="add_shipping_fee"),
    path("update/<str:classification>/product/shipping-fee/<str:pk>/", views.update_shipping_fee, name="update_shipping_fee"),
    path("delete/<str:classification>/product/shipping-fee/<str:pk>/", views.delete_shipping_fee, name="delete_shipping_fee"),


    path("<str:classification>/product/country/shipping-prices/", views.shipping_country_prices_list, name="shipping_country_prices_list"),
    path("<str:classification>/product/shipping-fee/<str:pk>/country-prices/", views.single_shipping_fee_country_prices_list, name="single_shipping_fee_country_prices_list"),
    path("<str:classification>/product/shipping-fee/<str:pk>/add/country-price/", views.add_shipping_fee_country_price, name="add_shipping_fee_country_price"),
    path("<str:classification>/product/shipping-fee/update/country-price/<str:pk>/", views.update_shipping_fee_country_price, name="update_shipping_fee_country_price"),
    path("<str:classification>/product/shipping-fee/delete/country-price/<str:pk>/", views.delete_shipping_fee_country_price, name="delete_shipping_fee_country_price"),


    path("customers/", views.customers, name="customers"),
    path("customer/<str:pk>/detail/", views.customer_detail, name="customer_detail"),
    path("delete/customer/<str:pk>/", views.delete_customer, name="delete_customer"),
    path("new/customer/", views.create_customer, name="create_customer"),
    path("update/customer/<str:pk>/profile/", views.update_customer, name="update_customer"),
    path("users_list/", views.users_list, name="users_list"),
    path("users/specific_username/", views.specific_username, name="specific_username"),
    path("user/check-username/", views.check_username, name="check_username"),
    path("user/resetting-password/<str:username>/", views.resetting_password, name="resetting_password"),


    path("create/new/order/", views.create_order, name="create_order"),
    path("orders_list/", views.orders_list, name="orders_list"),
    path("orders/<str:pk>/detail/", views.order_detail, name="order_detail"),
    path("update/order/<str:pk>/", views.update_order, name="update_order"),
    path("delete/order/<str:pk>/", views.delete_order, name="delete_order"),

    path("create/new/special-order/", views.create_special_order, name="create_special_order"),
    path("special-orders_list/", views.special_orders_list, name="special_orders_list"),
    path("special-orders/<str:pk>/detail/", views.special_order_detail, name="special_order_detail"),
    path("update/special-order/<str:pk>/", views.update_special_order, name="update_special_order"),
    path("delete/special-order/<str:pk>/", views.delete_special_order, name="delete_special_order"),
    path("special-orders/item/<str:pk>/detail/", views.special_order_item, name="special_order_item"),

    path("create/new/advert/", views.create_advert, name="create_advert"),
    path("update/advert/<str:pk>/", views.update_advert, name="update_advert"),
    path("delete/advert/<str:pk>/", views.delete_advert, name="delete_advert"),
    path("adverts-list/", views.adverts_list, name="adverts_list"),
    path("advert/<str:pk>/publish-unpublish/", views.pubish_unpublish_advert, name="pubish_unpublish_advert"),
    path("advert/<str:pk>/detail/", views.advert_detail, name="advert_detail"),


    path("invoice/<str:pk>/", views.GeneratePdf.as_view(), name="generate_pdf_invoice"),
    path("invoices_list/", views.invoices, name="invoices"),

]


