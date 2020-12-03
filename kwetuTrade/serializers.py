from rest_framework import serializers
from . import  models
from django.contrib.auth import get_user_model
from django.utils import timezone


UserModel = get_user_model()



#########################  ANIMAL SHIPPING COUNTRY PRICE SERIALIZER  ######################################################################################
class AnimalShippingCountryPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnimalShippingCountryPrice
        fields = '__all__'


    def create(self, request):
        animal_shipping_fee = models.AnimalShippingFee.objects.get(shippingfee_ID=request["animal_shipping_fee"].shippingfee_ID)

        try:
            last_shipping_price = models.AnimalShippingCountryPrice.objects.last().shippingcountryprice_ID
            shipping_price_obj = models.AnimalShippingCountryPrice(
                shippingcountryprice_ID=last_shipping_price + 1,
                country=request["country"],
                state_province=request["state_province"],
                price=request["price"],
                animal_shipping_fee=animal_shipping_fee
            )

            shipping_price_obj.save()

            return shipping_price_obj
        
        except:
            shipping_price_obj = models.AnimalShippingCountryPrice(
                shippingcountryprice_ID=1,
                country=request["country"],
                state_province=request["state_province"],
                price=request["price"],
                animal_shipping_fee=animal_shipping_fee
            )

            shipping_price_obj.save()

            return shipping_price_obj 
    
    def update(self, instance, validated_data):
        instance.country = validated_data.get("country", instance.country)
        instance.state_province = validated_data.get("state_province", instance.state_province)
        instance.price = validated_data.get("price", instance.price)

        instance.save()

        return instance



######################### COFFEE SHIPPING FEE COUNTRY PRICE SERIALIZER  #################################################################################################
class CoffeeShippingCountryPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CoffeeShippingCountryPrice
        fields = '__all__'
    

    def create(self, request):
        coffee_shipping_fee = models.CoffeeShippingFee.objects.get(shippingfee_ID=request["coffee_shipping_fee"].shippingfee_ID)

        try:
            last_shipping_price = models.CoffeeShippingCountryPrice.objects.last().shippingcountryprice_ID
            shipping_price_obj = models.CoffeeShippingCountryPrice(
                shippingcountryprice_ID=last_shipping_price + 1,
                country=request["country"],
                state_province=request["state_province"],
                price=request["price"],
                coffee_shipping_fee=coffee_shipping_fee
            )

            shipping_price_obj.save()

            return shipping_price_obj
        
        except:
            shipping_price_obj = models.CoffeeShippingCountryPrice(
                shippingcountryprice_ID=1,
                country=request["country"],
                state_province=request["state_province"],
                price=request["price"],
                coffee_shipping_fee=coffee_shipping_fee
            )

            shipping_price_obj.save()

            return shipping_price_obj 
    
    def update(self, instance, validated_data):
        instance.country = validated_data.get("country", instance.country)
        instance.state_province = validated_data.get("state_province", instance.state_province)
        instance.price = validated_data.get("price", instance.price)

        instance.save()

        return instance




######################### MATERIAL SHIPPING FEE COUNTRY PRICE SERIALIZER  #################################################################################################
class MaterialShippingCountryPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MaterialShippingCountryPrice
        fields = '__all__'

    
    def create(self, request):
        material_shipping_fee = models.MaterialShippingFee.objects.get(shippingfee_ID=request["material_shipping_fee"].shippingfee_ID)

        try:
            last_shipping_price = models.MaterialShippingCountryPrice.objects.last().shippingcountryprice_ID
            shipping_price_obj = models.MaterialShippingCountryPrice(
                shippingcountryprice_ID=last_shipping_price + 1,
                country=request["country"],
                state_province=request["state_province"],
                price=request["price"],
                material_shipping_fee=material_shipping_fee
            )

            shipping_price_obj.save()

            return shipping_price_obj
        
        except:
            shipping_price_obj = models.MaterialShippingCountryPrice(
                shippingcountryprice_ID=1,
                country=request["country"],
                state_province=request["state_province"],
                price=request["price"],
                material_shipping_fee=material_shipping_fee
            )

            shipping_price_obj.save()

            return shipping_price_obj 
    
    def update(self, instance, validated_data):
        instance.country = validated_data.get("country", instance.country)
        instance.state_province = validated_data.get("state_province", instance.state_province)
        instance.price = validated_data.get("price", instance.price)

        instance.save()

        return instance




