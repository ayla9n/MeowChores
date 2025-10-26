import pandas as pd
from datetime import date, timedelta


class ChoreCalendar:
    def __init__(self, siblings, start_date, num_days):
        self.siblings = siblings
        self.start_date = start_date
        self.num_days = num_days
        self.df = self._create_chore_df()

    def _create_chore_df(self):
        dates = [self.start_date + timedelta(days=i) for i in range(self.num_days)]
        assignments = [self.siblings[i % len(self.siblings)] for i in range(self.num_days)]
        df = pd.DataFrame({"Date": dates, "Next up": assignments})
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        return df

    def get_person_for_date(self, target_date):
        person = self.df.loc[self.df["Date"] == target_date, "Next up"]
        return person.values[0] if not person.empty else None

    def get_day_df(self):
        day_df = self.df.copy()
        day_df["Day"] = pd.to_datetime(day_df["Date"]).dt.day_name()
        return day_df[["Day", "Next up"]]

    def get_index_for_person(self, person):
        return self.df.index[self.df["Next up"] == person][0] if person in self.df["Next up"].values else 0
