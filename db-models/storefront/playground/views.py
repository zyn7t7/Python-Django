from django.shortcuts import render
from django.db.models import  Q , F  #Q is short form of query ,using this class we can represent a query expression or a piece of code produces a value, using this class we can calculate a keyword argument
from django.http import HttpResponse #F class is used to reference a particular field
from django.db.models.aggregates import Count,Max,Min,Avg,Sum
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Value
from django.db.models import Func
from django.db.models.functions import Concat
from django.db.models import ExpressionWrapper
from django.db import transaction, connection
from django.contrib.contenttypes.models import ContentType
from store.models import Product
from tags.models import TaggedItem
from store.models import Product,OrderItem, Customer, Collection ,Order
from django.forms import DecimalField

def say_hello(request):
    
    #########geting data by using filters #############
    #########################
    # product = Product.objects.filter(pk=0).first()
    
    # exists = Product.objects.filter(pk=0).exists()
    
    # try:
    #     product = Product.objects.get(pk=0)
    # except ObjectDoesNotExist:
    #     pass
    
    # product = Product.objects.get(pk=0)
    #########################
    
    ########################
    #keyword = value
    # queryset = Product.objects.filter(unit_price__range=(20,  30))
    # queryset = Product.objects.filter(collection__id__range=(1,2,3))
    # queryset = Product.objects.filter(title__icontains='coffee')
    # queryset = Product.objects.filter(title__startswith='coffee')
    # queryset = Product.objects.filter(last_update__year=2021)
    # queryset = Product.objects.filter(description__isnull=True)
    # queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    ##########################
    
    #Products: inventory < 10 OR price < 20
    ###########  showing AND operator in django debug tool
    # queryset = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    #same step with import Q ##Products: inventory < 10 OR price <20
    # queryset = Product.objects.filter(                               #this Q object translate logical expression into sql query
        # Q(inventory__lt=10) | Q(unit_price__lt=20))
        # Q(inventory__lt=10) & Q(unit_price__lt=20))
        # Q(inventory__lt=10) & ~Q(unit_price__lt=20))
    
    ##############################
    #Products: inventory = price
    # queryset = Product.objects.filter(inventory = F('unit_price')) #no results shown but it try to select class named unit_price 
    # queryset = Product.objects.filter(inventory = F('collection__id'))  #shows results of from table named collection_id
    ##############################
    
    #######SORTING DATA###########
    # queryset = Product.objects.order_by('title')  #shows data in ascending order
    # queryset = Product.objects.order_by('-title') #shows data in descending orfder
    # queryset = Product.objects.order_by('unit_price','-title')  #shows data with unit_price and title in descending order cheapest and most expensive
    # queryset = Product.objects.order_by('unit_price','-title').reverse() #this will reverse the direction of the sort shows result in unit_price-descending order and title-ascending order
   
    # return render(request, 'hello.html',{'name': 'Zayn','products':list(queryset)})
    ########
    #USING FILTER+SORTING
    # queryset = Product.objects.filter(collection__id=1).order_by('unit_price')        #NA
    # product = Product.objects.order_by('unit_price')[0]     #by this we will get an actual object so name of variable quesyset has been changed into product
    # product = Product.objects.earliest('unit_price')    #same step as above but order_by returns a queryset and ealiest returns an object
    # product = Product.objects.latest('unit_price')    #sorts the product by unit price in descending order and then return the first object
    # return render(request, 'hello.html',{'name': 'Zayn','products':product})
    ################################
    
    #########LIMITING RESULTS###############
    # queryset = Product.objects.all()[:5]   #show results from 0 to 4
    # queryset = Product.objects.all()[5:10]   #show results from 5 to 9
    # return render(request, 'hello.html',{'name': 'Zayn','products':list(queryset)})       #change the product.title in hello.html into product
    #########################################
    
    #######SELECTING FIELDS TO QUERY###########
    # queryset = Product.objects.all()
    # queryset = Product.objects.values('id','title')     #only show these two fields
    # queryset = Product.objects.values('id','title', 'collection__title')     #__ for accessing related fieldd it will show two fiels from prduct table and one field form collection table
    # queryset = Product.objects.values_list('id','title', 'collection__title')     #shows the same result in touple form the previous one is in dictionary form
    
    # return render(request, 'hello.html',{'name': 'Zayn','products':list(queryset)})   #change the product.title in hello.html into product
    #############################################
    #TASK
    # queryset = OrderItem.objects.values('product_id')   #selecting products_id from orderitem/table
    # queryset = OrderItem.objects.values('product_id').distinct()   #for not showing duplicate items
    ########
    # Product.objects.filter(id__in= )            #usnig in lookup type to select all products that id in the given list
    # queryset = OrderItem.objects.values('product_id').distinct()      #for not showing duplicate items
    # queryset = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct())            #show all products that have been ordered
    # queryset = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')          #sortec with title
    # return render(request, 'hello.html',{'name': 'Zayn','products':list(queryset)})  #change the product in hello.html into product.title
    ################################################
    
    ################ DIFFERING FIELDS ###############
    # queryset = Product.objects.only('id','title')            #with only() we will get instance of product class and with value we will get dictionary object 
    # queryset = Product.objects.only('id','title')     #LOAD WEBSITE       #also add {product_price } in hello.html
    ### OPPOSITE OF ONLY METHOD ###
    # queryset = Product.objects.defer('description')    #THIS WILL NOT BE SHOWN #ALSO ADD {product.description}
    # return render(request, 'hello.html',{'name': 'Zayn','products':list(queryset)})  #change the product in hello.html into product.title
    ##################################################
       
    ################# AGGREGATE #######################
    # Product.objects.aggregate(Count('description'))  #show the nmbr of products that have description #NA
    # result = Product.objects.aggregate(Count('id'))       #show the total nmber of products
    # result = Product.objects.aggregate(
        # count = Count('id') , min_price=Min('unit_price')) 
    # return render(request, 'hello.html',{'name': 'Zayn' , 'result': result})  #add results in hello.html
    #####################################################
    
    ################# ANNOTATING OBJECTS ################
    # WHEN WE WANT TO ADD SOME ATTRIBUTES OR OBJECTS WHILE QUERING
    
    # queryset = Customer.objects.annotate(is_new=Value(True))    #make a new column named as is_new
    # queryset = Customer.objects.annotate(is_new=F('id'))    #referencing the id field
    # queryset = Customer.objects.annotate(is_new=F('id') + 1)    #we can also perform computations
    # return render(request, 'hello.html',{'name': 'Zayn' , 'result':list(queryset)})  
    ######################################################
    
    ################## CALLING DATABASE FUNCTION ##########
    ################  CONCATINATION ##############  
    # queryset = Customer.objects.annotate(
    #     #CONCAT
    #     full_name = Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')
    # )
    
    ##### SAME STEP WITH CONCAT FUNCTION ######
    
    # queryset = Customer.objects.annotate(
    #     #CONCAT
    #     full_name = Concat('first_name', Value(' '), 'last_name')
    # )    
    # return render(request, 'hello.html',{'name': 'Zayn' , 'result':list(queryset)})    
    #################################################
    
    ##### COUNTING NUMBER OF ORDERS OF EACH CUSTOMER ##
    # queryset = Customer.objects.annotate(
    #     orders_count=Count('order')
    # )
    
    # return render(request, 'hello.html',{'name': 'Zayn' , 'result':list(queryset)})  
    ####################################################
    
    ########## WORKING WITH EXPRESSION ######
    # queryset = Product.objects.annotate(discounted_price=F('unit_price') * 0.8)     #using expression wrapper #Error 
    #######
    # discounted_price = ExpressionWrapper(
    #     F('unit_price') * 0.8, output_field=DecimalField())
    # queryset = Product.objects.annotate(
    #     discounted_price=discounted_price
    # )
    # return render(request, 'hello.html',{'name': 'Zayn' , 'result':list(queryset)})  
    #######################################################
    
    ########### QUERYING GENERIC RELATIONSHIPS #############
    # content_type = ContentType.objects.get_for_model(Product)        #ContentType manager has a special method called get_for_model()   hmne product ko ContentType k zrye get kiya which is ganeric or ContentType is an another field in the taggeditem model
    # queryset = TaggedItem.objects.select_related('tag').filter(content_type = content_type, object_id = 1)   # 'select_related' to preload the tag field ,tag_id = froeignkey to the tag model      (object = 1 )id of the product that u want to query ,   this will return a bunch of tagged items product
    # return render(request, 'hello.html',{'name': 'Zayn' , 'result':list(queryset)})  
    ########################################################
     
     ################### CUSTOM MANAGER #################### 
    # content_type = ContentType.objects.get_for_model(Product)
            
    # queryset = TaggedItem.objects \
    #     .select_related('tag')  \
    #     .filter(
    #         content_type = content_type,
    #         object_id = 1
    #     )        
    # return render(request, 'hello.html',{'name': 'Zayn' , 'result':list(queryset)})
    #############
    # TaggedItem.objects.get_tags_for(Product, 1)     #new custom made method to get object in tags.models 
   ##############
   
    ### CUT THE BELOW CODE ## AND PASTE ON tags.models.taggedItemManager ######
    #########
    # content_type = ContentType.objects.get_for_model(Product)
            
    # queryset = TaggedItem.objects \
    #     .select_related('tag')  \
    #     .filter(
    #         content_type = content_type,
    #         object_id = 1
    #     ) 
    ##########
    ##########################################################
    
    ########## INSERTING DATA TO DATABASE ###########
    # collection = Collection()
    # collection.title = 'Video Games'
    # collection.featured_product = Product(pk=1)
    #######
    # collection.featured_product_id = 1
    #######
    # collection = Collection(title='Video Gamed')
    #######
    # collection = Collection()
    # collection.title = 'Video Games'
    # collection.featured_product = Product(pk=1)
    # collection.save()
    ########
    # collection = Collection.objects.create(name ='a',featured_product_id =1)
    
    # return render(request,'hello.html',{'name':'Zain'})
    #####################################################
    
    ############# UPDATING OBJECTS ######################
    # collection = Collection(pk=11)
    # collection.title = 'Games'
    # collection.featured_product = None
    # collection.save()
    ###title changes###
    ####################
    # collection = Collection(pk=11)
    # collection.featured_product = None
    # collection.save()
    ### showing title = ""      #an empty string
    #####################
    # collection = Collection.objects.get(pk=11)
    # collection.featured_product = None
    # collection.save()
    #####ANOTHER METHOD#####
    # collection.objects.update(featured_product = None)
    # Collection.objects.filter(pk=11).update(featured_product=None)
    # return render(request,'hello.html',{'name':'Zain'})
    #########################################################
    
    ############### DELETING OBJECTS ##################
    # collection = Collection(pk = 11)
    # collection.delete() 
        
    # Collection.objects.filter(id__gt=5).delete()
    
    # return render(request,'hello.html',{'name':'Zain'})
    ####################################################
    
    ################## TRANSACTION #####################
    ## always create a child record before parent record ##
    # order = Order()
    # order.customer_id = 1
    # order.save()
    
    # item = OrderItem()
    # item.order = order
    # item.product_id = 1
    # item.quantity = 1
    # item.unit_price = 10
    # item.save()
    # Cause error bcz order can be placed before item 
    ## transaction....
    # @transaction.atomic()     should be placed before view or ..
    # with transaction.atomic():
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()

    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = -1
    #     item.quantity = 1
    #     item.unit_price = 10
    #     item.save()
    # return render(request,'hello.html',{'name':'Zain'})
    ################################################# 
    
    ######### EXECUTING RAW SQL QUERY ##############
    # Product.objects.raw('select * from store_product')
    # we dont need to do use filters etc
    # queryset = Product.objects.raw('select * from store_product')
    # queryset = Product.objects.raw('select id,title from store_product')
    ######### another method ###
    # cursor = connection.cursor()
    # cursor.execute('SELECT')
    # cursor.execute('INSERT')
    # cursor.close()
    #####
    # with connection.cursor() as cursor:
        # cursor.execute()
    #####
    # with connection.cursor() as cursor:
    #     cursor.callproc('get_customers',[1,2,'a'])
    # return render(request,'hello.html',{'name':'Zain','result':list(queryset)})
    ##################################################
    
    return render(request,'hello.html',{'name':'Zain'})

