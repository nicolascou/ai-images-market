from django.views import View
from django.shortcuts import render, redirect
from store.models import Customer

class InventoryView(View):
    template_name = 'inventory.html'

    def get(self, request):
        if 'customer' in request.session:
            customer = Customer.objects.get(id=request.session['customer'])
            inventory = customer.inventory.all()
        else: 
            request.session['alert_message'] = "You are not logged in"
            return redirect('store:home')

        ctx = {
            'customer': customer,
            'inventory': inventory
        }
        
        return render(request, self.template_name, ctx)


def account(request):
    if 'customer' in request.session:
        customer = Customer.objects.get(id=request.session['customer'])
    else: return redirect('store:home')

    ctx = {
        'customer': customer
    }

    return render(request, 'account.html', ctx)