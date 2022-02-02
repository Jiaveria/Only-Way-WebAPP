from ast import Pass
from decimal import Decimal
import imp
import secrets
from winreg import REG_QWORD
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render,get_object_or_404
from matplotlib import use
from scipy import rand
from .models import productDetails, purchasingHistory, userData
from django.contrib.auth.models import User, auth
from django.views.generic import DetailView, ListView
import random
from json import dumps

# Create your views here.
cart = []
cartObjectsPassedToTemplate = []
cartListForTotalPrice = []

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('market')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(username=email, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('market')
                messages.success(request, "Logged in")

            else:
                messages.warning(request, "Incorrect Username or Password")
                return render(request, 'login.html')
                

        else:
            return render(request, 'login.html')

def logoutUser(request):
    print(request.user.username)
    auth.logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    if request.user.is_authenticated:
        return redirect('market')
    else:
        if request.method == 'POST':
            firstNameFromForm = request.POST['firstname']
            lastNameFromForm = request.POST['lastname']
            emailFromForm = request.POST['email']
            passwordFromForm = request.POST['password']
            phoneFromForm = request.POST['phone']

            if userData.objects.filter(email=emailFromForm).exists():
                messages.warning(request, "Email already exists")
                return render(request, 'signup.html')

            else:
                newUser = userData(firstName=firstNameFromForm, lastName=lastNameFromForm, email=emailFromForm, password=passwordFromForm, phone=phoneFromForm)
                newUser.save()
                createUser = User.objects.create_user(username=emailFromForm ,email=emailFromForm, password=passwordFromForm)       
                user = auth.authenticate(
                    username=emailFromForm, password=passwordFromForm)
                auth.login(request, user)
                return HttpResponseRedirect('market')

        else:
            return render(request, 'signup.html')



class productsMarket(ListView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('loginUser')

        return super().dispatch(request, *args, **kwargs)
    model = productDetails
    template_name = 'market.html'
    items = productDetails.objects.filter(inStock=True)
    extra_context = {'items': items}



class productDetailView(DetailView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('loginUser')
        return super().dispatch(request, *args, **kwargs)
    model = productDetails
    template_name = 'product.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'
    allProducts = productDetails.objects.filter(inStock=True)
    randomProducts = []
    randomList = []
    for i in range(10):
        if len(randomList) == 4:
            break
        # else:
        #     pass
        #     r = random.randint(0, len(allProducts)-1)
        #     if r not in randomList:
        #         randomList.append(r)
    #print('randome List', randomList)
    # for i in range(4):
    #     randomProducts.append(allProducts[randomList[i]])
    # print(randomProducts[0], randomProducts[1], randomProducts[2],randomProducts[3])
    extra_context = {'randomProducts': randomProducts}



def add_to_cart(request,id):
    if request.user.is_authenticated:
        slug_field = id
        slug_url_kwarg = id
        #[product, quantity, user]
        addedProduct = get_object_or_404(productDetails, id=id)
        for item in cart:
            if item[0].name == addedProduct.name and request.user.username == item [2]:
                item[1] += 1
                print(addedProduct.name+" added to cart with quantity", str(item[1]))
                break
        else:
            cart.append([addedProduct, 1 , request.user.username])
            print("new item",addedProduct.name+" added to cart with quantity", str(cart[len(cart)-1][1]))
        messages.info(request, "Item added to cart")
        return redirect("product", id=id)
    else:
        return redirect('loginUser')


def remove_from_cart(request, id):
    if request.user.is_authenticated:
        slug_field = id
        slug_url_kwarg = id
        #[product, quantity, user]
        addedProduct = get_object_or_404(productDetails, id=id)
        for item in cart:
            if item[0].name == addedProduct.name and request.user.username == item[2]:
                cart.remove(item)
                print('removed')
                messages.warning(request, "Item removed from cart")
                break
        else:
            print('item not present')
            #messages.warning(request, "Item not present in carrt")
            return redirect("cartPage")
        # return redirect("product", id=id)
        return HttpResponseRedirect('cartPage')
    else:
        return redirect('loginUser')

    
def cartPage(request):
    if request.user.is_authenticated:
        totalPrice=0
        if request.method == 'POST':
            # copyOfcartObjectList = cartObjectList
            for productIncart in cartObjectsPassedToTemplate:
                print(productIncart)
                if productIncart.username == request.user.username:
                    print('modifying quantity')
                    modifiedQuantityOfProduct = int(request.POST[str(productIncart.item.id)])
                    if modifiedQuantityOfProduct == 0 or modifiedQuantityOfProduct > productIncart.item.quantity:
                        cart.remove(
                            [productIncart.item, productIncart.itemQuantity, request.user.username])
                        print('removed from cart')

                    else:
                        #modifiedQuantityOfProduct=productIncart.item.quantity
                        newTransaction = purchasingHistory(productId=productIncart.item.id,
                        username=request.user.username, priceOfOneUnit=productIncart.item.price,
                        quantityOfProduct=modifiedQuantityOfProduct)
                        newTransaction.save()
                        product = productDetails.objects.get(
                            id=productIncart.item.id)
                        product.quantity -= modifiedQuantityOfProduct
                        if product.quantity == 0:
                            product.inStock = False
                        product.save()

                        print('saved Transaction')
                        
                        cart.remove([productIncart.item, productIncart.itemQuantity, request.user.username])
            cartObjectsPassedToTemplate.clear()
            messages.success(request,'Order Placed. You will be called shortly.')
            return HttpResponseRedirect('market')
        else:
            cartObjectsPassedToTemplate.clear()
            cartListForTotalPrice = []
            for item in cart:
                if request.user.username == item[2]:
                    cartObjectsPassedToTemplate.append(
                        cartObject(item[0], item[1], item[2]))
                    totalPrice += item[0].price*Decimal(item[1])
                    print(item[1])
                    cartListForTotalPrice.append(
                        [item[0].id, int(item[0].price), item[1]]
                    )
            cartListForTotalPrice = dumps(cartListForTotalPrice)
            return render(request, 'cartTemplate.html', {'cartObjectList': cartObjectsPassedToTemplate,
            'totalPrice': totalPrice,
            'totalObjects':len(cartObjectsPassedToTemplate),
            'cartListForTotalPrice': cartListForTotalPrice})
    else:
        return HttpResponseRedirect('loginUser')

class cartObject:
    def __init__(self, a,b,c):
        self.item = a
        self.itemQuantity = b
        self.username = c
    
    