######################### CHEMICAL SHIPPING FEE COUNTRY PRICE SERIALIZER  #################################################################################################
class ChemicalShippingCountryPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChemicalShippingCountryPrice
        fields = '__all__'


    def create(self, request):
        chemical_shipping_fee = models.ChemicalShippingFee.objects.get(shippingfee_ID=request["chemical_shipping_fee"].shippingfee_ID)

        try:
            last_shipping_price = models.ChemicalShippingCountryPrice.objects.last().shippingcountryprice_ID
            shipping_price_obj = models.ChemicalShippingCountryPrice(
                shippingcountryprice_ID=last_shipping_price + 1,
                country=request["country"],
                state_province=request["state_province"],
                price=request["price"],
                chemical_shipping_fee=chemical_shipping_fee
            )

            shipping_price_obj.save()

            return shipping_price_obj
        
        except:
            shipping_price_obj = models.ChemicalShippingCountryPrice(
                shippingcountryprice_ID=1,
                country=request["country"],
                state_province=request["state_province"],
                price=request["price"],
                chemical_shipping_fee=chemical_shipping_fee
            )

            shipping_price_obj.save()

            return shipping_price_obj 
    
    def update(self, instance, validated_data):
        instance.country = validated_data.get("country", instance.country)
        instance.state_province = validated_data.get("state_province", instance.state_province)
        instance.price = validated_data.get("price", instance.price)

        instance.save()

        return instance





#########################  ANIMAL SHIPPING FEE SERIALIZER  #################################################################################################
class AnimalShippingFeeSerializer(serializers.ModelSerializer):
    animalshippingcountryprices = AnimalShippingCountryPriceSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.AnimalShippingFee
        fields = ['shippingfee_ID', 'unit', 'min_weight', 'max_weight', 'currency',
        'animal', 'animalshippingcountryprices']


    def create(self, request):
        animal_found = models.Animal.objects.get(animal_ID=request['animal'].animal_ID)

        try:
            last_shipping_fee=models.AnimalShippingFee.objects.last().shippingfee_ID
            animal_shipping_fee_obj = models.AnimalShippingFee(
                shippingfee_ID=last_shipping_fee + 1,
                unit=request["unit"],
                min_weight=request["min_weight"],
                max_weight=request["max_weight"],
                animal=animal_found
            )

            animal_shipping_fee_obj.save()
            return animal_shipping_fee_obj
            
        except:
            animal_shipping_fee_obj = models.AnimalShippingFee(
                shippingfee_ID=1,
                unit=request["unit"],
                min_weight=request["min_weight"],
                max_weight=request["max_weight"],
                animal=animal_found
            )

            animal_shipping_fee_obj.save()
            return animal_shipping_fee_obj
            
        
    def update(self, instance, validated_data):
        instance.unit = validated_data.get("unit", instance.unit)
        instance.min_weight = validated_data.get("min_weight", instance.min_weight)
        instance.max_weight = validated_data.get("max_weight", instance.max_weight)

        instance.save()

        return instance



######################### COFFEE SHIPPING FEE SERIALIZER  #################################################################################################
class CoffeeShippingFeeSerializer(serializers.ModelSerializer):
    coffeeshippingcountryprices = CoffeeShippingCountryPriceSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.CoffeeShippingFee
        fields = ['shippingfee_ID', 'unit', 'min_weight', 'max_weight', 'currency',
        'coffee', 'coffeeshippingcountryprices']
    

    def create(self, request):
        coffee_found = models.Coffee.objects.get(coffee_ID=request['coffee'].coffee_ID)

        try:
            last_shipping_fee=models.CoffeeShippingFee.objects.last().shippingfee_ID
            coffee_shipping_fee_obj = models.CoffeeShippingFee(
                shippingfee_ID=last_shipping_fee + 1,
                unit=request["unit"],
                min_weight=request["min_weight"],
                max_weight=request["max_weight"],
                coffee=coffee_found
            )
            coffee_shipping_fee_obj.save()
            return coffee_shipping_fee_obj
            
        except:
            coffee_shipping_fee_obj = models.CoffeeShippingFee(
                shippingfee_ID=1,
                unit=request["unit"],
                min_weight=request["min_weight"],
                max_weight=request["max_weight"],
                coffee=coffee_found
            )
            coffee_shipping_fee_obj.save()
            return coffee_shipping_fee_obj
            
        
    def update(self, instance, validated_data):
        instance.unit = validated_data.get("unit", instance.unit)
        instance.min_weight = validated_data.get("min_weight", instance.min_weight)
        instance.max_weight = validated_data.get("max_weight", instance.max_weight)

        instance.save()

        return instance




