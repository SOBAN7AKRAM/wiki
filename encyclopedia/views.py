from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util
import random
from django.shortcuts import redirect


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def displayEntry(request, name):
    entry = util.get_entry(name)
    if (entry):
        return render(request, "encyclopedia/entry.html", {
            "entries": entry,
            "title": name
        })
    else:
        return render(request, "encyclopedia/error.html",{
            "name" : name.upper()
        })
def search(request):
    name = request.GET.get('q')
    entry = util.get_entry(name)
    if (entry):
        return render(request, "encyclopedia/entry.html", {
            "entries": entry,
            "title": name.upper()
        })
    else:
        sublist = []
        list = util.list_entries()
        for i in list:
            if name.upper() in i.upper():
                sublist.append(i)
        return render(request, "encyclopedia/searchList.html", {
            "entries": sublist,
            "name": name
        })
class newPageForm(forms.Form):
    title = forms.CharField(
        label="Title:",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title of the page'}),
        required=True
        )
    textArea = forms.CharField(
        label="Markdown:",
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write Markdown here...'})
    )
def newPage(request):
    if request.method == "POST":
        form = newPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry = util.get_entry(title)
            content = form.cleaned_data["textArea"]
            if (entry):
                return render(request, "encyclopedia/already.html", {
                    "name" : title
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/newPage.html", {
                "form": form
            })
    return render(request, "encyclopedia/newPage.html", {
        "form": newPageForm(),
        "title": "New Page"
    })
class editPageForm(forms.Form):
    textArea = forms.CharField(
        label="Markdown:",
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
def editPage(request, name):
    if request.method == "POST":
        form = editPageForm(request.POST)
        if (form.is_valid()):
            content = form.cleaned_data["textArea"].strip()
            util.save_entry(name, content)
            return HttpResponseRedirect(reverse("entry", kwargs={'name': name}))
    
    else:
        entry = util.get_entry(name)
        entry = entry.strip()
        form = editPageForm(initial={'textArea': entry})
        return render(request, "encyclopedia/edit.html", {
            "title": name,
            "form": form,
        })
def getRandom(request):
    entries = util.list_entries()
    randomEntry = random.choice(entries)
    return redirect('entry', name = randomEntry)
    