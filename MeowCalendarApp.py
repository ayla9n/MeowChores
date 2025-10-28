import streamlit as st
import pandas as pd
from datetime import date, timedelta, datetime
from PIL import Image
import pytz


class ChoreCalendar:
    def __init__(self, person, start_date, num_days):
        self.person = person
        self.start_date = start_date
        self.num_days = num_days
        self.df = self._create_chore_df()

    "rotates chores daily based on thr order of the list"
    def _create_chore_df(self):
        dates = [self.start_date + timedelta(days=i) for i in range(self.num_days)]
        assignments = [self.person[i % len(self.person)] for i in range(self.num_days)]
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


cat_pic = Image.open("cat pics/meow.png")

st.set_page_config(
    page_title="Meowchores",
    page_icon='🐾',
    layout="centered"
)

st.image(cat_pic, width=100)
#--- App-----
st.title(f"Chore Calendar")
st.write("Automatically rotates chores every day.")

person = ["papAYA 🥭", "AYla 🐱", "Acai 🫐", "powderblue 🟦", "Tah ⛳", "Pixie 🧚🏾"]
calendar = ChoreCalendar(person, date(2025, 10, 24), 30)

# Dates
# local timezone
tz = pytz.timezone("America/New_York")

# Get today's date in your timezone
today = datetime.now(tz).date()
#today = date.today()
tomorrow = today + timedelta(days=1)

today_person = calendar.get_person_for_date(today)
tomorrow_person = calendar.get_person_for_date(tomorrow)

if today_person:
    st.write(f"\n{today.strftime("%A %B %d, %Y")}")
    st.subheader(f"⭐ Today is {today_person}'s dishes day!")
else:
    st.warning("No one assigned for today.")

if tomorrow_person:
    st.info(f"Tomorrow: {tomorrow_person}'s dishes day!")

# Data
info_col, img_col = st.columns(2)
catwashing = Image.open("cat pics/justwashingthedishes.jpg")
catmop = Image.open("cat pics/meowmop.jpg")
sage = Image.open("cat pics/valsage.jpg")
catface =  Image.open("cat pics/catface.jpg")

day_df = calendar.get_day_df()
tomorrow_index = calendar.get_index_for_person(tomorrow_person)

with info_col:
    #displays all people excluding the person who's washing day is today
    st.dataframe(day_df.set_index("Day").iloc[tomorrow_index:tomorrow_index + len(person) - 1], use_container_width=True)
 


with img_col:
    st.image(catwashing, caption="you in a little bit", width=250)
    
st.divider()

tips_col, catmop_col = st.columns(2)

with tips_col:
    st.subheader("Kitchen Reminders")
    st.markdown("""
    - 🍽️ Place clean plates on the dish rack  
    - 🧴 Wipe down counters  
    - ♨️ Scrub and wipe the stove  
    - 🧹 Sweep the kitchen floor  
    - 🚮 Take out the garbage if it's full  
    """)

with catmop_col:
    st.image(catmop, caption="also you in a little bit", width=250)

st.divider()

col1, col2 = st.columns(2)
with col1:
     # Talaja Rotation
    talaja = ["powderblue 🟦", "AYla 🐱", "Pixie 🧚🏾", "Acai 🫐"]
    last_to_clean = 1
    next_up = talaja[last_to_clean + 1:] + talaja[:last_to_clean]
    st.subheader("❄️ Fridge Day")
    st.info(f"{talaja[last_to_clean]} was the last person to clean the fridge")
    st.dataframe(pd.DataFrame({'Next up': next_up}), use_container_width=True)

with col2:
    st.image(catface)

st.divider()