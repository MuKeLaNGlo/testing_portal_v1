from django.contrib import admin

from testing.models import (Answer, Question, Test,
                            UserTest, UserTestResult)


class Answer(admin.StackedInline):
    model = Answer
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = (Answer,)
    list_display = ("text", "difficulty")


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "created_at")
    search_fields = ("title",)
    list_filter = ("status", "created_at")


@admin.register(UserTest)
class UserTestAdmin(admin.ModelAdmin):
    list_display = ("user", "test", "completed", "start_time", "end_time")
    search_fields = ("user__username", "test__title")
    list_filter = ("completed", "test__title")


@admin.register(UserTestResult)
class UserTestResultAdmin(admin.ModelAdmin):
    list_display = ("user_test", "question", "selected_answer", "is_correct")
    search_fields = (
        "user_test__user__username",
        "user_test__test__title",
        "question__text",
    )
    list_filter = ("is_correct",)
