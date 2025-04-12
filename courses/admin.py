from django.contrib import admin
from courses.models import Course, UserCourse, Learning, Video, Test, Question, Answer, CouponCode, Profile, Settings, \
    PlacementTest, PlacementQuestion, PlacementAnswer
from django.utils.html import format_html


# Register your models here.

class VideoAdmin(admin.TabularInline):
    model = Video


class LearningAdmin(admin.TabularInline):
    model = Learning


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4  # Кількість полів для введення відповідей


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = [AnswerInline]
    extra = 1  # Відображати по замовчуванню одне поле для питання при створенні/редагуванні


class QuestionInline(admin.TabularInline):
    model = Question
    inlines = [AnswerInline]
    extra = 1


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


class TestInline(admin.TabularInline):
    model = Test
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LearningAdmin, VideoAdmin, TestInline]  # Додано TestInline сюди
    list_display = ["name", 'get_price', 'get_discount', 'active']
    list_filter = ("discount", 'active')

    def get_discount(self, course):
        return f'{course.discount} %'

    def get_price(self, course):
        return f' {course.price} ₴'

    get_discount.short_description = "Discount"
    get_price.short_description = "Price"


# class PaymentAdmin(admin.ModelAdmin):
#     model = Payment   
#     list_display = ["order_id", 'get_user', 'get_course', 'status'] 
#     list_filter = ["status", 'course']

#     def get_user(self, payment):
#         return format_html(f"<a target='_blank' href='/admin/auth/user/{payment.user.id}'>{payment.user}</a>")

#     def get_course(self, payment):
#         return format_html(f"<a target='_blank' href='/admin/courses/course/{payment.course.id}'>{payment.course}</a>")

#     get_course.short_description = "Course"
#     get_user.short_description = "User"

class UserCourseAdminModel(admin.ModelAdmin):
    model = UserCourse
    list_display = ['click', 'get_user', 'get_course']
    list_filter = ['course']

    def get_user(self, usercourse):
        return format_html(f"<a target='_blank' href='/admin/auth/user/{usercourse.user.id}'>{usercourse.user}</a>")

    def click(self, usercourse):
        return "Click to Open"

    def get_course(self, usercourse):
        return format_html(
            f"<a target='_blank' href='/admin/courses/course/{usercourse.course.id}'>{usercourse.course}</a>")

    get_course.short_description = "Course"
    get_user.short_description = "User"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_test', 'balance', 'coins')


@admin.register(Settings)
class ProfileAdmin(admin.ModelAdmin):
    # list_display = ('user', 'balance', 'coins')
    model = Settings


class PlacementAnswerInline(admin.TabularInline):  # Відображення відповідей у вигляді таблиці
    model = PlacementAnswer
    extra = 4  # Додає одну порожню відповідь для зручного заповнення


@admin.register(PlacementQuestion)
class QuestionAdmin(admin.ModelAdmin):
    model = PlacementQuestion
    inlines = [PlacementAnswerInline]
    extra = 1  # Відображати по замовчуванню одне поле для питання при створенні/редагуванні


class PlacementQuestionInline(admin.TabularInline):
    model = PlacementQuestion
    inlines = [PlacementAnswerInline]
    extra = 1


@admin.register(PlacementTest)
class TestAdmin(admin.ModelAdmin):
    inlines = [PlacementQuestionInline]


class PlacementTestInline(admin.TabularInline):
    model = PlacementTest
    extra = 1



