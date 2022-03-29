from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title.capitalize()) is not None:
        return render(request, "encyclopedia/entry.html", {
            "title": util.get_entry(title.capitalize())
        })
    elif util.get_entry(title.upper()) is not None:
        return render(request, "encyclopedia/entry.html", {
            "title": util.get_entry(title.upper())
        })
    else:
        return render(request, "encyclopedia/error.html")
