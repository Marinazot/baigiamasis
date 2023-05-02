from django.contrib import admin
from .models import Preke, Product, ProductInstance, Gamintojas, Profilis

# Register your models here.
class ProductsInstanceInline(admin.TabularInline):
    model = ProductInstance
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'gamintojas', 'display_preke')
    inlines = [ProductsInstanceInline]


class ProductInstanceAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'status', 'due_back', 'vartotojas', 'quantity')
    # list_editable = ('status', 'due_back')
    list_filter = ('status', 'due_back')
    # search_fields = ('product__title', 'id')

    fieldsets = (
        (None, {
            'fields': ( 'product',)}),
        ('Availability',{
          'fields':('status', 'due_back','size', 'quantity', 'vartotojas')})
        )
    
    

    
class GamintojasAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'company_country','display_products')
   


admin.site.register(Preke)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductInstance, ProductInstanceAdmin)
admin.site.register(Gamintojas, GamintojasAdmin)
admin.site.register(Profilis)
