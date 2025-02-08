from django import forms
from django.utils.timezone import now

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'text', 'category',
            'location', 'image', 'pub_date', 'is_published']
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_pub_date(self):
        pub_date = self.cleaned_data['pub_date']
        # Используем .get() для безопасного получения 'is_published'
        is_published = self.cleaned_data.get('is_published', False)

        if pub_date > now() and not is_published:
            raise forms.ValidationError('Невозможно установить дату в будущем,\
                                         если пост не опубликован.')

        return pub_date


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']  # Заменили content на text
