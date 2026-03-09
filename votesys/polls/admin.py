from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
  model = Choice
  extra = 3

class QuestionAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {"fields": ["question_text"]}),  # ← removed pub_date section
  ]
  inlines = [ChoiceInline]
  list_display = ["question_text", "pub_date", "was_published_recently"]
  list_per_page = 20
  search_fields = ["question_text"]

admin.site.register(Question, QuestionAdmin)