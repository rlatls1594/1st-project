from django.db import models
from django.conf import settings # settings는 그대로 사용
from django.contrib.auth.models import AbstractUser # AbstractUser를 상속받음
# from django.contrib.auth.models import User  # 이 부분은 필요 없습니다!

import os

# Create your models here.
class Exhibition(models.Model):
    title = models.CharField("전시 제목", max_length=100)
    description = models.TextField("전시 설명")
    location = models.CharField("전시 장소", max_length=100)
    start_date = models.DateTimeField("시작일")
    end_date = models.DateTimeField("종료일")
    capacity = models.PositiveIntegerField("최대 예약 인원")
    file_upload = models.FileField("포스터/첨부파일", upload_to='exhibition/files/%Y/%m/%d/', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # AUTH_USER_MODEL 사용
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title
    
# Django의 기본 User 모델을 확장하여 사용
class CustomUser(AbstractUser): # 기존 'User' 클래스 이름을 'CustomUser'로 변경
    # username, email, password는 AbstractUser에 기본적으로 포함되어 있으므로
    # 특별히 변경할 사항이 없다면 여기서는 추가로 정의할 필요가 없습니다.
    # 만약 기존 AbstractUser의 필드(username, email)와 달리
    # email을 고유 ID로 사용하거나, 다른 필드를 추가하고 싶다면 여기에 정의합니다.
    # 예:
    # email = models.EmailField(unique=True, null=False, blank=False) # 이메일을 필수로 하고 유니크하게
    pass # 추가 필드가 없다면 pass

    def __str__(self):
        return self.username

# Customer 모델의 역할 재고:
# 만약 CustomUser가 모든 사용자 정보를 포함한다면 Customer 모델은 불필요할 수 있습니다.
# CustomUser 모델에 전화번호 같은 추가 정보를 넣거나,
# CustomUser와 OneToOneField로 연결된 UserProfile 같은 모델을 만드는 것이 좋습니다.
# 현재 Customer 모델이 단순히 이메일/전화번호 정보를 관리하는 용도라면,
# CustomUser에 해당 필드를 추가하는 것을 고려해보세요.
# 일단은 기존 Customer 모델도 유지하되, CustomUser와 연동하는 방안을 생각해야 합니다.
class Customer(models.Model):
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    # 위와 같이 settings.AUTH_USER_MODEL과 연결하는 것이 바람직합니다.
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    PAYMENT_CHOICES = [
        ('현장결제', '현장결제'),
        ('온라인결제', '온라인결제'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="예약자") # AUTH_USER_MODEL 사용
    exhibition = models.ForeignKey('Exhibition', on_delete=models.CASCADE, verbose_name="전시")
    num_people = models.PositiveIntegerField("예약 인원", default=1)
    date_reserved = models.DateTimeField("예약 일시", auto_now_add=True)
    payment_method = models.CharField("결제 방법", max_length=20, choices=PAYMENT_CHOICES, default='현장결제')
    is_paid = models.BooleanField("결제 완료 여부", default=False)
    coupon_code = models.CharField("쿠폰 코드", max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.exhibition.title} 예약 ({self.num_people}명)"