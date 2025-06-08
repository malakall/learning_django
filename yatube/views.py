from django.shortcuts import render, redirect
from .models import Group  # Импортируем модель групп
from .forms import RegisterForm
from django.contrib.auth import login

from .forms import GroupForm

def index(request):
    groups = Group.objects.all()
    # groups = Group.objects.filter(name__startswith="т") # работа с орм вытаскиваем данные который начинаются только на буквку "т"

    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user  # связываем с текущим пользователем
            group.save()
            return redirect('index')
    else:
        form = GroupForm()

    return render(request, "main/index.html", {"groups": groups, "form": form})


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
            return redirect("index")  # Меняем на главную страницу
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})



from .forms import ContactForm

def send_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('send_form')  
    else:
        form = ContactForm()

    return render(request, 'main/forms.html', {'form': form})