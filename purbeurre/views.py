# Imports
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm
from .models import Products, Substitutes

IMG = 'https://unsplash.com/photos/eqsEZNCm4-c'


# Index
def index(request):
    """
    Homepage
    """
    context = {
    "page_title" : "Accueil"
    }
    return render(request, 'purbeurre/index.html')


# Search queries
def search(request):
    """
    Search a food to replace
    Manage save products-operation if the user is logged
    """
    # Query
    query = request.GET.get('query')

    # If query matches with product_name
    query_prod = Products.objects.filter(product_name__iexact=query).first()

    # If query doesn't match exactly but can matches with product_name
    if not query_prod:
        query_prod = Products.objects.filter(product_name__icontains=query).first()

    # If query doesn't match at all
    if not query_prod:
        # Catch a 404 error -> not found product page
        raise Http404
    else:
        # Add the dishes to the products list filtered by category,
        products_list = Products.objects.filter(category=query_prod.category)
        # nutrition grade
        products_list = products_list.filter(nutriscore__lte=query_prod.nutriscore)
        # order them by nutrition score
        products_list = products_list.order_by('nutriscore')
        # exclude a saved product from products list
        products_list = products_list.exclude(pk=query_prod.id_product)


        # If user login = True
        if request.user.is_authenticated:
            # Remove dishes already in the user's list
            for product in products_list:
                listed = Substitutes.objects.filter(
                    origin = query_prod.id_product,
                    replacement = product.id_product,
                    user = request.user
                    )
                if listed:
                    products_list = products_list.exclude(pk=product.id_product)

    # If user wants to save a dish
    if request.user.is_authenticated and request.method == 'POST':
        # Meal searched
        origin = request.POST.get('origin')
        # Desired alternative
        replacement = request.POST.get('replacement')

        origin = Products.objects.get(pk=origin)
        replacement = Products.objects.get(pk=replacement)

        # Place the searched meal and his healthy alternative in the user's list
        Substitutes.objects.create(
            origin = origin,
            replacement = replacement,
            user = request.user
            )
        # Exclude saved item(s) from search results page
        products_list = products_list.exclude(pk=replacement.id_product)

    # Slice pages
    paginator = Paginator(products_list, 9) # 9 articles by page
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # Render
    context = {
        'products': products,
        'paginate': True,
        'query': query,
        'title': query_prod.product_name,
        'category': query_prod.category,
        'img': query_prod.img,
        'query_prod': query_prod.id_product,
        "page_title": "Résultats"
    }
    return render(request, 'purbeurre/search.html', context)


# Detail
def detail(request, id_product):
    """
    Products details page with nutritional info
    """

    # Get dish
    product = get_object_or_404(Products, pk=id_product)

    fat_index_img = ""
    saturated_fat_index_img = ""
    salt_index_img = ""
    sugar_index_img = ""
    url = "https://static.openfoodfacts.org/images/misc/"

    # Dish proprerties:
    if product.fat:
        if product.fat < 3:
            fat_index_img = url + "low_30.png" # URL corresponding to a green circe image to indicate a good choice
        elif 3 <= product.fat < 20:
            fat_index_img = url + "moderate_30.png" # URL corresponding to an orange circe image to indicate a quite good choice
        else:
            fat_index_img = url + "high_30.png" # URL corresponding to a red circe image to indicate a bad choice

    # Same URL priciple to all others food properties
    if product.saturated_fat:
        if product.saturated_fat < 1.5:
            saturated_fat_index_img = url + "low_30.png"
        elif 1.5 <= product.saturated_fat < 5:
            saturated_fat_index_img = url + "moderate_30.png"
        else:
            saturated_fat_index_img = url + "high_30.png"

    if product.salt:
        if product.salt < 0.3:
            salt_index_img = url + "low_30.png"
        elif 0.3 <= product.salt < 1.5:
            salt_index_img = url + "moderate_30.png"
        else:
            salt_index_img = url + "high_30.png"

    if product.sugar:
        if product.sugar < 5:
            sugar_index_img = url + "low_30.png"
        elif 5 <= product.sugar < 12.5:
            sugar_index_img = url + "moderate_30.png"
        else:
            sugar_index_img = url + "high_30.png"

    # Render
    context = {
        "product": product.product_name,
        "img": product.img,
        "nutriscore": product.nutriscore,
        "fat": product.fat,
        "saturated_fat": product.saturated_fat,
        "salt": product.salt,
        "sugar": product.sugar,
        "fat_index_img": fat_index_img,
        "saturated_fat_index_img": saturated_fat_index_img,
        "salt_index_img": salt_index_img,
        "sugar_index_img": sugar_index_img,
        "redirection": product.url,
        "page_title" : product.product_name
    }
    return render(request, 'purbeurre/detail.html', context)


# Sign up
def sign_up(request):
    """
    User registration page
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # if form is valid
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/purbeurre/account')
    else:
        form = SignUpForm()

    # Render
    context = {
        "form": form,
        "title": "S'enregistrer",
        "img": IMG,
        "page_title": "S'enregistrer"
    }
    return render(request, 'purbeurre/sign_up.html', context)


# User account
@login_required
def account(request):
    """
    User informations page
    """

    # Render
    context = {
        "user": request.user,
        "img": IMG,
        "page_title": 'Votre compte'
    }
    return render(request, 'purbeurre/account.html', context)


# Contacts
def contacts(request):
    """
    Contacts page on footer
    """

    # Render
    context = {
        "title": 'Contacts',
        "img": IMG,
        "page_title": 'Nous contacter'
        }
    return render(request, 'purbeurre/contacts.html', context)


# Legals
def legals(request):
    """
    Legal informations page on footer
    """

    # Render
    context = {
        "title": "Mentions légales",
        "img": IMG,
        "page_title": "Mentions légales"
    }
    return render(request, 'purbeurre/legals.html', context)


# User's saved meals and substitutes
@login_required
def saved(request):
    """
    User's saved products and manage food(s) deletion
    """
    products_saved = Substitutes.objects.filter(user=request.user)

    # If user wants to delete a substitute product
    if request.method == 'POST':
        origin = request.POST.get('origin')
        replacement = request.POST.get('replacement')

        origin = Products.objects.get(pk=origin)
        replacement = Products.objects.get(pk=replacement)

        # Delete product from user's list
        Substitutes.objects.get(
            origin=origin,
            replacement=replacement,
            user=request.user
            ).delete()

    # Slice pages
    paginator = Paginator(products_saved, 5) # show 5 items every page
    page = request.GET.get('page')

    try:
        products_saved = paginator.page(page)
    except PageNotAnInteger:
        products_saved = paginator.page(1)
    except EmptyPage:
        products_saved = paginator.page(paginator.num_pages)


    # Render
    context = {
        "title": "Vos aliments sauvegardés",
        "img": IMG,
        "products_saved": products_saved,
        "paginate": True,
        "page_title": "Vos aliments sauvegardés"
    }
    return render(request, 'purbeurre/saved.html', context)
