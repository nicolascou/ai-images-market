from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from store.views.form_views import Signup, Login, logout, ActivateView
from store.views.main_views import Index, ProductsDisplay
from store.views.details_view import DetailView
from store.views.cart_views import CartView, add_to_cart, remove_from_cart
from store.views.inventory_views import InventoryView, account

app_name = 'store'
urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('products/', ProductsDisplay.as_view(), name='products'),
    path('details/<int:pk>/', DetailView.as_view(), name='details'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<uid>/<product_id>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<uid>/<product_id>/', remove_from_cart, name='remove-from-cart'),
    path('inventory/', InventoryView.as_view(), name='inventory'),
    path('account/', account, name='account'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
