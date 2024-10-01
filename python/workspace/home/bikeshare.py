import time
import pandas as pd
import numpy as np
import click

# hi

# Constants
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTHS = ('january', 'february', 'march', 'april', 'may', 'june')
WEEKDAYS = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')

def get_user_input(prompt, CC):
    """Get a valid input from the user."""
    while True:
        user_input = input(prompt).lower().strip()
        if user_input == 'end':
            raise SystemExit

        if ',' in user_input:
            choices = [choice.strip() for choice in user_input.split(',')]
            if all(choice in CC for choice in choices):
                return choices
        elif user_input in CC:
            return user_input

        prompt = "Invalid input. Please try again:\n>"

def get_filters():
    """Ask the user to specify city(ies), month(s), and day(s)."""
    print("\nLet's explore some US bikeshare data!\n")
    print("Type 'end' at any time to exit the program.\n")

    cities = get_user_input("\nSelect city(ies) (New York City, Chicago, Washington):\n>", CITY_DATA.keys())
    months = get_user_input("\nSelect month(s) (January to June):\n>", MONTHS)
    days = get_user_input("\nSelect weekday(s):\n>", WEEKDAYS)

    confirmation = get_user_input(
        f"\nConfirm the filters:\nCity(ies): {cities}\nMonth(s): {months}\nDay(s): {days}\n[y/n]\n>", ['y', 'n'])
    
    if confirmation == 'y':
        return cities, months, days
    else:
        print("\nLet's try again!")
        return get_filters()

def load_data(city, month, day):
    """Load and filter data based on the user's choices."""
    print("\nLoading data...")
    start_time = time.time()

    if isinstance(city, list):
        df = pd.concat([pd.read_csv(CITY_DATA[c]) for c in city], sort=True)
        df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station', 'User Type', 'Gender', 'Birth Year'])
    else:
        df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour

    if isinstance(month, list):
        df = pd.concat([df[df['Month'] == MONTHS.index(m) + 1] for m in month])
    else:
        df = df[df['Month'] == MONTHS.index(month) + 1]

    if isinstance(day, list):
        df = pd.concat([df[df['Weekday'].str.lower() == d] for d in day])
    else:
        df = df[df['Weekday'].str.lower() == day]

    print(f"\nData loaded in {time.time() - start_time:.2f} seconds.")
    print('-'*40)
    return df

def display_time_stats(df):
    """Display the most common times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['Month'].mode()[0]
    most_common_day = df['Weekday'].mode()[0]
    most_common_hour = df['Start Hour'].mode()[0]

    print(f"Most common month: {MONTHS[most_common_month - 1].title()}")
    print(f"Most common day: {most_common_day}")
    print(f"Most common start hour: {most_common_hour}")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-'*40)

def display_station_stats(df):
    """Display the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_start_station = df['Start Station'].mode()[0]
    most_common_end_station = df['End Station'].mode()[0]
    most_common_trip = (df['Start Station'] + " to " + df['End Station']).mode()[0]

    print(f"Most common start station: {most_common_start_station}")
    print(f"Most common end station: {most_common_end_station}")
    print(f"Most common trip: {most_common_trip}")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-'*40)

def display_trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()

    print(f"Total travel time: {total_travel_time//86400}d {total_travel_time%86400//3600}h {total_travel_time%3600//60}m {total_travel_time%60}s")
    print(f"Mean travel time: {mean_travel_time//60:.0f}m {mean_travel_time%60:.0f}s")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-'*40)

def display_user_stats(df, city):
    """Display statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("User Types:")
    print(df['User Type'].value_counts().to_string())

    if 'Gender' in df.columns:
        print("\nGender Distribution:")
        print(df['Gender'].value_counts().to_string())
    else:
        print(f"\nNo gender data available for {city.title()}.")

    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])

        print(f"\nEarliest birth year: {earliest_year}")
        print(f"Most recent birth year: {most_recent_year}")
        print(f"Most common birth year: {most_common_year}")
    else:
        print(f"\nNo birth year data available for {city.title()}.")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-'*40)

def display_raw_data(df):
    """Display raw data 5 rows at a time."""
    mark_place = 0
    while True:
        print(df.iloc[mark_place:mark_place + 5])
        mark_place += 5

        if get_user_input("\nDo you want to see more raw data? [y/n]\n>", ['y', 'n']) != 'y':
            break

def main():
    while True:
        click.clear()
        city, month, day = get_filters()
        df = load_data(city, month, day)

        while True:
            user_choice = get_user_input(
                "\nChoose an option:\n[ts] Time Stats\n[ss] Station Stats\n[td] Trip Duration Stats\n[us] User Stats\n[rd] Raw Data\n[r] Restart\n>",
                ['ts', 'ss', 'td', 'us', 'rd', 'r']
            )
            click.clear()
            if user_choice == 'ts':
                display_time_stats(df)
            elif user_choice == 'ss':
                display_station_stats(df)
            elif user_choice == 'td':
                display_trip_duration_stats(df)
            elif user_choice == 'us':
                display_user_stats(df, city)
            elif user_choice == 'rd':
                display_raw_data(df)
            elif user_choice == 'r':
                break

        if get_user_input("\nDo you want to restart? [y/n]\n>", ['y', 'n']) != 'y':
            break

if __name__ == "__main__":
    main()
