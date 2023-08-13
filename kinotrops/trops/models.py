from django.db import models
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse


class Trops(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Описание тропа")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name="Категория")

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'троп'
        verbose_name_plural = 'тропы'
        ordering = ['-time_create', 'title']

    def get_absolute_url(self):
        return reverse('trops', kwargs={'trops_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['id']


    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


