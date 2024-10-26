from praytimes import PrayTimes
import time
from datetime import date, timedelta, datetime
import pandas as pd
from ics import Calendar, Event

# Initialize PrayTimes object with the desired calculation method
PT = PrayTimes('Karachi')  # Available methods: MWL, ISNA, Egypt, Makkah, Karachi, Tehran, Jafri

# Adjust Asr calculation to Hanafi
PT.adjust({'asr': 'Hanafi'})  # Available options: 'Hanafi', 'Standard'

def get_prayer_times(start_date, end_date, latitude, longitude):
    """
    Calculates prayer times for a given date range and location.

    Args:
        start_date: The starting date in YYYY-MM-DD format.
        end_date: The ending date in YYYY-MM-DD format.
        latitude: The latitude of the location.
        longitude: The longitude of the location.

    Returns:
        A pandas DataFrame with date and prayer times (Fajr, Sunrise, Dhuhr, Asr, Maghrib, Isha) as columns.
    """

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    # Initialize an empty list to store prayer times data
    prayer_times_data = []

    current_date = start_date
    while current_date <= end_date:
        prayer_times = PT.getTimes(current_date, (latitude, longitude), 6)  # Get prayer times for the current date
        # Append prayer time data to the list as a dictionary
        prayer_times_data.append({'Date': current_date.strftime('%Y-%m-%d'), **prayer_times})
        current_date += timedelta(days=1)

    # Create the DataFrame from the list of dictionaries
    prayer_times_df = pd.DataFrame(prayer_times_data)

    return prayer_times_df

def create_prayer_calendar(prayer_times_df): 
    """
    Creates an .ics calendar file with all prayer times, 
    allowing different durations for Dhuhr prayer.

    Args:
        prayer_times_df: A pandas DataFrame with date and prayer times.

    Returns:
        An ics.Calendar object.
    """

    c = Calendar()

    # Get default prayer duration
    default_duration = int(input("Enter default prayer duration in minutes (e.g., 15): "))

    # Ask for Dhuhr duration
    dhuhr_duration = input(f"Enter Dhuhr prayer duration in minutes (default: {default_duration}, press Enter to use default): ")
    dhuhr_duration = int(dhuhr_duration) if dhuhr_duration else default_duration

    for index, row in prayer_times_df.iterrows():
        date_str = row['Date']
        for prayer, time_str in row.items():
            if prayer != 'Date':
                prayer_time = datetime.strptime(time_str, '%H:%M').time()
                
                e = Event()
                e.name = prayer  # Set event name to the prayer name
                e.begin = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')  # Combine date and time string for event start time
                e.created = datetime.now()  # Set event creation time to now

                # Set duration based on prayer (case-insensitive comparison)
                if prayer.lower() == 'dhuhr': 
                    duration = dhuhr_duration
                else:
                    duration = default_duration
                e.end = e.begin + timedelta(minutes=duration)  # Calculate event end time by adding duration to start time
                c.events.add(e)  # Add the event to the calendar

    return c

# Get start and end dates from the user
start_date_str = input("Enter the start date in YYYY-MM-DD format: ")
end_date_str = input("Enter the end date in YYYY-MM-DD format: ")

# Get latitude and longitude from the user
latitude = float(input("Enter the latitude: "))
longitude = float(input("Enter the longitude: "))

# Calculate prayer times
prayer_times_df = get_prayer_times(start_date_str, end_date_str, latitude, longitude)

# Create the .ics calendar 
prayer_calendar = create_prayer_calendar(prayer_times_df) 

# Save the calendar to a file
with open('prayer_times.ics', 'w') as f:
    f.writelines(prayer_calendar)

print("prayer_times.ics file created successfully.")