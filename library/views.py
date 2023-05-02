from typing import Any, Dict, Optional
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Preke, Product, ProductInstance, Gamintojas
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfilisUpdateForm
from django.views.generic import ListView, DetailView, CreateView
from django.db import models

from .models import Product

# Create your views here.
@login_required
# @permission_required('app.can_input_data', raise_exception=True)
# def input_data(request):
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profilis.html', context)




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

@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
#             # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else: # jeigu passwordai Nesutampa
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')

def gamintojai(request):
    paginator = Paginator(Gamintojas.objects.all(), 4)
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
    # if request.method == "POST":
    #     pi = ProductInstance( 
            
    #         size = request.POST['size'],
    #         quantity = request.POST['quantity'],
    #         due_back = request.POST['due_back']
    #     )
        
    #     return redirect('index')

    # print(ProductInstance.objects.all())
     
    paginator = Paginator(Product.objects.all(), 6)
    page_number = request.GET.get('page')
    paged_product = paginator.get_page(page_number)
    context = {
        'products': paged_product}
    return render(request, 'product_list.html', context=context)


class LoanedProductsByUserListView(LoginRequiredMixin, generic.ListView):
    model = ProductInstance
    template_name ='user_products.html'
    context_object_name = 'products'
    paginate_by = 10
    
    def get_queryset(self):
        return ProductInstance.objects.filter(vartotojas=self.request.user).filter(status__exact='l').order_by('due_back')


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "product_detail.html"
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        object = Product.objects.get(pk=self.kwargs['pk'])
        sizes = object.instances.all()
        print(sizes)
        context['instances'] = sizes.order_by('size')
        return context

class ProductByUserDetailView(LoginRequiredMixin, DetailView):
    model = ProductInstance
    template_name = 'user_procuct.html'

class ProductByUserCreateView(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model = ProductInstance
    fields = ['product','size' ,'quantity' ,'due_back']
    success_url = "/library/my_products/"
    template_name = 'user_product_form.html'
   


    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        form.instance.status = 'a'
        return super().form_valid(form)
    
    def test_func(self) -> bool | None:
        return not self.request.user.groups.filter(name="sandelio darbuotojai").exists()
    

def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'product_list.html', context)

