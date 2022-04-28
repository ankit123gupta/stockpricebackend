from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import *


router = routers.DefaultRouter()
# for creating new user
router.register('signup', UserViewSet)

# to get filtered data
router.register('filter', FilterViewSet)

# for deleting data
router.register('delete', DeleteViewSet)

# Show all data grouped by company
router.register('showcategorizeddata', ShowDataViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # for searching in DB
    path('search/', SearchViewSet.as_view()),

    # add data using csv file
    path('uploadcsv', uploadCSV),

    # add data using json data
    path('uploadjson', uploadJSON),
]