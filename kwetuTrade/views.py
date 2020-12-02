from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser 
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import *
from .serializers import *
from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail

from django.views.generic import View

from .utils import render_to_pdf
from django.template.loader import get_template


UserModel = get_user_model()


############################# GENERATING PDF INVOICE ###########################################################################

class GeneratePdf(View):
    def get(self, request, pk, *args, **kwargs):
        invoice = CustomerOrderInvoice.objects.get(invoice_number=pk)
        order_number = invoice.order_number.order_number
        invoice_items = invoice.order_number.ordered_products.all()

        ground_total = invoice.order_number.amount_ordered + invoice.order_number.shipping_fee

        template = get_template('pdf/invoice.html')
        context = {
            "company_name": "Kwetu Trade Ltd",
            "address": "Bwishyura, Karongi, Western province, RWANDA",
            "email": "kwetutrade@gmail.com",
            "order_number": order_number,
            "invoice_id": invoice.invoice_number,
            "customer_name": invoice.order_number.billing_address.first_name + " " +invoice.order_number.billing_address.last_name,
            "customer_email": invoice.order_number.billing_address.email_address,
            "customer_phone": invoice.order_number.billing_address.phone_number,
            "customer_address": invoice.order_number.billing_address.country + ", " + invoice.order_number.billing_address.state_country + ", " + invoice.order_number.billing_address.city_town,
            "customer_zipCode": invoice.order_number.billing_address.zip_post_code,
            "amount": invoice.order_number.amount_ordered,
            "shipping_fee": invoice.order_number.shipping_fee,
            "ordered_date": invoice.order_number.ordered_date,
            "ground_total": ground_total,
            "invoice_date": invoice.invoice_date.utcnow().today(),
            "invoice_items":invoice_items
        }
        html = template.render(context)
        pdf = render_to_pdf('pdf/invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Kwetu_Trade_Invoice_%s.pdf" %(datetime.utcnow().today())
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content

            return response
        return HttpResponse("Not found")

################################# List of invoices ################################
@api_view(["GET"])
def invoices(request):
    invoices = CustomerOrderInvoice.objects.all().order_by("-invoice_date")
    serializer = InvoiceSerializer(invoices, many=True)

    return Response(serializer.data)

##################################  API URLS FOR THE PROJECT  ########################################################################
@api_view(["GET"])
def api_list(request):
    api_url ={
        'coffee_products_list': '/coffee/list/',
        'coffee_product_detail': '/coffee/detail/id/',
        'electronics_furniture_list': '/material/list/',
        'electronics_furniture_list': '/material/detail/id/',
        'live_animal_list': '/animal/list/',
        'live_animal_list': '/animal/detail/id/',
        'chemicals_list': '/chemical/list/',
        'chemicals_list': '/chemical/detail/id/',
    }

    return Response(api_url)



#################################### LIST OF PRODUCTS  ###############################################################################
@api_view(["GET"])
def products_list(request, classification):

    if classification == 'coffee':
        coffees = Coffee.objects.all().order_by('added_date')
        new_coffees = []
        for coffee in coffees:
            coffee.added_date= str(coffee.added_date.date())
            new_coffees.append(coffee)

        serializer = CoffeeSerializer(new_coffees, many=True)
        return Response(serializer.data)

    elif classification == 'material':
        materials = Material.objects.all().order_by("added_date")
        materials_serialized = []
        for material in materials:
            material.added_date = str(material.added_date.date())
            materials_serialized.append(material)

        serializer = MaterialSerializer(materials_serialized, many=True)

        return Response(serializer.data)

    
    elif classification == 'animal':
        animals = Animal.objects.all().order_by("added_date")
        animals_serialized = []

        for animal in animals:
            animal.added_date = str(animal.added_date.date())
            animals_serialized.append(animal)
        
        serializer = AnimalSerializer(animals_serialized, many=True)

        return Response(serializer.data)
    

    elif classification == 'chemical':
        chemicals = Chemical.objects.all().order_by("added_date")
        chemicals_serialized = []

        for chemical in chemicals:
            chemical.added_date = str(chemical.added_date.date())
            chemicals_serialized.append(chemical)
        
        serializer = ChemicalSerializer(chemicals_serialized, many=True)

        return Response(serializer.data)
    
    else:
        return HttpResponse("Invalid request!")


######################################## PRODUCT LIST TOBE SHOWN TO THE USERS ########################################################
@api_view(["GET"])
def products_list_to_users(request, classification):

    if classification == 'coffee':
        coffees = Coffee.objects.filter(status="Active").order_by('added_date')
        new_coffees = []
        for coffee in coffees:
            coffee.added_date= str(coffee.added_date.date())
            weights = coffee.coffeeweights.all()
            shipping_fees = coffee.coffee_shipping_fees.all()
            if len(shipping_fees) != 0:
                countryprices = shipping_fees[0].coffeeshippingcountryprices.all()
                if (len(weights) > 0 and len(shipping_fees) > 0 and len(countryprices) > 0):
                    new_coffees.append(coffee)

        serializer = CoffeeSerializer(new_coffees, many=True)
        return Response(serializer.data)

    elif classification == 'material':
        materials = Material.objects.filter(status="Active").order_by("added_date")
        materials_serialized = []
        for material in materials:
            material.added_date = str(material.added_date.date())
            shipping_fees = material.material_shipping_fees.all()
            if len(shipping_fees) != 0:
                country_prices = shipping_fees[0].materialshippingcountryprices.all()
                if (len(shipping_fees) > 0 and len(country_prices) > 0):
                    materials_serialized.append(material)

        serializer = MaterialSerializer(materials_serialized, many=True)

        return Response(serializer.data)

    
    elif classification == 'animal':
        animals = Animal.objects.filter(status="Active").order_by("added_date")
        animals_serialized = []

        for animal in animals:
            animal.added_date = str(animal.added_date.date())
            shipping_fees = animal.animal_shipping_fees.all()
            if len(shipping_fees) != 0:
                country_prices = shipping_fees[0].animalshippingcountryprices.all()
                if(len(shipping_fees) > 0 and len(country_prices) > 0):
                    animals_serialized.append(animal)
        
        serializer = AnimalSerializer(animals_serialized, many=True)

        return Response(serializer.data)
    

    # elif classification == 'chemical':
    #     chemicals = Chemical.objects.all().order_by("added_date")
    #     chemicals_serialized = []

    #     for chemical in chemicals:
    #         chemical.added_date = str(chemical.added_date.date())
    #         chemicals_serialized.append(chemical)
        
    #     serializer = ChemicalSerializer(chemicals_serialized, many=True)

    #     return Response(serializer.data)
    
    else:
        return HttpResponse("Invalid request!")


########################################   PRODUCT DETAIL  #############################################################################
@api_view(["GET"])
def detail_product(request, classification, pk):
    if classification == "coffee":
        try:
            coffee = Coffee.objects.get(coffee_ID=pk)
            coffee.added_date = str(coffee.added_date.date())
            serializer = CoffeeSerializer(coffee, many=False)
            return Response(serializer.data)
        
        except:
            return HttpResponse("<h3>Coffee does not exist with primary key: " + str(pk))
    
    elif classification == "material":
        try:
            material = Material.objects.get(material_ID=pk)
            material.added_date = str(material.added_date.date())
            serializer = MaterialSerializer(material, many=False)
            return Response(serializer.data)
        except:
            return HttpResponse("<h3>Material does not exist with primary key: " + str(pk))
    
    elif classification == "animal":
        try:
            animal = Animal.objects.get(animal_ID=pk)
            animal.added_date = str(animal.added_date.date())
            serializer = AnimalSerializer(animal, many=False)
            return Response(serializer.data)
        except:
            return HttpResponse("<h3>Animal does not exist with primary key: " + str(pk))
    
    elif classification == "chemical":
        try:
            chemical = Chemical.objects.get(chemical_ID=pk)
            chemical.added_date = str(chemical.added_date.date())
            serializer = ChemicalSerializer(chemical, many=False)
            return Response(serializer.data)
        except:
            return HttpResponse("<h3>Chemical does not exist with primary key: " + str(pk))

    
    else:
        return HttpResponse("Invalid request!")

############################################### UPDATING PRODUCTS  ####################################################################
@api_view(["PUT"])
@parser_classes([JSONParser, FormParser , MultiPartParser ])
def update_product(request, classification, pk):
    if classification == 'coffee':
        # try:
        coffee = Coffee.objects.get(coffee_ID=pk)
        serializer=CoffeeSerializer(instance=coffee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print("ERROS: ", serializer.errors)
            return Response({
                "message errors" : serializer.errors
            })
        # except:
        #     return HttpResponse("We are sorry, we didn't find product corresponding to that number!")


    elif classification == 'material':
        try:
            material = Material.objects.get(material_ID=pk)
            serializer = MaterialSerializer(instance=material, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({"ERROS": serializer.erros})
        except:
            return HttpResponse("We are sorry, we didn't find product corresponding to that number!")

    
    elif classification == 'animal':
        try:
            animal = Animal.objects.get(animal_ID=pk)
            serializer = AnimalSerializer(animal, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({"ERRORS": serializer.errors})
        except:
            return HttpResponse("We are sorry, we didn't find product corresponding to that number!") 
    

    elif classification == 'chemical':
            try:
                chemical = Chemical.objects.get(chemical_ID=pk)
                serializer = ChemicalSerializer(chemical, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response({"ERROS": serializer.errors})
            except:
                return HttpResponse("We are sorry, we didn't find product corresponding to that number!")
    
    else:
        return HttpResponse("Invalid request!")



##########################################  DELETING PRODUCTS  ########################################################################
@api_view(["DELETE"])
def delete_product(request, classification, pk):
    if classification == 'coffee':
        try:
            coffee = Coffee.objects.get(coffee_ID=pk)
            try:
                order_item = OrderItem.objects.get(product_id=pk)
                return Response({"answer": "this coffee can not be deleted, it has been ordered at least once!"})
            except:
                coffee.delete()
                return Response({"answer": "coffee deleted successfully!"})
        except:
            return HttpResponse("Sorry coffee was not found!")


    elif classification == 'material':
        try:
            material = Material.objects.get(material_ID=pk)
            try:
                order_item = OrderItem.objects.get(product_id=pk)
                return Response({"answer": "this product can not be deleted, it has been ordered at least once!"})
            except:
                material.delete()
                return Response({"answer": "product deleted successfully!"})
        except:
            return HttpResponse("Sorry material was not found!")

    
    elif classification == 'animal':
        try:
            animal = Animal.objects.get(animal_ID=pk)
            try:
                order_item = OrderItem.objects.get(product_id=pk)
                return Response({"answer": "this product can not be deleted, it has been ordered at least once!"})
            except:
                animal.delete()
                return Response({"answer": "product deleted successfully!"})
        except:
            return HttpResponse("Sorry animal was not found!")

    elif classification == 'chemical':
        try:
            chemical = Chemical.objects.get(chemical_ID=pk)
            try:
                order_item = OrderItem.objects.get(product_id=pk)
                return Response({"answer": "this product can not be deleted, it has been ordered at least once!"})
            except:
                chemical.delete()
                return Response({"answer": "product deleted successfully!"})
        except:
            return HttpResponse("Sorry chemical was not found!")
    
    else:
        return HttpResponse("Invalid request!")


###########################################   CREATING PRODUCTS   ######################################################################
@api_view(["POST"])
@parser_classes([JSONParser, FormParser , MultiPartParser ])
def create_product(request, classification):
    if classification == 'coffee':
        serializer = CoffeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print("ERROS: ", serializer.errors)
            emessage=serializer.errors
            return Response({"status": "Bad request","message": emessage})


    elif classification == 'material':
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"ERRORS": serializer.errors})


    elif classification == 'animal':
            serializer = AnimalSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({"ERROS": serializer.errors})
    

    elif classification == 'chemical':
            serializer = ChemicalSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({"ERROS": serializer.errors})
   
    else:
        return HttpResponse("Invalid request!")



###########################################   COFFEE WEIGHTS   #########################################################################
@api_view(["GET"])
def coffee_weights(request):

    weights = CoffeeWeight.objects.all().order_by('unit_ID')
    serializer = CoffeeWeightSerializer(weights, many=True)

    return Response(serializer.data)




###########################################   ADDING COFFEE WEIGHTS   ######################################################################
@api_view(["POST"])
def add_coffee_weight(request, pk):
    try:
        coffee_item = Coffee.objects.get(coffee_ID=pk)
        serializer = CoffeeWeightSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)
        else:
            return Response({
                "errors": serializer.errors,
                })
    except:
        return HttpResponse("Coffee was not found to add its weights!")



###########################################   UPDATING COFFEE WEIGHTS   #######################################################################
@api_view(["PUT"])
def update_coffee_weight(request, pk):
    try:
        weight = CoffeeWeight.objects.get(unit_ID=pk)
        serializer = CoffeeWeightSerializer(instance=weight, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        else:
            return Response({
                "Erros": serializer.errors
            })
    except:
        return HttpResponse("Updating was not done successfully! make sure you have entered correct weight id")




###########################################   DELETE COFFEE WEIGHTS   #########################################################################
@api_view(["DELETE"])
def delete_coffee_weight(request, pk):
    try:
        weight = CoffeeWeight.objects.get(unit_ID=pk)
        weight.delete()

        return HttpResponse("Weight deleted successfully!")
    except:
        return HttpResponse("Weight was not deleted!")



###########################################   COFFEE WEIGHTS LIST  SPECIFIC COFFEE################################################################
@api_view(["GET"])
def coffee_weights_list(request, pk):
        weight_for_coffee = CoffeeWeight.objects.filter(coffee=pk)
        serializer = CoffeeWeightSerializer(weight_for_coffee, many=True)
        return Response(serializer.data)

    
###########################################   SHIPPING FEE   ###################################################################################

########################### SHIPPING FEE LIST FOR PRODUCT OF CERTAIN CLASSIFICATION ###############
@api_view(["GET"])
def product_shipping_fees_list(request, classification):
    if classification == "coffee":
        coffee_shipping_fee = CoffeeShippingFee.objects.all()
        serializer = CoffeeShippingFeeSerializer(coffee_shipping_fee, many=True)
        return Response(serializer.data)
    

    elif classification == "material":
        material_shipping_fee = MaterialShippingFee.objects.all()
        serializer = MaterialShippingFeeSerializer(material_shipping_fee, many=True)
        return Response(serializer.data) 
    

    elif classification == "animal":
        animal_shipping_fee = AnimalShippingFee.objects.all()
        serializer = AnimalShippingFeeSerializer(animal_shipping_fee, many=True)
        return Response(serializer.data) 

    
    elif classification =="chemical":
        chemical_shipping_fee = ChemicalShippingFee.objects.all()
        serializer = ChemicalShippingFeeSerializer(chemical_shipping_fee, many=True)
        return Response(serializer.data) 
    
    else:
        return HttpResponse("Invalid request!")




############################ SHIPPING FEE LIST FOR SINGLE PRODUCT OF CERTAIN CLASSIFICATION ######################################################
@api_view(["GET"])
def single_product_shipping_fee_list(request, classification, pk):
    if classification == "coffee":
        coffee_shipping_fee = CoffeeShippingFee.objects.filter(coffee=pk)
        serializer = CoffeeShippingFeeSerializer(coffee_shipping_fee, many=True)

        return Response(serializer.data)
    
    elif classification == "material":
        material_shipping_fee = MaterialShippingFee.objects.filter(material=pk)
        serializer = MaterialShippingFeeSerializer(material_shipping_fee, many=True)

        return Response(serializer.data) 
    
    elif classification == "chemical":
        chemical_shipping_fee = ChemicalShippingFee.objects.filter(chemical=pk)
        serializer = ChemicalShippingFeeSerializer(chemical_shipping_fee, many=True)

        return Response(serializer.data) 
    
    elif classification == "animal":
        animal_shipping_fee = AnimalShippingFee.objects.filter(animal=pk)
        serializer = AnimalShippingFeeSerializer(animal_shipping_fee, many=True)

        return Response(serializer.data) 
    
    else:
        return HttpResponse("Invalid request!")




############################ ADDING SHIPPING FEE FOR EACH PRODUCT OF CERTAIN CLASSIFICATION #########################################################
@api_view(["POST"])
def add_shipping_fee(request, classification, pk):
    if classification == "coffee":
        try:
            coffee = Coffee.objects.get(coffee_ID=pk)
            serializer = CoffeeShippingFeeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({
                    "ERRORS": serializer.errors
                }) 
        except:
            return HttpResponse("Please make sure coffee id is valid!")

    elif classification == "material":
        try:
            material = Material.objects.get(material_ID=pk)
            serializer = MaterialShippingFeeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({
                    "ERRORS": serializer.errors
                }) 
        except:
            return HttpResponse("Please make sure material id is valid!") 

    elif classification == "animal":
        try:
            animal = Animal.objects.get(animal_ID=pk)
            serializer = AnimalShippingFeeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({
                    "ERRORS": serializer.errors
                }) 
        except:
            return HttpResponse("Please make sure animal id is valid!") 

    elif classification == "chemical":
        try:
            chemical = Chemical.objects.get(chemical_ID=pk)
            serializer = ChemicalShippingFeeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({
                    "ERRORS": serializer.errors
                }) 
        except:
            return HttpResponse("Please make sure chemical id is valid!")  
    
    else:
        return HttpResponse("Invalid request!")




############################ UPDATING SHIPPING FEE FOR EACH PRODUCT OF CERTAIN CLASSIFICATION ########################################################
@api_view(["PUT"])
def update_shipping_fee(request, classification, pk):
    if classification == "coffee":
        try:
            coffee_shipping_fee = CoffeeShippingFee.objects.get(shippingfee_ID=pk)
            serializer = CoffeeShippingFeeSerializer(instance=coffee_shipping_fee, data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)
            else:
                return Response({
                    "ERRORS": serializer.erros
                })
        except:
            return HttpResponse("Invalid request!")

    elif classification == "material":
        try:
            material_shipping_fee = MaterialShippingFee.objects.get(shippingfee_ID=pk)
            serializer = MaterialShippingFeeSerializer(instance=material_shipping_fee, data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)
            else:
                return Response({
                    "ERRORS": serializer.erros
                })
        except:
            return HttpResponse("INVALID REQUEST!")

    elif classification == "animal":
        try:
            animal_shipping_fee = AnimalShippingFee.objects.get(shippingfee_ID=pk)
            serializer = AnimalShippingFeeSerializer(instance=animal_shipping_fee, data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)
            else:
                return Response({
                    "ERRORS": serializer.erros
                })
        except:
            return HttpResponse("INVALID REQUEST!")

    elif classification == "chemical":
        try:
            chemical_shipping_fee = ChemicalShippingFee.objects.get(shippingfee_ID=pk)
            serializer = ChemicalShippingFeeSerializer(instance=chemical_shipping_fee, data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)
            else:
                return Response({
                    "ERRORS": serializer.erros
                })
        except:
            return HttpResponse("INVALID REQUEST!")
    
    else:
        return HttpResponse("Invalid request!")




############################ DELETING SHIPPING FEE FOR EACH PRODUCT OF CERTAIN CLASSIFICATION ########################################################
@api_view(["DELETE"])
def delete_shipping_fee(request, classification, pk):
    if classification == "coffee":
        try:
            coffee_shipping_fee = CoffeeShippingFee.objects.get(shippingfee_ID=pk)
            coffee_shipping_fee.delete()
            return HttpResponse("Shipping has been deleted!")
        except:
            return HttpResponse("Please enter a valid shipping fee id")

    elif classification == "material":
        try:
            material_shipping_fee = MaterialShippingFee.objects.get(shippingfee_ID=pk)
            material_shipping_fee.delete()
            return HttpResponse("Shipping has been deleted!")
        except:
            return HttpResponse("Please enter a valid shipping fee id") 

    elif classification == "animal":
        try:
            animal_shipping_fee = AnimalShippingFee.objects.get(shippingfee_ID=pk)
            animal_shipping_fee.delete()
            return HttpResponse("Shipping has been deleted!")
        except:
            return HttpResponse("Please enter a valid shipping fee id")

    elif classification == "chemical":
        try:
            chemical_shipping_fee = ChemicalShippingFee.objects.get(shippingfee_ID=pk)
            chemical_shipping_fee.delete()
            return HttpResponse("Shipping has been deleted!")
        except:
            return HttpResponse("Please enter a valid shipping fee id") 
    else:
        return HttpResponse("Invalid request!")




############################ SHIPPING FEE COUNTRY PRICES FOR A CERTAIN PRODUCT CLASSIFICATION #########################################################
@api_view(["GET"])
def shipping_country_prices_list(request, classification):
    if classification == "coffee":
        coffee_shipping_country_prices = CoffeeShippingCountryPrice.objects.all()
        serializer = CoffeeShippingCountryPriceSerializer(coffee_shipping_country_prices, many=True)

        return Response(serializer.data)

    elif classification == "material":
        material_shipping_country_prices = MaterialShippingCountryPrice.objects.all()
        serializer = MaterialShippingCountryPriceSerializer(material_shipping_country_prices, many=True)

        return Response(serializer.data) 


    elif classification == "animal":
        animal_shipping_country_prices = AnimalShippingCountryPrice.objects.all()
        serializer = AnimalShippingCountryPriceSerializer(animal_shipping_country_prices, many=True)

        return Response(serializer.data) 
    

    elif classification == "chemical":
        chemical_shipping_country_prices = ChemicalShippingCountryPrice.objects.all()
        serializer = ChemicalShippingCountryPriceSerializer(chemical_shipping_country_prices, many=True)

        return Response(serializer.data) 
    
    else:
        return HttpResponse("Invalid request!")




############################ SHIPPING FEE COUNTRY PRICES FOR A CERTAIN SHIPPING FEE OF A CERTAIN PRODUCT CLASSIFICATION ################################
@api_view(["GET"])
def single_shipping_fee_country_prices_list(request, classification, pk):
    if classification == "coffee":
        coffee_shipping_country_prices = CoffeeShippingCountryPrice.objects.filter(coffee_shipping_fee=pk)
        serializer = CoffeeShippingCountryPriceSerializer(coffee_shipping_country_prices, many=True)
        return Response(serializer.data)

    elif classification == "material":
        material_shipping_country_prices = MaterialShippingCountryPrice.objects.filter(material_shipping_fee=pk)
        serializer = MaterialShippingCountryPriceSerializer(material_shipping_country_prices, many=True)
        return Response(serializer.data) 


    elif classification == "animal":
        animal_shipping_country_prices = AnimalShippingCountryPrice.objects.filter(animal_shipping_fee=pk)
        serializer = AnimalShippingCountryPriceSerializer(animal_shipping_country_prices, many=True)
        return Response(serializer.data) 
    

    elif classification == "chemical":
        chemical_shipping_country_prices = ChemicalShippingCountryPrice.objects.filter(chemical_shipping_fee=pk)
        serializer = ChemicalShippingCountryPriceSerializer(chemical_shipping_country_prices, many=True)
        return Response(serializer.data)  
    
    else:
        return HttpResponse("Invalid request!")





############################ ADDING SHIPPING FEE COUNTRY PRICES FOR A CERTAIN SHIPPING FEE OF A CERTAIN PRODUCT CLASSIFICATION ##########################
@api_view(["POST"])
def add_shipping_fee_country_price(request, classification, pk):
    if classification == "coffee":
        try:
            coffee_shipping_fee = CoffeeShippingFee.objects.get(shippingfee_ID=pk)
            serializer = CoffeeShippingCountryPriceSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)
            
            else:
                return Response({
                    "ERRORS": serializer.errors
                })
        
        except:
            return HttpResponse("coffee shipping with such id does not exist")

    elif classification == "material":
        try:
            material_shipping_fee = MaterialShippingFee.objects.get(shippingfee_ID=pk)
            serializer = MaterialShippingCountryPriceSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)
            
            else:
                return Response({
                    "ERRORS": serializer.errors
                })
        
        except:
            return HttpResponse("material shipping with such id does not exist") 


    elif classification == "animal":
        try:
            animal_shipping_fee = AnimalShippingFee.objects.get(shippingfee_ID=pk)
            serializer = AnimalShippingCountryPriceSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)
            
            else:
                return Response({
                    "ERRORS": serializer.errors
                })
        
        except:
            return HttpResponse("animal shipping with such id does not exist") 
    

    elif classification == "chemical":
        try:
            chemical_shipping_fee = ChemicalShippingFee.objects.get(shippingfee_ID=pk)
            serializer = ChemicalShippingCountryPriceSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)
            
            else:
                return Response({
                    "ERRORS": serializer.errors
                })
        
        except:
            return HttpResponse("chemical shipping with such id does not exist") 

    else:
        return HttpResponse("Invalid request!") 





