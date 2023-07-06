import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS =  ['january', 'february', 'march', 'april', 'may', 'june']
DAYOFWEEK = ['monday', 'tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
    while city not in ('chicago', 'new york', 'washington'):
        city = input('Please select one option from the list:\nChicago, New York, or Washington\n')

    # get user input for month (all, january, february, ... , june)
    month = input('Would you like to filter the data by month (january, february, march, april, may, or june), or not at all? Type "all" for no filter.\n').lower()
    while month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
        month = input('Please select one option from the list:\nall, january, february, march, april, may, or june\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)monday tuesday wednesday thursday friday saturday sunday
    day = input('Would you like to filter by day (monday, tuesday, wednesday, thursday, friday, saturday, or sunday)? Type "all" for no filter.\n').lower()
    while day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
        day = input('Please select one option from the list:\nall, monday, tuesday, wednesday, thursday, friday, saturday, or sunday\n')

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['dayofweek'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        df = df[df['month'] == MONTHS.index(month) + 1]

    if day != 'all':
        df = df[df['dayofweek'] == DAYOFWEEK.index(day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    # start time to measure how long it takes to calculate the statistics
    start_time = time.time()

    # display the most common month
    print('Most common month:', MONTHS[df['month'].mode()[0] - 1])

    # display the most common day of week
    print('Most common day of week:', DAYOFWEEK[df['dayofweek'].mode()[0]])

    # display the most common start hour
    print('Most common start hour:', df['dayofweek'].mode()[0])

    # display how long it took to calculate the statistics
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_mode = df['Start Station'].mode()[0]
    print('Most commonly used start station:', start_station_mode)

    # display most commonly used end station
    end_station_mode = df['End Station'].mode()[0]
    print('Most commonly used end station:', end_station_mode)

    # display most frequent combination of start station and end station trip
    comb_mode = (df['Start Station'] + " to " + df['End Station']).mode()[0]
    print('Most frequent combination of start station and end station trip:',
          "From", comb_mode)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    # start time to measure how long it takes to calculate the statistics
    start_time = time.time()

    # display total travel time
    print('Total travel time:', df['Trip Duration'].sum())

    # display mean travel time
    print('Mean travel time:', df['Trip Duration'].mean())

    # display how long it took to calculate the statistics
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    # start time to measure how long it takes to calculate the statistics
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types:\n\n', df['User Type'].value_counts().to_string(), '\n')

    # Display counts of gender
    if 'Gender' in df:
        print('Counts of gender:\n\n', df['Gender'].value_counts().to_string(), '\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('Earliest year of birth:', int(df['Birth Year'].min()))
        print('Most recent year of birth:', int(df['Birth Year'].max()))
        print('Most common year of birth:', int(df['Birth Year'].mode()[0]))

    # display how long it took to calculate the statistics
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def data_request():
    """
    Prompts the user if they want to see 5 lines of raw data,.

    Returns:
        True - If the user wants to see 5 lines of raw data.
        False - Otherwise.
    """

    raw_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n').lower()
    while raw_data not in ('yes', 'no'):
        raw_data = input('Please select yes or no\n')

    if raw_data == 'yes':
        return True
    else:
        return False

def main():
    while True:
        city, month, day = get_filters()
        print('='*50)
        print('City:', city.title() + ',', 'month:', month + ',', 'day:', day)
        print('='*50)
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        row = 0
        # Prompts the user if they want to see 5 lines of raw data
        while data_request():
            print(df.iloc[row:row+5, :-3])
            row += 5
            # Stop the program when there is no more raw data to display.
            if row > len(df.index):
                break


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
