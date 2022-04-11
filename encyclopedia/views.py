from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random
import re

from . import util


class NewPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Title'}))
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={'placeholder': 'Content'}))


class EditPageForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea(), initial='')


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def markdown(entry):
    a = re.compile(r'(?P<hash>#{1,6}) (?P<heading>\w+)')
    # b = a.finditer(util.get_entry('Git'))
    b = a.finditer(entry)
    print(b)
    for match in b:
        if match.group('hash'):
            if len(match.group('hash')) == 1:
                entry = f'<h1>{match.group("heading")}</h1>'
            elif len(match.group('hash')) == 2:
                entry += f'<h2>{match.group("heading")}</h2>'
            elif len(match.group('hash')) == 3:
                entry += f'<h3>{match.group("heading")}</h3>'
            elif len(match.group('hash')) == 4:
                entry += f'<h4>{match.group("heading")}</h4>'
            elif len(match.group('hash')) == 5:
                entry += f'<h5>{match.group("heading")}</h5>'
            elif len(match.group('hash')) == 6:
                entry += f'<h6>{match.group("heading")}</h6>'
    return entry
    # print(entry)
        # entry += f'<h1>{match.group(1)}</h1>'
        # print(entry)
        # return entry
    # b = re.findall(r'# \w+', util.get_entry('Git'))
    # if b:
    #     # print('Match found: ', b.group())
    #     for match in b:
    #         print(f'<h1>{match}</h1>')
    # else:
    #     print('No match')

# markdown(util.get_entry('Git'))


def entry(request, entry):
    if util.get_entry(entry.capitalize()) is not None:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown(util.get_entry(entry.capitalize())),
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


def edit_page(request, title):
    if request.method == 'POST':
        form = EditPageForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data["content"]

            # Edit content
            util.save_entry(title, content)

            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title.lower()]))
        else:
            return render(request, "encyclopedia/edit-page.html", {
                "form": EditPageForm()
            })
    else:
        if util.get_entry(title.capitalize()):
            return render(request, "encyclopedia/edit-page.html", {
                "form": EditPageForm(initial={'content': util.get_entry(title.capitalize())}),
                "title": title
            })
        elif util.get_entry(title.upper()):
            return render(request, "encyclopedia/edit-page.html", {
                "form": EditPageForm(initial={'content': util.get_entry(title.upper())}),
                "title": title
            })
        else:
            return render(request, "encyclopedia/edit-page.html", {
                "form": EditPageForm(initial={'content': util.get_entry(title)}),
                "title": title
            })


def random_page(request):
    # Get random entry
    entry = random.choice(util.list_entries())

    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "entry": util.get_entry(entry)
    })