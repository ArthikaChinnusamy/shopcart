from django.db import  models
import datetime
import os  #---------

from django.contrib.auth.models import User

# from django.utils.text import slugify

def getFileName(request,filename):  #----------
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%H:%M:%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('uploads/',new_filename)
 
# Create your models here.
class Catagory(models.Model):
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    description=models.CharField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default='False',help_text='0-show,1-Hidden')
    created_at=models.DateTimeField(auto_now_add=True)

    # slug = models.SlugField(unique=True, blank=True, null=True)  # Add this


    # def save(self, *args, **kwargs):
    #     if not self.slug:  # Auto-generate slug if empty
    #         self.slug = self.name.replace(" ", "-").lower()
    #     super().save(*args, **kwargs)

    # slug = models.SlugField(blank=True, null=True)  # No unique constraint


    def __str__(self):  #----------
        return self.name
    
class Product(models.Model):
    catagory=models.ForeignKey(Catagory,on_delete=models.CASCADE)
    name=models.CharField(max_length=150,null=False,blank=False)
    vendor=models.CharField(max_length=150,null=False,blank=False) 
    product_image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    quantity=models.IntegerField(null=False,blank=False)
    original_price=models.FloatField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)

    description=models.CharField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default='False',help_text='0-show,1-Hidden')
    trending=models.BooleanField(default='False',help_text='0-default,1-Trending')
    created_at=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True) 

    # def __str__(self):
    #     return f"{self.user.username} - {self.product.name} ({self.product_qty})"

    @property
    def total_cost(self):
        return self.product_qty*self.product.selling_price