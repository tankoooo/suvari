"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from django.db import models
from .models import Comment

from .models import Blog


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Логин'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))
class AnketaForm(forms.Form):
    name = forms.CharField(label='Ваше ФИО', min_length=2, max_length=100)
    city = forms.CharField(label="Ваш город", min_length=2, max_length=100)
    job = forms.CharField(label="В каком университете обучаетеь?", min_length=2, max_length=100)
    gender = forms.ChoiceField(label='Ваш пол',
                               choices=[('1', "Мужской"), ('2', 'Женский' )],
                               widget=forms.RadioSelect, initial=1)
    internet = forms.ChoiceField(label='Курс обучения',
                                choices=(('1',"1"),
                                         ('2', '2' ),
                                         ('3',"3" ),
                                         ('4', '4')), initial=1)
    notice = forms.BooleanField(label='Получать новости сайта на e-mail?',
                                 required=False)
    email = forms.EmailField(label='Baш e-mail', min_length=7)
    message = forms.CharField(label="Коротко о себе (указать факультет)",
                               widget=forms.Textarea(attrs={"rows":12,'cols':20}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': 'Комментарий'}

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image')
        labels = {
            'title': 'Заголовок',
            'description': 'Краткое содержание', 
            'content': 'Полное содержание',
            'image': 'Картинка'
        }