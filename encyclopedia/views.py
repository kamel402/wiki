from django.forms.widgets import TextInput, Textarea
from django.shortcuts import render
from django import forms
from . import util
from django.urls import reverse
from django.http import HttpResponseRedirect, request
from markdown2 import Markdown
import random

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

class NewEdit(forms.Form):
    edit = forms.CharField(widget=forms.Textarea, label="Edit")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    search = request.GET.get('q')
    if util.get_entry(search) != None :
        return HttpResponseRedirect(f"{search}")
    else :
        substrings = []
        entries = util.list_entries()
        for entry in entries :
            if entry.find(search.upper()) != -1 or entry.find(search.capitalize()) != -1 or entry.find(search) != -1:
                substrings.append(entry)
        length = len(substrings)
    return render(request, "encyclopedia/search.html",{
        "title": search,
        "entries": substrings,
        "length": length
    })

def entry_page(request, name):
    if util.get_entry(name) != None :
        request.session["title"] = name
        markdowner = Markdown() 
        html = markdowner.convert(util.get_entry(name))
    else:
        html = None
    return render(request, "encyclopedia/entry_page.html",{
        "html": html,
        "title": name
    })

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) == None :
                util.save_entry(title,bytes(content, 'utf8'))
                return HttpResponseRedirect(f"{title}")
            else :
                return render(request, "encyclopedia/new_page.html", {
                    "error": 1
                })
    return render(request, "encyclopedia/new_page.html", {
        "error": 0,
        "form": NewPageForm()
    })
    
def edit(request):
    if request.method == "POST" :
        form = NewEdit(request.POST)
        if form.is_valid():
            title = request.session["title"]
            edit = form.cleaned_data["edit"]
            util.save_entry(title,bytes(edit, 'utf8'))
            return HttpResponseRedirect(f"{title}")
        else :
            return render(request, "encyclopedia/edit.html", {
                "form":form
            })
    title = request.session["title"]
    initial = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "form":NewEdit(initial={'edit': initial})  
    })

def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return HttpResponseRedirect(f"{title}")
