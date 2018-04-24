import pdb
import pandas as pd
import numpy  as np
from collections import deque

# Run this first to remove lines that don't have browser: or android:
# Make sure line has all the things we expect
# And discard if it has "unknown" (site-24x7)
#   cat production.log | grep method: | grep path: | grep status: | grep duration: | grep to: grep -v unknown > production-grepped.log

array_of_dicts = []
with open('kept.log', 'r') as f:
    for line in f:
        my_dict = {}

        my_array = line.split(' ')
        my_deque = deque(my_array)
        my_dict['timestamp'] = my_deque.popleft()

        for pair in my_deque:
            #pdb.set_trace()

            if len(pair) < 2:
                pdb.set_trace()
            key, value = pair.split(':', 1)
            my_dict[key] = value

        items_of_interest = {}
        items_of_interest['hour'] = my_dict['timestamp'][0:13]
        items_of_interest['to'] = my_dict['to']
        items_of_interest['duration'] = int(my_dict['duration'])

        array_of_dicts.append(items_of_interest)

data_frame = pd.DataFrame(array_of_dicts)
aggregates = {'duration' : [np.mean, np.size]}
new_names  = {'mean' : 'mean_duration', 'size' : 'requests_per_day' }

#payload = data_frame.groupby('to').agg(aggregates).sort_values(['duration'])
#payload = data_frame.groupby('to').agg(aggregates).rename(columns=new_names).sort_values(by='mean')


payload = data_frame.groupby('to').agg(aggregates).rename(columns=new_names)

# Additional Column added
payload['total_duration'] = payload.duration.mean_duration * payload.duration.requests_per_day

sorted_by_mean_duration    = payload.sort_values(by=[('duration', 'mean_duration')])
sorted_by_requests_per_day = payload.sort_values(by=[('duration', 'requests_per_day')])
sorted_by_total_duration   = payload.sort_values(by='total_duration')

with open('stats.dataframe', 'w') as f:
    f.write('\n\nSORTED BY MEAN DURATION')
    f.write(sorted_by_mean_duration.to_string())

    f.write('\n\nSORTED BY REQESTS PER DAY')
    f.write(sorted_by_requests_per_day.to_string())

    f.write('\n\nSORTED BY TOTAL DURATION')
    f.write(sorted_by_total_duration.to_string())




