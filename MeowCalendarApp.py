import streamlit as st
import pandas as pd
from datetime import date, timedelta
from PIL import Image 
from meowCalendar import ChoreCalendar


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