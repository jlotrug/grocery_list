from django.shortcuts import render, redirect
from .models import Item, ListItem, List
from django.views.generic.edit import CreateView

def home(request):
    print("Hello ALl Worlds")

    if request.user.is_authenticated:

        #print(List.objects.get(user= request.user))
        lists = List.objects.filter(user= request.user)

        return render(request, 'grocery_list/home.html', {'lists': lists})

    return render(request, 'grocery_list/home.html')


def create_list(request):
    print("Hello World")

    if request.method == 'POST':
        name = request.POST.get('name', '')
        new_list = List.objects.create(list_name=name, user=request.user)
        new_list.save()

        print(name)

        return redirect('/grocery_list')

    return render(request, 'grocery_list/list-form.html')

# class ListCreate(CreateView):
#     model = List
#     fields = ['list_name']
#     template_name= 'grocery_list/list-form.html'

#     print("Hello World")