############################ UPDATING SHIPPING FEE COUNTRY PRICES FOR A CERTAIN SHIPPING FEE OF A CERTAIN PRODUCT CLASSIFICATION ########################
@api_view(["PUT"])
def update_shipping_fee_country_price(request, classification, pk):
    if classification == "coffee":
        try:
            shipping_country_price =  CoffeeShippingCountryPrice.objects.get(shippingcountryprice_ID=pk)
            serializer = CoffeeShippingCountryPriceSerializer(instance=shipping_country_price, data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)
            
            else:
                return Response({
                    "ERROS": serializer.errors
                })
        except:
            return HttpResponse("Invalid data for updating!")
    

    elif classification == "material":
        try:
            shipping_country_price =  MaterialShippingCountryPrice.objects.get(shippingcountryprice_ID=pk)
            serializer = MaterialShippingCountryPriceSerializer(instance=shipping_country_price, data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)
            
            else:
                return Response({
                    "ERROS": serializer.errors
                })
        except:
            return HttpResponse("Invalid data for updating!") 


    elif classification == "animal":
        try:
            shipping_country_price =  AnimalShippingCountryPrice.objects.get(shippingcountryprice_ID=pk)
            serializer = AnimalShippingCountryPriceSerializer(instance=shipping_country_price, data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)
            
            else:
                return Response({
                    "ERROS": serializer.errors
                })
        except:
            return HttpResponse("Invalid data for updating!") 
    

    elif classification == "chemical":
        try:
            shipping_country_price =  ChemicalShippingCountryPrice.objects.get(shippingcountryprice_ID=pk)
            serializer = ChemicalShippingCountryPriceSerializer(instance=shipping_country_price, data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)
            
            else:
                return Response({
                    "ERROS": serializer.errors
                })
        except:
            return HttpResponse("Invalid data for updating!")

    else:
        return HttpResponse("Invalid request!")  





