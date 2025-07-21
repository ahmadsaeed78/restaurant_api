# reservations/cron.py
from datetime import datetime, timedelta
import random
from .models import Reservation, Table

def assign_and_release_tables():
    now = datetime.now()

    # --- ASSIGN TABLES ---
    # Find reservations that are approved and have no table yet,
    # and that are scheduled for 30 minutes from now.
    assign_time = now + timedelta(minutes=30)
    reservations_to_assign = Reservation.objects.filter(
        status='Approved',
        table__isnull=True,
        date=assign_time.date(),
        time__hour=assign_time.hour,
        time__minute=assign_time.minute,
    )
    for reservation in reservations_to_assign:
        available_tables = Table.objects.filter(is_booked=False)
        if available_tables.exists():
            table = random.choice(list(available_tables))
            reservation.table = table
            reservation.save()
            # Mark the table as booked
            table.is_booked = True
            table.save()

    # --- RELEASE TABLES ---
    # Find reservations that are approved and have a table,
    # and that were scheduled for 1.5 hours ago.
    release_time = now - timedelta(minutes=90)
    reservations_to_release = Reservation.objects.filter(
        status='Approved',
        table__isnull=False,
        date=release_time.date(),
        time__hour=release_time.hour,
        time__minute=release_time.minute,
    )
    for reservation in reservations_to_release:
        if reservation.table:
            table = reservation.table
            table.is_booked = False
            table.save()
