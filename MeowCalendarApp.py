import streamlit as st
import pandas as pd
from datetime import date, timedelta
from PIL import Image 


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



#--- App-----
st.title("🏡 Chore Calendar")
st.write("Automatically rotates chores every day.")

siblings = ["papAYA 🥭", "AYla 🐱", "Acai 🫐", "powderblue 🟦", "hellenKeller ⛳", "Pixie 🧚🏾"]
calendar = ChoreCalendar(siblings, date(2025, 10, 24), 30)

# Dates
today = date.today()
tomorrow = today + timedelta(days=1)

today_person = calendar.get_person_for_date(today)
tomorrow_person = calendar.get_person_for_date(tomorrow)

if today_person:
    st.subheader(f"⭐ Today is {today_person}'s Idda day!")
else:
    st.warning("No one assigned for today.")

if tomorrow_person:
    st.info(f"Tomorrow: {tomorrow_person}'s Idda day!")

# Data
info_col, img_col = st.columns(2)
catwashing = Image.open("cat pics/justwashingthedishes.jpg")
catmop = Image.open("cat pics/meowmop.jpg")

day_df = calendar.get_day_df()
tomorrow_index = calendar.get_index_for_person(tomorrow_person)

with info_col:
    #displays all siblings excluding the sbling who's washing day is today
    st.dataframe(day_df.set_index("Day").iloc[tomorrow_index:tomorrow_index + len(siblings) - 1], use_container_width=True)
    st.divider()

    # Talaja Rotation
    talaja = ["powderblue 🟦", "AYla 🐱", "Pixie 🧚🏾", "Acai 🫐"]
    last_to_clean = 1
    next_up = talaja[last_to_clean + 1:] + talaja[:last_to_clean]
    st.subheader("❄️ Talaja Day")
    st.info(f"{talaja[last_to_clean]} was the last person to clean the fridge")
    st.dataframe(pd.DataFrame({'Next up': next_up}), use_container_width=True)

with img_col:
    st.image(catwashing, caption="you in a little bit")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Kitchen Reminders")
    st.markdown("""
    - 🍽️ Place clean plates on the dish rack  
    - 🧴 Wipe down counters  
    - ♨️ Scrub and wipe the stove  
    - 🧹 Sweep the kitchen floor  
    - 🚮 Take out the garbage if it's full  
    """)

with col2:
    st.image(catmop, caption="also you in a little bit")

st.divider()