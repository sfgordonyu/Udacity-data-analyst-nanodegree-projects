import time
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
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # create months and days lists to later check if the input is valid
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days= ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    # get user input for city (chicago, new york city, washington)
    city=input('Which city\'s data would you like to analyze? You can choose from Chicago, New York City, or Washington? \n').lower()
    
    # handle invalid input
    while city not in CITY_DATA:
        city=input('That\'s not one of the available cities. Please try again. \n').lower()
    
    # get user input for filter options
    answer=input('Would you like to filter the data by month, day, both or not at all? Type "none" for no time filter \n').lower()
    
    # sets month and day to all if no filter is selected
    if answer == 'none':
        month='all'
        day='all'
        
    # get user input for month if they decide to filter by month               
    elif answer == 'month':     
        #set day to all since there is no filter for day
        day='all'
        
        #get
        month=input('Which month? January, February, March, April, May, or June? \n').lower()      
        
        # handle invalid input
        while month not in months:
            month=input('That\'s not a valid month. Please try again. \n').lower()   
        
    # get user input for day of week if they decide to filter by day 
    elif answer == 'day':
        #set month to all since there is no filter for month
        month='all'
        # get user input for day of week (monday, tuesday, ... sunday)
        day=input('Which day of the week? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? \n').lower()
        # handle invalid input
        while day not in days:
            day=input('That is not a valid day of the week. Please try again.\n').lower()

    # get input from user if they filter for both months and day of the week        
    else:
        # get user input for month (january, february, ... , june)
        month=input('Which month? January, February, March, April, May, or June? \n') .lower()   
        # handle invalid input
        while month not in months:
            month=input('That\'s not a valid month. Please try again. \n').lower()
        # get user input for day of week (monday, tuesday, ... sunday)
        day=input('Which day of the week? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? \n').lower()
        # handle invalid input
        while day not in days:
            day=input('That is not a valid day of the week. Please try again. \n').lower()
 
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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
 
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

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

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular month:',popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular day of the week:',popular_day)

    # display the most common start hour 
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station:',popular_end_station)

    # display most frequent combination of start station and end station trip
    most_frequent_station_combo=df.groupby(['Start Station','End Station']).size().nlargest().head(1)
    print('Most frequent combination of start and end stations:\n',most_frequent_station_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time=df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time)

    # display mean travel time
    avg_travel_time=df['Trip Duration'].mean()
    print('Average travel time:', avg_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    
    # Check to make sure that gender column is included in the data
    if 'Gender' in df:
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print(gender)

        # Display earliest, most recent, and most common year of birth
        earliest_year=int(df['Birth Year'].min())
        print('Earliest year of birth:', earliest_year)
    
        most_recent_year=int(df['Birth Year'].max())
        print('Most recent year of birth:', most_recent_year)
    
        most_common_year=int(df['Birth Year'].mode()[0])
        print('Most common year of birth', most_common_year)
    
    #handle missing gender and year of birth columns in Washington D.C. data
    else:
        print('The data for Washington D.C. does not contrain info about genders and birth years.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data upon user request. """
    
    #Ask the user if they want to view raw data
    answer = input("Would you like to view the raw data for individual trips? Type 'yes' or 'no'.\n").lower()
    # goes through a loop if the user decides to view the data.
    if answer == 'yes':
        
        #initialize a variable to count the lines of data shown
        count=0
        
        # Keeps printing more lines of data as long as the user doesn't enter 'no'.         
        while answer != 'no':
            
            #prints 5 lines of data
            print(df.iloc[count:count+5])
            
            # increments the count in case the user wants to display more data    
            count+=5
            
            #ask user if they want to view more data
            answer = input("Would you like to view more data for individual trips? Type 'yes' or 'no'.").lower()
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
