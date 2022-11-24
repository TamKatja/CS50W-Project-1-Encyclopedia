import random

from django.shortcuts import redirect, render
from markdown2 import Markdown

from . import util

markdowner = Markdown()


def index(request):
    # List existing entries
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def display_entry(request, title):
    # Get entry content
    entry = util.get_entry(title)
    # Identify invalid title (i.e. no content retrieved)
    if entry == None:
        return render(request, "encyclopedia/error.html", { 
                "error_message": "Page not found."
        })
    # If valid, display entry matching title
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdowner.convert(entry)
        })

    
def search(request):
    # List existing entries
    entries = util.list_entries()
    # Get user query
    query = request.POST.get("q")
    # Iterate through existing entries
    for entry in entries:
        # Identify title matching user query
        if query.lower() == entry.lower():
            return redirect("display_entry", query)
    # No titles matching user query
    else:
        results = []
        count = 0
        # List existing entries with user query as substring 
        for entry in entries:
            if query.lower() in entry.lower():
                results.append(entry)
                count += 1
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "count": count,
            "entries": results
        })
 
    
def create(request):
    # User submits new entry
    if request.method == "POST":
        # Retrieve new title and content
        title = request.POST.get("title")
        content = request.POST.get("content")
        entries = util.list_entries()
        # Check title is unique
        for entry in entries:
            if title.lower() == entry.lower():
                # Display error message if title is not unique
                return render(request, "encyclopedia/error.html", { 
                        "error_message": "Oops, entry already exists."
                })
        # Save new entry
        util.save_entry(title, content)
        return redirect("display_entry", title)
    else:
        # User clicks "Create New Page"
        return render(request, "encyclopedia/create.html")

      
def edit(request, title):
    # User submits edited content
    if request.method == "POST":
        # Retrieve edited content
        content = request.POST.get("content")
        # Save edited content
        util.save_entry(title, content)
        # Redirect user to edited entry page
        return redirect("display_entry", title)
    else:
        # User clicks "Edit"
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
                "title": title,
                "content": content
        })

    
def random_entry(request):
    # Redirect user to random entry page
    return redirect("display_entry", random.choice(util.list_entries()))
