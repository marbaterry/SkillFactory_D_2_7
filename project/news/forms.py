from django.forms import ModelForm
from django import forms
from allauth.account.forms import SignupForm

from .models import Post, CategorySubscriber
from django.contrib.auth.models import Group


# class EquipmentModelPost(forms.ModelForm):
#     class Meta:
#         model = Post
#
#     def __init__(self, *args, **kwargs):
#         forms.ModelForm.__init__(self, *args, **kwargs)
#         self.fields['title'].queryset = Post.avail.all()


class PostForm(ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control mb-2'}))

    class Meta:
        model = Post
        fields = ['post_type', 'title', 'author', 'content', 'category']


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class SubsForm(ModelForm):
    class Meta:
        model = CategorySubscriber
        fields = ['classTrough',]
