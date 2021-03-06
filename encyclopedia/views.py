from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import markdown
from . import util
from django import forms
from django.urls import reverse
import random 

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def open(request, title):
    if util.get_entry(title) == None:
            return render(request, "encyclopedia/pagenotfound.html", {"title": title})
    else:
            markdowncontent = util.get_entry(title)
            content = markdown.markdown(markdowncontent)
            return render(request, "encyclopedia/entry-page.html", {
            "content": content,
            "title": title
         })


def search(request):
    title = str(request.GET['q'])
    entries = util.list_entries()
    for i in entries:
        if i == title:
            markdowncontent = util.get_entry(title)
            content = markdown.markdown(markdowncontent)
            return render(request, "encyclopedia/entry-page.html", {
            "content": content,
            "title": title
         })
    for i in entries:
        for j in range(10):
                substring = str(i[0:j])
                if substring == title:
                    return render (request, "encyclopedia/search.html", {"entry":i})
                elif substring.lower() == title.lower():
                    return render (request, "encyclopedia/search.html", {"entry":i})
     
    return render(request, "encyclopedia/pagenotfound.html", {"title": title})


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title:")
    content = forms.CharField(widget=forms.Textarea)


def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            #entry = form.cleaned_data["entry"]
            title = str(request.POST['title'])
            content = str(request.POST['content'])
            entries = util.list_entries()
            for i in entries:
                if i == title:
                    return HttpResponse("Error: Entry already present")    
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("title", args=[str(title)]))

    return render(request, "encyclopedia/create.html", {"form":NewEntryForm()})

def randompage(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    markdowncontent = util.get_entry(random_entry)
    content = markdown.markdown(markdowncontent)
    return render(request, "encyclopedia/entry-page.html", {"content": content, "title": random_entry})
            
class NewEditForm(forms.Form):
    #title = forms.CharField(label="Title:")
    content = forms.CharField(widget=forms.Textarea)

def edit(request, title):
    if request.method == "POST":
        form = NewEditForm(request.POST)
        if form.is_valid():
            content = str(request.POST['content'])   
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("title", args=[str(title)]))
    precontent = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {"form":NewEditForm(initial={'content': precontent}), "title":title})

