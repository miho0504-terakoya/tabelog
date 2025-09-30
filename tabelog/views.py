from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Restaurant

def restaurant_list(request):
    #全軒取得
    restaurants = Restaurant.objects.all().order_by("-open_date")
    
    #駅名フィルター
    station = request.GET.get("station")
    if station:
        restaurants = restaurants.filter(station__icontains=station)
        
    #ジャンルフィルター
    genre = request.GET.get("genre")
    if genre:
        restaurants = restaurants.filter(genre__icontains=genre)
    
    #フリーワード検索(名前・ジャンル)
    q = request.GET.get("q")
    if q:
        restaurants = restaurants.filter(name__icontains=q) | restaurants.filter(genre__icontains=q)
        
        
    
    return render(request, "restaurant_list.html", {
        "restaurants": restaurants,
        "station": station or "",
        "genre": genre or "",
        "q": q or ""
        })




class TopView(TemplateView):
    template_name = "top.html"
