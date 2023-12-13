from django.shortcuts import render , redirect, get_object_or_404   
from courses.models import Course , Video , UserCourse, Test, Answer, Question
from django.shortcuts import HttpResponse
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.db.models import Q

@method_decorator(login_required(login_url='login'), name='dispatch')
class MyCoursesList(ListView):
    template_name = 'courses/my_courses.html'
    context_object_name = 'user_courses'

    def get_queryset(self):
        return UserCourse.objects.filter(
            user=self.request.user,
            course__active=True,
        )

@login_required(login_url='/login')
def coursePage(request, slug):
    course = get_object_or_404(Course, slug=slug)
    serial_number = request.GET.get('lecture')
    videos = course.video_set.all().order_by("serial_number")

    if serial_number is None:
        serial_number = 1 

    video = Video.objects.get(serial_number=serial_number, course=course)

    if (video.is_preview is False):
        if request.user.is_authenticated is False:
            return redirect("login")
        else:
            user = request.user
            try:
                user_course, created = UserCourse.objects.get_or_create(user=user, course=course)
                # Позначення, що користувач переглянув це відео
                user_course.viewed = True
                user_course.save()
            except:
                return redirect("check-out", slug=course.slug)
        
    context = {
        "course": course, 
        "video": video, 
        'videos': videos
    }
    return render(request, template_name="courses/course_page.html", context=context)

def take_test(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    try:
        test = Test.objects.get(course=course)
    except Test.DoesNotExist:
        test = None
    
    return render(request, 'courses/test_page.html', {'course': course, 'test': test})


# Ваша функція process_test
def process_test(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        total_questions = Question.objects.filter(test__course=course).count()
        correct_answers = 0

        # Логіка для перевірки правильних відповідей
        for question in Question.objects.filter(test__course=course):
            answer_ids = request.POST.getlist(f'question_{question.id}', [])
            correct_answers_count = Answer.objects.filter(question=question, is_correct=True).count()

            if len(answer_ids) == correct_answers_count:
                correct = True
                for answer_id in answer_ids:
                    if not Answer.objects.filter(id=answer_id, question=question, is_correct=True).exists():
                        correct = False
                        break
                if correct:
                    correct_answers += 1

        # Оцінка тесту
        percentage = round((correct_answers / total_questions) * 100, 2)
        incorrect_answers = total_questions - correct_answers
        
        if percentage == 100:
            user = request.user
            try:
                user_course = UserCourse.objects.get(user=user, course=course)
                user_course.status = 'Complete'  # Оновлюємо статус на 'Complete'
                user_course.save()
            except UserCourse.DoesNotExist:
                pass

        # Отримання питань та відповідей для курсу
        questions = Question.objects.filter(test__course=course)
        question_data = []

        for question in questions:
            correct_answers_for_question = Answer.objects.filter(question=question, is_correct=True)
            user_selected_answers_ids = request.POST.getlist(f'question_{question.id}', [])
            user_selected_answers = Answer.objects.filter(id__in=user_selected_answers_ids)
            answers = Answer.objects.filter(question=question)
            question_data.append({
                'question_text': question.text,
                'correct_answers': correct_answers_for_question,
                'answers': answers,
                'user_answers': user_selected_answers,
                'correct_answers_ids': [answer.id for answer in correct_answers_for_question],
            })

        # Поверніть результати тестування
        return render(request, 'courses/test_result.html', {
            'percentage': percentage,
            'correct_answers': correct_answers,
            'total_questions':total_questions,
            'incorrect_answers': incorrect_answers,
            'question_data': question_data,  # Додано дані про питання та відповіді
        })

    # Якщо метод не POST, направте користувача на іншу сторінку або виведіть помилку
    return redirect('home')


