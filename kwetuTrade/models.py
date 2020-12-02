from django.db import models
# from datetime import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model

UserModel = get_user_model()


################## CUSTOMER MODEL ###################################################################################################
class Customer(models.Model):
    """
    Customer model
    """
    customer_id = models.PositiveIntegerField(default=1, primary_key=True)
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default="customers/profiles/default-profile-pic.png", blank=True, null=True, upload_to="customers/profiles")


    def __str__(self):
        return self.user.username


################################## Billing and Shipping address Models #######################################################################
class BillingAddress(models.Model):
    """
    Billing Address Model
    """
    customer = models.ForeignKey(Customer, related_name="billing_address", on_delete=models.SET_NULL, null=True)
    billing_address_no = models.PositiveIntegerField(default=1, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=60, null=True, blank=True)
    country=models.CharField(max_length=40, null=True, blank=True)
    street_name_house_number = models.CharField(max_length=60)
    apartment_name = models.CharField(max_length=60, null=True, blank=True)
    city_town = models.CharField(max_length=60)
    state_country = models.CharField(max_length=50)
    zip_post_code = models.CharField(max_length=60)
    phone_number = models.CharField(max_length=15)
    email_address = models.EmailField(max_length=60)



    def __str__(self):
        return f"{self.state_country} {self.city_town} {self.zip_post_code}"



class ShippingAddress(models.Model):
    """
    Shipping Address Model
    """
    customer = models.ForeignKey(Customer, related_name="shipping_address", on_delete=models.SET_NULL, null=True)
    shipping_address_no = models.PositiveIntegerField(default=1, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=60, null=True, blank=True)
    country=models.CharField(max_length=40, null=True, blank=True)
    street_name_house_number = models.CharField(max_length=60)
    apartment_name = models.CharField(max_length=60, null=True, blank=True)
    city_town = models.CharField(max_length=60)
    state_country = models.CharField(max_length=50)
    zip_post_code = models.CharField(max_length=60)
    phone_number = models.CharField(max_length=15)
    email_address = models.EmailField(max_length=60)



    def __str__(self):
        return f"{self.state_country} {self.city_town} {self.zip_post_code}"



################## COFFEE MODEL #######################################################################################################
class Coffee(models.Model):
    coffee_ID = models.PositiveIntegerField(primary_key=True, default=1)
    name = models.CharField(max_length=30, default="name")
    classification = models.CharField(max_length=30, default="coffee")
    image = models.ImageField(null=True, upload_to="products/images/coffee", blank=True)
    status = models.CharField(max_length=30, default="Deactive")
    added_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=True)
    currency = models.CharField(max_length=10, default="$")
    brand = models.CharField(max_length=30, null=True)
    coffee_type = models.CharField(max_length=30, null=True)


    def __str__(self):
        return str(self.name) + "(" + self.coffee_type + "   " + self.brand + "  " + self.classification +")"


############################## COFFEE WEIGHT MODEL ####################################################################################
class CoffeeWeight(models.Model):
    unit_ID = models.PositiveIntegerField(primary_key=True, default=1)
    unit = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE, related_name='coffeeweights', null=True)



    def __str__(self):
        return str(self.quantity) + self.unit + "  " + self.coffee.currency + str(self.price)



############################## MATERIAL MODEL #########################################################################################
class Material(models.Model):
    material_ID = models.PositiveIntegerField(primary_key=True, default=1)
    name = models.CharField(max_length=30, default="name")
    classification = models.CharField(max_length=30, default="material")
    image = models.ImageField(null=True, upload_to="products/images/materials", blank=True)
    status = models.CharField(max_length=30, default="Deactive")
    added_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=True)
    unit = models.CharField(default="kg", max_length=10)
    weight = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default="$")
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.name + self.classification



############################## ANIMAL MODEL ###########################################################################################
class Animal(models.Model):
    animal_ID = models.PositiveIntegerField(primary_key=True, default=1)
    name = models.CharField(max_length=30, default="name")
    classification = models.CharField(max_length=30, default="animal")
    image = models.ImageField(null=True, upload_to="products/images/animals", blank=True)
    status = models.CharField(max_length=30, default="Deactive")
    added_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=True)
    currency = models.CharField(max_length=10, default="$")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(default="kg", max_length=10)
    weight = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)


    def __str__(self):
        return self.name + self.classification



############################## CHEMICAL MODEL ##########################################################################################
class Chemical(models.Model):
    chemical_ID = models.PositiveIntegerField(primary_key=True, default=1)
    name = models.CharField(max_length=30, default="name")
    classification = models.CharField(max_length=30, default="chemical")
    image = models.ImageField(null=True, upload_to="products/images/chemicals", blank=True)
    status = models.CharField(max_length=30, default="Deactive")
    added_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=True)
    currency = models.CharField(max_length=10, default="$")
    weight = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.name + self.classification



