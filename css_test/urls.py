from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'css_test'

urlpatterns = [
    path('', views.index, name='index'),
    # path('', include('css_test.urls') ),
    path("signup/", views.signup_view, name="signup"),
    path('login/', views.signin_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('mypage/', views.mypage_view, name='mypage'),  # 마이페이지 뷰 연결
    path('exhibition/<int:exhibition_id>/', views.exhibition_detail_view, name='exhibition_detail'),
    path('exhibition/<int:exhibition_id>/add_review/', views.add_review, name='add_review'), # 리뷰 작성 URL
    path('reserve/<int:exhibition_id>/', views.reserve_view, name='reserve'),
    path('reserve/success/', views.reserve_success_view, name='reserve_success'), # 예약 완료 페이지 URL 추가
]
