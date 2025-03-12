from django import forms
from .models import Comic, Chapter, Genre


class ComicForm(forms.ModelForm):
    class Meta:
        model = Comic
        fields = ['title', 'status', 'genre', 'subgenre', 'format_type', 'description', 'cover_image']

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['comic', 'title', 'chapter_number', 'content', 'image']



"""
class ComicSearchForm(forms.Form):
    query = forms.CharField(required=False, label="Buscar")
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), required=False, label="Género")
    format_type = forms.ChoiceField(choices=[('', 'Todos')] + Comic.FORMAT_CHOICES, required=False, label="Formato")
"""

class ComicSearchForm(forms.Form):
    query = forms.CharField(label="Obra", required=False)

    author = forms.CharField(label="Autor", required=False)

    genre = forms.ChoiceField(choices=[('', 'Todos')] + list(Comic.GENRE_CHOICES), required=False)
    subgenre = forms.ChoiceField(choices=[('', 'Todos')] + list(Comic.SUBGENRE_CHOICES), required=False)
    

    format_type = forms.ChoiceField(choices=[('', 'Todos')] + list(Comic.FORMAT_CHOICES), required=False)

