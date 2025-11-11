"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import AnketaForm 
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from django.db import models
from .models import Blog
from .forms import BlogForm
from .models import Comment
from .forms import CommentForm


def blog(request):
    """Render the blog page."""
    posts = Blog.objects.all()  # запрос на выбор всех статей блога из модели
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Блог',
            'posts': posts,  # передача списка статей в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )


def blogpost(request, parameter):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parameter)  # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parameter)

    if request.method == "POST":  # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user  # добавляем автора
            comment_f.date = datetime.now()  # добавляем текущую дату
            comment_f.post = Blog.objects.get(id=parameter)  # добавляем статью
            comment_f.save()  # сохраняем изменения после добавления полей
            return redirect('blogpost', parameter=post_1.id)  # переадресация на ту же страницу
    else:
        form = CommentForm()  # создание формы для ввода комментария

    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,  # передача конкретной статьи в шаблон
            'comments': comments,  # передача комментариев в шаблон
            'form': form,  # передача формы в шаблон
            'year': datetime.now().year,
        }
    )
def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":  # после отправки формы
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user  # исправлено с subrc на author
            blog_f.save()  # сохранение изменений после добавления полей
            return redirect('blog')  # переадресация на страницу Блог после создания статьи
    else:
        blogform = BlogForm()  # создание объекта формы для ввода данных

    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,  # передача формы в шаблон веб-страницы
            'title': 'Добавить статью блога',
            'year': datetime.now().year,
        }
    )

def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            
            'year':datetime.now().year,
        }
    )

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )
def links(request):
    """Renders the links page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ресурсы',
            'year':datetime.now().year,
        }
    )
def anketa(request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Мужчина', '2': 'Женщина'}
    internet = {'1': 'Каждый день', '2': 'Несколько раз в день', 
                '3': 'Несколько раз в неделю', '4': 'Несколько раз в месяц'}
    if request. method == 'POST':
       form = AnketaForm(request.POST)
       if form.is_valid():
          data = dict()
          data['name'] = form.cleaned_data['name']
          data['city'] = form.cleaned_data['city']
          data['job'] = form.cleaned_data['job']
          data['gender'] = gender[ form.cleaned_data['gender']]
          data['internet'] = internet[ form.cleaned_data['internet']]
          if (form.cleaned_data['notice'] == True):
              data['notice'] = 'Да'
          else:
              data['notice'] = "Нет"
              data['email'] = form.cleaned_data['email']
              data['message'] = form.cleaned_data['message']
              form = None
    else:
     form = AnketaForm()
    return render(
    request,
    'app/anketa.html',
     {
         'form': form,
         'data': data
     }
)
def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)
    
    if request.method == "POST":  # после отправки формы
        regform = UserCreationForm(request.POST)
        
        if regform.is_valid():  # валидация полей формы
            reg_f = regform.save(commit=False)  # не сохраняем автоматически данные формы
            reg_f.is_staff = False  # запрещен вход в административный раздел
            reg_f.is_active = True  # активный пользователь
            reg_f.is_superuser = False  # не является суперпользователем
            reg_f.date_joined = datetime.now()  # дата регистрации
            reg_f.last_login = datetime.now()  # дата последней авторизации
            reg_f.save()  # сохраняем изменения после добавления данных
            
            return redirect('home')  # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm()  # создание объекта формы для ввода данных нового пользователя
    
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,  # передача формы в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )

