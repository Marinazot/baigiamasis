
from django.db import models
from django.urls import reverse 
import uuid
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField
from PIL import Image




class Preke(models.Model):
    pavadinimas = models.CharField('Pavadinimas', max_length=200, help_text='Išrinkite prekes tipa(pvz. Batai)')

    def __str__(self):
        return self.pavadinimas
    
    class Meta:
        verbose_name = 'Prekė'
        verbose_name_plural = 'Prekes'

# Create your models here.

class Product(models.Model):
    title = models.CharField('Pavadinimas', max_length=200)
    gamintojas = models.ForeignKey('Gamintojas', on_delete=models.SET_NULL, null=True, related_name='products')
    summary = HTMLField('Aprašymas')
    code =  models.CharField('Prekes kodas', max_length=25, null=True )
    cover = models.ImageField('Nuotrauka', upload_to='covers', null=True)
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Simbolių <a href="https://www.isbn-international.org/content/what-isbn">ISBN kodas</a>')
    preke = models.ManyToManyField(Preke,  help_text='Išrinkite tipa šiai prekei')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])
    
    class Meta:
        verbose_name = 'Produktas'
        verbose_name_plural = 'Produktai'
    
    def display_preke(self):
        return ',' .join(preke.pavadinimas for preke in self.preke.all()[:4])
    
    display_preke.prekeshort_discription = 'Produktas'  #!!!!!?????

    
class ProductInstance(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, help_text='Unikalus ID')
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='instances') 
    size = models.CharField('Dydis',max_length=10)
    due_back = models.DateField('Numatytas gavymas', null=True, blank=True)
    ser_number = models.CharField('Serijos numeris', max_length=25, null=True )
    quantity = models.IntegerField('Kiekis', default=0)
    vartotojas = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    

    LOAN_STATUS = (
        ('a', 'Atvyksta'),
        ('p', 'Parduota'),
        ('r', 'Rezervuota'),
        ('l', 'Likutis'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='l',
        help_text='Statusas',
    )

    @property
    def is_overdue(self):
        if set.due_back and date.today() > self.due_back:
            return True
        return False
    

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_add", "Leisti pridėti prekes"),)
        

    def __str__(self):
        return f'{self.id} ({self.product})'
    
    class Meta:
        verbose_name = 'Produkto lentelė'
        verbose_name_plural = 'Produktų lentelė'
        
def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])


class Gamintojas(models.Model):
    
    company_name = models.CharField('Gamintojo pavadinimas', max_length=100)
    company_country = models.CharField('Kilmės šalis', max_length=100, null=True)
    description = HTMLField("Aprasymas", max_length=2000, default='')

    class Meta:
        ordering = ['company_name', 'company_country']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.company_name} {self.company_country}' 

    class Meta:
        verbose_name = 'Gamintojas'
        verbose_name_plural = 'Ganintojai'

    def display_products(self):
        return ', '.join(product.title for product in self.products.all()[:4])
    
    display_products.short_discription = 'Produktai'



class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"
    
    class Meta:
        verbose_name = 'Profilis'
        verbose_name_plural = 'profiliai'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)    


