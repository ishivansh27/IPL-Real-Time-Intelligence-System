# 🏏 IPL Real-Time Intelligence System

## 📌 Overview

This project simulates a live IPL match using historical ball-by-ball data and provides real-time insights such as score updates, win probability, and match events.

## 🚀 Features

* 📊 Ball-by-ball match simulation
* 🎯 Target calculation for second innings
* 📈 Dynamic win probability (based on match situation)
* 🔥 Event detection (Fours, Sixes, Wickets)
* 📉 Live probability graph
* 🧠 Momentum-based match understanding

## 🛠️ Tech Stack

* Python
* Pandas
* Streamlit

## 🧠 How It Works

* Uses `deliveries.csv` for ball-by-ball data
* Uses `matches.csv` for match context (teams, winner)
* Simulates match progression in real-time
* Calculates win probability based on:

  * Runs required
  * Balls remaining
  * Wickets lost

## ▶️ Run the Project

```bash
python -m streamlit run app.py
```

## 💡 Key Learning

* Real-time data simulation
* Feature engineering for sports analytics
* Converting raw data into meaningful insights

## 📷 Output

* Live scoreboard
* Win probability updates
* Event highlights

## 📌 Future Improvements

* Add ML-based prediction model
* Improve UI to resemble broadcast systems
* Add player-level analytics

NOTE:
For data files download from :
https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020?resource=download
