from django import forms
from .models import DiscussionThread, Comment


class DiscussionThreadForm(forms.ModelForm):
    """
    Форма для создания и редактирования темы обсуждения.
    """
    
    class Meta:
        model = DiscussionThread
        fields = ['title', 'content', 'episode']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок темы...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Опишите тему обсуждения...'
            }),
            'episode': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('Заголовок слишком короткий (минимум 5 символов)!')
        return title


class CommentForm(forms.ModelForm):
    """
    Форма для добавления комментария.
    """
    
    class Meta:
        model = Comment
        fields = ['content', 'parent']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Напишите комментарий...'
            }),
            'parent': forms.HiddenInput(),  # Скрытое поле для родителя
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем parent необязательным
        self.fields['parent'].required = False