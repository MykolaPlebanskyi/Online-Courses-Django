from django.shortcuts import render
from collections import Counter
from courses.models import PlacementQuestion, PlacementAnswer, Course, PlacementTest
from courses.forms import PlacementTestForm
from django.shortcuts import render, get_object_or_404, redirect, reverse



# def placement_test_view(request):
#     test = PlacementTest.objects.first()  # Беремо тест
#     questions = PlacementQuestion.objects.filter(test=test)
#
#     if request.method == 'POST':
#         form = PlacementTestForm(request.POST, questions=questions)
#         if form.is_valid():
#             user_answers = {q: PlacementAnswer.objects.get(id=int(a)) for q, a in form.cleaned_data.items()}
#             levels = [ans.question.level for ans in user_answers.values() if ans.is_correct]
#
#             if levels:
#                 recommended_level = Counter(levels).most_common(1)[0][0]  # Визначаємо найчастіший рівень
#                 recommended_courses = Course.objects.filter(level=recommended_level)
#
#                 return render(request, 'test_result.html', {'courses': recommended_courses, 'level': recommended_level})
#
#     else:
#         form = PlacementTestForm(questions=questions)
#
#     return render(request, 'placement_test.html', {'form': form})

def select_language(request):
    languages = PlacementTest.LANGUAGES  # Отримуємо список мов
    return render(request, 'courses/select_language.html', {'languages': languages})


def placement_test(request, language):
    test = get_object_or_404(PlacementTest, language=language)
    return render(request, 'courses/placement_test.html', {'test': test})


# def placement_take_test(request, language):
#     test = get_object_or_404(PlacementTest, language=language)
#     questions = test.questions.all()
#
#     if request.method == 'POST':
#         score = 0
#         total_questions = questions.count()
#
#         for question in questions:
#             selected_answer_id = request.POST.get(f'question_{question.id}')
#             if selected_answer_id:
#                 try:
#                     selected_answer = PlacementAnswer.objects.get(id=selected_answer_id)
#                     if selected_answer.is_correct:
#                         score += 1
#                 except PlacementAnswer.DoesNotExist:
#                     pass  # Якщо відповідь не знайдена, просто пропускаємо
#
#         # Визначаємо рівень знань
#         if score <= 4:
#             level = "Beginner (A1)"
#             description = [
#                 "Мінімальний запас слів",
#                 "Розуміння простих фраз",
#                 "Можливість представитися та відповісти на прості запитання"
#             ]
#         elif score <= 7:
#             level = "Elementary (A2)"
#             description = [
#                 "Розуміння базової граматики",
#                 "Можливість будувати прості речення",
#                 "Розуміння повсякденних ситуацій"
#             ]
#         elif score <= 11:
#             level = "Pre-Intermediate (B1)"
#             description = [
#                 "Більш впевнене використання граматики",
#                 "Можливість підтримувати розмову",
#                 "Читання простих текстів та розуміння загального сенсу"
#             ]
#         elif score <= 15:
#             level = "Intermediate (B2)"
#             description = [
#                 "Гарне володіння мовою",
#                 "Використання складніших граматичних конструкцій",
#                 "Вміння висловлювати думки на різні теми"
#             ]
#         elif score <= 18:
#             level = "Upper-Intermediate (C1)"
#             description = [
#                 "Високий рівень володіння мовою",
#                 "Вільне спілкування без значних помилок",
#                 "Розуміння складних текстів та абстрактних понять"
#             ]
#         else:
#             level = "Proficient (C2)"
#             description = [
#                 "Володіння мовою майже на рівні носія",
#                 "Використання ідіом, складних конструкцій",
#                 "Читання та розуміння наукових та художніх текстів"
#             ]
#
#         # Відображаємо результат з рівнем
#         return render(request, 'courses/placement_test_result.html', {
#             'score': score,
#             'total_questions': total_questions,
#             'test': test,
#             'level': level,
#             'description': description
#         })
#
#     return render(request, 'courses/placement_test.html', {'test': test, 'questions': questions})
from django.shortcuts import get_object_or_404, render
from courses.models import Course, PlacementTest, PlacementAnswer

def placement_take_test(request, language):
    profile = request.user.profile  # Отримуємо профіль користувача
    test = get_object_or_404(PlacementTest, language=language)
    questions = test.questions.all()

    if request.method == 'POST':
        score = 0
        total_questions = questions.count()

        for question in questions:
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                try:
                    selected_answer = PlacementAnswer.objects.get(id=selected_answer_id)
                    if selected_answer.is_correct:
                        score += 1
                except PlacementAnswer.DoesNotExist:
                    pass  # Якщо відповідь не знайдена, пропускаємо

        # Визначаємо рівень знань
        levels = [
            (4, "a1", "Beginner (A1)", ["Мінімальний запас слів", "Розуміння простих фраз"]),
            (7, "a2", "Elementary (A2)", ["Розуміння базової граматики", "Можливість будувати прості речення"]),
            (11, "b1", "Pre-Intermediate (B1)", ["Більш впевнене використання граматики", "Можливість підтримувати розмову"]),
            (15, "b2", "Intermediate (B2)", ["Гарне володіння мовою", "Використання складних конструкцій"]),
            (18, "c1", "Upper-Intermediate (C1)", ["Вільне спілкування без значних помилок", "Розуміння складних текстів"]),
            (100, "c2", "Proficient (C2)", ["Володіння мовою майже на рівні носія", "Розуміння наукових текстів"])
        ]

        level_code = "a1"
        level_name = "Beginner (A1)"
        description = ["Мінімальний запас слів", "Розуміння простих фраз"]

        for threshold, code, name, desc in levels:
            if score <= threshold:
                level_code, level_name, description = code, name, desc
                break

        # Знайти відповідний курс
        recommended_course = Course.objects.filter(level=level_code, language=language, active=True).first()
        if not profile.start_test:
            profile.coins = 200 + profile.coins
            profile.start_test = True
        profile.save()

        return render(request, 'courses/placement_test_result.html', {
            'score': score,
            'total_questions': total_questions,
            'test': test,
            'level': level_name,
            'description': description,
            'recommended_course': recommended_course
        })

    return render(request, 'courses/placement_test.html', {'test': test, 'questions': questions})