######################### MATERIAL SHIPPING FEE SERIALIZER  #################################################################################################
class MaterialShippingFeeSerializer(serializers.ModelSerializer):
    materialshippingcountryprices = MaterialShippingCountryPriceSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.MaterialShippingFee
        fields = ['shippingfee_ID', 'unit', 'min_weight', 'max_weight', 'currency',
        'material', 'materialshippingcountryprices']

    def create(self, request):
        material_found = models.Material.objects.get(material_ID=request['material'].material_ID)

        try:
            last_shipping_fee=models.MaterialShippingFee.objects.last().shippingfee_ID
            material_shipping_fee_obj = models.MaterialShippingFee(
                shippingfee_ID=last_shipping_fee + 1,
                unit=request["unit"],
                min_weight=request["min_weight"],
                max_weight=request["max_weight"],
                material=material_found
            )

            material_shipping_fee_obj.save()
            return material_shipping_fee_obj
            
        except:
            material_shipping_fee_obj = models.MaterialShippingFee(
                shippingfee_ID=1,
                unit=request["unit"],
                min_weight=request["min_weight"],
                max_weight=request["max_weight"],
                material=material_found
            )

            material_shipping_fee_obj.save()
            return material_shipping_fee_obj
            
        
    def update(self, instance, validated_data):
        instance.unit = validated_data.get("unit", instance.unit)
        instance.min_weight = validated_data.get("min_weight", instance.min_weight)
        instance.max_weight = validated_data.get("max_weight", instance.max_weight)

        instance.save()

        return instance



######################### CHEMICAL SHIPPING FEE SERIALIZER  #################################################################################################
class ChemicalShippingFeeSerializer(serializers.ModelSerializer):
    chemicalshippingcountryprices = ChemicalShippingCountryPriceSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.ChemicalShippingFee
        fields = ['shippingfee_ID', 'unit', 'min_weight', 'max_weight', 'currency',
        'chemical', 'chemicalshippingcountryprices']


    def create(self, request):
        chemical_found = models.Chemical.objects.get(chemical_ID=request['chemical'].chemical_ID)

        try:
            last_shipping_fee=models.ChemicalShippingFee.objects.last().shippingfee_ID
            chemical_shipping_fee_obj = models.ChemicalShippingFee(
                shippingfee_ID=last_shipping_fee + 1,
                unit=request["unit"],
                min_weight=request["min_weight"],
                max_weight=request["max_weight"],
                chemical=chemical_found
            )

            chemical_shipping_fee_obj.save()
            return chemical_shipping_fee_obj
            
        except:
            chemical_shipping_fee_obj = models.ChemicalShippingFee(
                shippingfee_ID=1,
                unit=request["unit"],
                min_weight=request["min_weight"],
                max_weight=request["max_weight"],
                chemical=chemical_found
            )

            chemical_shipping_fee_obj.save()
            return chemical_shipping_fee_obj
            
        
    def update(self, instance, validated_data):
        instance.unit = validated_data.get("unit", instance.unit)
        instance.min_weight = validated_data.get("min_weight", instance.min_weight)
        instance.max_weight = validated_data.get("max_weight", instance.max_weight)

        instance.save()

        return instance


##########################  COFFEE WEIGHTS SERIALIZER  ##############################################################################################
class CoffeeWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CoffeeWeight
        fields = '__all__'
    
    def create(self, request):
        coffee_found = models.Coffee.objects.get(coffee_ID=request["coffee"].coffee_ID)
        try:
            last_weight = models.CoffeeWeight.objects.last().unit_ID
            weight = models.CoffeeWeight(
                unit_ID=last_weight + 1,
                unit=request["unit"],
                quantity=request["quantity"],
                price=request["price"],
                coffee=coffee_found
            )
            weight.save()
            return weight
        except:
            weight = models.CoffeeWeight(
                unit_ID=1,
                unit=request["unit"],
                quantity=request["quantity"],
                price=request["price"],
                coffee=coffee_found
            )
            weight.save()
            return weight
    
    def update(self, instance, validated_data):
        instance.unit = validated_data.get("unit", instance.unit)
        instance.quantity = validated_data.get("quantity", instance.quantity)
        instance.price = validated_data.get("price", instance.price)

        instance.save()

        return instance