############################ DELETING SHIPPING FEE COUNTRY PRICES FOR A CERTAIN SHIPPING FEE OF A CERTAIN PRODUCT CLASSIFICATION ########################
@api_view(["DELETE"])
def delete_shipping_fee_country_price(request, classification, pk):
    if classification == "coffee":
        try:
            shipping_country_price =  CoffeeShippingCountryPrice.objects.get(shippingcountryprice_ID=pk)
            shipping_country_price.delete()

            return HttpResponse("Data deleted successfully!")
        except:
            return HttpResponse("We are unbale to process your request, try with correct data!") 

    elif classification == "material":
        try:
            shipping_country_price =  MaterialShippingCountryPrice.objects.get(shippingcountryprice_ID=pk)
            shipping_country_price.delete()

            return HttpResponse("Data deleted successfully!")
        except:
            return HttpResponse("We are unbale to process your request, try with correct data!")  


    elif classification == "animal":
        try:
            shipping_country_price =  AnimalShippingCountryPrice.objects.get(shippingcountryprice_ID=pk)
            shipping_country_price.delete()

            return HttpResponse("Data deleted successfully!")
        except:
            return HttpResponse("We are unbale to process your request, try with correct data!")  
    

    elif classification == "chemical":
        try:
            shipping_country_price =  ChemicalShippingCountryPrice.objects.get(shippingcountryprice_ID=pk)
            shipping_country_price.delete()

            return HttpResponse("Data deleted successfully!")
        except:
            return HttpResponse("We are unbale to process your request, try with correct data!")  
    
    else:
        return HttpResponse("Invalid request!")



