from django.urls import path

from . import views

app_name = 'booking'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    path('hotels/', views.HotelsView.as_view(), name='hotels'),
    path('hotel/<int:pk>/', views.HotelDetailView.as_view(), name='hotel'),
    path('room/<int:pk>/', views.RoomDetailView.as_view(), name='room'),
    path('order/', views.OrderProcessingView.as_view(), name="order_process"),
    path('remove_order/', views.delete_order, name="remove-order"),
    path('faq/', views.FAQView.as_view(), name="faq"),
    path('hotel/<int:pk>/check-rooms/', views.RoomsView.as_view(), name="check-rooms"),
    path('search_hotel/', views.search_hotel, name="search-hotel"),
]
