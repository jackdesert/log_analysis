from lib import parser

import numpy as np
import pdb
import pandas as pd
import sys
import matplotlib

# Specify backend before importing pyplot
# Using the Agg backend because it is available on systems with no X-server
matplotlib.use('Agg')

import matplotlib.pyplot as plt

class Report:
    DEFAULT_GREPPED_LOG = '../shared_log_files/grepped_for_performance_report.log'

    SECONDS_PER_HOUR = 3600


    def __init__(self, grepped_log, output_dir):
        pd.set_option('display.expand_frame_repr', False)
        self.grepped_log = grepped_log
        self.output_dir  = output_dir


    def plot(self, data, title):
        # Scatter plot of 'seconds_since_midnight' vs 'duration'

        plt.scatter(data['seconds_since_midnight'], data['duration'])

        plt.xlabel('Time of Day')
        plt.ylabel('Response Time (ms)')
        plt.title(f'Response Time vs Time of Day', fontweight='bold')

        ticks_in_seconds = np.array([0, 6, 12, 18]) * self.SECONDS_PER_HOUR

        plt.xticks(ticks_in_seconds, ['0:00', '6:00', '12:00', '18:00'])

        plt.ylim(ymin=0)

        t = title.replace('/', '__').replace('#', '-')
        png_filename = f'{ t }__duration-scatter.png'
        abs_filename = f'{self.output_dir}/{png_filename}'
        print(f'Saving to { abs_filename }')
        plt.savefig(abs_filename)
        plt.clf()



    def process(self):
        with open(self.grepped_log) as f:
            dicts = []
            for line in f:
                p = parser.LineParser(line)
                dicts.append(p.parse())
            data = pd.DataFrame(dicts)


        to_seconds_since_midnight = np.vectorize(lambda x: int(x[11:13]) * 3600 + int(x[14:16]) * 60 + int(x[17:19]))

        data['seconds_since_midnight'] = to_seconds_since_midnight(data.timestamp)

        self.plot(data, 'all_endpoints')

        endpoints = data.to.unique()
        endpoints.sort()
        for ep in endpoints:
            scatter = data[data['to'] == ep]
            self.plot(scatter, ep)




if __name__ == '__main__':
    # Accept filename as input, with fallback to default
    grepped_log = Report.DEFAULT_GREPPED_LOG
    output_dir  = '/tmp'

    if len(sys.argv) > 1:
        grepped_log = sys.argv[1]

    if len(sys.argv) > 2:
        output_dir  = sys.argv[2]

    r = Report(grepped_log, output_dir)
    r.process()
