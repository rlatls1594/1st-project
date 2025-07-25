from django.shortcuts import render, redirect
from .forms import SignUpForm, SignInForm
from django.contrib.auth.decorators import login_required
# from .models import User, Reservation # <-- 이 줄을 삭제하거나 주석 처리합니다.

# Django에서 현재 활성화된 User 모델을 가져오는 표준 방법입니다.
from django.contrib.auth import get_user_model
User = get_user_model() # 이제 'User' 변수는 settings.AUTH_USER_MODEL에 지정된 'CustomUser' 클래스를 참조합니다.

# Reservation 모델은 여전히 css_test.models에 있으므로 아래와 같이 임포트합니다.
from .models import Reservation, Exhibition, Customer # 필요한 모든 모델을 임포트합니다.

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect


all_exhibitions_data = [
    {'id': 1, 'image_url': 'dummy/1.jpg', 'title': '투탕카멘의 비밀', 'date_range': '2025.02.01 ~ 2025.12.31',
     'description': '고대 이집트의 황금 마스크, 화려한 보물, 그리고 신비로운 전설의 주인공 투탕카멘을 만나는 특별한 전시입니다. 그의 무덤에서 발굴된 유물들은 당시 이집트 문명의 정수를 보여주며, 고대인의 삶과 죽음, 그리고 영생에 대한 믿음을 엿볼 수 있게 합니다. 미스터리한 투탕카멘의 삶과 그의 죽음을 둘러싼 이야기들을 통해 고대 이집트의 황금기를 생생하게 느껴보세요.',
     'location': '국립중앙박물관 기획전시실',
     'artist': '고대 이집트 장인들', 'opening_hours': '10:00 ~ 18:00 (입장 마감 17:00, 매주 월요일 휴관)',
     'price_info': '성인 17,000원, 청소년 13,000원',
     'contact_phone': '02-1234-5678', 'parking_info': '유료 주차 가능 (최초 1시간 3,000원, 추가 30분당 1,000원)',
     'public_transport': '지하철 4호선 이촌역 2번 출구 (도보 5분)',
     'schedule_items': [
         {'category': '오프닝 행사', 'date': '2025.02.01', 'time': '14:00', 'notes': '사전 신청 필수'},
         {'category': '큐레이터 토크', 'date': '2025.03.10', 'time': '16:00', 'notes': '매월 둘째 주 월요일'},
     ]
    },
    {'id': 2, 'image_url': 'dummy/2.jpg', 'title': '일본인이 발음하기 어렵다는 공룡 테마', 'date_range': '2025.02.11 ~ 2025.12.31',
     'description': '거대한 공룡들의 세계로 떠나는 시간 여행! 티라노사우루스, 트리케라톱스 등 다양한 공룡 화석과 실제 크기 모형을 통해 중생대 지구의 지배자들을 만나보세요. 공룡들의 생태와 멸종 미스터리까지, 온 가족이 함께 즐길 수 있는 교육적인 전시입니다.',
     'location': '서울과학관 제2전시실',
     'artist': '공룡 연구소', 'opening_hours': '09:00 ~ 17:00 (입장 마감 16:00, 매주 화요일 휴관)',
     'price_info': '성인 15,000원, 어린이 10,000원',
     'contact_phone': '02-9876-5432', 'parking_info': '과학관 주차장 이용 (유료)',
     'public_transport': '버스 147번 과학관역 하차',
     'schedule_items': [
         {'category': '공룡 발자국 체험', 'date': '매주 주말', 'time': '11:00, 15:00', 'notes': '선착순 현장 접수'},
     ]
    },
    {'id': 3, 'image_url': 'dummy/3.jpg', 'title': '반센트 반 고흐는 미치광이인가', 'date_range': '2025.02.21 ~ 2025.12.31',
     'description': '고통 속에서도 아름다움을 찾아낸 불꽃 같은 예술가, 빈센트 반 고흐의 삶과 예술을 심층적으로 탐구합니다. 그의 대표작들을 통해 격정적인 감정과 독창적인 색채 표현을 느껴보세요. 고흐의 삶의 궤적을 따라가며 그의 작품에 담긴 깊은 의미를 재조명합니다.',
     'location': '예술의 전당 한가람미술관',
     'artist': '빈센트 반 고흐', 'opening_hours': '10:00 ~ 19:00 (입장 마감 18:00, 매월 마지막 주 월요일 휴관)',
     'price_info': '성인 18,000원, 학생 15,000원',
     'contact_phone': '02-4567-8901', 'parking_info': '예술의 전당 주차장 (유료)',
     'public_transport': '지하철 3호선 남부터미널역 5번 출구',
     'schedule_items': [
         {'category': '오디오 가이드', 'date': '상시 운영', 'time': '자유', 'notes': '유료 대여'},
         {'category': '강연: 고흐의 삶', 'date': '2025.04.05', 'time': '14:00', 'notes': '사전 예약 필수'},
     ]
    },
    {'id': 4, 'image_url': 'dummy/4.jpg', 'title': '황소인가 칡소인가', 'date_range': '2025.03.01 ~ 2025.12.31',
     'description': '한국 근대 미술의 거장, 이중섭 화가의 작품 세계를 총망라한 전시입니다. 그의 상징적인 소 그림부터 가족에 대한 애틋한 마음이 담긴 은지화까지, 뜨거운 예술혼을 느껴보세요. 한국인의 정서가 담긴 그의 작품들은 오늘날 우리에게 깊은 울림을 선사합니다.',
     'location': '덕수궁 미술관',
     'artist': '이중섭', 'opening_hours': '10:00 ~ 17:00 (입장 마감 16:00, 매주 화요일 휴관)',
     'price_info': '성인 12,000원, 청소년 8,000원',
     'contact_phone': '02-2345-6789', 'parking_info': '주변 공영 주차장 이용',
     'public_transport': '지하철 1호선 시청역 1번 출구',
     'schedule_items': [
         {'category': '도슨트 해설', 'date': '매일', 'time': '11:00, 14:00', 'notes': '정해진 시간에 진행'},
     ]
    },
    {'id': 5, 'image_url': 'dummy/5.jpg', 'title': '이런 것도 예술인가?', 'date_range': '2025.03.21 ~ 2025.12.31',
     'description': '이해하기 힘든 예술의 세계, 한번 느껴보세요. 현대 예술의 다양한 면모를 탐구합니다. 백남준을 중심으로 한 미디어 아트, 설치 미술 등 파격적인 현대 미술 작품들을 통해 예술의 경계를 허무는 경험을 해보세요.',
     'location': '대안 공간 아트 스페이스',
     'artist': '백남준 외', 'opening_hours': '13:00 ~ 20:00 (입장 마감 19:00, 매주 수요일 휴관)',
     'price_info': '무료 (일부 유료 프로그램 별도)',
     'contact_phone': '070-1234-5678', 'parking_info': '인근 유료 주차장 이용 권장',
     'public_transport': '버스 7016번 아트스페이스 정류장 하차',
     'schedule_items': [
         {'category': '작가와의 대화', 'date': '2025.04.10', 'time': '17:00', 'notes': '사전 신청 필요'},
         {'category': '워크숍', 'date': '2025.05.01', 'time': '10:00', 'notes': '재료비 발생'},
     ]
    },
]

