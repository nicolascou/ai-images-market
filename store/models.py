from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    prompt = models.CharField(max_length=250)
    image = models.ImageField(upload_to='store/uploads/')

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)
    
    @staticmethod
    def get_all_products():
        return Product.objects.all()

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    coins = models.IntegerField(default=1000)
    inventory = models.ManyToManyField(Product)
    is_active = models.BooleanField(default=False)

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return None
    
    def exists_with_email(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False

    def __str__(self):
        return self.name + self.last_name

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product)

    def __str__(self):
        return f'{self.customer} - {self.items}'