import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.conf import settings

from apps.access.models import UserBox

# Create your views here.
from apps.main.templatetags.main_extra import has_perm_both_gender
from apps.main.views import BaseViewClass


class Login(View):
    def get(self, request):
        if request.user.is_active:
            return redirect(reverse("main_index"))
        return render(request, "apps/access/login.html")

    def post(self, request):
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        if phone_number and username:
            request.session['username'] = username
            request.session['phone_number'] = phone_number

            post_req = {
                "user_name": username,
                "phone_number": phone_number,
            }
            get_res = requests.post(
                url=settings.SERVER_FULL_URL + "/api/v1/user/login/",
                data=post_req
            )
            if get_res.status_code == 200:
                return redirect(reverse("confirm_code"))
        return render(request, "apps/access/login.html", {"error": True})


class ConfirmCode(View):
    def get(self, request):
        if request.user.is_active:
            return redirect(reverse("main_index"))
        return render(request, "apps/access/confirm_code.html")

    def post(self, request):
        phone_number = request.session.get("phone_number", False)
        code = request.POST.get('code')
        if not code:
            return render(request, "apps/access/confirm_code.html", {"error": True})

        if not phone_number:
            return render(request, "apps/access/login.html", {"error": True})

        post_req = {
            "activation_code": code,
            "to_phone_number": phone_number,
        }
        get_res = requests.post(
            url=settings.SERVER_FULL_URL + "/api/v1/user/check/",
            data=post_req
        )
        data = get_res.json()
        if get_res.status_code == 200 and data["success"]:
            try:
                UserBox.objects.get(username=phone_number).delete()
            except ObjectDoesNotExist:
                pass

            user = data["user"]
            user_model = UserBox()
            user_model.username = phone_number
            user_model.token = data["token"]
            user_model.api_user_id = user["id"]
            user_model.full_name = user['first_name'] + " " + user['last_name']
            user_model.image = user.get('image')

            if 'school_name' in user:
                user_model.school_name = user['school_name']

            if 'school_id' in user:
                user_model.school_id = user['school_id']

            if 'province_id' in user:
                user_model.province_id = user['province_id']

            levels = ""
            user_model.role_select = self.get_top_level(user['level'])

            for level in user['level']:
                levels += level + ","

            user_model.user_type = user['type']
            user_model.user_level = levels
            user_model.gender = user['gender']
            user_model.gender_select = user['gender']

            user_model.save()
            auth.login(request, user_model)

            if user['type'] == "teacher" and 'advisor' in user['level'] or 'expert' in user['level'] or 'top_expert' in user['level']:
                return redirect(reverse("question_manager_index"))
            return redirect(reverse("main_index"))
        return render(request, "apps/access/confirm_code.html", {"error": True})

    @staticmethod
    def get_top_level(user_levels):

        if "country" in user_levels:
            return 'country'

        elif "province" in user_levels or 'province_m' in user_levels or 'province_f' in user_levels:
            if 'province' in user_levels:
                return 'province'
            elif 'province_m' in user_levels:
                return 'province_m'
            return 'province_f'

        elif "county" in user_levels:
            return 'county'

        elif "camp" in user_levels:
            return 'camp'

        elif "coach" in user_levels:
            return 'coach'

        return user_levels[0]


class ResendConfirmCode(View):
    def post(self, request):
        username = request.session.get('username')
        phone_number = request.session.get('phone_number')
        response = {
            'success': False,
            'redirect': True,
        }
        if not username and not phone_number:
            return JsonResponse(response)
        data = {
            'username': username,
            'phone_number': phone_number
        }

        get_res = requests.post(
            url=settings.SERVER_FULL_URL + "/api/v1/user/resend_confirm_code/",
            data=data
        )
        response = get_res.json()

        return JsonResponse(response)


def do_logout(request):
    try:
        auth.logout(request=request)
    except:
        pass
    return redirect('access_login')


class UserProfile(BaseViewClass):
    @staticmethod
    def get(request):
        return render(request, "apps/access/user_profile.html")


class UserProfileImage(BaseViewClass):

    def post(self, request):
        get_res = requests.post(
            url=settings.SERVER_FULL_URL + "/api/v1/user/change_image/",
            headers=self.get_http_header(request),
            files={'image': request.FILES.get('image')}
        )
        self.is_auth_valid(request, get_res)

        if get_res.status_code == 200:
            message = "success"
            request.user.userbox.image = get_res.json()["image"]
            request.user.userbox.save()

        else:
            message = "error"

        return JsonResponse({"message": message})


class ChangeRoleAndGender(BaseViewClass):

    def post(self, request):
        user_level = request.user.userbox.user_level
        user_levels = user_level.split(',')
        role = request.POST.get("role_select")
        gender = self.get_gender(request)

        request.user.userbox.gender_select = gender

        if role in user_levels:
            request.user.userbox.role_select = role
            message = "success"

        else:
            message = "no_has_perm"

        request.user.userbox.save()

        return JsonResponse({"message": message})

    @staticmethod
    def get_gender(request):
        has_perm = has_perm_both_gender(request)
        if has_perm:
            gender = request.POST.get("gender_select", request.user.userbox.gender)

        else:
            gender = request.user.userbox.gender
        return gender