############################## SHIPPINGFEE MODEL #######################################################################################
class MaterialShippingFee(models.Model):
    shippingfee_ID = models.PositiveIntegerField(primary_key=True, default=1)
    unit = models.CharField(max_length=5, default="kg")
    min_weight = models.DecimalField(max_digits=10, decimal_places=2)
    max_weight = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="$")
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="material_shipping_fees", null=True, blank=True)
   
  
    def __str__(self):
        return str(self.min_weight) + self.unit + " - " + str(self.max_weight) + self.unit


class CoffeeShippingFee(models.Model):
    shippingfee_ID = models.PositiveIntegerField(primary_key=True, default=1)
    unit = models.CharField(max_length=5, default="g")
    min_weight = models.DecimalField(max_digits=10, decimal_places=2)
    max_weight = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="$")
    coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE, related_name="coffee_shipping_fees", null=True, blank=True)

    def __str__(self):
        return str(self.min_weight) + self.unit + " - " + str(self.max_weight) + self.unit


class AnimalShippingFee(models.Model):
    shippingfee_ID = models.PositiveIntegerField(primary_key=True, default=1)
    unit = models.CharField(max_length=5, default="kg")
    min_weight = models.DecimalField(max_digits=10, decimal_places=2)
    max_weight = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="$")
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="animal_shipping_fees", null=True, blank=True)


    def __str__(self):
        return str(self.min_weight) + self.unit + " - " + str(self.max_weight) + self.unit


class ChemicalShippingFee(models.Model):
    shippingfee_ID = models.PositiveIntegerField(primary_key=True, default=1)
    unit = models.CharField(max_length=5, default="g")
    min_weight = models.DecimalField(max_digits=10, decimal_places=2)
    max_weight = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="$")
    chemical = models.ForeignKey(Chemical, on_delete=models.CASCADE, related_name="chemical_shipping_fees", null=True, blank=True)


    def __str__(self):
        return str(self.min_weight) + self.unit + " - " + str(self.max_weight) + self.unit



############################## SHIPPING COUNTRY PRICE MODEL #############################################################################
class CoffeeShippingCountryPrice(models.Model):
    shippingcountryprice_ID = models.PositiveIntegerField(primary_key=True, default=1)
    country = models.CharField(max_length=50)
    state_province = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    coffee_shipping_fee = models.ForeignKey(CoffeeShippingFee, on_delete=models.CASCADE, related_name="coffeeshippingcountryprices", null=True)



    def __str__(self):
        return self.country + "   " + self.shipping_fee.currency + str(self.price)


class AnimalShippingCountryPrice(models.Model):
    shippingcountryprice_ID = models.PositiveIntegerField(primary_key=True, default=1)
    country = models.CharField(max_length=50)
    state_province = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    animal_shipping_fee = models.ForeignKey(AnimalShippingFee, on_delete=models.CASCADE, related_name="animalshippingcountryprices", null=True)



    def __str__(self):
        return self.country + "   " + self.shipping_fee.currency + str(self.price)



class MaterialShippingCountryPrice(models.Model):
    shippingcountryprice_ID = models.PositiveIntegerField(primary_key=True, default=1)
    country = models.CharField(max_length=50)
    state_province = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    material_shipping_fee = models.ForeignKey(MaterialShippingFee, on_delete=models.CASCADE, related_name="materialshippingcountryprices", null=True)



    def __str__(self):
        return self.country + "   " + self.shipping_fee.currency + str(self.price)


class ChemicalShippingCountryPrice(models.Model):
    shippingcountryprice_ID = models.PositiveIntegerField(primary_key=True, default=1)
    country = models.CharField(max_length=50)
    state_province = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    chemical_shipping_fee = models.ForeignKey(ChemicalShippingFee, on_delete=models.CASCADE, related_name="chemicalshippingcountryprices", null=True)



    def __str__(self):
        return self.country + "   " + self.shipping_fee.currency + str(self.price)


####################################### ORDER MODEL ##########################################################################
class OrderItem(models.Model):
    """
    ordered products model
    """
    order_item_id = models.PositiveIntegerField(primary_key=True, default=1)
    item_name = models.CharField(max_length=100)
    item_image = models.ImageField(null=True, blank=True, upload_to="products_ordered/images")
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    classification = models.CharField(max_length=50)
    description = models.TextField()
    weight = models.FloatField()
    product_id = models.PositiveIntegerField()


    def __str__(self):
        return f"{self.item_name}  {self.classification}"




