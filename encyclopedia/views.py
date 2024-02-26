from django.shortcuts import render
from django.http import HttpResponse
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def displayEntry(request, name):
    entry = util.get_entry(name)
    if (entry):
        return render(request, "encyclopedia/entry.html", {
            "entries": entry,
            "title": name.upper()
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