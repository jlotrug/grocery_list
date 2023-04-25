from django.shortcuts import render, redirect
from .models import Item, ListItem, List
from .forms import RegistrationForm
from django.views.generic.edit import CreateView
from decimal import Decimal
from django.contrib import messages
from .helper_functions.view_functions import get_list_total, get_list_calorie_count, get_error_list

def home(request):
    if not request.user.is_authenticated:
        messages.warning(request, f'Please login to continue')
        return redirect('/login')

    lists = List.objects.filter(user= request.user)

    return render(request, 'grocery_list/home.html', {'lists': lists})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')

    return render(request, 'grocery_list/register.html')


def create_list(request):

    if not request.user.is_authenticated:
        messages.warning(request, f'Please login to continue')
        return redirect('/login')

    if request.method == 'POST':
        name = request.POST.get('name', '')
        new_list = List.objects.create(
            list_name=name, 
            user=request.user
            )
        new_list.save()

        print(name)

        return redirect('/grocery_list')

    return render(request, 'grocery_list/list-form.html')

def grocery_list(request, id):

    if not request.user.is_authenticated:
        messages.warning(request, f'Please login to continue')
        return redirect('/login')

    list = List.objects.get(id=id)

    if request.method == 'POST':
        req_type = request.POST.get('req-type', '')

        if req_type == 'to-delete':
            item_id = request.POST.get('item', '')
            list_item = ListItem.objects.get(id=item_id)
            if list_item.quantity > 1:
                list_item.quantity -= 1
                list_item.save()
            else:
                list_item.delete()
        else:
            item_id = request.POST.get('new_item', '')
            new_item = Item.objects.get(id=item_id)
            matching_items = ListItem.objects.filter(item_id=new_item, list_id=list)

            if len(matching_items) > 0:

                matching_items[0].quantity += 1
                matching_items[0].save()
            else:
                ListItem.objects.create(item_id=new_item, list_id=list )

    
    items = list.items.all()
    list_items = ListItem.objects.filter(list_id=list)
    all_items = Item.objects.filter(user=request.user)
    list_total = get_list_total(list_items)
    calorie_count = get_list_calorie_count(list_items)

    for li in list_items:
        print(li.item_id.item_name)

    return render(request,'grocery_list/list.html' ,{'list': list, 'all_items': all_items, 'list_total': list_total, 'calories': calorie_count, 'list_items': list_items})



def create_item(request):

    if not request.user.is_authenticated:
        messages.warning(request, f'Please login to continue')
        return redirect('/login')

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

        error_list = get_error_list(new_item)
        if not price_error == '':
            error_list.append(price_error)


        # new_item = Item.objects.create(
        #     item_name = name,
        #     item_carbs = carbs,
        #     item_fat = fat,
        #     item_protein = protein,
        #     item_calories = calories,
        #     item_notes = notes,
        #     item_price = price,
        #     item_image = image,
        #     user = request.user
        # )

        if len(error_list) > 0:
            return render(request, 'grocery_list/item-form.html', {'item': new_item, 'error_list': error_list})

        if new_item.item_image == '':
            new_item.item_image = 'https://liftlearning.com/wp-content/uploads/2020/09/default-image.png'

        new_item.save()
        return redirect('/grocery_list/item/' + str(new_item.id))

    return render(request, 'grocery_list/item-form.html')

def item_details(request, id):

    if not request.user.is_authenticated:
        messages.warning(request, f'Please login to continue')
        return redirect('/login')

    item = Item.objects.get(id=id)

    return render(request, 'grocery_list/item.html', {'item': item})


def all_items(request):

    if not request.user.is_authenticated:
        messages.warning(request, f'Please login to continue')
        return redirect('/login')

    if request.method == 'POST':
        item_id = request.POST.get('item', '')
        item = Item.objects.get(id=item_id)
        item.delete()

    items = Item.objects.filter(user=request.user)

    return render(request, 'grocery_list/all-items.html', {'items': items})


def edit_item(request, id):

    if not request.user.is_authenticated:
        messages.warning(request, f'Please login to continue')
        return redirect('/login')

    item = Item.objects.get(id=id)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        carbs = request.POST.get('carbs', '')
        fat = request.POST.get('fat', '')
        protein = request.POST.get('protein', '')
        calories = request.POST.get('calories', '')
        notes = request.POST.get('notes', '')
        price = request.POST.get('price', '')
        price = Decimal(price)
        image = request.POST.get('image', '')

        if image == '':
            image = 'https://liftlearning.com/wp-content/uploads/2020/09/default-image.png'

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
