from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'postCategory',
            'author',
            'post_title',
            'post_text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("post_text")
        if text is not None and len(text) < 20:
            raise ValidationError({
                "post_title": "Текст статьи не может быть менее 20 символов."
            })

        title = cleaned_data.get("post_title")
        if title == text:
            raise ValidationError(
                "Заголовок не должен быть идентичен посту."
            )

        return cleaned_data
