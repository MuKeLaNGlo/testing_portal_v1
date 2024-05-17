from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from testing.models import (Answer, Question, Test,
                            UserTest, UserTestResult, User, Tag)


class Answer(admin.StackedInline):
    model = Answer
    extra = 0


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личные данные', {'fields': ('first_name', 'last_name', 'patronymic')}),
        ('Доступы', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_interviewer')}),
        ('Активность', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': (
            'username',
            'password1',
            'password2',
        )}),
    )


admin.site.register(User, CustomUserAdmin)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = (Answer,)
    list_display = ("text", "difficulty")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


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
