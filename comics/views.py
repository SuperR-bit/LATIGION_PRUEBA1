from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Comic, Chapter, Genre 
import random
from .forms import ComicForm, ChapterForm
import os
import zipfile
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.db.models import Q 
from .forms import ComicSearchForm  # Importa el formulario correctamente


#esta primera funcion piensalo ....
def comics_home(request):
    return render(request, 'comics/comics_home.html')


def home(request):
    comics = Comic.objects.all().order_by('-created_at')
    return render(request, 'comics/home.html', {'comics': comics})

def popular_comics(request):
    comics = Comic.objects.all().order_by('-views', '-likes')[:10] # ordenar por popularidad
    return render(request, 'comics/popular_comics.html', {'comics': comics})

def comic_list(request):
    comics = Comic.objects.order_by('-views')[:10]  # Los más populares
    return render(request, 'comics/comic_list.html', {'comics': comics})

def recent_comics(request):
    comics = Comic.objects.order_by('-created_at')[:10]  # Recientes
    return render(request, 'comics/recent_comics.html', {'comics': comics})

def random_comic(request):
    comic = Comic.get_random_comic()
    if comic:
        return redirect('comic_detail', comic.id)
    return redirect('home')


from django.shortcuts import render, get_object_or_404
from .models import Comic, Chapter

def comic_detail(request, comic_id):
    comic = get_object_or_404(Comic, id=comic_id)
    comic.views += 1 # contador de visitas
    # chapters = Chapter.objects.filter(comic=comic).order_by('chapter_number')   me asusta que esto no este
    comic.save()

    chapters = comic.chapters.all().order_by('chapter_number')

    #print(f"🔍 Capítulos encontrados para {comic.title}: {[ch.title for ch in chapters]}")  # Depuración

    return render(request, 'comics/comic_detail.html', {'comic': comic, 'chapters': chapters})


"""
def comic_detail(request, comic_id):
    comic = get_object_or_404(Comic, id=comic_id)
    comic.views += 1  # Aumentar vistas
    comic.save()
    chapters = comic.chapters.all().order_by('chapter_number')
    return render(request, 'comics/comic_detail.html', {'comic': comic, 'chapters': chapters})
"""

def like_comic(request, comic_id):
    comic = get_object_or_404(Comic, id=comic_id)
    if request.method == "POST":
        comic.likes += 1
        comic.save()
        return JsonResponse({'likes': comic.likes})
    return JsonResponse({'error': 'Método no permitido'}, status=400)

"""
def delete_comic(request, comic_id):
    comic = get_object_or_404(Comic, id=comic_id)
    comic.delete()
    return redirect('popular_comics')
"""
"""
def delete_chapter(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    comic_id = chapter.comic.id
    chapter.delete()
    return redirect('comic_detail', comic_id=comic_id)
"""

def search_comics(request):
    form = ComicSearchForm(request.GET)
    comics = Comic.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        genre = form.cleaned_data.get('genre')
        format_type = form.cleaned_data.get('format_type')

        if query:
            comics = comics.filter(Q(title__icontains=query) | Q(author__icontains=query))
        if genre:
            comics = comics.filter(genre=genre)
        if format_type:
            comics = comics.filter(format_type=format_type)

    return render(request, 'comics/search_results.html', {'form': form, 'comics': comics})



def read_chapter(request, comic_id, chapter_number):
    comic = get_object_or_404(Comic, id=comic_id)
    chapter = get_object_or_404(Chapter, comic=comic, chapter_number=chapter_number)
    
    # Obtener imágenes del capítulo
    chapter_path = os.path.join(settings.MEDIA_ROOT, chapter.image_folder)
    images = chapter.get_images()  # Ahora obtenemos las imágenes correctamente
    #images = sorted(os.listdir(chapter_path)) if os.path.exists(chapter_path) else []

    # Buscar capítulo anterior y siguiente
    previous_chapter = Chapter.objects.filter(comic=comic, chapter_number__lt=chapter_number).order_by('-chapter_number').first()
    next_chapter = Chapter.objects.filter(comic=comic, chapter_number__gt=chapter_number).order_by('chapter_number').first()

    return render(request, 'comics/read_chapter.html', {
        'comic': comic,
        'chapter': chapter,
        'images': images,
        'previous_chapter': previous_chapter,
        'next_chapter': next_chapter
        #"MEDIA_URL": settings.MEDIA_URL   Asegura que el template tenga acceso a MEDIA_URL
    })


def comics_by_genre(request):
    genres = Genre.objects.all()
    comics_by_genre = {genre: genre.comic_set.all() for genre in genres}

    return render(request, 'comics/comics_by_genre.html', {'comics_by_genre': comics_by_genre})

def comics_by_format(request, format_type):
    comics = Comic.objects.filter(format_type=format_type)
    return render(request, 'comics/comics_by_format.html', {'comics': comics, 'format_type': format_type})





import os
import zipfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Comic, Chapter
from .forms import ComicForm

@login_required(login_url = "/users/login/" )
def upload_comic(request):
    if request.method == 'POST':
        form = ComicForm(request.POST, request.FILES)
        if form.is_valid():
            comic = form.save(commit=False)
            comic.author = request.user  # Solo el usuario logueado puede subirlo
            comic.save()
            messages.success(request, "Cómic subido correctamente.")
            return redirect('recent_comics')
    else:
        form = ComicForm()
    return render(request, 'comics/upload_comic.html', {'form': form})

@login_required
def upload_chapter(request, comic_id):
    comic = get_object_or_404(Comic, id=comic_id)

    if request.user != comic.author:
        messages.error(request, "No puedes subir capítulos a un cómic que no te pertenece.")
        return redirect('comic_detail', comic_id=comic.id)

    if request.method == "POST" and request.FILES.get("zip_file"):
        zip_file = request.FILES["zip_file"]
        
        last_chapter = Chapter.objects.filter(comic=comic).order_by('-chapter_number').first()
        chapter_number = (last_chapter.chapter_number + 1) if last_chapter else 1

        folder_name = os.path.join("comics", str(comic_id), "chapters", str(chapter_number))
        folder_path = os.path.join(settings.MEDIA_ROOT, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        zip_path = os.path.join(settings.MEDIA_ROOT, "temp.zip")
        with open(zip_path, "wb+") as temp_zip:
            for chunk in zip_file.chunks():
                temp_zip.write(chunk)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(folder_path)

        os.remove(zip_path)

        chapter_title = request.POST.get("chapter_title", f"Capítulo {chapter_number}")
        chapter = Chapter.objects.create(
            comic=comic,
            chapter_number=chapter_number,
            title=chapter_title,
            image_folder=folder_name  
        )

        messages.success(request, f"Capítulo {chapter.chapter_number} subido correctamente.")
        return redirect("comic_detail", comic_id=comic.id)

    return render(request, "comics/upload_chapter.html", {"comic": comic})

@login_required
def delete_comic(request, comic_id):
    comic = get_object_or_404(Comic, id=comic_id)

    if request.user != comic.author:
        messages.error(request, "No puedes borrar un cómic que no es tuyo.")
        return redirect('recent_comics')

    comic.delete()
    messages.success(request, "Cómic eliminado correctamente.")
    return redirect('recent_comics')

@login_required
def delete_chapter(request, comic_id, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id, comic_id=comic_id)

    if request.user != chapter.comic.author:
        messages.error(request, "No puedes borrar un capítulo de un cómic que no te pertenece.")
        return redirect('recent_comics')

    chapter.delete()
    messages.success(request, f"Capítulo {chapter.chapter_number} eliminado correctamente.")
    return redirect('comic_detail', comic_id=comic_id)




