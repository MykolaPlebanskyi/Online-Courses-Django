from courses.models import Course, PlacementTest, PlacementAnswer
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required


def select_language(request):
    languages = PlacementTest.LANGUAGES  # Отримуємо список мов
    return render(request, 'courses/select_language.html', {'languages': languages})


@login_required(login_url='/login')
def placement_test(request, language):
    test = get_object_or_404(PlacementTest, language=language)
    return render(request, 'courses/placement_test.html', {'test': test})


def calculate_score(request, questions):
    score = 0
    for question in questions:
        selected_answer_id = request.POST.get(f'question_{question.id}')
        if selected_answer_id:
            try:
                selected_answer = PlacementAnswer.objects.get(id=selected_answer_id)
                if selected_answer.is_correct:
                    score += 1
            except PlacementAnswer.DoesNotExist:
                pass
    return score


def determine_level(score):
    levels = [
        (4, "a1", "Beginner (A1)", ["Мінімальний запас слів", "Розуміння простих фраз"]),
        (7, "a2", "Elementary (A2)", ["Розуміння базової граматики", "Можливість будувати прості речення"]),
        (11, "b1", "Pre-Intermediate (B1)",
         ["Більш впевнене використання граматики", "Можливість підтримувати розмову"]),
        (15, "b2", "Intermediate (B2)", ["Гарне володіння мовою", "Використання складних конструкцій"]),
        (18, "c1", "Upper-Intermediate (C1)", ["Вільне спілкування без значних помилок", "Розуміння складних текстів"]),
        (100, "c2", "Proficient (C2)", ["Володіння мовою майже на рівні носія", "Розуміння наукових текстів"])
    ]

    for threshold, code, name, desc in levels:
        if score <= threshold:
            return code, name, desc
    return "a1", "Beginner (A1)", ["Мінімальний запас слів", "Розуміння простих фраз"]


def update_profile_on_first_test(profile):
    if not profile.start_test:
        profile.coins += 200
        profile.start_test = True
        profile.save()


def placement_take_test(request, language):
    profile = request.user.profile
    test = get_object_or_404(PlacementTest, language=language)
    questions = test.questions.all()

    if request.method == 'POST':
        score = calculate_score(request, questions)
        total_questions = questions.count()

        level_code, level_name, description = determine_level(score)
        recommended_course = Course.objects.filter(level=level_code, language=language, active=True).first()

        update_profile_on_first_test(profile)

        return render(request, 'courses/placement_test_result.html', {
            'score': score,
            'total_questions': total_questions,
            'test': test,
            'level': level_name,
            'description': description,
            'recommended_course': recommended_course
        })

    return render(request, 'courses/placement_test.html', {'test': test, 'questions': questions})
