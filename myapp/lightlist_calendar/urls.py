from django.urls import path
from . import views

urlpatterns = [
    path('', views.Calendar.as_view(), name='calendar'),
    path('api/<int:month>/<int:year>/', views.CalendarApi.as_view(), name='calendar_api'),
    path('api/detail/<int:id>', views.CalendarDetailApi.as_view(), name='calendar_detail_api'),
    path('add/', views.AddCalendarItem.as_view(), name='add_calendar_item'),
]