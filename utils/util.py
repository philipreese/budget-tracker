import calendar


def get_start_end_date_from_month(date: str):
    year_filter, month_str = date.split("-")
    month_int = int(month_str)
    start_date = f"{date}-01"
    end_date = f"{date}-" + str(
        calendar.monthrange(int(year_filter), int(month_int))[1]
    )
    return start_date, end_date
