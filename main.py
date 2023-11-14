import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

day_df = pd.read_csv("day_data.csv")
hour_df = pd.read_csv("hour_data.csv")


def rental_stats(df, year=None):
    if year:
        df = df[df["yr"] == year]

    highest_month = df.groupby("mnth")["cnt"].sum().idxmax()
    lowest_month = df.groupby("mnth")["cnt"].sum().idxmin()

    return highest_month, lowest_month


def weather_analysis(df):
    weather_rental = df.groupby("weathersit")["cnt"].sum()
    st.write("Rata-rata jumlah rental untuk setiap kondisi cuaca:")
    st.write(weather_rental)


def holiday_analysis(df):
    rental_holiday = df[df["holiday"] == "yes"]["cnt"].sum()
    rental_non_holiday = df[df["holiday"] == "no"]["cnt"].sum()
    st.write(f"Rata-rata jumlah rental pada hari libur : {rental_holiday}")
    st.write(f"Rata-rata jumlah rental diluar hari libur : {rental_non_holiday}")


def main():
    st.title("Bike Rental Analysis")

    st.header("Monthly Statistics")
    year_range = st.selectbox("Select Year Range", ["2011", "2012", "2011-2012"])

    if year_range == "2011":
        filtered_df = day_df[day_df["yr"] == 2011]
    elif year_range == "2012":
        filtered_df = day_df[day_df["yr"] == 2012]
    else:  # For 2011-2012
        filtered_df = day_df[(day_df["yr"] >= 2011) & (day_df["yr"] <= 2012)]

    highest_month = filtered_df.groupby("mnth")["cnt"].sum().idxmax()
    lowest_month = filtered_df.groupby("mnth")["cnt"].sum().idxmin()

    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                   "November", "December"]

    filtered_df["mnth"] = pd.Categorical(filtered_df["mnth"], categories=month_order, ordered=True)

    plt.figure(figsize=(10, 5))
    monthly_rentals = filtered_df.groupby("mnth")["cnt"].mean()
    plot = monthly_rentals.plot(kind="bar", color="skyblue")

    # Highlight highest and lowest months
    plot.patches[month_order.index(highest_month)].set_facecolor("blue")
    plot.patches[month_order.index(lowest_month)].set_facecolor("blue")

    plt.title(f"Monthly Rentals in {year_range}")
    plt.xlabel("Month")
    plt.ylabel("Rental Count")
    plt.xticks(rotation=45)

    st.pyplot(plt)

    st.header("Weather Analysis")
    weather_rental = hour_df.groupby("weathersit")["cnt"].sum()

    fig, ax = plt.subplots()
    ax.pie(weather_rental, labels=weather_rental.index, autopct="%1.3f%%", startangle=90,
           colors=sns.color_palette("Set3"))
    ax.set(title="Total Rentals by Weather Condition")
    st.pyplot(fig)

    st.header("Holiday Analysis")
    holiday_data = {
        "Holiday": day_df[day_df["holiday"] == "yes"]["cnt"],
        "Non-Holiday": day_df[day_df["holiday"] == "no"]["cnt"]
    }

    fig, ax = plt.subplots()
    sns.boxplot(data=pd.DataFrame(holiday_data))
    ax.set(xlabel="Day Type", ylabel="Total Rentals")
    st.pyplot(fig)

    st.caption('Copyright © Felix 2023')


main()
