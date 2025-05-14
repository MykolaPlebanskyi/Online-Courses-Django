from django.urls import path
from courses.views import MyCoursesList, HomePageView, coursePage, SignupView, LoginView, signout, checkout, \
    process_test, take_test, user_profile, CoursesPageView, exchange_coins, pay_with_balance, select_language, placement_test, placement_take_test
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('courses', CoursesPageView.as_view(), name='courses'),
    path('logout', signout, name='logout'),
    path('my-courses', MyCoursesList.as_view(), name='my-courses'),
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('course/<str:slug>', coursePage, name='coursepage'),
    path('check-out/<str:slug>', checkout, name='check-out'),
    path('course/<int:course_id>/test/', take_test, name='take_test'),
    path('process_test/<int:course_id>/', process_test, name='process_test'),
    path('profile/', user_profile, name='user_profile'),
    path('exchange/', exchange_coins, name='exchange_coins'),
    path('pay_with_balance/<int:course_id>/', pay_with_balance, name='pay_with_balance'),
    path('select-language/', select_language, name='select_language'),
    path('<str:language>/placement-test/', placement_test, name='placement_test'),
    path('<str:language>/placement-test/take/', placement_take_test, name='placement_take_test'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
