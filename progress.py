#!/usr/bin/env python
"""
http://code.activestate.com/recipes/473899-progress-meter/
2006-02-20 Denis Barmenkov: ANSI codes replaced by Backspace (0x08) characters

also nice: http://code.google.com/p/python-progressbar/
"""
import time, sys, math

class ProgressMeter(object):
    #ESC = chr(27)
    def __init__(self, **kw):
        # What time do we start tracking our progress from?
        self.timestamp = kw.get('timestamp', time.time())
        # What kind of unit are we tracking?
        self.unit = str(kw.get('unit', ''))
        # Number of units to process
        self.total = int(kw.get('total', 100))
        # Number of units already processed
        self.count = int(kw.get('count', 0))
        # Refresh rate in seconds
        self.rate_refresh = float(kw.get('rate_refresh', .5))
        # Number of ticks in meter
        self.meter_ticks = int(kw.get('ticks', 60))
        self.meter_division = float(self.total) / self.meter_ticks
        self.meter_value = int(self.count / self.meter_division)
        self.last_update = None
        self.rate_history_idx = 0
        self.rate_history_len = 4
        self.rate_history = [None] * self.rate_history_len
        self.rate_current = 0.0
        self.rate_avg = 0.0
        self.last_refresh = 0
        self.prev_meter_len = 0

    def update(self, count, **kw):
        now = time.time()
        # Caclulate rate of progress
        rate = 0.0
        frate = 0.0
        # Add count to Total
        self.count += count
        self.count = min(self.count, self.total)
        if self.last_update:
            fdelta = now - float(self.timestamp)
            if fdelta:
                frate = self.count / fdelta
            else:
                frate = count
            delta = now - float(self.last_update)
            if delta:
                rate = count / delta
            else:
                rate = count
            self.rate_history[self.rate_history_idx] = rate
            self.rate_history_idx += 1
            self.rate_history_idx %= self.rate_history_len
            cnt = 0
            total = 0.0
            # Average rate history
            for rate in self.rate_history:
                if rate == None:
                    continue
                cnt += 1
                total += rate
            rate = total / cnt
        self.rate_current = rate
        self.rate_avg = frate
        self.last_update = now
        # Device Total by meter division
        value = int(self.count / self.meter_division)
        if value > self.meter_value:
            self.meter_value = value
        if self.last_refresh:
            if (now - self.last_refresh) > self.rate_refresh or \
                (self.count >= self.total):
                    self.refresh()
        else:
            self.refresh()

    def get_meter(self, **kw):
        bar = '-' * self.meter_value
        pad = ' ' * (self.meter_ticks - self.meter_value)
        perc = (float(self.count) / self.total) * 100
        cnt = self.count
        tot = self.total
        cur = self.rate_current
        avg = self.rate_avg
        return '[%s>%s] %d%%  (%d of %d)   cur: %.1f/sec   avg: %.1f/sec' % (bar, pad, perc, cnt, tot, cur, avg)

    def refresh(self, **kw):
        # Clear line and return cursor to start-of-line
        sys.stdout.write(' ' * self.prev_meter_len + '\x08' * self.prev_meter_len)
        # Get meter text
        meter_text = self.get_meter(**kw)
        # Write meter and return cursor to start-of-line
        sys.stdout.write(meter_text + '\x08'*len(meter_text))
        self.prev_meter_len = len(meter_text)

        # Are we finished?
        if self.count >= self.total:
            sys.stdout.write('\n')
        sys.stdout.flush()
        # Timestamp
        self.last_refresh = time.time()


if __name__ == '__main__':
    import time
    import random

    total = 1000
    p = ProgressMeter(total=total)

    while total > 0:
        cnt = random.randint(1, 25)
        p.update(cnt)
        total -= cnt
        time.sleep(random.random())
