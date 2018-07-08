from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm
from .models import Dishes, Substitutes

IMG = 'https://unsplash.com/photos/eqsEZNCm4-c'

def index(request):
    context = {
    "page_title" : "Accueil"
    }
    return render(request, 'openfoodfacts/index.html')


def search(request):
    query = request.GET.get('query')

    # if query matches with dish_name
    query_prod = Dishes.objects.filter(dish_name__iexact=query).first()

    # if query doesn't match exactly but can matches with dish_name
    if not query_prod:
        query_prod = Dishes.objects.filter(dish_name__icontains=query).first()

    # query doesn't match at all
    if not query_prod:
        raise Http404 # catch a 404 error -> not found
    else:
        dishes_list = Dishes.objects.filter(category=query_prod.category)
        dishes_list = dishes_list.filter(nutriscore__lte=query_prod.nutriscore)
        dishes_list = dishes_list.order_by('nutriscore')
        dishes_list = dishes_list.exclude(pk=query_prod.dish_id)


        if request.user.is_authenticated:
            # Remove dishes already in the user's list
            for dish in dishes_list:
                listed = Substitutes.objects.filter(
                    origin_dish=query_prod.dish_id,
                    alternative_dish=dish.dish_id,
                    user=request.user
                    )
                if listed:
                    dishes_list = dishes_list.exclude(pk=dish.dish_id)

    # If user wants to save a dish
    if request.user.is_authenticated and request.method == 'POST':
        origin_dish = request.POST.get('origin_dish')
        alternative_dish = request.POST.get('alternative_dish')

        origin_dish = Dishes.objects.get(pk=origin_dish)
        alternative_dish = Dishes.objects.get(pk=alternative_dish)

        Substitutes.objects.create(
            origin_dish=origin_dish,
            alternative_dish=alternative_dish,
            user=request.user
            )
        dishes_list = dishes_list.exclude(pk=alternative_dish.dish_id)

    # Slice pages
    paginator = Paginator(dishes_list, 9) # dispose 9 articles by page
    page = request.GET.get('page')

    try:
        dishes = paginator.page(page)
    except PageNotAnInteger:
        dishes = paginator.page(1)
    except EmptyPage:
        dishes = paginator.page(paginator.num_pages)

    context = {
        'dishes': dishes,
        'paginate': True,
        'query': query,
        'title': query_prod.dish_name,
        'img': query_prod.img,
        'query_prod': query_prod.dish_id,
        "page_title": "Résultats"
    }
    return render(request, 'openfoodfacts/search.html', context)


def detail(request, dish_id):
    dish = get_object_or_404(Dishes, pk=dish_id)

    fat_index_img = ""
    saturated_fat_index_img = ""
    salt_index_img = ""
    sugar_index_img = ""
    url = "https://static.openfoodfacts.org/images/misc/"

    # dish proprerties:
    if dish.fat:
        if dish.fat < 3:
            fat_index_img = url + "low_30.png" # URL corresponding to a green circe image to indicate a good choice
        elif 3 <= dish.fat < 20:
            fat_index_img = url + "moderate_30.png" # URL corresponding to an orange circe image to indicate a quite good choice
        else:
            fat_index_img = url + "high_30.png" # URL corresponding to a red circe image to indicate a bad choice

    # same URL priciple to all others food properties
    if dish.saturated_fat:
        if dish.saturated_fat < 1.5:
            saturated_fat_index_img = url + "low_30.png"
        elif 1.5 <= dish.saturated_fat < 5:
            saturated_fat_index_img = url + "moderate_30.png"
        else:
            saturated_fat_index_img = url + "high_30.png"

    if dish.salt:
        if dish.salt < 0.3:
            salt_index_img = url + "low_30.png"
        elif 0.3 <= dish.salt < 1.5:
            salt_index_img = url + "moderate_30.png"
        else:
            salt_index_img = url + "high_30.png"

    if dish.sugar:
        if dish.sugar < 5:
            sugar_index_img = url + "low_30.png"
        elif 5 <= dish.sugar < 12.5:
            sugar_index_img = url + "moderate_30.png"
        else:
            sugar_index_img = url + "high_30.png"

    context = {
        "dish": dish.dish_name,
        "img": dish.img,
        "nutriscore": dish.nutriscore,
        "fat": dish.fat,
        "saturated_fat": dish.saturated_fat,
        "salt": dish.salt,
        "sugar": dish.sugar,
        "fat_index_img": fat_index_img,
        "saturated_fat_index_img": saturated_fat_index_img,
        "salt_index_img": salt_index_img,
        "sugar_index_img": sugar_index_img,
        "redirection": dish.url,
        "page_title" : dish.dish_name
    }
    return render(request, 'openfoodfacts/detail.html', context)


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/openfoodfacts/account')
    else:
        form = SignUpForm()

    context = {
        "form": form,
        "title": "S'enregistrer",
        "img": IMG,
        "page_title": "S'enregistrer"
    }
    return render(request, 'openfoodfacts/sign_up.html', context)


@login_required
def account(request):
    context = {
        "user": request.user,
        "img": IMG,
        "page_title": 'Votre compte'
    }
    return render(request, 'openfoodfacts/account.html', context)


def contacts(request):
    context = {
        "title": 'Contacts',
        "img": IMG,
        "page_title": 'Nous contacter'
        }
    return render(request, 'openfoodfacts/contacts.html', context)


def legals(request):
    context = {
        "title": "Mentions légales",
        "img": IMG,
        "page_title": "Mentions légales"
    }
    return render(request, 'openfoodfacts/legals.html', context)


@login_required
def saved(request):
    saved_dishes = Substitutes.objects.filter(user=request.user)

    if request.method == 'POST':
        origin_dish = request.POST.get('origin_dish')
        alternative_dish = request.POST.get('alternative_dish')

        origin_dish = Dishes.objects.get(pk=origin_dish)
        alternative_dish = Dishes.objects.get(pk=alternative_dish)

        Substitutes.objects.get(
            origin_dish=origin_dish,
            alternative_dish=alternative_dish,
            user=request.user
            ).delete()

    # Slice pages
    paginator = Paginator(saved_dishes, 5)
    page = request.GET.get('page')

    try:
        saved_dishes = paginator.page(page)
    except PageNotAnInteger:
        saved_dishes = paginator.page(1)
    except EmptyPage:
        saved_dishes = paginator.page(paginator.num_pages)


    context = {
        "title": "Vos aliments sauvegardés",
        "img": IMG,
        "saved_dishes": saved_dishes,
        "paginate": True,
        "page_title": "Vos aliments sauvegardés"
    }
    return render(request, 'openfoodfacts/saved.html', context)