##################################### CUSTOMER CREATION ##########################################################################

@api_view(["POST"])
def create_customer(request):
    try:
        user = UserModel(
            first_name=request.data["firstName"],
            last_name=request.data["lastName"],
            username=request.data["email"],
            email=request.data["email"],
            password=request.data["password"]
        )
        user.set_password(request.data["password"])
        user.save()
        request.data["user"] = user.id
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
        
        return Response(serializer.data)
    except:
        return HttpResponse("errors")



@api_view(["PUT"])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def update_customer(request, pk):
    user = UserModel.objects.get(id=pk)
    customer = Customer.objects.get(user=user)
    serializer = CustomerSerializer(instance=customer, data=request.data)
    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)

###################################### LIST OF CUSTOMER ##########################################################################
@api_view(["GET"])
def customers(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def customer_detail(request, pk):
    customer = Customer.objects.get(customer_id=pk)
    serializer = CustomerSerializer(customer, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
def delete_customer(request, pk):
    customer = Customer.objects.get(customer_id=pk)
    user = customer.user
    user.delete()
    customer.delete()


@api_view(["GET"])
def users_list(request):
    users = UserModel.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def specific_username(request):
    username = request.data["username"]
    password = request.data["password"]
    user = authenticate(request, username=username, password=password)

    if user is not None:
        serializer= UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"erros": "incorrect email or password"})


