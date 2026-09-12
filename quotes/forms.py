from django import forms
from .models import Quote

class QuoteForm(forms.ModelForm):
    
    class Meta:
        model = Quote
        fields = ("",)

    """
    Форма для создания и редактирования цитат.
    Использует ModelForm для автоматической генерации полей.
    """
    class Meta:
        model = Quote
        fields = ['text', 'character', 'episode']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Введите текст цитаты...'
            }),
            'character': forms.Select(attrs={
                'class': 'form-select'
            }),
            'episode': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'text': 'Текст цитаты',
            'character': 'Персонаж',
            'episode': 'Серия',
        }
    
    def clean_text(self):
        """
        Валидация текста цитаты.
        """
        text = self.cleaned_data.get('text')
        if len(text) < 3:
            raise forms.ValidationError('Текст цитаты слишком короткий (минимум 3 символа)!')
        if len(text) > 1000:
            raise forms.ValidationError('Текст цитаты слишком длинный (максимум 1000 символов)!')
        return text