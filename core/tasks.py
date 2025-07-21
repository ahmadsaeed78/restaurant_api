# core/tasks.py
import random
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Reservation, Table

@shared_task
def assign_table_for_reservation(reservation_id):
    """
    Assign a random available table 30 minutes before the reservation.
    """
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        # Only assign if reservation status is still pending or approved (if that's your logic)
        if reservation.status.lower() == "approved":
            available_tables = Table.objects.filter(is_booked=False)
            if available_tables.exists():
                # Choose a random available table
                table = random.choice(available_tables)
                # Assign the table to the reservation
                reservation.table = table
                reservation.save()
                # Mark the table as booked
                table.is_booked = True
                table.save()
                return f"Assigned table {table.table_number} to reservation {reservation_id}"
            else:
                return f"No available tables for reservation {reservation_id}"
        return f"Reservation {reservation_id} is not approved; no table assigned."
    except Reservation.DoesNotExist:
        return f"Reservation {reservation_id} not found."

@shared_task
def release_table_for_reservation(reservation_id):
    """
    Release the table 1.5 hours after the reservation.
    """
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        if reservation.table:
            table = reservation.table
            table.is_booked = False
            table.save()
            # Optionally, clear the table field in the reservation:
            reservation.table = None
            reservation.save()
            return f"Released table {table.table_number} for reservation {reservation_id}"
        return f"No table assigned to reservation {reservation_id}"
    except Reservation.DoesNotExist:
        return f"Reservation {reservation_id} not found."
