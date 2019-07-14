# Code to create new columns for CSV!

from datetime import datetime
import pandas as pd
data = pd.read_csv('full_dataset.csv')

def years_yelping(yelping_since):
    '''

    '''

    yelping_since = datetime.strptime(yelping_since, '%Y-%m-%d %H:%M:%S')
    years_yelping = datetime(2019, 1, 15, 0, 0, 0) - yelping_since
    years_yelping = years_yelping.days / 365

    return years_yelping

data['years_yelping'] = data['yelping_since'].apply(years_yelping)
data['total_compliments_given'] = data['useful'] + data['funny'] + data['cool']
data['total_compliments_received'] = data['num_hot_compliment'] + \
data['num_more_compliment'] + data['num_profile_compliment'] + \
data['num_cute_compliment'] + data['num_list_compliment'] + \
data['num_note_compliment'] + data['num_plain_compliment'] + \
data['num_cool_compliment'] + data['num_funny_compliment'] + \
data['num_writer_compliment'] + data['num_photos_compliment']
# ^more concise way of writing this? probably


data.to_csv("full_dataset_final.csv", index = False)