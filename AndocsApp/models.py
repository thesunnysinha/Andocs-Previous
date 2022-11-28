from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
import numpy as np
from django.db.models.signals import post_save
from django.dispatch import receiver

STATE_CHOICES = (
    ('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
    ('Andhra Pradesh','Andhra Pradesh',),
    ('Arunachal Pradesh','Arunachal Pradesh',), 
    ('Assam','Assam'), 
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh',),
    ('Chhattisgarh','Chhattisgarh'),
    ('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
    ('Daman & Diu','Daman & Diu'),
    ('Delhi','Delhi'),  
    ('Goa','Goa'), 
    ('Gujarat','Gujarat'), 
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'), 
    ('Jammu & Kashmir','Jammu & Kashmir'),
    ('Jharkhand','Jharkhand'), 
    ('Karnataka','Karnataka'), 
    ('Kerala','Kerala'),
    ('Ladakh','Ladakh'),
    ('Lakshadweep','Lakshadweep'), 
    ('Madhya Pradesh','Madhya Pradesh'), 
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Orissa','Orissa'),
    ('Puducherry','Puducherry'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Tripura','Tripura'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('Uttarakhand','Uttarakhand'),
    ('West Bengal','West Bengal'),
    ('Telangana','Telangana'),
)

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=50)
    mobile_number = models.CharField(max_length=10)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES = (
    ('C','Cosmetics'),
    ('PP','Pet Products')
)
COUNTRY_CHOICES = (
    ('NP','Nepal'),
    ('IN','India'),
    ("BT",'Both'),
)

SUBCATEGORY_CHOICES = (
    ("FW",'Face Wash'),
    ("PU","Pet Utensils"),
    ("N","None"),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    country = models.CharField(choices=COUNTRY_CHOICES,max_length=2,default="Both")
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    sub_category = models.CharField(choices=SUBCATEGORY_CHOICES,max_length=2,default="None")
    product_image = models.ImageField(upload_to='productimg')

    @property
    def get_discount_percent(self):
        percent = (self.selling_price-self.discounted_price)/self.selling_price*100
        return percent

    def average_rating(self):
        all_ratings = list(map(lambda x: x.rating, self.review_set.all()))
        return np.mean(all_ratings)

    def __str__(self):
        return str(self.id)



STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ("On The Way",'On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True,blank=True)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Accepted')
    transaction_id = models.CharField(max_length=200,null=True,default=1)

    @property
    def get_total(self):
        total = self.product.discounted_price * self.quantity
        return total

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(OrderPlaced,on_delete=models.SET_NULL,null=True)
    quantity = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True,blank=True)

    @property
    def get_total(self):
        total = self.product.discounted_price * self.quantity
        return total
    @property
    def get_discount_percent(self):
        percent = (self.product.selling_price-self.product.discounted_price)/self.product.selling_price*100
        return percent

    def __str__(self):
        return str(self.id)


class UserOtp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_st = models.DateTimeField(auto_now=True)
    otp = models.SmallIntegerField()
    

GENDER_CHOICES = (
    ('Male','Male'),
    ('Female','Female'),
    ('Prefer Not to Say','Prefer Not to Say'),
)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_num = models.CharField(max_length=10)
    gender = models.CharField(max_length=50,choices=GENDER_CHOICES)
    profile_pic = models.ImageField(null=True,blank = True,upload_to='profilepic')
    birth_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
@receiver(post_save, sender=User)
def update_user_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(OrderPlaced,on_delete=models.SET_NULL,null=True)
    quantity = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True,blank=True)

    @property
    def get_total(self):
        total = self.product.discounted_price * self.quantity
        return total
    @property
    def get_discount_percent(self):
        percent = (self.product.selling_price-self.product.discounted_price)/self.product.selling_price*100
        return percent

    def __str__(self):
        return str(self.id)

class Comment(models.Model):
    STATUS = {
        ('New','New'),
        ('True','True'),
        ('False','False'),
    }
    RATINGS = {
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5'),
        
    }
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="review_set")
    user_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=50,blank=True)
    comment = models.CharField(max_length=250,blank=True)
    rating = models.IntegerField(choices=RATINGS, default="1")
    ip = models.CharField(max_length=20,blank=True)
    status = models.CharField(max_length=10,choices=STATUS,default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class Cluster(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def get_members(self):
        return "\n".join([u.username for u in self.users.all()])