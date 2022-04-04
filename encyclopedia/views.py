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
