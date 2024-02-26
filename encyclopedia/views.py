from django.shortcuts import render

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