import os
import django
from datetime import datetime, timedelta

# Django 설정 로드
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "css_project.settings")  # 프로젝트 이름에 맞게 수정
django.setup()

from css_test.models import User, Exhibition, Reservation

def insert_dummy_data():
    # 1. 유저 생성
    if not User.objects.filter(username='testuser').exists():
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        print(f"✅ 사용자 생성: {user.username}")
    else:
        user = User.objects.get(username='testuser')
        print(f"ℹ️ 이미 존재하는 사용자: {user.username}")

    # 2. 전시 데이터 생성
    for i in range(5):
        title = f"전시회 제목 {i+1}"
        description = f"이것은 전시회 {i+1}에 대한 설명입니다."
        location = f"서울시 어딘가 {i+1}층"
        start_date = datetime.now() + timedelta(days=i)
        end_date = start_date + timedelta(days=10)
        capacity = 100 + i * 10

        exhibition, created = Exhibition.objects.get_or_create(
            title=title,
            defaults={
                "description": description,
                "location": location,
                "start_date": start_date,
                "end_date": end_date,
                "capacity": capacity,
                "author": user,
            }
        )

        if created:
            print(f"✅ 전시 생성: {exhibition.title}")
        else:
            print(f"ℹ️ 전시 이미 존재: {exhibition.title}")

    # 3. 예약 데이터 생성
    for exhibition in Exhibition.objects.all():
        reservation = Reservation.objects.create(
            user=user,
            exhibition=exhibition,
            num_people=2,
            payment_method="온라인결제",
            is_paid=True,
            coupon_code="SAVE10"
        )
        print(f"✅ 예약 생성: {reservation}")

if __name__ == "__main__":
    insert_dummy_data()
