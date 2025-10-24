import streamlit as st
import pandas as pd
from datetime import date, timedelta
from PIL import Image 


siblings = ["papAYA 🥭", "AYla 🐱", "Acai 🫐", "powderblue 🟦", "hellenKeller ⛳", "Pixie 🧚🏾"]
start_date = date(2025, 10, 24) 
num_days = 30 

#CHORE ROTATION 
dates = [start_date + timedelta(days=i) for i in range(num_days)]
assignments = [siblings[i % len(siblings)] for i in range(num_days)]
chore_df = pd.DataFrame({"Date": dates, "Assigned To": assignments})

#adding photos
catwashing = Image.open("cat pics/justwashingthedishes.jpg")
catmop = Image.open("cat pics/meowmop.jpg")


# STREAMLIT UI 
st.title("🏡Chore Calendar")
st.write("Automatically rotates chores every day.")

# Highlights today
today = date.today()
st.markdown(f"### Today: **{today.strftime('%A, %B %d')}**")

# Converting DataFrame dates to date 
chore_df['Date'] = pd.to_datetime(chore_df['Date']).dt.date

today_person = chore_df.loc[chore_df['Date'] == today, 'Assigned To']

if not today_person.empty:
    st.subheader(f"⭐ {today_person.values[0]}'s Idda day!")
else:
    st.warning("No one assigned for today.")

# Tomorrow 
tomorrow = today + timedelta(days=1)
tomorrow_person = chore_df.loc[chore_df['Date'] == tomorrow, 'Assigned To']

if not tomorrow_person.empty:
    st.info(f"Tomorrow: {tomorrow_person.values[0]}'s Idda day!")


info_col, img_col = st.columns(2)

with info_col:
     # calendar table
    st.dataframe(chore_df.set_index("Date"), use_container_width=True)
    
with img_col:
    st.image(catmop, caption="you in a little bit",)


st.divider()

col1, col2 = st.columns(2)


with col1:
    #KITCHEN REMINDERS
    st.subheader("Kitchen Reminders")
    st.markdown("""
    Quick reminders to keep the kitchen clean:
                
    - 🍽️ **Place clean plates on the dish rack** (don’t leave them near the sink!).
    - 🧴 **Wipe down counters**.
    - ♨️ **Scrub and wipe the stove**.    
    - 🧹 **Sweep the kitchen floor**.
    - 🚮 **Take out the garbage** if it’s full — don’t wait for someone else.    

    Keeping the kitchen clean helps everyone start fresh the next day woohoo 😋
    """)

with col2:
    st.image(catwashing, caption="meow")


st.divider()

talaja = ["powderblue 🟦", "AYla 🐱",  "Pixie 🧚🏾","Acai 🫐" ]
last_to_clean = 1  #change index here
st.subheader("❄️Talaja Day")
st.info(f'{talaja[last_to_clean]} was the last person to clean the fridge')
next_up = talaja[last_to_clean+1:]  + talaja[:last_to_clean]
next_up_df = pd.DataFrame({'Next up': next_up})
st.dataframe(next_up_df, use_container_width=True)


    
st.divider()

# date lookup
st.markdown("### 🔎 Check who has chores on a specific day")
selected_date = st.date_input("Pick a date", today)
chosen = chore_df.loc[chore_df['Date'] == selected_date, 'Assigned To']
if not chosen.empty:
    st.info(f"{chosen.values[0]} is assigned on {selected_date.strftime('%A, %B %d')}.")
else:
    st.warning("That date isn’t in the current range.")