# 임시 리뷰 데이터 (DB 모델 대신 사용)
all_temp_reviews = [
    {'exhibition_id': 1, 'author': '방문객1', 'rating': 5, 'review_text': '정말 감동적인 전시였어요!', 'created_at': '2025-07-20 10:00'},
    {'exhibition_id': 1, 'author': '이집트매니아', 'rating': 4, 'review_text': '투탕카멘의 유물들을 직접 보니 신비로웠습니다. 다만 사람이 너무 많았어요.', 'created_at': '2025-07-21 14:30'},
    {'exhibition_id': 2, 'author': '공룡러버', 'rating': 5, 'review_text': '아이들이 너무 좋아했어요! 공룡 모형이 실감나서 좋았습니다.', 'created_at': '2025-07-22 16:45'},
    {'exhibition_id': 2, 'author': '과학소년', 'rating': 4, 'review_text': '생각보다 규모는 작았지만, 공룡들의 특징을 잘 설명해줘서 유익했어요.', 'created_at': '2025-07-23 09:15'},
    {'exhibition_id': 3, 'author': '고흐사랑', 'rating': 5, 'review_text': '고흐의 열정이 느껴지는 전시였습니다. 그의 삶을 이해하는 데 큰 도움이 되었어요.', 'created_at': '2025-07-20 11:30'},
    {'exhibition_id': 3, 'author': '아트감성', 'rating': 3, 'review_text': '작품은 좋았지만, 왠지 모르게 좀 어수선한 느낌이 있었습니다.', 'created_at': '2025-07-24 08:00'},
    {'exhibition_id': 4, 'author': '미술관람객', 'rating': 5, 'review_text': '이중섭 화가님의 작품을 한 자리에서 볼 수 있어 영광이었습니다. 황소 그림은 정말 최고예요.', 'created_at': '2025-07-21 17:00'},
    {'exhibition_id': 5, 'author': '현대예술탐험가', 'rating': 4, 'review_text': '기존 예술의 틀을 깨는 새로운 시도가 인상 깊었습니다. 신선한 충격이었어요!', 'created_at': '2025-07-22 10:00'},
]



def index(request):
    context = {
        'exhibitions': all_exhibitions_data
    }
    return render(request, 'css_test/main/index.html', context)


# def signup_view(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "회원가입이 완료되었습니다. 로그인해주세요.")
#             return render(request, "css_test/Common/login.html", {"form": form})
#     return render(request, "css_test/Common/login.html", {"form": form})

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data['password']
            user.set_password(raw_password)  # ✅ 비밀번호 암호화
            user.save()
            messages.success(request, "회원가입이 완료되었습니다. 로그인해주세요.")
            return redirect('css_test:login')  # 로그인 페이지로 이동
    else:
        form = SignUpForm()
    return render(request, "css_test/Common/login.html", {"form": form})

# def signin_view(request):
#     if request.method == "POST":
#         form = SignInForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']

