from django.contrib.auth.models import User
from django.db import models

from testing.consts import DIFFICULTY_CHOICES, STATUS_CHOICES


class Question(models.Model):
    text = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    image = models.ImageField(upload_to="answer_images/", null=True, blank=True)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.text


# class Criterion(models.Model):
#     name = models.CharField(max_length=255)
#     min_value = models.IntegerField()
#     max_value = models.IntegerField()

#     class Meta:
#         verbose_name = 'Критерий'
#         verbose_name_plural = 'Критерии'

#     def __str__(self):
#         return self.name


# class TypeCriterion(models.Model):
#     name = models.CharField(max_length=255)
#     criteria = models.ManyToManyField(Criterion, through='TypeCriterionRelation', related_name='type_criteria')

#     class Meta:
#         verbose_name = 'Тип критерия'
#         verbose_name_plural = 'Типы критериев'

#     def __str__(self):
#         return self.name


# class TypeCriterionRelation(models.Model):
#     type_criterion = models.ForeignKey(TypeCriterion, on_delete=models.CASCADE)
#     criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = 'Связь типа критерия с критерием'
#         verbose_name_plural = 'Связи типов критериев с критериями'


class Test(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)
    questions = models.ManyToManyField(Question, related_name="tests")
    users = models.ManyToManyField(User, through="UserTest")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Активен")
    duration_minutes = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="test_images/", null=True, blank=True)
    # type_criterion = models.ForeignKey(
    #     TypeCriterion, on_delete=models.SET_NULL, null=True, blank=True
    # )

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self):
        return self.title

    def get_total_questions(self):
        return self.questions.count()


class UserTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Результат теста пользователя"
        verbose_name_plural = "Результаты тестов пользователей"
        unique_together = ["user", "test"]

    def __str__(self):
        return f'{self.user.username} - {self.test.title} - {"Пройдено" if self.completed else "Не пройдено"}'


class UserTestResult(models.Model):
    user_test = models.ForeignKey(UserTest, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, null=True, blank=True
    )
    is_correct = models.BooleanField(null=True, blank=True)

    class Meta:
        verbose_name = "Результат по вопросу"
        verbose_name_plural = "Результаты по вопросам"

    def __str__(self):
        return f"{self.user_test.user.username} - {self.user_test.test.title} - {self.question.text}"
