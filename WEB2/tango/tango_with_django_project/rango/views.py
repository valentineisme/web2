# coding: utf-8

from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from .models import Category, Page
from .forms import CategoryForm, PageForm

def index(request):
    context_dict = {}

    category_list = Category.objects.order_by('-likes')[:5] #categorias mais curtidas
    page_list = Page.objects.order_by('-views')[:5] #páginas mais visitadas

    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    return render(request, 'rango/index.html', context_dict)


def about(request):
    texto = '''
    <h2> Essa é a página About do Rango! </h2>
    <br/>
    <a href='/rango/'> Home </a>
    '''
    return HttpResponse(texto)


def category(request, category_name_slug):
    context_dict = {}
    context_dict['category_name_slug'] = category_name_slug

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category'] = category

        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages

    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    #TODO: Verificar se página já existe na categoria e não permitir adicionar novamente.

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return redirect('/rango/category/'+category_name_slug)
                #return category(request, category_name_slug)
        else:
            print(form.errors)
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)