######################### COFFEE SERIALIZER  ########################################################################################################
class CoffeeSerializer(serializers.ModelSerializer):
    coffeeweights = CoffeeWeightSerializer(many=True, read_only=True)
    coffee_shipping_fees = CoffeeShippingFeeSerializer(many=True, read_only=True)
    class Meta:
        model = models.Coffee
        fields = [
            'coffee_ID', 'name', 'classification', 'image',
            'status', 'added_date', 'description', 'currency',
            'brand', 'coffee_type', 'coffeeweights', 'coffee_shipping_fees']
        
    def create(self, request):
        try:
            lastCoffee=models.Coffee.objects.last().coffee_ID
            coffee_obj = models.Coffee(
                coffee_ID=lastCoffee+1,
                name=request['name'],
                image=request['image'],
                description=request['description'],
                brand=request['brand'],
                coffee_type=request['coffee_type']
            )
            coffee_obj.save()
            return coffee_obj
        except:
            coffee_obj = models.Coffee(
                coffee_ID=1,
                name=request['name'],
                image=request['image'],
                description=request['description'],
                brand=request['brand'],
                coffee_type=request['coffee_type']
            )
            coffee_obj.save()
            return coffee_obj

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.status = validated_data.get('status',instance.status)
        instance.description = validated_data.get('description', instance.description)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.coffee_type = validated_data.get('coffee_type', instance.coffee_type)

        instance.save()

        return instance
        



###########################  MATERIAL SERIALIZER   #################################################################################################
class MaterialSerializer(serializers.ModelSerializer):
    material_shipping_fees = MaterialShippingFeeSerializer(many=True, read_only=True)
    class Meta:
        model = models.Material
        fields = [
        'material_ID', 'name', 'classification', 'image',
        'status', 'added_date', 'description', 'currency',
        'price', 'unit', 'weight', 'material_shipping_fees']


    def create(self, request):
        try:
            last_material = models.Material.objects.last().material_ID
            material_obj = models.Material(
                material_ID=last_material + 1,
                name=request["name"],
                image=request["image"],
                description= request["description"],
                price=request["price"],
                weight=request["weight"]
            )

            material_obj.save()
            return material_obj
        except:
            material_obj = models.Material(
                material_ID=1,
                name=request["name"],
                image=request["image"],
                description= request["description"],
                price=request["price"],
                weight=request["weight"]
            )

            material_obj.save()
            return material_obj
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.status = validated_data.get("status", instance.status)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.weight = validated_data.get("weight", instance.weight)

        instance.save()

        return instance





########################################  ANIMAL SERIALIZER  ##########################################################################################
class AnimalSerializer(serializers.ModelSerializer):
    animal_shipping_fees = AnimalShippingFeeSerializer(many=True, read_only=True)
    class Meta:
        model = models.Animal
        fields = [
            'animal_ID', 'name', 'classification', 'image',
            'status', 'added_date', 'description', 'currency',
            'price', 'unit', 'weight', 'animal_shipping_fees']
    
    def create(self, request):
        try:
            last_animal = models.Animal.objects.last().animal_ID
            animal = models.Animal(
                animal_ID=last_animal + 1,
                name=request["name"],
                image=request["image"],
                description=request["description"],
                price=request["price"],
                weight=request["weight"],
            )
            animal.save()
            return animal
        
        except:
            animal = models.Animal(
                animal_ID=1,
                name=request["name"],
                image=request["image"],
                description=request["description"],
                price=request["price"],
                weight=request["weight"],
            )
            animal.save()
            return animal 
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.status = validated_data.get("status", instance.status)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.weight = validated_data.get("weight", instance.weight)

        instance.save()
        return instance




