from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from .views import (
    AboutView,
    ApiOrderView,
    ApiReserveView,
    ContactView,
    DeliveryView,
    HomeView,
    MenuView,
    ReservationView,
    ServiceDetailView,
    ServicesListView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('about/', AboutView.as_view(), name='about'),
    path('posluhy/', ServicesListView.as_view(), name='services'),
    path('posluhy/<slug:slug>/', ServiceDetailView.as_view(), name='service_detail'),
    path('broniuvannia/', ReservationView.as_view(), name='reservation'),
    path('dostavka/', DeliveryView.as_view(), name='delivery'),
    path('kontakty/', ContactView.as_view(), name='contacts'),
    # API endpoints for AJAX
    path('api/reserve/', ApiReserveView.as_view(), name='api_reserve'),
    path('api/order/', ApiOrderView.as_view(), name='api_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
