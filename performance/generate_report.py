import pdb
import pandas as pd
import numpy as np
from collections import deque

class LineParser:
    SPACE = ' '
    COLON = ':'
    MEMORY_GROWTH = 'memory_growth'
    PID           = 'pid'
    MEMORY        = 'memory'

    KEYS_OF_INTEREST            = set(['timestamp', 'duration', 'to'])
    INTERMEDIATE_KEYS           = set([MEMORY, PID])
    KEYS_TO_CONVERT_TO_INTEGERS = set([MEMORY, 'duration'])

    MEMORY_BY_PID = {}

    def __init__(self, line):
        self.line = line


    def parse(self):
        snippets = deque(self.line.split(self.SPACE))
        output = { 'timestamp' : snippets.popleft() }
        intermediate = {}
        for snip in snippets:
            key, value = snip.split(self.COLON, 1)
            if key in self.KEYS_TO_CONVERT_TO_INTEGERS:
                value = int(value.strip())
            if key in self.KEYS_OF_INTEREST:
                output[key] = value
            if key in self.INTERMEDIATE_KEYS:
                intermediate[key] = value

        output[self.MEMORY_GROWTH] = self.__memory_growth(intermediate)


        return(output)

    def __memory_growth(self, intermediate):
        # How much did memory increase since the last request of this same PID
        pid = intermediate[self.PID]

        memory        = intermediate[self.MEMORY]
        memory_before = memory

        if pid in self.MEMORY_BY_PID:
            memory_before = self.MEMORY_BY_PID[pid]

        self.MEMORY_BY_PID[pid] = memory
        return(memory - memory_before)




class PerformanceReport:
    GREPPED_LOG = '../shared_log_files/grepped_for_performance_report.log'
    HEAD_COUNT  = 10
    TITLE_WIDTH = 124

    NAME_MAP = {'duration': 'mean_duration_ms',
                'memory_growth': 'mean_memory_growth_mb',
                'median_duration': 'median_duration_ms'}
    SORTED_COLUMNS = 'median_duration_ms 90p_duration_ms total_duration_ms hits mean_memory_growth_mb total_memory_growth_mb'.split()

    def __init__(self):
        pd.set_option('display.expand_frame_repr', False)

    def process(self):
        with open(self.GREPPED_LOG) as f:
            dicts = []
            for line in f:
                p = LineParser(line)
                dicts.append(p.parse())
            all_data = pd.DataFrame(dicts)

        grouped = all_data.groupby('to')

        report = grouped.agg('mean').rename(columns=self.NAME_MAP)

        report['hits'] = grouped.agg('size')
        report['total_duration_ms'] = report.mean_duration_ms * report.hits
        report['total_memory_growth_mb'] = report.mean_memory_growth_mb * report.hits

        report['median_duration_ms'] = grouped.quantile()['duration']
        report['90p_duration_ms'] = grouped.quantile(0.9)['duration']

        # Remove unwanted intermediate columns
        del report['mean_duration_ms']

        self.report = report.reindex(self.SORTED_COLUMNS, axis=1)


    def print(self):
        for column in self.report.columns.tolist():
            self.__print_ranking(column)

        self.__print_title('', manual_content='All Data Sorted by Endpoint')
        with pd.option_context('display.max_rows', 1000):
            print(self.report)
        self.__print_glossary()

    def __print_title(self, by, manual_content=None):
        content = f'Top {self.HEAD_COUNT} Sorted By {by.upper()}'
        if manual_content:
            content = manual_content
        dots_after = ' ' * self.TITLE_WIDTH
        line = f'\n\n\n### {content}{dots_after}'
        print(line[:self.TITLE_WIDTH])

    def __enhanced_columns(self, column_to_enhance):
        columns = self.report.columns.tolist()
        new_columns = []
        for cc in columns:
            if cc == column_to_enhance:
                cc = cc.upper()
            new_columns.append(cc)
        return(new_columns)


    def __print_ranking(self, by):
        ordered = self.report.sort_values(by, ascending=False)
        ordered.columns = self.__enhanced_columns(by)
        self.__print_title(by)
        print(ordered.head(self.HEAD_COUNT))

    def __print_glossary(self):
        g = ('\n\n## Glossary\n'
                'hits:                   Total number of requests in log file.\n'
                'median_duration_ms:     Median response time for puma process, in milliseconds\n'
                '90p_duration_ms:        90th percentile of response time for puma process, in milliseconds\n'
                '                        (90 % of requests are faster than this)\n'
                'total_duration_ms:      total time spent processing requests, in milliseconds (Equivalent to hits * mean_duration_ms)\n'
                'mean_memory_growth_mb:  Mean delta resident size (MB) between two consecutive requests by the same PID.\n'
                '                        Note memory is reported as an integer.\n'
                '                        Also note that because puma is multithreaded, delta resident size is expected to \n'
                '                        bleed onto other concurrent requests.\n'
                'total_memory_growth_mb: hits * mean_memory_growth_mb\n')
        print(g)





#p = LineParser('2018-03-14T10:21:40 method:GET path:/house_dashboard/recent_alerts status:200 duration:4 pid:52 duration:34 to:alerts#index browser:da9940e2 memory:5\n')



# TODO verify that input is a FILE, not a DIR
r = PerformanceReport()
r.process()
r.print()
