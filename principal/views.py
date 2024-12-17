#encoding:utf-8
from principal.models import Usuario, Puntuacion, Pelicula,Categoria
from principal.populateDB import populate
from principal.forms import  UsuarioBusquedaForm, PeliculaBusquedaForm
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.conf import settings
from principal.recommendations import  transformPrefs, getRecommendations, topMatches
import shelve

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


# Funcion que carga en el diccionario Prefs todas las puntuaciones de usuarios a peliculas. Tambien carga el diccionario inverso
# Serializa los resultados en dataRS.dat

def loadDict():
    Prefs={}   # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataRS.dat")
    ratings = Puntuacion.objects.all()
    for ra in ratings:
        user = int(ra.idUsuario.idUsuario)
        itemid = int(ra.idPelicula.idPelicula)
        rating = float(ra.puntuacion)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf.close()


def populateDatabase(request):
    populate()
    logout(request)  # se hace logout para obligar a login cada vez que se vaya a poblar la BD
    return HttpResponseRedirect('/index.html')


def loadRS(request):
    loadDict()
    return HttpResponseRedirect('/index.html')

def index(request):
    return render(request, 'index.html')

def ViewGenders(request):
    categorias = Categoria.objects.all()
    return render(request, 'ver_categorias.html', {'categorias': categorias, 'STATIC_URL':settings.STATIC_URL})
