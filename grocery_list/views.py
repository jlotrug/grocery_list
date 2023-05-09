from django.shortcuts import render, redirect
from .models import Item, ListItem, List
from .forms import RegistrationForm
from django.views.generic.edit import CreateView
from decimal import Decimal
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from .helper_functions.view_functions import get_list_total, get_list_calorie_count, get_error_list
from django.core.paginator import Paginator

def home(request):
    if not request.user.is_authenticated:
        messages.warning(request, f'Please login to continue')
        return redirect('/login')
    
    # Handles deleting a list
    if request.method == 'POST':
        list_id = request.POST.get('list', '')
        list = List.objects.get(id=list_id)
        list.delete()
        
    lists = List.objects.filter(user= request.user)

    return render(request, 'grocery_list/home.html', {'lists': lists})

def login(request):
    print("Hello May Ninth")
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Username or password is incorrect')
            messages.error(request, 'Please try again')
    return render(request, 'grocery_list/login.html', {})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        # Validates signup info and saves user
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')

    return render(request, 'grocery_list/register.html')


def create_list(request):

    if not request.user.is_authenticated:
        messages.warning(request, f'Please login to continue')
        return redirect('/login')

    # Creates a new list and takes user to it
    if request.method == 'POST':
        name = request.POST.get('name', '')
        new_list = List.objects.create(
            list_name=name, 
            user=request.user
            )
        new_list.save()

        return redirect('/grocery_list/' + str(new_list.id))

    return render(request, 'grocery_list/list-form.html')

def grocery_list(request, id):

    if not request.user.is_authenticated:
        messages.warning(request, f'Please login to continue')
        return redirect('/login')

    # Gets list
    list = List.objects.get(id=id)

    # There are several POST options on this page
    if request.method == 'POST':
        req_type = request.POST.get('req-type', '')

        # Deletes an item from a list or decrements quantity
        if req_type == 'to-delete':
            item_id = request.POST.get('item', '')
            list_item = ListItem.objects.get(id=item_id)
            if list_item.quantity > 1:
                list_item.quantity -= 1
                list_item.save()
            else:
                list_item.delete()
        else:
            # Checks if item is already on list
            item_id = request.POST.get('new_item', '')
            new_item = Item.objects.get(id=item_id)
            matching_items = ListItem.objects.filter(item_id=new_item, list_id=list)

            # Increases quantity instead of adding new item if item exists
            if len(matching_items) > 0:

                matching_items[0].quantity += 1
                matching_items[0].save()
            else:
                # Creates new ListItem
                ListItem.objects.create(item_id=new_item, list_id=list )

    # Gets all list items and calorie/cost totals
    items = list.items.all()
    list_items = ListItem.objects.filter(list_id=list)
    all_items = Item.objects.filter(user=request.user)
    list_total = get_list_total(list_items)
    calorie_count = get_list_calorie_count(list_items)

    # Handles pagination
    paginator = Paginator(list_items, 5)
    page = request.GET.get('page')
    list_items = paginator.get_page(page)

    return render(request,'grocery_list/list.html' ,{'list': list, 'all_items': all_items, 'list_total': list_total, 'calories': calorie_count, 'list_items': list_items})

def edit_item(request, id):

    if not request.user.is_authenticated:
        messages.warning(request, f'Please login to continue')
        return redirect('/login')

    # Gets item to edit
    item = Item.objects.get(id=id)

    # Gathers and validates user edits
    if request.method == 'POST':
        name = request.POST.get('name', '')
        carbs = request.POST.get('carbs', '')
        fat = request.POST.get('fat', '')
        protein = request.POST.get('protein', '')
        calories = request.POST.get('calories', '')
        notes = request.POST.get('notes', '')
        price = request.POST.get('price', '')
        if price == '':
            price = '0'
        if price.replace('.', '', 1).isnumeric():
            price = Decimal(price)
            price_error = ''
        else:
            price = 0
            price_error = "Price must be numeric"
        image = request.POST.get('image', '')

        # Creates new item with user edits to test
        new_item = Item(
            item_name = name,
            item_carbs = carbs,
            item_fat = fat,
            item_protein = protein,
            item_calories = calories,
            item_notes = notes,
            item_price = price,
            item_image = image,
            user = request.user
        )

        # Tests user's edits
        error_list = get_error_list(new_item)

        if not price_error == '':
            error_list.append(price_error)

        if image == '':
            image = 'https://liftlearning.com/wp-content/uploads/2020/09/default-image.png'
        new_item.item_image = image

        # Displays errors if needed
        if len(error_list) > 0:
            return render(request, 'grocery_list/edit-item.html', {'item': new_item, 'error_list': error_list})

        # Updates Item and saves
        item.item_calories = calories
        item.item_name = name
        item.item_carbs = carbs
        item.item_fat = fat
        item.item_protein = protein
        item.item_notes = notes
        item.item_price = price
        item.item_image = image
        item.save()

        return redirect('/grocery_list/item/' + str(item.id))

    return render(request, 'grocery_list/edit-item.html', {'item': item})

def create_item(request):

    if not request.user.is_authenticated:
        messages.warning(request, f'Please login to continue')
        return redirect('/login')

    if request.method == 'POST':
        # Gets user input and validates data
        name = request.POST.get('name', '')
        carbs = request.POST.get('carbs', '')
        fat = request.POST.get('fat', '')
        protein = request.POST.get('protein', '')
        calories = request.POST.get('calories', '')
        notes = request.POST.get('notes', '')
        price = request.POST.get('price', '')
        if price == '':
            price = '0'
        if price.replace('.', '', 1).isnumeric():
            price = Decimal(price)
            price_error = ''
        else:
            price = 0
            price_error = "Price must be numeric"
        image = request.POST.get('image', '')        

        # Creates Item object to test before saving
        new_item = Item(
            item_name = name,
            item_carbs = carbs,
            item_fat = fat,
            item_protein = protein,
            item_calories = calories,
            item_notes = notes,
            item_price = price,
            item_image = image,
            user = request.user
        )
        # Tests user input for valid data
        error_list = get_error_list(new_item)
        if not price_error == '':
            error_list.append(price_error)

        # Displays errors if needed
        if len(error_list) > 0:
            return render(request, 'grocery_list/item-form.html', {'item': new_item, 'error_list': error_list})

        if new_item.item_image == '':
            new_item.item_image = 'https://liftlearning.com/wp-content/uploads/2020/09/default-image.png'

        # Saves item
        new_item.save()
        return redirect('/grocery_list/item/' + str(new_item.id))

    return render(request, 'grocery_list/item-form.html')

def item_details(request, id):

    if not request.user.is_authenticated:
        messages.warning(request, f'Please login to continue')
        return redirect('/login')
    # Gets Item
    item = Item.objects.get(id=id)

    return render(request, 'grocery_list/item.html', {'item': item})


def all_items(request):

    if not request.user.is_authenticated:
        messages.warning(request, f'Please login to continue')
        return redirect('/login')
    # Deletes Item
    if request.method == 'POST':
        item_id = request.POST.get('item', '')
        item = Item.objects.get(id=item_id)
        item.delete()
    # Gathers all user items
    items = Item.objects.filter(user=request.user)

    return render(request, 'grocery_list/all-items.html', {'items': items})



