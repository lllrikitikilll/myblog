from .models import Comment
from django import forms


# Форма EmailPostForm наследует от
# базового класса Form. Мы используем различные типы полей, чтобы выполнять 
# валидацию данных в соответствии с ними
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, label='Имя')  # Имя человека до 25 символов
    email = forms.EmailField( label='От кого')  # Валидация по email
    to = forms.EmailField( label='Кому')
    comments = forms.CharField(required=False,
                               widget=forms.Textarea,
                               label='Комментарий')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

# Поле поиска
class SearchForm(forms.Form):
    query = forms.CharField()

