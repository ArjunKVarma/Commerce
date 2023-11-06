from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from auctions.models import Listings, Comments, bids
from datetime import datetime
from .models import User


def index(request):
    return render(request, "auctions/index.html",{
        "Listings" : Listings.objects.all().order_by('active'),
        
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def listing(request,id):
    item =  Listings.objects.get(pk = id)
    
    return render(request, "auctions/listings.html",{
        
        "Listing" : item,
        "comments" : Comments.objects.filter(Listing = item)
    })


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='/login')
def newBid(request,id):
    currentuser = request.user
    newbid = request.POST["bid"]
    listdata = Listings.objects.get(pk=id)

    
    
    if int(newbid) >= listdata.price:
        updateBid = bids(user = currentuser, value = int(newbid))
        updateBid.save()

        listdata.price = int(newbid)
        listdata.highest_bidder = currentuser.username
        listdata.save()
    else:
        return render(request,"auctions/listings.html", {
            "Listing" : listdata,
            "comments" : Comments.objects.filter(Listing = listdata),
            "message" : "Place a higher bid"
             })

    return render(request, "auctions/listings.html",{
        
        "Listing" : listdata,
        "comments" : Comments.objects.filter(Listing = listdata)
    })



@login_required(login_url='/login')
def addListing(request):
    cato = Listings.objects.values('category').distinct()
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        photo= request.POST['photo']
        owner = request.user
        category = request.POST["category"].lower()
        date = datetime.now()

        NewList = Listings(name= name, description = description,price = price, photo = photo, date = date,owner =owner, category = category)
        NewList.save()

        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "auctions/addListing.html",{
            "cato": cato
        })


@login_required(login_url='/login')
def watchlist(request,id):
    
    listobj = Listings.objects.get(pk = id)
    currentuser = request.user

    listobj.watchlist.add(currentuser)

    return render(request, "auctions/listings.html",{
        
        "Listing" : listobj,
        "comments" : Comments.objects.filter(Listing = listobj)
    })
    
    
@login_required(login_url='/login')
def removelist(request,id):
    listobj = Listings.objects.get(pk = id)
    currentuser = request.user

    listobj.watchlist.remove(currentuser)

    return render(request, "auctions/listings.html",{
        
        "Listing" : listobj,
        "comments" : Comments.objects.filter(Listing = listobj)
    })

    
@login_required(login_url='/login')
def closebid(request,id):
    listobj = Listings.objects.get(pk = id)

    listobj.active = False
    listobj.save()
    

    return HttpResponseRedirect(reverse('index'))


    
    
@login_required(login_url='/login')
def watchpage(request):
    user = request.user
    list = Listings.objects.filter(watchlist = user)
    
    
    return render(request, "auctions/watchlist.html", {
                'objects' : list
            })
    

    
@login_required(login_url='/login')
def comment(request,id):
    listobj = Listings.objects.get(pk = id)
    comment = request.POST['comment']
    user = request.user

    addcomment = Comments(User = user, Listing = listobj, Comment = comment)
    addcomment.save()
    
    return render(request, "auctions/listings.html",{
        
        "Listing" : listobj,
        "comments" : Comments.objects.filter(Listing = listobj)
    })


def categories(request):
    cato = Listings.objects.values('category').distinct()
    return render(request, "auctions/categories.html", {
                'cats' : cato
            })


def category(request,name):
    cat = name
    return render(request, "auctions/category.html", {
                'obs' : Listings.objects.filter(category=cat)
            })