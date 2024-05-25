#importing libraries
from random import randint

from django.shortcuts import render

from django.shortcuts import redirect

from . import util

from django import forms

from markdown2 import Markdown

mk = Markdown()

#defining classes

class Entry(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your title here'}),label='')
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Type your content here','rows':20, 'cols':20}),label='')

class Search(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search'}))

class Edit(forms.Form):
     content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Type your content here','rows':20, 'cols':20}), label='')


#defining functions

def index(request):
    entries = util.list_entries()
    searched = []
    if request.method == 'POST':
         item = Search(request.POST)
         if item.is_valid():
            title = item.cleaned_data["title"]
            for entry in entries:    
                if title in entries:
                    return HttpResponseRedirect(f"wiki/{title}")
                if title.lower() in entry.lower():
                    searched.append(entry)
            context={
                "searched":searched,
                "search":Search(),
                "title":title
            }
            return render(request,"encyclopedia/search.html",context)
    else:
        context={
               "search": Search(),
                "entries": util.list_entries()
            }
        return render(request, "encyclopedia/index.html", context)

def create(request):
    if request.method == 'POST':
         entry = Entry(request.POST)
         if entry.is_valid():
              title = entry.cleaned_data["title"]
              content = entry.cleaned_data["content"]
              entries= [entry.lower() for entry in util.list_entries()]
              if title.lower() in entries:
                   context={
                            "search": Search(),
                            "message": "The page already exists"
                            }
                   return render(request, "encyclopedia/error.html",context)
              else:
                   util.save_entry(title,content)
                   context={
                        "search": Search(),
                        "title":title,
                        "content":content
                   }
                   return render(request, "encyclopedia/entry.html",context)
    context={
                "search": Search(),
                "entry": Entry() 
            }
    return render(request, "encyclopedia/create.html",context)

def view_entry(request,title):
    entries= [entry.lower() for entry in util.list_entries()]
    if title.lower() in entries:
            content = mk.convert(util.get_entry(title))
            context = {
                    "search": Search(),
                    "content": content,
                    "title":title
                    }
            return render(request, "encyclopedia/entry.html", context)
    else:
         context={
              "search": Search(),
              "message": "The requested page not found"
                }
         return render(request, "encyclopedia/error.html",context)
    

def edit_entry(request, title):
    if request.method == 'GET':
        content = util.get_entry(title)
        if content is None:
            context = {
                "search": Search(),
                "message": "The requested page not found"
            }
            return render(request, "encyclopedia/error.html", context)
        
        context = {
            "search": Search(),
            "content": Edit(initial={'content': content}),
            "title": title
        }
        return render(request, "encyclopedia/edit.html", context)
    elif request.method == 'POST':
        entry_edit = Edit(request.POST)
        if entry_edit.is_valid():
            content = entry_edit.cleaned_data["content"]
            util.save_entry(title, content)
            content = mk.convert(util.get_entry(title))
            context = {
                "search": Search(),
                "content": content,
                "title": title
            }
            return render(request, "encyclopedia/entry.html", context)
    else:
        # Handle other request methods (e.g., PUT, DELETE) or invalid requests
        context = {
            "search": Search(),
            "message": "Invalid request method"
        }
        return render(request, "encyclopedia/error.html", context)
    
def random(request):
    if request.method == 'GET':
        entries = util.list_entries()
        num = randint(0,len(entries)-1)
        random_page = entries[num]
        return redirect("wiki:entry",random_page)