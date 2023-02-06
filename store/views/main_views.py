from django.shortcuts import render
from django.views import View
from store.models import Product, Category, Customer

class Index(View):
    template_name = 'index.html'
    
    def get(self, request):
        if 'customer' in request.session:
            customer = Customer.objects.get(id=request.session['customer'])
        else: customer = None
        products = Product.get_all_products().order_by('name')[:10]
        categories = Category.objects.all()
        ctx = {
            'products': products,
            'categories': categories,
            'customer': customer,
            'show_search': True
        }
        if 'alert_message' in request.session:
            ctx['alert_message'] = request.session['alert_message']
            del request.session['alert_message']
        
        return render(request, self.template_name, ctx)

class ProductsDisplay(View):
    template_name = 'index.html'

    def get(self, request):
        if 'customer' in request.session:
            customer = Customer.objects.get(id=request.session['customer'])
        else: customer = None

        if request.GET.get('category'):
            products = Product.objects.filter(category=request.GET.get('category')).order_by('name')
        elif request.GET.get('q'):
            products = Product.objects.filter(prompt__contains=request.GET.get('q'))
        else:
            products = Product.objects.all()

        categories = Category.objects.all()
        ctx = {
            'products': products,
            'categories': categories,
            'customer': customer,
            'show_search': True
        }

        return render(request, self.template_name, ctx)