class Order(models.Model):
    """
    Order model
    """
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, related_name="orders", null=True)
    order_number = models.PositiveIntegerField(default=1, primary_key=True)
    quantity_ordered = models.PositiveIntegerField()
    amount_ordered = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    ordered_date = models.DateTimeField(default=timezone.now)
    out_of_delivery_date = models.DateTimeField(null=True, blank=True)
    delivered_date = models.DateTimeField(null=True, blank=True)
    rejected_date = models.DateTimeField(null=True, blank=True)
    order_status = models.CharField(max_length=50, default="pending")
    newness_order_status = models.CharField(max_length=50, default="new")
    ordered_products = models.ManyToManyField(OrderItem, related_name="order_items")
    billing_address = models.ForeignKey(BillingAddress, related_name="orders", on_delete=models.SET_NULL, null=True)
    shipping_address = models.ForeignKey(ShippingAddress, related_name="shipping_address", on_delete=models.SET_NULL, null=True)
    

    def set_newness_order_status(self):
        self.newness_order_status = "old"
        self.save()
    
    def set_out_of_delivery_date(self):
        self.out_of_delivery_date = timezone.now()
        self.save()
    
    def set_delivered_date(self):
        self.delivered_date = timezone.now()
        self.save() 

    def set_rejected_date(self):
        self.rejected_date = timezone.now()
        self.save()   


    def __str__(self):
        return f"order {self.order_number}"


################################# generating invoices ################################################################

class CustomerOrderInvoice(models.Model):
    invoice_number = models.PositiveIntegerField(default=1, primary_key=True)
    invoice_date = models.DateTimeField(default=timezone.now)
    order_number = models.ForeignKey(Order, null=True, blank=True, related_name="invoices", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.invoice_number)




####################################################  SLIDING ADVERTS, ANNOUNCEMENTS AND BRAND NEW PRODUCTS MARKETING ###################################################

class Advert(models.Model):
    advert_number = models.PositiveIntegerField(default=1, primary_key=True)
    name = models.CharField(max_length=100)
    uploaded_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(null=True, blank=True)
    published = models.BooleanField(default=False)
    status = models.CharField(default="Deactive", max_length=30)
    image = models.ImageField(upload_to="adverts/images", blank=True, null=True)
    caption = models.TextField(null=True, blank=True)


    def set_active_status(self):
        self.status = "Active"
        self.save()

    def set_deactive_status(self):
        self.status = "Deactive"
        self.save()

    def publish(self):
        self.published_date = timezone.now()
        self.published = True 
        self.save()
        self.set_active_status()
    

    def unpublish(self):
        self.published_date = None
        self.status = "Deactive"
        self.published = False
        self.save()
        self.set_deactive_status()

    
    def __str__(self):
        return self.name




###################################################### ORDER OF YOUR CHOICE NOT ON THE LIST #################################################

class OrderNotOnSiteItem(models.Model):
    item_number = models.PositiveIntegerField(default=1, primary_key=True)
    item_name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    quantity = models.DecimalField(decimal_places=2, max_digits=12)
    price = models.DecimalField(decimal_places=2, max_digits=12)
    image = models.ImageField(null=True, blank=True, upload_to="special_order/images")
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.item_name
    

class OrderNotOnSite(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, related_name="orders_not_on_site", null=True)
    order_number = models.PositiveIntegerField(default=1, primary_key=True)
    quantity_ordered = models.PositiveIntegerField()
    amount_ordered = models.DecimalField(max_digits=12, decimal_places=2)
    ordered_date = models.DateTimeField(default=timezone.now)
    out_of_delivery_date = models.DateTimeField(null=True, blank=True)
    delivered_date = models.DateTimeField(null=True, blank=True)
    rejected_date = models.DateTimeField(null=True, blank=True)
    order_status = models.CharField(max_length=50, default="pending")
    newness_order_status = models.CharField(max_length=50, default="new")
    ordered_products = models.ManyToManyField(OrderNotOnSiteItem, related_name="order_items")
    country = models.CharField(max_length=30, null=True, blank=True)
    province = models.CharField(max_length=30, null=True, blank=True)
    email_address = models.EmailField(max_length=60, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    

    def set_newness_order_status(self):
        self.newness_order_status = "old"
        self.save()
    
    def set_out_of_delivery_date(self):
        self.out_of_delivery_date = timezone.now()
        self.save()
    
    def set_delivered_date(self):
        self.delivered_date = timezone.now()
        self.save()

    def set_rejected_date(self):
        self.rejected_date = timezone.now()
        self.save()   


    def __str__(self):
        return f"special order {self.order_number} for {self.customer.user.first_name} {self.customer.user.last_name}"




