from collections import deque

# Typical line that gets parsed
#   '2018-03-14T10:21:40 method:GET path:/house_dashboard/recent_alerts status:200 duration:4 pid:52 duration:34 to:alerts#index browser:da9940e2 memory:5\n'
class LineParser:
    SPACE = ' '
    COLON = ':'
    MEMORY_GROWTH = 'memory_growth'
    PID           = 'pid'
    MEMORY        = 'memory'

    KEYS_OF_INTEREST            = { 'timestamp', 'duration', 'to', 'browser', 'android' }
    INTERMEDIATE_KEYS           = { MEMORY, PID }
    KEYS_TO_CONVERT_TO_INTEGERS = { MEMORY, 'duration' }

    # (class) variable that gets updated by each LineParser
    memory_by_pid = {}


    def __init__(self, line):
        self.line = line


    def parse(self):
        snippets = deque(self.line.split(self.SPACE))
        output = { 'timestamp' : snippets.popleft() }
        intermediate = {}
        for snip in snippets:
            try:
                key, value = snip.split(self.COLON, 1)
            except(ValueError) as e:
                print(f'\nERROR: unable to parse {snippets}\n')
                raise(e)
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

        if pid in self.memory_by_pid:
            memory_before = self.memory_by_pid[pid]

        self.memory_by_pid[pid] = memory
        return(memory - memory_before)
