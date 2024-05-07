from django.contrib.auth.models import User
from django.db import models

from testing import consts


class Question(models.Model):
    text = models.TextField('текст вопроса')
    difficulty = models.CharField('сложность вопроса', max_length=20, choices=consts.DIFFICULTY_CHOICES)

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        verbose_name='вопросы',
        on_delete=models.CASCADE,
        related_name='answers',
    )
    text = models.CharField('текст', max_length=255)
    is_correct = models.BooleanField('является верным', default=False)
    image = models.ImageField('картинка', upload_to='answer_images/', null=True, blank=True)

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'

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
    title = models.CharField('название', max_length=255)
    description = models.TextField('описание', max_length=255, blank=True, null=True)
    questions = models.ManyToManyField(Question, verbose_name='вопросы', related_name='tests')
    users = models.ManyToManyField(User, verbose_name='пользователи', related_name='tests', through='UserTest')
    status = models.CharField('статус', max_length=20, choices=consts.STATUS_CHOICES, default=consts.ACTIVE)
    duration_minutes = models.PositiveIntegerField('продолжительность', default=30)
    created_at = models.DateTimeField('дата создания', auto_now_add=True)
    image = models.ImageField('картинка', upload_to='test_images/', null=True, blank=True)
    # type_criterion = models.ForeignKey(
    #     TypeCriterion, on_delete=models.SET_NULL, null=True, blank=True
    # )

    class Meta:
        verbose_name = 'тест'
        verbose_name_plural = 'тесты'

    def __str__(self):
        return self.title

    @property
    def get_total_questions(self):
        return self.questions.count()


class UserTest(models.Model):
    user = models.ForeignKey(User, verbose_name='пользователи', related_name='usertests', on_delete=models.CASCADE)
    test = models.ForeignKey(Test, verbose_name='тесты', related_name='usertests', on_delete=models.CASCADE)
    completed = models.BooleanField('завершен', default=False)
    start_time = models.DateTimeField('время начала', null=True, blank=True)
    end_time = models.DateTimeField('время завершения', null=True, blank=True)

    class Meta:
        verbose_name = 'результат теста пользователя'
        verbose_name_plural = 'результаты тестов пользователей'
        unique_together = ['user', 'test']

    def __str__(self):
        return f'{self.user.username} - {self.test.title} - {"Пройдено" if self.completed else "Не пройдено"}'


class UserTestResult(models.Model):
    user_test = models.ForeignKey(
        UserTest,
        verbose_name='пользователь-тест',
        related_name='usertestresults',
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        Question,
        verbose_name='вопрос',
        related_name='userteststesults',
        on_delete=models.CASCADE,
    )
    selected_answer = models.ForeignKey(
        Answer,
        verbose_name='выбранный ответ',
        related_name='userstestresults',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_correct = models.BooleanField(null=True, blank=True)

    class Meta:
        verbose_name = 'результат по вопросу'
        verbose_name_plural = 'результаты по вопросам'

    def __str__(self):
        return f'{self.user_test.user.username} - {self.user_test.test.title} - {self.question.text}'
