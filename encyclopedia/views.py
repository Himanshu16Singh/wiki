import markdown2
import random
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from . import util


class NewPage(forms.Form):
    title = forms.CharField(label="Title")
    markdown_content = forms.\
        CharField(label="Markdown Content", widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def edit_page(request, TITLE):
    if request.method != "POST":
        entry = util.get_entry(TITLE)
        return render(request, "encyclopedia/editPage.html", {
            "entry": entry,
            "title": TITLE
        })
    else:
        text = request.POST.get("markValue")
        util.save_entry(TITLE, text)
        return HttpResponseRedirect(reverse("wiki:entry_page", args=[TITLE]))


def entry_page(request, TITLE):
    entry = util.get_entry(TITLE)
    if entry is not None:
        return render(request, "encyclopedia/entryPage.html", {
            "entry": markdown2.markdown(entry),
            "title": TITLE
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "status": 404
        })


def new_page(request):
    if request.method != "POST":
        return render(request, "encyclopedia/newPage.html", {
            "newpage": NewPage()
        })
    else:
        newpage = NewPage(request.POST)
        if newpage.is_valid():
            title = newpage.cleaned_data["title"]
            if(util.get_entry(title) is None):
                content = newpage.cleaned_data["markdown_content"]
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("wiki:entry_page", args=[title]))
            else:
                return render(request, "encyclopedia/error.html", {
                    "status": 500
                })


def random_page(request):
    return HttpResponseRedirect(reverse("wiki:entry_page", args=[random.choice(util.list_entries())]))


def search(request):
    query = request.POST.get("q")
    related_entry = []
    if util.get_entry(query):
        return HttpResponseRedirect(reverse("wiki:entry_page", args=[query]))
    else:
        all_entry = util.list_entries()
        for entry in all_entry:
            if query.lower() in entry.lower():
                related_entry.append(entry)

        if len(related_entry) is 0:
            return render(request, "encyclopedia/error.html", {
                "status": 404
            })
        else:
            return render(request, "encyclopedia/searchPage.html", {
                "related_entry": related_entry
            })
