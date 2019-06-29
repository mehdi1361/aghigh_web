from aghighweb.middleware import DisablePartManager


def disable_part(request):
    try:
        user_type = request.user.userbox.user_type
        user_level = request.user.userbox.user_level

        if user_type == 'advisor' or user_type == 'admin':
            return {"app_list_disable": DisablePartManager.app_list_disable_str_for_admin}
        elif 'country' in user_level:
            return {"app_list_disable": DisablePartManager.app_list_disable_str_for_admin}
        else:
            return {"app_list_disable": DisablePartManager.app_list_disable_str}
    except:
        return {"app_list_disable": DisablePartManager.app_list_disable_str}
    # DisablePartManager.app_list_disable_str = []
    # DisablePartManager.app_list_disable_str_for_admin = []
    # return {"app_list_disable": DisablePartManager.app_list_disable}
