
# from django.contrib import admin
from django.urls import path, include
# from views import register


from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('gamintojai/', views.gamintojai, name='gamintojai'),
    path('gamintojas/<int:gamintojas_id>', views.gamintojas, name='gamintojas'),
    path('products/', views.product_list, name='products'),
    path('products/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('search/', views.search, name='search')
]

urlpatterns += [
    # path('register/', register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    
]