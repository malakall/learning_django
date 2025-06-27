from django.shortcuts import render, redirect
from .models import Group, Comment 
from .forms import RegisterForm
from django.contrib.auth import login

from .forms import GroupForm
from django.core.paginator import Paginator

from django.views.decorators.cache import cache_page


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
        form = GroupForm(request.POST, request.FILES)
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
from django.core.exceptions import PermissionDenied

@login_required
def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)


    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES, instance=group)

        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = GroupForm(instance=group)

    return render(request, 'main/edit_group.html', {'form': form, 'group': group})


@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if group.user != request.user:
        raise PermissionDenied  # запретить удалять чужие записи
    if request.method == "POST":
        group.delete()
        return redirect('index')
    return render(request, "main/confirm_delete.html", {"group": group})


from .forms import CommentForm
from .models import Comment

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    comments = group.comments.all().order_by('-created')  # последние сверху

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login') 

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = group
            comment.author = request.user
            comment.save()
            return redirect('group_detail', group_id=group.id)
    else:
        form = CommentForm()

    context = {
        'group': group,
        'comments': comments,
        'form': form,
    }
    return render(request, 'main/group_detail.html', context)


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('group_detail', group_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'main/edit_comment.html', {'form': form, 'comment': comment})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        group_id = comment.post.id
        comment.delete()
        return redirect('group_detail', group_id=group_id)

    return render(request, 'main/confirm_delete_comment.html', {'comment': comment})



def change_data_group(request):
    return render(request, "main/change_data_group.html")

# @cache_page(60 * 5)
def about(request):
    return render(request, "main/about.html")

# @cache_page(60 * 5)
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

@login_required
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


