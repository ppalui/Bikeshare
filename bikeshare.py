import pandas as pd
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by
        (str) day - name of the day of week to filter by
    """

    city = str(input("Which city do you like to analyse Chicago, New York or Washington?\n")).lower().strip()
    while city not in CITY_DATA.keys():
        city = str(input("\nInvalid city name, please try again.\n")).lower().strip()

    month = str(input("\nWould you like to filter data by month?\nPlease type month in full or “skip” for no month filter.\n")).title().strip()
    # Check is input is in the list ['January', 'February', 'March', 'April', 'May', 'June']
    while month not in calendar.month_name[1:7] and month != "Skip":
        month = str(input("\nInvalid input, please try again.\n")).title().strip()

    day = str(input("\nWould you like to filter data by day?\nPlease type day of week or “skip” for no day filter.\n")).title().strip()
    # Check is input is in the list ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    while day not in calendar.day_name and day != "Skip":
        day = str(input("\nInvalid input, please try again.\n")).title().strip()

    return city, month, day

def cleansing_data(df):
    #Handle NaN or missing data.
    target_column = ['User Type', 'Gender','Birth Year']
    df[target_column]=df[target_column].fillna(df.mode().iloc[0])
    return df


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by
        (str) day - name of the day of week to filter by
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time and End time columns to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #Handle NaN or missing data.
    if city in list(CITY_DATA)[:2]:
        df = cleansing_data(df)

    # Extract hour from Start Time and End Time columns to create a new hour columns.
    df['Start Hour'] = df['Start Time'].dt.hour
    df['End Hour'] = df['End Time'].dt.hour
    # Extract month and day from Start Time column to create a new month and day columns.
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday_name

    return df

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    """
    print("\n{}\nThe most popular stations and trip.\n{}\n".format('.'*50, '.'*50))

    # display most commonly used start station
    print("The most popular starting point is : {} station\n".format(df["Start Station"].mode()[0]))

    # display most commonly used end station
    print("The most popular ending point is : {} station\n".format(df["End Station"].mode()[0]))

    # find the most common matching between start station and end station.
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().reset_index().max()
    # display most frequent combination of start station and end station trip
    print("The most common trip is : a trip from {} to {}, {} times\n"
    .format(most_common_trip["Start Station"],most_common_trip["End Station"], most_common_trip[0]))

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    """
    print("\n{}\nThe total and average trip duration.\n{}\n".format('.'*50, '.'*50))

    # display total travel time
    print("Total trip duration is {} hours\n".format(df["Trip Duration"].sum()/360))

    # display mean travel time
    print("Average trip duration is {} hours\n".format(df["Trip Duration"].mean()/360))

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    """
    print("\n{}\nThe most frequent times of travel.\n{}\n".format('.'*50, '.'*50))

    # display the most common month
    print("The most common month is {}\n".format(df["Month"].mode()[0]))

    # display the most common day of week
    print("The most common day of week is {}\n".format(df["Day"].mode()[0]))

    # display the most common start hour
    print("The most common start hour is {}\n".format(df["Start Hour"].mode()[0]))
    print("The most common end hour is {}\n".format(df["End Hour"].mode()[0]))

def user_stats(df):
    """
    Displays statistics on bikeshare users.

    """
    print("\n{}\nBikeshare users statistics\n{}\n".format('.'*50, '.'*50))

    # Display counts of user types
    subscriber = df["User Type"].value_counts()["Subscriber"]
    customer = df["User Type"].value_counts()["Customer"]
    print("The quantity of each user type.\n\tSubscriber : {}\n\tCustomer : {}\n".format(subscriber, customer))

    # Display counts of gender
    if "Gender" in df.columns:
        male = df["Gender"].value_counts()["Male"]
        female = df["Gender"].value_counts()["Female"]
        print("The quantity of each gender.\nMale : {}\nFemale : {}\n".format(male, female))

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        print("The most common birth year is {}\n".format(int(df["Birth Year"].mode()[0])))

def main():
    while True:
        print("\t\n{}\n\nHello!, Let’s explore some US bikeshare data!\n\n{}\n".format('#'*50, '#'*50))

        city, month, day = get_filters()

        print("\n{} Loading Data {}\n".format('.'*20, '.'*20))
        df = load_data(city, month, day)

        print("\n{} Processing Data {}\n".format('.'*20, '.'*20))

        station_stats(df)
        trip_duration_stats(df)
        time_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower().strip() != 'yes':
            break

if __name__ == "__main__":
	main()
