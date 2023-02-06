from django.views import View
from django.shortcuts import render
from store.models import Product,Customer

class DetailView(View):
    template_name = 'details.html'

    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        if 'customer' in request.session:
            customer = Customer.objects.get(id=request.session['customer'])
        else: customer = None
        
        ctx = {
            'product': product,
            'customer': customer
        }
        
        return render(request, self.template_name, ctx)