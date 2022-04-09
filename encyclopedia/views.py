from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Content'}))


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
    elif util.get_entry(entry):
        return render(request, "encyclopedia/entry.html", {
            "entry": util.get_entry(entry),
            "title": entry
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "number": 404,
            "message": "Not found!"
        })


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


def new_page(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # Check if title exists
            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/error.html", {
                    "number": "",
                    "message": "This entry already exists"
                })
            else:
                # Save entry
                util.save_entry(title, content)

                return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
        else:
            return render(request, "encyclopedia/new-page", {
                "form": NewPageForm
            })
    else:
        return render(request, "encyclopedia/new-page.html", {
            "form": NewPageForm()
        })