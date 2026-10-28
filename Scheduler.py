import datetime

def schedule(Interval, Ease, Repeats, Lapses, LeechState, SuspendState, rating):

    if rating == 0:
        # Suspend the card if it has reached leech status
        # Reset consecutive passes
        Repeats = 0
        # Increase consecutive failures
        Lapses += 1
        # Reset interval
        Interval = 0
        # Decrease ease, with a minimum of 1.3
        Ease = max(1.3, Ease - 0.2)

    elif rating == 1:
        # Learning steps
        if Repeats == 0:
            Interval = 1
        elif Repeats == 1:
            Interval = 3
        else:
            Interval = round(Interval * Ease)

        # Increase consecutive passes
        Repeats = Repeats + 1

        # Increase ease slightly
        Ease += 0.05

    else:
        print("rating must be 0 or 1")

    # Check whether the card has reached leech status

    Leech_Point = 8
    LeechState = Lapses >= Leech_Point

    if LeechState:
            SuspendState = True

    # Calculate the next review date
    New_Due = datetime.date.today() + datetime.timedelta(days=Interval)
    New_Due = str(New_Due)

    new_schedule_data = {
        "Due": New_Due,
        "Interval": Interval,
        "Ease": Ease,
        "Repeats": Repeats,
        "Lapses": Lapses,
        "Leech": LeechState,
        "Suspended": SuspendState
    }

    return new_schedule_data
