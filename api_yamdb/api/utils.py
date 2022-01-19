def check_role(request, *args):
    if request.user.is_authenticated:
        if request.user.role in args:
            return True
        elif request.user.is_superuser:
            return True
    return False