@api_view(["POST"])
def check_username(request):
    username= request.data
    try:
        user = UserModel.objects.get(username=username)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except:
        return Response({"erros": "no account for " + username + " found"})


@api_view(["POST"])
def resetting_password(request, username):
    try:
        user = UserModel.objects.get(username=username)
        user.set_password(request.data)
        user.save()
        return Response({"success": "password resetted succesfully!"})
    except:
        return Response({"fail": "Resetting password failed!"})

############################################# inserting orders ##########################################################################
@api_view(["POST"])
@parser_classes([JSONParser, FormParser , MultiPartParser ])
def create_order(request):
    order_items_IDs = []
    last_order_item_id = 1
    last_billing_id = 1
    last_shipping_id = 1
    last_order_number = 1

    quantity_ordered = 0.00
    amount_ordered = float(request.data["cart"]["subTotal"])

    if len(request.data["billing_address"]["company"]) == 0:
        request.data["billing_address"]["company"]= None

    if len(request.data["billing_address"]["apartment"]) == 0:
        request.data["billing_address"]["apartment"] = None
    
    if len(request.data["shipping_address"]["company"]) == 0:
        request.data["shipping_address"]["company"]= None

    if len(request.data["shipping_address"]["apartment"]) == 0:
        request.data["shipping_address"]["apartment"] = None


    #looking for last id for certain object tyle
    try:
        last_billing_id = BillingAddress.objects.last().billing_address_no
        last_billing_id += 1
    except:
        last_billing_id = 1
    
    try:
        last_shipping_id = ShippingAddress.objects.last().shipping_address_no
        last_shipping_id += 1
    except:
        last_shipping_id = 1
    
    try:
        last_order_number = Order.objects.last().order_number
        last_order_number += 1
    except:
        last_order_number = 1
    
    try:
        last_invoice_number = CustomerOrderInvoice.objects.last().invoice_number 
        last_invoice_number += 1
    
    except:
        last_invoice_number = 1 


    user = UserModel.objects.get(id=request.data["user"]["id"])
    customer = Customer.objects.get(user=user)

    billing_obj = BillingAddress(
        customer=customer,
        billing_address_no=last_billing_id,
        first_name=request.data["billing_address"]["firstName"],
        last_name=request.data["billing_address"]["lastName"],
        company_name=request.data["billing_address"]["company"],
        country=request.data["billing_address"]["billingCountry"],
        street_name_house_number=request.data["billing_address"]["houseStreetName"],
        apartment_name=request.data["billing_address"]["apartment"],
        city_town=request.data["billing_address"]["townCity"],
        state_country=request.data["billing_address"]["billingCountry"],
        zip_post_code=request.data["billing_address"]["postCode"],
        phone_number=request.data["billing_address"]["phoneNumber"],
        email_address=request.data["billing_address"]["emailAddress"]
    )
    billing_obj.save()

    shipping_obj = ShippingAddress(
        customer=customer,
        shipping_address_no=last_shipping_id,
        first_name=request.data["shipping_address"]["firstName"],
        last_name=request.data["shipping_address"]["lastName"],
        company_name=request.data["shipping_address"]["company"],
        country=request.data["shipping_address"]["shippingCountry"],
        street_name_house_number=request.data["shipping_address"]["houseStreetName"],
        apartment_name=request.data["shipping_address"]["apartment"],
        city_town=request.data["shipping_address"]["townCity"],
        state_country=request.data["shipping_address"]["shippingCountry"],
        zip_post_code=request.data["shipping_address"]["postCode"],
        phone_number=request.data["shipping_address"]["phoneNumber"],
        email_address=request.data["shipping_address"]["emailAddress"]
    )

    shipping_obj.save()


    for item in request.data["cart"]["items"]:
        quantity_ordered = float(quantity_ordered) + float(item["quantity"])
        try:
            last_order_item_id = OrderItem.objects.last().order_item_id
            last_order_item_id += 1
        except:
            last_order_item_id = 1

        order_item = OrderItem(
            order_item_id=last_order_item_id,
            item_name=item["itemName"],
            item_image=item["image"],
            quantity=item["quantity"],
            price=item["price"],
            classification=item["classification"],
            description=item["description"],
            weight=item["weight"],
            product_id=item["productId"]
        )
        order_item.save()
        order_items_IDs.append(order_item.order_item_id)

    
    order = Order(
      customer=customer,
      order_number= last_order_number,
      quantity_ordered= quantity_ordered,
      amount_ordered= amount_ordered,
      shipping_fee= float(request.data["shipping_fee"]),
      billing_address= billing_obj,
      shipping_address= shipping_obj
    )

    order.save()

    for order_item_id in order_items_IDs:
        order_item = OrderItem.objects.get(order_item_id=order_item_id)
        order.ordered_products.add(order_item)
    
    invoice = CustomerOrderInvoice(
        invoice_number=last_invoice_number,
        order_number=order
    )
    invoice.save()

    # subject = "Receiving Order Confirmation"
    # message = f"""Dear {billing_obj.first_name} {shipping_obj.last_name}, we have received your order and for any change on your order will be sent on this email\n
    # Thank you for choosing Kwetu Trade!"""
    # email_from = settings.EMAIL_HOST_USER
    # email_to = [order.shipping_address.email_address, order.shipping_address.email_address]

    # send_mail(subject, message, email_from, email_to, fail_silently=True)

    
    return HttpResponse("ok done")


