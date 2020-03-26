import time
import datetime
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    name = input("Please enter your name").lower()
    print('Hello! ' + name +' Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Select city from list below: \n1. Chicago \n2. New York City \n3. Washington\nEnter selected city name here: ").lower()
        if city not in CITY_DATA.keys():
            print("\n!!!!!Enter Valid City name from the list!!!!!!\n")
            continue
        else :
            break            
    # get user input for month (all, january, february, ... , june)
    month_list = ['january', 'february', 'march', 'april', 'may', 'june','all']
    while True:
        month = input("Select month from list below:\n1. January\n2. February\n3. March\n4. April\n5. May\n6. June\n7. All\nEnter selected Month here: ").lower()
        if month not in month_list:
            print("\n!!!!!Enter Valid Month from the list!!!!!!\n")
            continue
        else :
            break 
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_list = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
    while True:
        day = input("Select Day from list below:\n1. Sunday\n2. Monday\n3. Tuesday\n4. Wednesday\n5. Thursday\n6. Friday\n7. Saturday\n8. All\nEnter selected Day here: ").lower()
        if day not in day_list:
            print("\n!!!!!Enter Valid day of the week from the list!!!!!!\n")
            continue
        else :
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].apply(lambda x: calendar.month_name[x]).mode()[0]
    print('Most popular month:', popular_month)
    
    # display the most common day of week
    df['day'] = df['Start Time'].dt.weekday_name
    popular_day = df['day'].mode()[0]
    print('Most Frequent day:', popular_day)
    
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station is: ',start_station)
    
    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most commonly used end station is: ',end_station)

    # display most frequent combination of start station and end station trip
    df['Combo Station'] = df['Start Station'] +' & '+df['End Station']
    combo_station = df['Combo Station'].mode()[0]
    print("Most commomly used combination of start station and end station is: ", combo_station) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time_sec = df['Trip Duration'].sum()
    converted_total_time = time.strftime("%H:%M:%S", time.gmtime(total_time_sec))
    print('Total travel time in HH:MM:SS is:', converted_total_time)
    
    # display mean travel time
    mean_time_sec = df['Trip Duration'].mean()
    converted_mean_time = time.strftime("%H:%M:%S", time.gmtime(mean_time_sec))
    print('Mean time in HH:MM:SS is:', converted_mean_time)
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
        
    # Display counts of user types
    user_count = df['User Type'].value_counts()
    print('List of user types and count of user in each category:\n', user_count)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('Count of user for each gender:\n', gender_count)
    else:
        print('Gender information is not available')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print('The oldest user was born in: ', earliest_year)
        print('The youngest user was born in: ',recent_year)
        print('The most common year of birth is: ',common_year)
    else:
        print('Birth year of users is not available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter y or n.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