#             try:
#                 user_obj = User.objects.get(email=email)
#                 user = authenticate(request, username=user_obj.username, password=password)
#             except User.DoesNotExist:
#                 user = None

#             if user is not None:
#                 login(request, user)
#                 print("✅ 로그인 성공:", user.username)
#                 messages.success(request, "로그인 성공! 환영합니다.")
#                 # return redirect('css_test:index')  # ✅ 메인 페이지로 이동
#                 return render(request, "css_test/base.html", {"form": form})

#             else:
#                 print("❌ 로그인 실패 - 인증 실패")
#                 messages.error(request, "이메일 또는 비밀번호가 잘못되었습니다.")
#     else:
#         form = SignInForm()

#     return render(request, "css_test/Common/login.html", {"form": form})


def signin_view(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            print(f"[로그인 시도] username: {username}, password: {password}")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "로그인 성공! 환영합니다.")
                return redirect('css_test:index')  # 로그인 성공 시 메인으로
            else:
                messages.error(request, "아이디 또는 비밀번호가 잘못되었습니다.")
    else:
        form = SignInForm()

    return render(request, "css_test/Common/login.html", {"form": form})


@login_required
def mypage_view(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user).order_by('-date_reserved')
    return render(request, 'css_test/Common/mypage.html', {
        'user': user,
        'reservations': reservations
    })


def exhibition_detail_view(request, exhibition_id):
    exhibition = next((item for item in all_exhibitions_data if item['id'] == exhibition_id), None)

    if exhibition is None:
        return render(request, 'css_test/Common/404.html', {'message': '해당 전시를 찾을 수 없습니다.'}, status=404)

    reviews = [r for r in all_temp_reviews if r['exhibition_id'] == exhibition_id]
    reviews.sort(key=lambda x: x['created_at'], reverse=True)

    context = {
        'exhibition': exhibition,
        'reviews': reviews,
    }
    return render(request, 'css_test/Common/exhibition_detail.html', context)


def add_review(request, exhibition_id):
    if request.method == 'POST':
        review_text = request.POST.get('review_text')
        rating = request.POST.get('rating')
        print(f"전시 ID {exhibition_id}에 대한 리뷰: 별점 {rating}, 내용: '{review_text}'")
    return redirect(reverse('css_test:exhibition_detail', args=[exhibition_id]))



def reserve_view(request, exhibition_id):
    exhibition = next((item for item in all_exhibitions_data if item['id'] == exhibition_id), None)

    if exhibition is None:
        return render(request, 'css_test/Common/404.html', {'message': '해당 전시를 찾을 수 없습니다.'}, status=404)

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        tickets = request.POST.get('tickets')
        receive_method = request.POST.get('receive_method')
        payment_method = request.POST.get('payment_method')
        coupon = request.POST.get('coupon')
        agree_terms = request.POST.get('agree_terms') == 'on'

        if name and phone and email and tickets and receive_method and payment_method and agree_terms:
            try:
                tickets = int(tickets)
                print(f"\n--- 예약 정보 ---")
                print(f"전시명: {exhibition['title']}")
                print(f"이름: {name}")
                print(f"핸드폰: {phone}")
                print(f"이메일: {email}")
                print(f"티켓 수: {tickets}")
                print(f"수령 방법: {receive_method}")
                print(f"결제 방법: {payment_method}")
                print(f"쿠폰: {coupon if coupon else '없음'}")
                print(f"약관 동의: {agree_terms}")
                print(f"-----------------\n")
                # --- 핵심: 세션에 예약 정보 저장 ---
                request.session['reservation_info'] = {
                    'exhibition_name': exhibition['title'],
                    'name': name,
                    'phone': phone,
                    'email': email,
                    # 필요한 다른 예약 정보도 여기에 추가
                    'coupon': coupon if coupon else '없음',
                }
                # ----------------------------------
                return redirect(reverse('css_test:reserve_success'))
            except ValueError:
                print("오류: 티켓 수량이 올바르지 않습니다.")
            except Exception as e:
                print(f"예약 중 오류 발생: {e}")
        else:
            print("오류: 모든 필수 정보를 입력해주세요.")

    context = {
        'exhibition': exhibition,
    }
    return render(request, 'css_test/reserve.html', context)


def reserve_success_view(request):
    # --- 핵심: 세션에서 예약 정보 가져오기 ---
    reservation_info = request.session.get('reservation_info', None)

    if not reservation_info:
        # 세션에 정보가 없으면 홈으로 리다이렉트 (새로고침 방지)
        return redirect('/')

    context = {
        'exhibition': {'name': reservation_info['exhibition_name']}, # 템플릿의 exhibition.name에 맞춤
        'name': reservation_info['name'],
        'email': reservation_info['email'],
        'phone': reservation_info['phone'],
        'coupon': reservation_info['coupon'],
        # 필요하다면 다른 정보도 추가
    }

    # 세션에서 예약 정보 삭제 (선택 사항: 한 번만 표시되도록)
    if 'reservation_info' in request.session:
        del request.session['reservation_info']

    return render(request, 'css_test/reserve_success.html', context)