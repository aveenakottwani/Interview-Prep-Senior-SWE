from enum import Enum
from typing import Dict, List
from collections import deque,defaultdict

class SeverityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class AlertMonitor:
    
    def __init__(self) -> None:
        self.recent = deque()  # timestamps
        self.hours = {}  # hour -> {sev: int}
        self.minutes = deque()  # [minute, count]


    def record_alert(self, ts: int, sev: SeverityLevel) -> None:
        """Record an alert with a timestamp (seconds) and severity."""
        self.recent.append(ts)
        while self.recent[0] < ts - 900:
            self.recent.popleft()

        h = ts // 3600
        if h not in self.hours:
            self.hours = {h: {s: 0 for s in SeverityLevel}}  # drops old hour
        self.hours[h][sev] += 1

        m = ts // 60
        if self.minutes and self.minutes[-1][0] == m:
            self.minutes[-1][1] += 1
        else:
            self.minutes.append([m, 1])
        while self.minutes[0][0] <= m - 15:                   # keep 15 minutes
            self.minutes.popleft()

    def report_alerts_last_15_min(self, t: int) -> int:
        """Return the number of alerts in the last 900 seconds."""
        while self.recent and self.recent[0] < t - 900:
            self.recent.popleft()
        return len(self.recent)

    def report_severity_distribution(self, t: int) -> Dict[SeverityLevel, int]:
        """
        Return counts per severity within the current hour.
        Current hour = the 3600-second block containing the most
        recent timestamp. Example: most recent = 3720 → block 3600..7199.
        """
        counts = self.hours.get(t // 3600)
        return dict(counts) if counts else {s: 0 for s in SeverityLevel}

    def detect_alert_volume_spike(self) -> List[int]:
        """
        For each minute in the last 15 min of data, return the index of
        the next minute with a greater alert count to its right, else -1.
        Example:
        Minutes:      0, 1, 2, 3, 4, 5
        Counts:      [1, 2, 5, 2, 2, 1]
        Output:      [1, 2, -1, 4, -1, -1]
        """

        counts = [c for _, c in self.minutes]
        res, stack = [-1] * len(counts), []
        for i in range(len(counts) - 1, -1, -1):
            while stack and counts[stack[-1]] < counts[i]:
                stack.pop()
            if stack:
                res[i] = stack[-1]  # peek, don't pop
            stack.append(i)
        return res

am=AlertMonitor()

am.record_alert(30,SeverityLevel.MEDIUM)
am.record_alert(65,SeverityLevel.MEDIUM)
am.record_alert(70,SeverityLevel.LOW)
am.record_alert(120,SeverityLevel.MEDIUM)
am.record_alert(125,SeverityLevel.MEDIUM)
am.record_alert(125,SeverityLevel.HIGH)
am.record_alert(125,SeverityLevel.MEDIUM)
am.record_alert(125,SeverityLevel.HIGH)
am.record_alert(180,SeverityLevel.MEDIUM)
am.record_alert(180,SeverityLevel.MEDIUM)
am.record_alert(240,SeverityLevel.LOW)
am.record_alert(240,SeverityLevel.HIGH)
am.record_alert(300,SeverityLevel.LOW)

print(am.report_alerts_last_15_min(45))
print(am.report_severity_distribution(45))
print(am.detect_alert_volume_spike())


