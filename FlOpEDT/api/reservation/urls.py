from rest_framework import routers
from api.reservation import views

routerReservation = routers.SimpleRouter()

routerReservation.register(r'reservation', views.ReservationViewSet, basename='reservation')
