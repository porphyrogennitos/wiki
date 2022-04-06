from django.shortcuts import render
from django import forms    

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    if util.get_entry(entry.capitalize()) is not None:
        return render(request, "encyclopedia/entry.html", {
            "entry": util.get_entry(entry.capitalize()),
            "title": entry.capitalize()
        })
    elif util.get_entry(entry.upper()) is not None:
        return render(request, "encyclopedia/entry.html", {
            "entry": util.get_entry(entry.upper()),
            "title": entry.upper()
        })
    else:
        return render(request, "encyclopedia/error.html")

def search(request):
    q = request.GET.get("q")

    if util.get_entry(q.capitalize()):
        return render(request, "encyclopedia/entry.html", {
            "entry": util.get_entry(q.capitalize()),
            "title": q.capitalize()
        })
    elif util.get_entry(q.upper()):
        return render(request, "encyclopedia/entry.html", {
            "entry": util.get_entry(q.upper()),
            "title": q.upper()
        })
    else:
        entries = []

        for entry in util.list_entries():
            if q in entry.lower():
                entries.append(entry)

        return render(request, "encyclopedia/list.html", {
            "entries": entries,
        })