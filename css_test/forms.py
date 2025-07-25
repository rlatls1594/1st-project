from django import forms
# from .models import User # <-- 이 줄을 삭제하거나 주석 처리합니다.

# Django에서 현재 활성화된 User 모델을 가져오는 표준 방법입니다.
from django.contrib.auth import get_user_model
User = get_user_model() # 이제 'User' 변수는 settings.AUTH_USER_MODEL에 지정된 'CustomUser' 클래스를 참조합니다.


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User # 이제 여기서 참조하는 User는 CustomUser입니다.
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    # 회원가입 폼에서 비밀번호를 해싱하여 저장해야 합니다.
    # save 메소드를 오버라이드하여 비밀번호 해싱 로직을 추가하는 것이 좋습니다.
    # (선택 사항이지만 보안을 위해 중요합니다.)
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class SignInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)