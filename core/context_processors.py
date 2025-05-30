from .models import Notification

def notification_count(request):
    if request.user.is_authenticated:
        return {
            'unread_notification_count': Notification.objects.filter(user=request.user, is_read=False).count()
        }
    return {'unread_notification_count': 0} 