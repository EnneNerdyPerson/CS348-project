from django.contrib import admin
from django.urls import include,path
from django.urls import path

from . import views

app_name = "helloworld"

urlpatterns = [
    path("", views.index, name=""),
    path("name", views.get_name, name="get_state"),
    path("state-name", views.state_name, name="state_name"),
    path("state/<str:region_list>-<str:type_list>-<str:state_list>", views.state, name="state"),
    
    path("landmark_get/<str:states_picked_list>-<str:type_list>", views.landmark_get, name="landmark_get"),
    path("landmark_sort/<str:states_picked_list>-<str:type_list>-<str:landtype_list>-<str:start>-<str:end>", views.landmark_sort, name="landmark_sort"),
    
    path("resturant_get/<str:states_picked_list>-<str:type_list>", views.resturant_get, name="resturant_get"),
    path("resturant_sort/<str:states_picked_list>-<str:type_list>-<str:price_range>-<str:rating>-<str:start>-<str:end>-<str:cusine>", views.resturant_sort, name="resturant_sort"),
    
    path("activity_get/<str:states_picked_list>-<str:type_list>", views.activity_get, name="activity_get"),
    path("activity_sort/<str:states_picked_list>-<str:type_list>-<str:activity_type>-<str:keyword>", views.activity_sort, name="activity_sort"),

    path("edit-landmark", views.edit_landmark, name="edit-landmark"),
    path("edit_landmark_get", views.edit_landmark_get, name="edit-landmark_get"),
    path("edit_landmark_edit/<str:name>", views.edit_landmark_edit, name="edit_landmark_edit"),
    path("add_edit_landmark/<str:name>-<str:state>-<str:city>-<str:landtype>-<str:price>-<str:start>-<str:end>", views.add_edit_landmark, name="add_edit_landmark"),

    path("edit-resturant", views.edit_resturant, name="edit-resturant"),
    path("edit_resturant_get", views.edit_resturant_get, name="edit-resturant_get"),
    path("edit_resturant_edit/<str:name>", views.edit_resturant_edit, name="edit_resturant_edit"),
    path("add_edit_resturant/<str:name>-<str:state>-<str:city>-<str:type>-<str:price>-<str:rating>-<str:start>-<str:end>", views.add_edit_resturant, name="add_edit_resturant"),

    path("edit-activity", views.edit_activity, name="edit-activity"),
    path("edit_activity_get", views.edit_activity_get, name="edit_activity_get"),
    path("edit_activity_edit/<str:name>", views.edit_activity_edit, name="edit_activity_edit"),
    path("add_edit_activity/<str:name>-<str:state>-<str:city>-<str:type>-<str:description>", views.add_edit_activity, name="add_edit_activity")
    #name, state, city, type, price, rating, start, end
    # ex: /polls/5/
    # path("<str:name>/", views.sort, name="sort"),
    #price_range, rating, start, end, cusine
]