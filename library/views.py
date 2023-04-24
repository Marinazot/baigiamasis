from django.shortcuts import render, get_object_or_404, redirect
from .models import Preke, Product, ProductInstance, Gamintojas
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.


def index(request):
    num_products = Product.objects.all().count()
    num_instances = ProductInstance.objects.all().count()

    num_instances_available = ProductInstance.objects.filter(status__exact='l').count()
    num_gamintojai = Gamintojas.objects.all().count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_products': num_products,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_gamintojai': num_gamintojai,
        'num_visits': num_visits
    }  

    return render(request, 'index.html', context=context)

def gamintojai(request):
    paginator = Paginator(Gamintojas.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_gamintojai = paginator.get_page(page_number)
    # gamintojai = Gamintojas.objects.all() nebereikia
    context = {
        'gamintojai': paged_gamintojai
        }
    return render(request, 'gamintojai.html', context=context)

def gamintojas(request, gamintojas_id):
    single_gamintojas = get_object_or_404(Gamintojas, pk=gamintojas_id)
    return render(request, 'gamintojas.html', {'gamintojas': single_gamintojas})


def search(request):
    query = request.GET.get('query')
    search_results = Product.objects.filter(Q(title__icontains=query) | Q(summary__icontains=query) | Q(gamintojas__company_name__icontains=query))
    return render(request, 'search.html', {'products': search_results, 'query': query})


def product_list(request):
    paginator = Paginator(Product.objects.all(), 8)
    page_number = request.GET.get('page')
    paged_product = paginator.get_page(page_number)
    context = {
        'products': paged_product}
    return render(request, 'product_list.html', context=context)

# class ProductListView(generic.ListView):
#     model = Product
#     context_object_name = 'products'
#     paginate_by = 5
#     # queryset = Product.objects.filter(title__icontains='') galima sudaryti  pajieska pagal  savo  salygas
#     template_name = "product_list.html"

    # def get_queryset(self):
    #     return Product.objects.filter(title__icontains='b')  irgi  atlike  paieska  pagal  salygas

    # def get_context_data(self, **kwargs): 
    #     context = super(ProductListView, self ).get_context_data(**kwargs)
    #     context['duomenys'] = 'duomenys kazkokie'
    #     return context

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "product_detail.html"
