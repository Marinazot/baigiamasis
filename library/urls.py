

from django.urls import path, include
from django.conf.urls.static import static

# from django.conf import settings
from . import views


from . import views

urlpatterns = [
   
    path('', views.index, name='index'),
    path('gamintojai/', views.gamintojai, name='gamintojai'),
    path('gamintojas/<int:gamintojas_id>', views.gamintojas, name='gamintojas'),
    path('products/', views.product_list, name='products'),
    path('products/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('search/', views.search, name='search'),
    path('my_products/', views.LoanedProductsByUserListView.as_view(), name='my-borrowed'),
    path('register/', views.register, name='register'),
    path('profilis/', views.profilis, name='profilis'),
    path('my_products/<uuid:pk>', views.ProductByUserDetailView.as_view(), name='my-product'),
    path('my_products/new', views.ProductByUserCreateView.as_view(), name='my-borrowed-new'),

] 
urlpatterns += [
    
    path('accounts/', include('django.contrib.auth.urls')),
    
] 