from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.conf import settings
from . import views


urlpatterns = [
    
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addNewBid/<int:id>", views.newBid, name="addNewBid" ),
    path("addListing", views.addListing, name="addListing"),
    path('watchlist/<int:id>', views.watchlist, name="watchlist"),
    path('removelist/<int:id>', views.removelist, name="removelist"),
    path('closebid/<int:id>', views.closebid, name="closebid"),
    path('comment/<int:id>', views.comment, name="comment" ),
    path('listings/<int:id>', views.listing, name="listing"),
    path('watchpage/', views.watchpage, name="watchpage"),
    path('categories',views.categories, name="categories"),
    path('category/<name>',views.category, name="category"),


]


