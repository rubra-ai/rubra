# Standard Library
import datetime

# Third Party
from dateutil.relativedelta import relativedelta


class GetNowTool:
    name = "GetNowTool"
    description = "Get date of the current day. Returns year, month, day"
    parameters = {
        "type": "object",
        "properties": {},
        "required": [],
    }

    async def _arun(self, time=None):
        return get_date()

    def _run(self):
        return get_date()


def get_date(day_delta=0, month_delta=0, year_delta=0, year_only=False):
    res_date = datetime.date.today()
    if day_delta != 0:
        res_date += datetime.timedelta(days=day_delta)
    if month_delta != 0:
        res_date += relativedelta(months=month_delta)
    if year_delta != 0:
        res_date += relativedelta(years=year_delta)
    if year_only:
        res_date = res_date.year
    res = f"{str(res_date)}"
    return res
