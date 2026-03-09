from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
  # ex: /polls/
  path("", views.IndexView.as_view(), name="index"),
  # ex: /polls/5/
  # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
  path("<int:pk>/", views.detail, name="detail"),
  # ex: /polls/5/results
  path("<int:pk>/results/", views.ResultView.as_view(), name="results"),
  # ex: /polls/5/vote/
  path("<int:question_id>/vote/", views.vote, name="vote"),
  path('share/<uuid:token>/', views.share_poll, name='share'),
  path('<int:question_id>/comment/', views.add_comment, name='add_comment'),
  path('<int:question_id>/react/', views.add_reaction, name='add_reaction'),
]