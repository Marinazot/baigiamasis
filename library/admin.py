from django.contrib import admin
from .models import Preke, Product, ProductInstance, Gamintojas

# Register your models here.
class ProductsInstanceInline(admin.TabularInline):
    model = ProductInstance
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'gamintojas', 'display_preke')
    inlines = [ProductsInstanceInline]


class ProductInstanceAdmin(admin.ModelAdmin):
    list_display = ('product', 'status', 'due_back')
    list_filter = ('status', 'due_back')

    fieldsets = (
        ('General', {'fields': ('id', 'product')}),
        ('Availability', {'fields':('status', 'due_back','size', 'quantity')})
        )
    
    search_fields = ('id', 'product__id') #?????
    

    
class GamintojasAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'company_country','display_products')
   


admin.site.register(Preke)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductInstance, ProductInstanceAdmin)
admin.site.register(Gamintojas, GamintojasAdmin)
