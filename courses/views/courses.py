from django.shortcuts import render, redirect, get_object_or_404
from courses.models import Course, Video, UserCourse, Test, Answer
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator


@method_decorator(login_required(login_url='login'), name='dispatch')
class MyCoursesList(ListView):
    template_name = 'courses/my_courses.html'
    context_object_name = 'user_courses'

    def get_queryset(self):
        return UserCourse.objects.filter(
            profile=self.request.user.profile,
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
            profile = request.user.profile
            try:
                user_course, created = UserCourse.objects.get_or_create(profile=profile, course=course)
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

    test = course.tests.first()

    context = {
        'course': course,
        'test': test
    }

    return render(request, 'courses/test_page.html', context)


def process_test(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        test_id = request.POST.get('test_id')

        if not test_id:
            return redirect('take_test', course_id=course_id)

        test = get_object_or_404(Test, pk=test_id)

        if test not in course.tests.all():
            return redirect('take_test', course_id=course_id)

        total_questions = test.questions.count()
        correct_answers = 0

        for question in test.questions.all():
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

        percentage = round((correct_answers / total_questions) * 100, 2) if total_questions > 0 else 0
        incorrect_answers = total_questions - correct_answers

        if percentage == 100:
            profile = request.user.profile
            try:
                user_course = UserCourse.objects.get(profile=profile, course=course)
                user_course.status = 'Complete'
                user_course.save()
            except UserCourse.DoesNotExist:
                pass

        question_data = []
        for question in test.questions.all():
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
            'total_questions': total_questions,
            'incorrect_answers': incorrect_answers,
            'question_data': question_data,
            'test': test,
            'course': course,
        })

    return redirect('home')


class CoursesPageView(ListView):
    template_name = "courses/courses.html"
    queryset = Course.objects.filter(active=True)
    context_object_name = 'courses'
