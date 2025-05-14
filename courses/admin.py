from courses.models import Course, UserCourse, Learning, Video, Test, Question, Answer, CouponCode, Profile, Settings, \
    PlacementTest, PlacementQuestion, PlacementAnswer
from django.utils.html import format_html
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .forms import RegistrationForm


class VideoAdmin(admin.TabularInline):
    model = Video


class LearningAdmin(admin.TabularInline):
    model = Learning


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    fields = ['text', 'is_correct']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'get_tests']
    search_fields = ['text']
    inlines = [AnswerInline]

    def get_tests(self, obj):
        return ", ".join([test.name for test in obj.tests.all()])

    get_tests.short_description = 'Використовується в тестах'


class TestQuestionInline(admin.TabularInline):
    model = Test.questions.through
    extra = 1
    verbose_name = "Питання"
    verbose_name_plural = "Питання"


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_courses', 'get_question_count']
    search_fields = ['name']
    inlines = [TestQuestionInline]
    exclude = ['questions']

    def get_courses(self, obj):
        return ", ".join([course.name for course in obj.courses.all()])

    get_courses.short_description = 'Курси'

    def get_question_count(self, obj):
        return obj.questions.count()

    get_question_count.short_description = 'Кількість питань'


class CourseTestInline(admin.TabularInline):
    model = Course.tests.through
    extra = 1
    verbose_name = "Тест"
    verbose_name_plural = "Тести"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LearningAdmin, VideoAdmin, CourseTestInline]  # Додано TestInline сюди
    list_display = ["name", 'get_price', 'get_discount', 'active']
    list_filter = ("discount", 'active')

    def get_discount(self, course):
        return f'{course.discount} %'

    def get_price(self, course):
        return f' {course.price} ₴'

    get_discount.short_description = "Discount"
    get_price.short_description = "Price"


class UserCourseAdminModel(admin.ModelAdmin):
    model = UserCourse
    list_display = ['click', 'get_user', 'get_course']
    list_filter = ['course']

    def get_user(self, usercourse):
        return format_html(f"<a target='_blank' href='/admin/auth/user/{usercourse.profile.user.id}'>{usercourse.profile.user}</a>")

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
class ProfileAdminSettings(admin.ModelAdmin):
    model = Settings


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профіль'
    fk_name = 'user'

    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False


class UserAdmin(BaseUserAdmin):
    form = RegistrationForm
    add_form = RegistrationForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )

    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')
    list_select_related = ('profile',)

    def get_role(self, instance):
        return instance.profile.role

    get_role.short_description = 'Роль'


admin.site.unregister(User)

admin.site.register(User, UserAdmin)
admin.site.register(CouponCode)
admin.site.register(UserCourse, UserCourseAdminModel)


class PlacementAnswerInline(admin.TabularInline):
    model = PlacementAnswer
    extra = 4


@admin.register(PlacementQuestion)
class PlacementQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'get_tests')
    search_fields = ('text',)
    inlines = [PlacementAnswerInline]

    def get_tests(self, obj):
        return ", ".join([test.name for test in obj.tests.all()])

    get_tests.short_description = 'Тести'


class PlacementQuestionInline(admin.TabularInline):
    model = PlacementTest.questions.through
    extra = 20
    verbose_name = "Питання"
    verbose_name_plural = "Питання"


@admin.register(PlacementTest)
class PlacementTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'language', 'get_question_count')
    list_filter = ('language',)
    search_fields = ('name',)
    exclude = ('questions',)
    inlines = [PlacementQuestionInline]

    def get_question_count(self, obj):
        return obj.questions.count()

    get_question_count.short_description = 'Кількість питань'


@admin.register(PlacementAnswer)
class PlacementAnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('text', 'question__text')
