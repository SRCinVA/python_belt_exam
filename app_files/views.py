from django.shortcuts import render, redirect
from .models import User, Quote
from django.contrib import messages

def index(request):
    return render(request, "index.html")

def register(request):
    results = User.objects.register(request.POST) 
    if isinstance(results, User):                        
        request.session['user_id'] = results.id   
        messages.add_message(request, messages.SUCCESS, 'Welcome to our site, {}'.format(results.alias))
        return redirect("/") 
    else:                                        
        for key in results:                       
            messages.add_message(request, messages.ERROR, results[key]) 
        return redirect("/")

def login(request):
    results = User.objects.login(request.POST)
    if isinstance(results, User):
        request.session['user_id'] = results.id   
        messages.add_message(request, messages.SUCCESS, "Welcome back,{}".format(results.name))
        return redirect("/show_dashboard")
    else:
        for key in results:
            messages.add_message(request, messages.ERROR, results[key])
        return redirect("/")

def show_dashboard(request):
    fav_quotes = User.objects.get(id=request.session["user_id"]).fav_quotes.all()
    quotes = Quote.objects.all()
    for quote in fav_quotes:
        quotes = quotes.exclude(id=quote.id)
    return render(request, "dashboard.html", {"quotes": quotes, "fav_quotes": fav_quotes}) 

def logout(request):
    request.session.clear()
    return redirect('/')

# def add_item_button_in_dashboard(request):
#     return redirect('/redirect_to_create')

# def redirect_to_create(request):
#     return render(request, "create.html")

def add_thing_in_dashboard(request):
    results = Quote.objects.add_quote(request.POST, request.session['user_id'])
    print(results)

    if isinstance(results, Quote):
        messages.add_message(request, messages.SUCCESS, 'You successfully added a quote')
        return redirect('/show_dashboard')
    else:
        for key in results:
            messages.add_message(request, messages.ERROR, results[key])
    return redirect('/show_dashboard')

# def deleting_items_by_user(request):
#     Item.objects.filter(request.POST, request.session['user_id']).delete()
#     return redirect('/items')

def your_favorites(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    user = User.objects.get(id=request.session['user_id'])
    quote.favs.remove(user)
    return redirect("/show_dashboard")

def quotable_quotes(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    user = User.objects.get(id=request.session['user_id'])
    quote.favs.add(user)
    return redirect("/show_dashboard")

def userInfo(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        "user":user
    }
    return render(request,"userInfo.html",context)