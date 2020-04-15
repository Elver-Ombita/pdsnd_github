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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('The bicycle mobility study is available for any of these three cities: Chicago, New York City or Washington; please type the name of one of them. ').lower()

    while city not in CITY_DATA:
        print('Sorry, the city entered does not have a mobility study. Please try again.')
        city = input('The bicycle mobility study is available for any of these three cities: Chicago, New York City or Washington; please type the name of one of them.').lower()
    print('The selected city is: {}'.format(city))

    # TO DO: get user input for month (all, january, february, ... , june)
    MONTH_DATA=('all','january', 'february', 'march', 'april', 'may', 'june')

    month = input('Type a month between January and June or enter all to select the semester. ').lower()

    while month not in MONTH_DATA:
        print ('Error entering the month, please try again.')
        month = input('Type a month between January and June or enter all to select the semester. ').lower()
    print('The selected month is: {}'.format(month))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    DAY_DATA=('all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')

    day = input('Write a day of the week or type all to select the seven days. ').lower()

    while day not in DAY_DATA:
        print ('The day entered does not exist, please try again.')
        day = input('Write a day of the week or type all to select the seven days. ').lower()
    print('The selected day is: {}'.format(day))

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
    df = pd.read_csv('{}.csv'.format(city).replace(' ', '_'))
    # The data type is changed to'Start Time' column
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # TO DO: display the most common month
    # Improvement point, show te city in string type#
    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].mode()[0]
    print('\nThe most common month of travel is {}\n'.format(common_month))

    # TO DO: display the most common day of week
    df['day'] = df['Start Time'].dt.day
    common_day = df['day'].mode()[0]
    print('\nThe most common day of travel is {}\n'.format(common_day))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('\nThe most common hour of travel is {}\n'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    S_Station_count_dict = {}

    for StartStation in df['Start Station']:
        if StartStation not in S_Station_count_dict:
            S_Station_count_dict[StartStation] = 1
        else:
            S_Station_count_dict[StartStation] += 1

    highest_count = max(S_Station_count_dict.values())

    most_start = [key for key, value in S_Station_count_dict.items() if value == highest_count]
    print('\nThe most commonly station of start is {}'.format(most_start))

    # TO DO: display most commonly used end station
    E_Station_count_dict = {}

    for EndStation in df['End Station']:
        if EndStation not in E_Station_count_dict:
            E_Station_count_dict[EndStation] = 1
        else:
            E_Station_count_dict[EndStation] += 1

    highest_count_end = max(E_Station_count_dict.values())

    most_end = [key for key, value in E_Station_count_dict.items() if value == highest_count_end]
    print('\nThe most commonly station of end is {}'.format(most_end))


    # TO DO: display most frequent combination of start station and end station trip
    frequent_journey = df.groupby (['Start Station', 'End Station']).size().reset_index().rename(columns = {0: 'Count'}).sort_values(by=['Count'], ascending = False)
    max_frequency = frequent_journey.head(1)
    print ('\nThe most popular journey, station on start and end are: \n {}'.format(max_frequency))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\n The total travel time is {}'.format(total_travel_time) +' Seconds')

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nThe mean travel time is {}'.format(mean_travel_time) +' Seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].value_counts()
    print('The types of users are: \n{}' .format(user_type))

    # TO DO: Display counts of gender
    while True:
        try:
            gender_type = df['Gender'].value_counts()
            print('The users classified by gender are: \n{}' .format(gender_type))
            max_birth_year = df.groupby(['Gender'])['Birth Year'].max()
            min_birth_year = df.groupby(['Gender'])['Birth Year'].min()
            mode_birth_year = df['Birth Year'].mode()
            print ('1. The most recent year of birth is: {}\n2. The most earliest year of birth is: {}\n3. The most common year of birth is: {}'.format(max_birth_year, min_birth_year, mode_birth_year))

    # TO DO: Display earliest, most recent, and most common year of birth


            print("\nThis took %s seconds." % (time.time() - start_time))
            print('-'*40)
            break
        except:
            print('\n Sorry, the genre field does not exist in the selected file, so no results are shown.')
            break

#To display five records of the file#
# Improvement point, a single question to enter the cycle#
def data(df):
    row_data = 0
    while True:
        response = input("Do you want to see five records of the file? Yes or No ").lower()
        if response not in ['yes', 'no']:
            response = input("You must write Yes or No.").lower()
        elif response == 'yes':
            row_data += 5
            print(df.iloc[row_data : row_data + 5])
            again = input("Do you want to see other five records? Yes or No ").lower()
            if again == 'no':
                break
        elif response == 'no':
            return

def main():
    city = ""
    month = ""
    day = ""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