######################## Retrieving orders #######################################
@api_view(["GET"])
def orders_list(request):
    orders = Order.objects.all().order_by("-ordered_date")
    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def order_detail(request, pk):

    try:
        order = Order.objects.get(order_number=pk)
        order.set_newness_order_status()
        serializer = OrderSerializer(order, many=False)

        return Response(serializer.data)
    
    except:
        return HttpResponse("not found")


@api_view(["PUT"])
def update_order(request, pk):
    try:
        order=Order.objects.get(order_number=pk)
        if request.data["order_status"] == "pending":
            order.out_of_delivery_date=None
            order.delivered_date=None
            order.rejected_date=None

            # subject = "Changing Order Status Confirmation"
            # message = f"""Dear {order.billing_address.first_name} {order.billing_address.last_name}, your order status has been changed to {request.data["order_status"]}\n
            # Thank you for choosing Kwetu Trade!"""
            # email_from = settings.EMAIL_HOST_USER
            # email_to = [order.shipping_address.email_address, order.shipping_address.email_address]

            # send_mail(subject, message, email_from, email_to, fail_silently=True)

        elif request.data["order_status"] == "out for delivery":
            order.set_out_of_delivery_date()
            order.delivered_date=None
            order.rejected_date=None

            # subject = "Changing Order Status Confirmation"
            # message = f"""Dear {order.billing_address.first_name} {order.billing_address.last_name}, your order status has been changed to {request.data["order_status"]}\n
            # Thank you for choosing Kwetu Trade!"""
            # email_from = settings.EMAIL_HOST_USER
            # email_to = [order.shipping_address.email_address, order.shipping_address.email_address]

            # send_mail(subject, message, email_from, email_to, fail_silently=True)

        elif request.data["order_status"] == "delivered":
            order.rejected_date=None
            order.set_delivered_date()

            # subject = "Changing Order Status Confirmation"
            # message = f"""Dear {order.billing_address.first_name} {order.billing_address.last_name}, your order status has been changed to {request.data["order_status"]}\n
            # Thank you for choosing Kwetu Trade!"""
            # email_from = settings.EMAIL_HOST_USER
            # email_to = [order.shipping_address.email_address, order.shipping_address.email_address]

            # send_mail(subject, message, email_from, email_to, fail_silently=True)


        elif request.data["order_status"] == "rejected":
            order.set_rejected_date()
            order.out_of_delivery_date=None
            order.delivered_date=None
            
            # subject = "Changing Order Status Confirmation"
            # message = f'Dear {order.billing_address.first_name} {order.billing_address.last_name}, your order status has been changed to {request.data["order_status"]}\nThank you for choosing Kwetu Trade!'
            # email_from = settings.EMAIL_HOST_USER
            # email_to = [order.shipping_address.email_address.strip(),]
            # print(email_from, "\t", email_to)

            # send_mail(subject, message, email_from, email_to)

        serializer = OrderSerializer(instance=order, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        
        else:
            return HttpResponse("error")
    
    except:
        return HttpResponse("Not found")

@api_view(["DELETE"])
def delete_order(request, pk):
    order = Order.objects.get(order_number=pk)
    ordered_products = order.ordered_products.all()
    items = OrderItem.objects.all()
    for item in ordered_products:
        if item in items:
            item.delete()
    order.delete()
    items = OrderItem.objects.all()
    return HttpResponse("deleted")



############################################# inserting special orders ##########################################################################
@api_view(["POST"])
@parser_classes([JSONParser, FormParser , MultiPartParser ])
def create_special_order(request):
    order_items_IDs = []
    last_order_item_id = 1
    last_order_number = 1
    quantity_ordered = float(request.data["quantityOrdered"])
    amount_ordered = float(request.data["amountOrdered"])

    try:
        last_order_number = OrderNotOnSite.objects.last().order_number
        last_order_number += 1
    except:
        last_order_number = 1

    user = UserModel.objects.get(id=request.data["customerId"])
    customer = Customer.objects.get(user=user)

    orderedItems = []
    
    numbers = [i for i in range(int(request.data["numberOfItems"]))]

    for i in numbers:
        item = {}
        name = "name_" + str(i)
        unit = "unit_" + str(i) 
        price = "price_" + str(i) 
        quantity = "quantity_" + str(i) 
        image = "image_" + str(i) 
        description = "description_" + str(i) 

        if name in request.data:
            item["name"] = request.data[name]
        
        if unit in request.data:
            item["unit"] = request.data[unit]
        
        if price in request.data:
            item["price"] = request.data[price]
        
        if quantity in request.data:
            item["quantity"] = request.data[quantity]
        
        if image in request.data:
            item["image"] = request.data[image]
        
        if description in request.data:
            item["description"] = request.data[description]
        
        orderedItems.append(item)


    for item in orderedItems:
        try:
            last_order_item_id = OrderNotOnSiteItem.objects.last().item_number
            last_order_item_id += 1
        except:
            last_order_item_id = 1

        order_item = OrderNotOnSiteItem(
            item_number=last_order_item_id,
            item_name=item["name"],
            image=item["image"],
            unit=item["unit"],
            quantity=item["quantity"],
            price=item["price"],
            description=item["description"],
        )
        order_item.save()
        order_items_IDs.append(order_item.item_number)

    
    order = OrderNotOnSite(
      customer=customer,
      order_number= last_order_number,
      quantity_ordered= quantity_ordered,
      amount_ordered= amount_ordered,
      country= request.data["country"],
      province= request.data["province"],
      email_address= request.data["email"],
      phone_number= request.data["phone"]
    )

    order.save()

    for order_item_id in order_items_IDs:
        order_item = OrderNotOnSiteItem.objects.get(item_number=order_item_id)
        order.ordered_products.add(order_item)
    
    # subject = "Receiving Special Order Confirmation"
    # message = f"""Dear {customer.user.first_name} {customer.user.last_name}, we have received your order and for any change on your order will be sent on this email\n
    # Thank you for choosing Kwetu Trade!"""
    # email_from = settings.EMAIL_HOST_USER
    # email_to = [order.email_address,]

    # send_mail(subject, message, email_from, email_to, fail_silently=True)

    
    return HttpResponse("ok done")


######################## Retrieving special orders #######################################
@api_view(["GET"])
def special_orders_list(request):
    orders = OrderNotOnSite.objects.all().order_by("-ordered_date")
    serializer = SpecialOrderSerializer(orders, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def special_order_detail(request, pk):

    try:
        order = OrderNotOnSite.objects.get(order_number=pk)
        order.set_newness_order_status()
        serializer = SpecialOrderSerializer(order, many=False)

        return Response(serializer.data)
    
    except:
        return HttpResponse("not found")


@api_view(["PUT"])
def update_special_order(request, pk):
    try:
        order=OrderNotOnSite.objects.get(order_number=pk)
        if request.data["order_status"] == "pending":
            order.out_of_delivery_date=None
            order.delivered_date=None
            order.rejected_date=None

            # subject = "Changing Special Order Status Confirmation"
            # message = f"""Dear {order.customer.user.first_name} {order.customer.user.last_name}, your order status has been changed to {request.data["order_status"]}\n
            # Thank you for choosing Kwetu Trade!"""
            # email_from = settings.EMAIL_HOST_USER
            # email_to = [order.email_address,]

            # send_mail(subject, message, email_from, email_to, fail_silently=True)

        elif request.data["order_status"] == "out for delivery":
            order.set_out_of_delivery_date()
            order.delivered_date=None
            order.rejected_date=None

            # subject = "Changing Special Order Status Confirmation"
            # message = f"""Dear {order.customer.user.first_name} {order.customer.user.last_name}, your order status has been changed to {request.data["order_status"]}\n
            # Thank you for choosing Kwetu Trade!"""
            # email_from = settings.EMAIL_HOST_USER
            # email_to = [order.email_address,]

            # send_mail(subject, message, email_from, email_to, fail_silently=True)

        elif request.data["order_status"] == "delivered":
            order.rejected_date=None
            order.set_delivered_date()

            # subject = "Changing Special Order Status Confirmation"
            # message = f"""Dear {order.customer.user.first_name} {order.customer.user.last_name}, your order status has been changed to {request.data["order_status"]}\n
            # Thank you for choosing Kwetu Trade!"""
            # email_from = settings.EMAIL_HOST_USER
            # email_to = [order.email_address,]

            # send_mail(subject, message, email_from, email_to, fail_silently=True)

        elif request.data["order_status"] == "rejected":
            order.set_rejected_date()
            order.out_of_delivery_date=None
            order.delivered_date=None
            
            # subject = "Changing Special Order Status Confirmation"
            # message = f"""Dear {order.customer.user.first_name} {order.customer.user.last_name}, your order status has been changed to {request.data["order_status"]}\n
            # Thank you for choosing Kwetu Trade!"""
            # email_from = settings.EMAIL_HOST_USER
            # email_to = [order.email_address,]

            # send_mail(subject, message, email_from, email_to, fail_silently=True)
        
        serializer = SpecialOrderSerializer(instance=order, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        
        else:
            return HttpResponse("error")
    
    except:
        return HttpResponse("Not found")


@api_view(["DELETE"])
def delete_special_order(request, pk):
    order = OrderNotOnSite.objects.get(order_number=pk)
    order.delete()

    return HttpResponse("deleted")


@api_view(["GET"])
def special_order_item(request, pk):
    item = OrderNotOnSiteItem.objects.get(item_number=pk)
    serializer = SpecialOrderItems(item, many=False)
    
    return Response(serializer.data)

####################################  adverts ###############################################

@api_view(["POST"])
@parser_classes([JSONParser, FormParser , MultiPartParser ])
def create_advert(request):
    
    serializer = AdvertSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response({"erros":serializers.errors})



@api_view(["PUT"])
def update_advert(request, pk):
    try:
        advert = Advert.objects.get(advert_number=pk)
        serializer = AdvertSerializer(instance=advert, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
   
        else:
            return Response({"erros":serializer.errors})
    
    except:
        return HttpResponse("Not found")


@api_view(["DELETE"])
def delete_advert(request, pk):
    try:
        advert = Advert.objects.get(advert_number=pk)
        advert.delete()
        return Response({"success": "deleted succesfully!"})

    except:
        return HttpResponse("Not found") 


@api_view(["GET"])
def adverts_list(request):
    adverts = Advert.objects.all().order_by("-uploaded_date")
    serializer = AdvertSerializer(adverts, many=True)
    return Response(serializer.data) 


@api_view(["GET"])
def advert_detail(request, pk):
    try:
        advert = Advert.objects.get(advert_number=pk)
        serializer = AdvertSerializer(advert, many=False)
        return Response(serializer.data)
    
    except:
        return HttpResponse("Not found") 


@api_view(["GET"])
def pubish_unpublish_advert(request, pk):
    try:
        advert = Advert.objects.get(advert_number=pk)
        if advert.published:
            advert.unpublish()
        else:
           advert.publish()

        adverts = Advert.objects.all().order_by("-uploaded_date")
        serializer = AdvertSerializer(adverts, many=True)
        return Response(serializer.data)

    except:
       return HttpResponse("Not found")  














       




    