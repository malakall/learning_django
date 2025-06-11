from django.shortcuts import render, redirect
from .models import Group  # Импортируем модель групп
from .forms import RegisterForm
from django.contrib.auth import login

from .forms import GroupForm
from django.core.paginator import Paginator


def index(request):
    groups_list = Group.objects.all()
    author = request.GET.get('author')
    if author:
        # Фильтруем группы по user_name, содержащему введённый текст (регистронезависимо)
        groups_list = groups_list.filter(user_name__icontains=author)


    paginator = Paginator(groups_list, 2) 
    page_number = request.GET.get('page')
    groups = paginator.get_page(page_number)

    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            group.save()
            return redirect('index')
    else:
        form = GroupForm()

    return render(request, "main/index.html", {"groups": groups, "form": form})

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
@login_required
def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)


    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = GroupForm(instance=group)

    return render(request, 'main/edit_group.html', {'form': form, 'group': group})




from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if group.user != request.user:
        raise PermissionDenied  # запретить удалять чужие записи
    if request.method == "POST":
        group.delete()
        return redirect('index')
    return render(request, "main/confirm_delete.html", {"group": group})


def change_data_group(request):
    return render(request, "main/change_data_group.html")


def about(request):
    return render(request, "main/about.html")

def orders(request):
    return render(request, "main/orders.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)  # Автоматически логиним пользователя после регистрации
            return redirect("index")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})



from .forms import ContactForm
from django.contrib.auth.decorators import login_required

def send_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sucsess_form')  
    else:
        form = ContactForm()

    return render(request, 'main/forms.html', {'form': form})



def sucsess_form(request):
    return render(request, "main/sucsess_form.html")