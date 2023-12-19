from django_q.tasks import Schedule


Schedule.objects.create(
    func="borrowings.notifications.overdue_borrowings", schedule_type=Schedule.DAILY
)
