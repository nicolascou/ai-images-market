from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Cart, Customer

class CartView(View):
    template_name = 'cart.html'
    
    def get(self, request):
        if 'customer' in request.session:
            customer = Customer.objects.get(id=request.session['customer'])
        else:
            request.session['alert_message'] = 'You are not logged in'
            return redirect('store:home')

        cart, created = Cart.objects.get_or_create(customer=customer)
        products = cart.items.all()
        total_price = 0
        for product in products:
            total_price += product.price
        last_coins = customer.coins - total_price

        ctx = {
            'customer': customer,
            'products': products,
            'total_price': total_price,
            'last_coins': last_coins
        }

        return render(request, self.template_name, ctx)

    def post(self, request):
        if 'customer' in request.session:
            customer = Customer.objects.get(id=request.session['customer'])
        else:
            return redirect('store:cart')
        
        cart = Cart.objects.get(customer=customer)

        total_price = 0
        for product in cart.items.all():
            customer.inventory.add(product)
            total_price += product.price
        customer.coins -= total_price
        customer.save()
        cart.items.clear()

        return redirect('store:home')

def add_to_cart(request, uid, product_id):
    customer = get_object_or_404(Customer, id=uid)
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(customer=customer)
    cart.items.add(product)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def remove_from_cart(request, uid, product_id):
    customer = get_object_or_404(Customer, id=uid)
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(customer=customer)
    cart.items.remove(product)
    return redirect('store:cart')
