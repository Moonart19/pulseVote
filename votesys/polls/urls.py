from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
  path("", views.IndexView.as_view(), name="index"),
  path("<int:pk>/", views.detail, name="detail"),
  path("<int:pk>/results/", views.results, name="results"),
  path("<int:question_id>/vote/", views.vote, name="vote"),
  path('share/<uuid:token>/', views.share_poll, name='share'),
  path('<int:question_id>/comment/', views.add_comment, name='add_comment'),
  path('<int:question_id>/react/', views.add_reaction, name='add_reaction'),
  path('create/', views.create_poll, name='create'),
]