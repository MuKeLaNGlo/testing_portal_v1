from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from testing.models import Test, UserTest, UserTestResult


def home(request):
    all_tests = Test.objects.all().order_by("-created_at")
    if not request.user.is_anonymous:
        completed_tests_m2m = UserTest.objects.filter(user=request.user, completed=True)
        completed_tests = [item.test for item in completed_tests_m2m]

    tests = []
    for test in all_tests:
        item = {"test": test}
        item["questions_count"] = test.get_total_questions()

        if not request.user.is_anonymous and test in completed_tests:
            user_test = UserTest.objects.get(
                user=request.user, test=test, completed=True
            )
            user_test_results = UserTestResult.objects.filter(
                user_test=user_test, is_correct=True
            )
            item["completed"] = True
            item["right_questions"] = user_test_results.count()

        tests.append(item)

    context = {
        "tests": tests,
    }

    return render(request, "testing/home.html", context)


@login_required
def test(request, test_id):
    test = get_object_or_404(Test, id=test_id)

    # Проверяем, проходил ли пользователь уже этот тест
    user_test = UserTest.objects.filter(user=request.user, test=test).first()

    if user_test and user_test.completed:
        return redirect("testing:home")

    # Если пользователь еще не проходил тест, продолжаем обработку
    return render(request, "testing/test.html", {"test": test})


@login_required
def submit_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)

    if request.method == "POST":
        UserTest.objects.create(user=request.user, test=test, completed=True)
        # Проходим по вопросам и сохраняем результаты ответов пользователя
        for question in test.questions.all():
            answer_id = request.POST.get("question_{}".format(question.id))
            selected_answer = question.answers.get(pk=answer_id) if answer_id else None
            is_correct = selected_answer.is_correct if selected_answer else False

            # Создаем объект UserTestResult для сохранения результата по каждому вопросу
            UserTestResult.objects.create(
                user_test=UserTest.objects.get(user=request.user, test=test),
                question=question,
                selected_answer=selected_answer,
                is_correct=is_correct,
            )

        # Помечаем тест как пройденный для пользователя
        user_test = UserTest.objects.get(user=request.user, test=test)
        user_test.completed = True
        user_test.save()

        # messages.success(request, 'Тест успешно пройден!')
        return redirect("testing:home")

    # Если это не POST-запрос, например, GET-запрос, просто отображаем страницу теста
    return render(request, "testing/pass_test.html", {"test": test})
