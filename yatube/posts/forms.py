from django import forms

from posts.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        help_texts = {
            'text': 'Текст нового поста',
            'group': 'Группа, к которой будет относиться пост',
        }
        labels = {
            'text': ('Текст нового поста'),
            'pub_date': ('Дата публикации'),
            'author': ('Автор'),
            'group': ('Группа'),
        }
