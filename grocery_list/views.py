from django.shortcuts import render, redirect
from .models import Item, ListItem, List
from django.views.generic.edit import CreateView
from decimal import Decimal
from .helper_functions.view_functions import get_list_total, get_list_calorie_count

def home(request):

    if request.user.is_authenticated:

        #print(List.objects.get(user= request.user))
        lists = List.objects.filter(user= request.user)

        return render(request, 'grocery_list/home.html', {'lists': lists})

    return render(request, 'grocery_list/home.html')


def create_list(request):

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

    list = List.objects.get(id=id)

    if request.method == 'POST':
        req_type = request.POST.get('req-type', '')

        if req_type == 'to-delete':
            item_id = request.POST.get('item', '')
            item = Item.objects.get(id=item_id)
            list_item = ListItem.objects.get(item_id=item, list_id=list)
            list_item.delete()
        else:
            item_id = request.POST.get('new_item', '')
            new_item = Item.objects.get(id=item_id)
            # list = List.objects.get(id=id)
            ListItem.objects.create(item_id=new_item, list_id=list )

    
    items = list.items.all()
    all_items = Item.objects.filter(user=request.user)
    list_total = get_list_total(items)
    calorie_count = get_list_calorie_count(items)

    return render(request,'grocery_list/list.html' ,{'items': items, 'list': list, 'all_items': all_items, 'list_total': list_total, 'calories': calorie_count})



def create_item(request):

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

        new_item = Item.objects.create(
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

        new_item.save()
        return redirect('/grocery_list/item/' + str(new_item.id))



    return render(request, 'grocery_list/item-form.html')

def item_details(request, id):
    item = Item.objects.get(id=id)

    return render(request, 'grocery_list/item.html', {'item': item})

# class ListCreate(CreateView):
#     model = List
#     fields = ['list_name']
#     template_name= 'grocery_list/list-form.html'

#     print("Hello World")
