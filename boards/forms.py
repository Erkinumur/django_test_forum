from django import forms

from .models import Topic, Post


class TopicForm(forms.ModelForm):
    subject = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': "form-control"}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control"}), max_length=2000)

    class Meta:
        model = Topic
        fields = ['subject', 'message']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]