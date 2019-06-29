from django.conf.urls import url
from apps.access.views import (
    Login,
    do_logout,
    ConfirmCode,
    ResendConfirmCode,
    UserProfile,
    UserProfileImage,
    ChangeRoleAndGender,
)

urlpatterns = [
    url(r'^login/$', Login.as_view(), name='access_login'),
    url(r'^logout/$', do_logout, name='access_logout'),
    url(r'^confirm_code/$', ConfirmCode.as_view(), name='confirm_code'),
    url(r'^resend_confirm_code/$', ResendConfirmCode.as_view(), name='resend_confirm_code'),
    url(r'^user_profile/$', UserProfile.as_view(), name='user_profile'),
    url(r'^update_profile_image/$', UserProfileImage.as_view(), name='update_profile_image'),
    url(r'^change_role_and_gender/$', ChangeRoleAndGender.as_view(), name='change_role_and_gender'),
]
