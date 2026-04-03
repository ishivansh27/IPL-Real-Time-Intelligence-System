import pandas as pd
import streamlit as st
import time

# Load data
deliveries = pd.read_csv("deliveries.csv")
matches = pd.read_csv("matches.csv")

st.set_page_config(layout="wide")

st.title("🏏 IPL Real-Time Intelligence System")

# ---------------- SELECT MATCH ----------------
match_id = st.selectbox("Select Match ID", deliveries['match_id'].unique())

match_df = deliveries[deliveries['match_id'] == match_id].copy()
match_info = matches[matches['id'] == match_id]

# ---------------- MATCH INFO ----------------
team1 = match_info['team1'].values[0]
team2 = match_info['team2'].values[0]
winner = match_info['winner'].values[0]

st.subheader(f"{team1} 🆚 {team2}")
st.write(f"🏆 Actual Winner: {winner}")

# ---------------- SPLIT INNINGS ----------------
innings1 = match_df[match_df['inning'] == 1]
innings2 = match_df[match_df['inning'] == 2]

# ---------------- WIN PROB FUNCTION ----------------
def calculate_win_probability(score, wickets, balls, target):
    runs_left = target - score
    balls_left = 120 - balls

    # Match finished cases
    if runs_left <= 0:
        return 1.0
    if balls_left <= 0:
        return 0.0

    req_rate = (runs_left * 6) / balls_left

    # Better base probability
    prob = 1 / (1 + req_rate / 6)

    # Wicket impact (lighter penalty)
    prob *= (1 - wickets * 0.03)

    # Clamp to realistic range
    prob = max(0.05, min(0.95, prob))

    return prob

start = st.button("Start Match Simulation")

if start:

    col1, col2 = st.columns(2)

    score_box = col1.empty()
    event_box = col1.empty()
    info_box = col1.empty()

    prob_box = col2.empty()
    chart_box = col2.empty()

    prob_list = []

    # ---------------- FIRST INNINGS ----------------
    st.markdown("## 🟡 First Innings")

    score = 0
    wickets = 0
    balls = 0

    for _, row in innings1.iterrows():

        runs = row['total_runs']
        is_wicket = row['is_wicket']

        score += runs
        balls += 1

        if is_wicket == 1:
            wickets += 1

        overs = balls / 6
        run_rate = score / overs if overs > 0 else 0

        score_box.subheader(f"{team1}: {score}/{wickets}")
        info_box.write(f"Overs: {overs:.1f} | Run Rate: {run_rate:.2f}")

        if runs == 4:
            event_box.success("🔥 FOUR!")
        elif runs == 6:
            event_box.success("💥 SIX!")
        elif is_wicket == 1:
            event_box.error("🚨 WICKET!")

        time.sleep(0.3)

    target = score + 1
    st.success(f"🎯 Target for {team2}: {target}")

    # ---------------- SECOND INNINGS ----------------
    st.markdown("## 🔵 Second Innings")

    score = 0
    wickets = 0
    balls = 0

    for _, row in innings2.iterrows():

        runs = row['total_runs']
        is_wicket = row['is_wicket']

        score += runs
        balls += 1

        if is_wicket == 1:
            wickets += 1

        overs = balls / 6
        run_rate = score / overs if overs > 0 else 0

        runs_left = target - score
        balls_left = 120 - balls
        req_rate = (runs_left * 6 / balls_left) if balls_left > 0 else 0

        # ---------------- WIN PROB ----------------
        prob = calculate_win_probability(score, wickets, balls, target)
        prob_list.append(prob)

        # ---------------- UI ----------------
        score_box.subheader(f"{team2}: {score}/{wickets}")
        info_box.write(f"Overs: {overs:.1f}")
        info_box.write(f"Runs Needed: {runs_left}")
        info_box.write(f"Req Rate: {req_rate:.2f}")

        # 🔥 SHOW BOTH TEAMS
        prob_box.subheader(f"{team2}: {prob*100:.1f}% chance")
        prob_box.write(f"{team1}: {(1-prob)*100:.1f}% chance")

        if runs == 4:
            event_box.success("🔥 FOUR!")
        elif runs == 6:
            event_box.success("💥 SIX!")
        elif is_wicket == 1:
            event_box.error("🚨 WICKET!")

        chart_box.line_chart(prob_list)

        time.sleep(0.3)

    # ---------------- RESULT ----------------
    if score >= target:
        st.success(f"🏆 {team2} WON!")
    else:
        st.error(f"🏆 {team1} WON!")