from django import forms
from django.forms import ModelForm
from .models import Post, Area, MountainArea

class PostForm(ModelForm):
    parent_category = forms.ModelChoiceField(
        queryset=Area.objects,
        required=False
    )
    class Meta:
        model = Post
        fields = ['photo', 'comment', 'area','mountain_name', 'category','plantname']
        labels = {'photo':'写真', 'comment':'コメント', 'area':'地域','mountain_name':'山域', 'category':'カテゴリ','plantname':'植物名'}