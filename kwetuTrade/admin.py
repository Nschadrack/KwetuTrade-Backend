from django.contrib import admin
from .models import *


admin.site.register(Coffee)
admin.site.register(CoffeeWeight)
admin.site.register(Animal)
admin.site.register(Material)
admin.site.register(Chemical)
admin.site.register(CoffeeShippingFee)
admin.site.register(MaterialShippingFee)
admin.site.register(AnimalShippingFee)
admin.site.register(ChemicalShippingFee)
admin.site.register(CoffeeShippingCountryPrice)
admin.site.register(AnimalShippingCountryPrice)
admin.site.register(MaterialShippingCountryPrice)
admin.site.register(ChemicalShippingCountryPrice)
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(BillingAddress)
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderNotOnSiteItem)
admin.site.register(OrderNotOnSite)
admin.site.register(Advert)
admin.site.register(CustomerOrderInvoice)

