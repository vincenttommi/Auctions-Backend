from django.urls import path
from . import views 




urlpatterns= [
    path('signup/', views.signup),
    path('login/', views.login),
    path('test/', views.TestView),
    path('logout/',views.logout),
    path('list_auction_items/', views.list_auction_items),
    path('create_auction_item/', views.create_auction_item),
    path('update_auction_item/<int:pk>/', views.update_auction_item),
    path('delete_auction_item/<int:pk>/', views.delete_auction_item)
]