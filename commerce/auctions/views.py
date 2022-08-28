from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import Form


def index(request):
    return render(request, "auctions/index.html", {
        "Listings": Listings.objects.all(),
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


def create(request):
    if request.method == "POST":
        form = Form(request.POST, request.FILES)
        if form.is_valid():
            # create the new bid object
            bid = Bids()
            bid.bid = form.cleaned_data['bid']
            bid.save()
            # save the data of the listing
            Listing = Listings()
            Listing.title = form.cleaned_data['title']
            Listing.description = form.cleaned_data['desc']
            Listing.picture = form.cleaned_data['pic']
            Listing.bid = bid
            Listing.save()
            # save the user that created the listing
            user = request.user
            user.created_listing.add(Listing)
            # don't need to use .save() with while saving
            # manytomany field

    else:
        form = Form()
    return render(request, "auctions/create.html", {'form': form})


def Listing(request, name):
    listing = Listings.objects.get(id=name)
    if request.method == "POST":
        data = request.POST
        print(data.get)
        # check if a bid was submitted
        if data.get('Bid'):
            bid_value = int(data.get('Bid'))
            # check if the bid is bigger than the current one
            if bid_value > listing.bid.bid:
                # save the current bid
                original_bid = listing.bid
                # create the new bid
                new_bid = Bids(bid=bid_value)
                new_bid.save()
                # relate this new bid with the user and listing
                user = User.objects.get(id=request.user.id)
                user.bids.remove(listing.bid)
                user.bids.add(new_bid)
                listing.bid = new_bid
                listing.save()
                # delete the original bid
                original_bid.delete()

        if data.get('close_listing'):
            winning_user = User.objects.get(bids=listing.bid)
            print(winning_user)

        if data.get('comment'):
            new_comment = Comments()
            new_comment.comment = data.get('comment')
            new_comment.save()
            listing.comments.add(new_comment)
    else:
        if request.GET.get('watch') == "Add to Watchlist":
            request.user.watchlist.add(listing)
        if request.GET.get('watch') == "Remove from Watchlist":
            request.user.watchlist.remove(listing)
    return render(request, "auctions/listing.html", {
        "Listing": listing,
    })


def watchlist(request):
    print(request.user.watchlist.all())
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all()
    })
