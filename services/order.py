from django.utils import timezone

from datetime import datetime

from django.db import transaction

from db.models import Order, User, Ticket


def create_order(tickets: list, username: str, date: datetime = None) -> Order:
    user = User.objects.get(username=username)
    with transaction.atomic():
        if date is None:
            date = timezone.now()

        order = Order.objects.create(user=user, created_at=date)

        for ticket_data in tickets:
            Ticket.objects.create(
                movie_session_id=ticket_data["movie_session"],
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )
    return order


@transaction.atomic
def get_orders(username: str = None) -> list[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()