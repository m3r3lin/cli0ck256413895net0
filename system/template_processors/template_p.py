from datetime import timedelta, datetime

from django.utils import timezone

from system.models import User, TanzimatPaye, Tabligh


def template_process(request):
    # online members count
    online_time_limite = timezone.now() - timedelta(seconds=600)
    count_user_online = User.objects.filter(
        last_activity__gte=online_time_limite).count()

    daramad_pardakhtshode = 0
    all_user = User.objects.count()
    all_tabligh = Tabligh.objects.count()
    today = datetime.today()
    all_user_today = User.objects.filter(date_joined__year=today.year, date_joined__month=today.month,
                                         date_joined__day=today.day).count()

    # fake part
    amar_jali = TanzimatPaye.objects.filter(
        onvan__startswith='amar_jaali').all()
    for item in amar_jali:
        if item.onvan == "amar_jaali.count_user_online":
            count_user_online += int(item.value)
        if item.onvan == "amar_jaali.count_all_user":
            all_user += int(item.value)
        if item.onvan == "amar_jaali.count_user_new_today":
            all_user_today += int(item.value)
        if item.onvan == "amar_jaali.count_tabligh_thabti":
            all_tabligh += int(item.value)
        if item.onvan == "amar_jaali.meghdar_daramad_pardahkti":
            daramad_pardakhtshode += int(item.value)

    if request:
        return {
            "cpp": {
                "count_user_online": count_user_online,
                "all_users": all_user,
                "all_user_today": all_user_today,
                "all_tabligh": all_tabligh,
                "daramad_pardakhtshode": daramad_pardakhtshode
            }
        }
    return {}
