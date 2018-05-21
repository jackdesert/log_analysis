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

class PerformanceReport:
    DEFAULT_GREPPED_LOG = '../shared_log_files/grepped_for_performance_report.log'

    NAME_MAP = {'duration':'mean_duration_ms', 'memory_growth': 'mean_memory_growth_mb'}

    TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S'
    MINUTES_PER_HOUR = 60
    MINUTES_PER_DAY = 24 * MINUTES_PER_HOUR

    RES_10 = 10
    RES_60 = 60
    ACCEPTABLE_RESOLUTIONS = set([RES_10, RES_60])

    def __init__(self, res, grepped_log, output_dir):
        pd.set_option('display.expand_frame_repr', False)
        self.grepped_log = grepped_log
        self.output_dir  = output_dir
        self.res = res
        if res not in self.ACCEPTABLE_RESOLUTIONS: raise


    @property
    def bin_count(self):
        return (self.MINUTES_PER_DAY // self.res)

    @property
    def range_max(self):
        return (self.bin_count - 1)

    def plot(self, data, title):
        # Some endpoints receive no hits in a period.
        # Make sure there is one data point in the bar graph regardless
        palette = np.zeros(self.bin_count)

        # Fill in Values that actually received hits
        for string_index, value in zip(data.index, data.values):
            if self.res == self.RES_10:
                hours = int(string_index[0:2])
                tens_of_minutes = int(string_index[3])
                minutes = self.MINUTES_PER_HOUR * hours + 10 * tens_of_minutes
                palette_index = minutes // self.res
                palette[palette_index] = value
            elif self.res == self.RES_60:
                palette[int(string_index)] = value


        if self.res == self.RES_60:
            ylabel = 'Hits per hour'
            plot_function = 'bar'
        elif self.res == self.RES_10:
            ylabel = 'Hits per 10 min'
            plot_function = 'plot'

        getattr(plt, plot_function)(range(self.bin_count), palette, 0.9)
        plt.xlabel('Hour')
        plt.ylabel(ylabel)
        plt.title(title, fontweight='bold')

        # set the locations of the xticks
        #xticks_loc = [ idx * 6 for idx in range(len(all_endpoints_by_60))]
        #plt.xticks( xticks_loc )

        # set the locations and labels of the xticks
        #xticks( arange(5), ('Tom', 'Dick', 'Harry', 'Sally', 'Sue') )
        base_ticks = [0, self.bin_count / 4, self.bin_count / 2, self.bin_count * 3/4]
        offset_ticks = [t - 0.45 for t in base_ticks]
        plt.xticks(offset_ticks, ['0:00', '6:00', '12:00', '18:00'])
        #if self.res == self.RES_60:
        #    plt.xticks([-0.45, 5.55, 11.55, 17.55], ['0:00', '6:00', '12:00', '18:00'])
        #elif self.res == self.RES_10:
        #    plt.xticks([-0.45, 5.55, 11.55, 17.55], ['0:00', '6:00', '12:00', '18:00'])

        t = title.replace('/', '__').replace('#', '-')
        png_filename = f'{ t }--max-{ data.max() }.png'
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



        if self.res == self.RES_10:
            to_res_10 = np.vectorize(lambda x: x[11:15])
            data['timestamp_res_10']   = to_res_10(data.timestamp)
            hist = data.groupby('timestamp_res_10').agg('size')
        elif self.res == self.RES_60:
            to_res_60 = np.vectorize(lambda x: x[11:13])
            data['timestamp_res_60']   = to_res_60(data.timestamp)
            hist = data.groupby('timestamp_res_60').agg('size')


        self.plot(hist, 'all_endpoints')

        endpoints = data.to.unique()
        endpoints.sort()
        for ep in endpoints:
            if self.res == self.RES_10:
                hist = data[data['to'] == ep].groupby('timestamp_res_10').agg('size')
                self.plot(hist, ep)
            elif self.res == self.RES_60:
                hist = data[data['to'] == ep].groupby('timestamp_res_60').agg('size')
                self.plot(hist, ep)




if __name__ == '__main__':
    # Accept filename as input, with fallback to default
    grepped_log = PerformanceReport.DEFAULT_GREPPED_LOG
    output_dir  = '.'

    if len(sys.argv) > 1:
        grepped_log = sys.argv[1]

    if len(sys.argv) > 2:
        output_dir  = sys.argv[2]

    r = PerformanceReport(10, grepped_log, output_dir)
    r.process()
