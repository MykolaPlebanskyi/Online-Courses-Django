
from django.contrib import admin
from django.urls import path , include
from courses.views import MyCoursesList, HomePageView, coursePage, SignupView, LoginView, signout, checkout, process_test, take_test, user_profile
# from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', HomePageView.as_view() , name = 'home'),
    path('logout', signout , name = 'logout'),
    path('my-courses', MyCoursesList.as_view() , name = 'my-courses'),
    path('signup', SignupView.as_view() , name = 'signup'),
    path('login', LoginView.as_view() , name = 'login'),
    path('course/<str:slug>', coursePage , name = 'coursepage'),
    path('check-out/<str:slug>', checkout , name = 'check-out'),
    path('course/<int:course_id>/test/', take_test, name='take_test'),
    path('process_test/<int:course_id>/', process_test, name='process_test'),
    path('profile/', user_profile, name='user_profile'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)