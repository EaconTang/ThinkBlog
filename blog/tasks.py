from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def update_site_visit(add=1, sub=0):
    """
    update site_visit, default to add 1 each time when called
    :param add:
    :param sub:
    :return:
    """
    from .models import SiteInfo, SiteVisit
    from .utils import datetime_hour_now

    try:
        site_info = SiteInfo.objects.get(site_is_published=True)
        site_info.site_visit += add
        site_info.site_visit -= sub
        site_info.save()

        # site visit for each hour
        c_hour = datetime_hour_now()
        site_visit = SiteVisit.objects.get_or_create(time_visit=c_hour,
                                                     day_visit=c_hour.date(),
                                                     month_visit=c_hour.strftime('%Y-%m'))[0]
        site_visit.site_visit += add
        site_visit.site_visit -= sub
        site_visit.save()
    except Exception:
        raise
    else:
        return 'Update visit finished!'