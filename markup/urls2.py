from django.contrib import admin
from django.urls import path
from markup import views

urlpatterns = [
    path('polygon/', views.PolygonList.as_view()),  # Add polygons
    path('polygon/<int:pk>/', views.PolygonDetail.as_view()),  # Delete polygon at PK
    path('folders/<int:pk>/', views.ImageList.as_view()),  # Show images in category PK
    path('image/<int:pk>/polygons/', views.PolygonsInImage.as_view()),  # Show polygons in image PK
    path('comment/', views.CommentList.as_view()),  # Add comments
    path('comment/<int:pk>/', views.CommentDetail.as_view()),  # Delete/show comment at PK
    path('image/<int:pk>/comments/', views.CommentsInImage.as_view()),  # Show comments in image PK
    path('labels/', views.LabelList.as_view()),  # lists labels
    # show folders to a user. Does not show a folder which is empty/all of the contents are invisible.
]