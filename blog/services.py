from django.core.cache import cache
from blog.models import Blog
from config.settings import CACHE_ENABLED


def get_data_from_cache():
    """ Получаем данные из кэша или из БД, если кэш пуст. """

    if not CACHE_ENABLED:
        return Blog.objects.all()
    key = "blogs_list"
    blogs = cache.get(key)
    if blogs is not None:
        return blogs
    blogs = Blog.objects.all()
    cache.set(key, blogs)
    return blogs
