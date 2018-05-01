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

    KEYS_OF_INTEREST = {'timestamp': True,
                        'duration' : True,
                        'to'       : True }

    INTERMEDIATE_KEYS = {'memory' : True,
                         'pid'    : True }

    KEYS_TO_CONVERT_TO_INTEGERS = { MEMORY     : True,
                                    'duration' : True }

    MEMORY_BY_PID = {}

    def __init__(self, line):
        self.line = line

    def memory_growth(self, intermediate):
        # How much did memory increase since the last request of this same PID
        pid    = intermediate[self.PID]

        # Last character will be newline
        memory = intermediate[self.MEMORY]

        memory_before = memory

        if pid in self.MEMORY_BY_PID:
            memory_before = self.MEMORY_BY_PID[pid]

        self.MEMORY_BY_PID[pid] = memory
        return(memory - memory_before)

    def parse(self):
        snippets = deque(self.line.split(self.SPACE))
        output = { 'timestamp' : snippets.popleft() }
        intermediate = {}
        for snip in snippets:
            key, value = snip.split(self.COLON)
            if key in self.KEYS_TO_CONVERT_TO_INTEGERS:
                value = int(value.strip())
            if key in self.KEYS_OF_INTEREST:
                output[key] = value
            if key in self.INTERMEDIATE_KEYS:
                intermediate[key] = value

        output[self.MEMORY_GROWTH] = self.memory_growth(intermediate)


        return(output)




class Dyno:
    GREPPED_LOG = '../shared_log_files/grepped_for_performance_report.log'
    HEAD_COUNT  = 5
    TITLE_WIDTH = 124

    NAME_MAP = {'duration':'mean_duration', 'memory_growth': 'mean_memory_growth'}

    def __init__(self):
        pd.set_option('display.expand_frame_repr', False)

    def process(self):
        with open(self.GREPPED_LOG) as f:
            dicts = []
            for line in f:
                p = LineParser(line)
                dicts.append(p.parse())
            all_data = pd.DataFrame(dicts)

        report = all_data.groupby('to').agg('mean').rename(columns=self.NAME_MAP)

        report['hits'] = all_data.groupby('to').agg('size')
        report['total_duration'] = report.mean_duration * report.hits
        report['total_memory_growth'] = report.mean_memory_growth * report.hits

        self.report = report

    def print_title(self, by, manual_content=None):
        content = f'Top {self.HEAD_COUNT} Sorted By {by.upper()}'
        if manual_content:
            content = manual_content
        dots_after = ' ' * self.TITLE_WIDTH
        line = f'\n\n\n### {content}{dots_after}'
        print(line[:self.TITLE_WIDTH])

    def enhanced_columns(self, column_to_enhance):
        columns = self.report.columns.tolist()
        new_columns = []
        for cc in columns:
            if cc == column_to_enhance:
                cc = cc.upper()
            new_columns.append(cc)
        return(new_columns)


    def print_ranking(self, by):
        ordered = self.report.sort_values(by, ascending=False)
        ordered.columns = self.enhanced_columns(by)
        self.print_title(by)
        print(ordered.head(self.HEAD_COUNT))

    def print_glossary(self):
        g = ('\n\n## Glossary\n'
                'hits:                Total number of requests in log file.\n'
                'mean_duration:       Mean response time for puma process\n'
                'total_duration:      hits * mean_duration\n'
                'mean_memory_growth:  Mean delta resident size (MB) between two consecutive requests by the same PID.\n'
                '                     Note memory is reported as an integer.\n'
                '                     Also note that because puma is multithreaded, delta resident size is expected to \n'
                '                     bleed onto other concurrent requests.\n'
                'total_memory_growth: hits * mean_memory_growth\n')
        print(g)

    def print(self):
        for column in self.report.columns.tolist():
            self.print_ranking(column)

        self.print_title('', manual_content='All Data Sorted by Endpoint')
        print(self.report)
        self.print_glossary()




#p = LineParser('2018-03-14T10:21:40 method:GET path:/house_dashboard/recent_alerts status:200 duration:4 pid:52 duration:34 to:alerts#index browser:da9940e2 memory:5\n')


d = Dyno()
d.process()
d.print()