######################################  CHEMICAL SERIALIZER  ########################################################################################
class ChemicalSerializer(serializers.ModelSerializer):
    chemical_shipping_fees = ChemicalShippingFeeSerializer(many=True, read_only=True)
    class Meta:
        model = models.Chemical
        fields = [
            'chemical_ID', 'name', 'classification', 'image',
            'status', 'added_date', 'description', 'currency', 'weight',
            'price', 'chemical_shipping_fees']



    def create(self, request):
        try:
            last_chemical = models.Chemical.objects.last().chemical_ID
            chemical = models.Chemical(
                chemical_ID=last_chemical + 1,
                name=request["name"],
                image=request["image"],
                description=request["description"],
                price=request["price"],
                weight=request["weight"]
            )
            chemical.save()
            return chemical
        
        except:
            chemical = models.Chemical(
                chemical_ID=1,
                name=request["name"],
                image=request["image"],
                description=request["description"],
                price=request["price"],
                weight=request["weight"]
            )
            chemical.save()
            return chemical 
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.status = validated_data.get("status", instance.status)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.weight = validated_data.get("weight", instance.weight)

        instance.save()
        return instance


##################### billing address serializer  ############################
class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BillingAddress
        fields = "__all__"

#################### shipping address serializer ############################
class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShippingAddress
        fields = "__all__"

################################ users serializer ###########################
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude =["password"]


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomerOrderInvoice
        fields = "__all__"


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = "__all__"
    


class OrderSerializer(serializers.ModelSerializer):
    ordered_products = OrderItemsSerializer(many=True, read_only=True)
    billing_address = BillingAddressSerializer(many=False, read_only=True)
    shipping_address = ShippingAddressSerializer(many=False, read_only=True)
    invoices = InvoiceSerializer(many=True, read_only=True)

    class Meta:
        model = models.Order
        fields = ["order_number", "quantity_ordered", "amount_ordered", "shipping_fee", "ordered_date",
        "out_of_delivery_date", "delivered_date","rejected_date", "order_status", "newness_order_status", "ordered_products",
        "billing_address", "shipping_address", "customer", "invoices"]


    def update(self, instance, validated_data):
        instance.order_status = validated_data.get("order_status", instance.order_status)

        instance.save()
        return instance


#################################### SPECIAL ORDER SERIALIZER ########################################################################

class SpecialOrderItems(serializers.ModelSerializer):
    class Meta:
        model = models.OrderNotOnSiteItem
        fields = "__all__"


class SpecialOrderSerializer(serializers.ModelSerializer):
    ordered_products = SpecialOrderItems(many=True, read_only=True)

    class Meta:
        model = models.OrderNotOnSite
        fields = ["order_number", "quantity_ordered", "amount_ordered", "ordered_date", "out_of_delivery_date",
        "delivered_date", "rejected_date", "order_status", "newness_order_status", "ordered_products", "country", "province", "email_address", "phone_number", "customer"]
    


#################################### CUSTOMER SERIALIZER #############################################################################
class CustomerSerializer(serializers.ModelSerializer):
    user=UserSerializer(many=False, read_only=True)
    orders=OrderSerializer(many=True, read_only=True)
    orders_not_on_site=SpecialOrderSerializer(many=True, read_only=True)
    billing_address = BillingAddressSerializer(many=True, read_only=True)
    shipping_address = ShippingAddressSerializer(many=True, read_only=True)
    class Meta:
        model = models.Customer
        fields = ["customer_id", "user", "profile_pic", "orders", "orders_not_on_site", "billing_address", "shipping_address"]

    def create(self, request):
        user = UserModel.objects.last()
        try:
            last_customer_id = models.Customer.objects.last().customer_id
            customer_obj = models.Customer(
                customer_id=last_customer_id + 1,
                user=user

                )
            customer_obj.save()
        except:
            customer_obj = models.Customer(
                customer_id=1,
                user=user
                )
            customer_obj.save()
        
        return customer_obj
    
    def update(self, instance, validated_data):
        instance.profile_pic = validated_data.get("profile_pic", instance.profile_pic)

        instance.save()

        return instance



#####################################################  Advert serializer ##########################################################################

class AdvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Advert
        fields = "__all__"

    def create(self, request):
        try:
            last_advert_id = models.Advert.objects.last().advert_number
            advert_obj = models.Advert(
              advert_number= last_advert_id + 1,
              name = request["name"],
              image=request["image"],
              caption=  request["caption"]
            )

            advert_obj.save()
            return advert_obj
        except:
            advert_obj = models.Advert(
              advert_number= 1,
              name = request["name"],
              image=request["image"],
              caption=  request["caption"]
            )

            advert_obj.save()
            return advert_obj  

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.caption = validated_data.get("caption", instance.caption)

        instance.save()
        return instance
    


