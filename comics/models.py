from django.db import models
from django.utils.timezone import now
import random
import os
from django.conf import settings
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length = 50, unique = True)

    def __str__(self):
        return self.name
    
class SubGenre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="subgenres")
    
    def __str__(self):
        return self.name 


class Comic(models.Model):
    GENRE_CHOICES = [
        ('Any', 'Ninguno'),
        ('Adventure', 'Aventura'),
        ('Science fiction', 'Ciencia ficción'),
        ('Comedy', 'Cómedia'),
        ('Sport', 'Deporte'),
        ('Fancy', 'Fantasia'),
        ('book', 'Misterio'),
        ('Drama', 'Drama'),
        ('Action', 'Acción'),
        ('Daily life', 'Vida cotidiana'),
        ('Romance', 'Romance'),
        ('Paranormal', 'Paranormal'),
        ('Suspense', 'Suspenso'),
        ('Terror', 'Terror'),
        ('Superheroes', 'Superhéroes'),
        ('Historical', 'Histórico'),
        ('Informative', 'Informativo'),
        ('Touching', 'Conmovedor')
    ]
    SUBGENRE_CHOICES = [
        ('Any', 'Ninguno'),
        ('Cyberpunk', 'Ciberpunk'),
        ('Science fiction', 'Bélico'),
        ('Police', 'Policial'),
        ('Meccas', 'Mecas'),
    ]
    FORMAT_CHOICES = [
        ('novel', 'Novela'),
        ('manhwa', 'Manhwa'),
        ('comic', 'Cómic'),
        ('manga', 'Manga'),
        ('story', 'Cuento'),
        ('book', 'Libro')
    ]
    STATUS_CHOICES = [
        ('ongoing', 'En emisión'),
        ('completed', 'Finalizado'),
        ('hiatus', 'En pausa')
    ]
    title = models.CharField(max_length=255)

    #author = models.CharField(max_length=100, default = "Anonimo")

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comics")

    created_at = models.DateTimeField(default=now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0])
    #genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    genre = models.CharField(max_length=30, choices=GENRE_CHOICES, default=FORMAT_CHOICES[0])
    #subgenre = models.ForeignKey(SubGenre, on_delete=models.SET_NULL, null=True, blank=True)
    subgenre = models.CharField(max_length=30, choices=SUBGENRE_CHOICES, default=SUBGENRE_CHOICES[0])
    format_type = models.CharField(max_length=10, choices=FORMAT_CHOICES, default=FORMAT_CHOICES[2])
    description = models.TextField(default="")
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)
    views = models.IntegerField(default=2000)  # Para calcular popularidad
    likes = models.PositiveIntegerField(default=500)  # Nueva columna para los likes
    

    def __str__(self):
        return self.title

    @classmethod
    def get_random_comic(cls):
        comics = list(cls.objects.all())
        return random.choice(comics) if comics else None

class Chapter(models.Model):
    comic = models.ForeignKey(Comic, related_name="chapters" ,on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="Título del Capítulo")
    chapter_number = models.PositiveIntegerField(default=1) 
    #chapter_number = models.IntegerField(null=True, blank=True)   Ahora puede ser nulo
    #content = models.TextField(default="Contenido vacío")
    content = models.TextField(default="Content") 
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image_folder = models.CharField(max_length=255, blank = True, null = True)
    image = models.ImageField(upload_to='chapters/', null=True, blank=True)

    class Meta:
        ordering = ['chapter_number'] 


    def __str__(self):
        return f"{self.comic.title} - Capítulo {self.chapter_number if self.chapter_number else '?'}"
    
    def get_images(self):
        """Devuelve las URLs completas de las imágenes del capítulo"""
        if self.image_folder:
            image_path = os.path.join(settings.MEDIA_ROOT, self.image_folder)
            if os.path.exists(image_path):
                images = sorted(os.listdir(image_path))  # Ordenamos las imágenes
                return [f"{settings.MEDIA_URL}{self.image_folder}/{img}" for img in images]
        return []
    
    
    












