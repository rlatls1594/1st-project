from django.contrib import admin
# CustomUser를 임포트하고 UserAdmin을 사용하여 관리자 페이지에 등록
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin # 기존 UserAdmin 가져오기
from .models import CustomUser, Exhibition, Reservation, Customer # CustomUser 임포트

# CustomUser 모델을 관리자 페이지에 등록
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin): # BaseUserAdmin을 상속받아 기존 기능 유지
    # 필요한 경우 CustomUser에 추가된 필드를 list_display 등에 추가
    pass # 기본 AbstractUser의 필드들은 BaseUserAdmin에서 다 관리됩니다.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email')

@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'location')
    search_fields = ('title', 'location')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    # Reservation 모델의 user 필드가 CustomUser 모델을 참조하므로,
    # user__username으로 검색할 수 있습니다.
    list_display = ('user', 'exhibition', 'num_people', 'date_reserved', 'payment_method', 'is_paid')
    list_filter = ('date_reserved', 'is_paid', 'payment_method')
    search_fields = ('user__username', 'exhibition__title')
    raw_id_fields = ('user', 'exhibition') # 외래키 필드를 ID로 직접 입력 가능하게 하여 편의성 증대