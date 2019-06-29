from django.shortcuts import redirect
from django.urls import reverse


def get_token(request):
    try:
        return request.user.userbox.token
    except:
        return ""



def get_header(request):
    token = get_token(request)
    return {"authorization": "JWT " + token}
    # if token:
    #     return {"authorization": "JWT " + token}
    # else:
    #     # return HttpResponseForbidden()
    #     return redirect(reverse("access_login"))
