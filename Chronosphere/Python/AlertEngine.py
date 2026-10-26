from dataclasses import dataclass
from enum import Enum
import heapq
import sys

class AlertStatus(Enum):
    IDLE = "idle"
    PENDING = "pending"
    FIRED = "fired"

@dataclass
class AlertRule:
    name:str
    metric:str
    threshold:int
    for_seconds:int
    repeat_seconds:int
    status: AlertStatus=AlertStatus.IDLE
    version:int=1



class AlertEngine:
    def __init__(self):
        # alertruleMap key=metric , value=[alert indexes]
        self.alertRulesMetric = {}
        self.alerts=[]
        # (timestamp+for_seconds, metric, alert_index,version)
        self.heap=[]
        self.result=[]



    def drain(self, timestamp):
        while len(self.heap)>0 and self.heap[0][0] <= timestamp:
            timestamp_for_alert, metric, alert_index, version=heapq.heappop(self.heap)
            rule=self.alerts[alert_index]
            if rule.version != version:
                # discard this as the event has expired/resolved
                continue
            if rule.status is AlertStatus.PENDING:
                self.result.append(("ALERT", rule.metric, rule.name,timestamp_for_alert))
            elif rule.status is AlertStatus.FIRED:
                self.result.append(("REMINDER", rule.metric, rule.name,timestamp_for_alert))
            rule.status=AlertStatus.FIRED
            # next reminder
            heapq.heappush(self.heap,(timestamp_for_alert+rule.repeat_seconds, metric, alert_index, version))




    def process_sample(self, timestamp:int, metric:str, value:int):
        # fire any alerts/reminders due up to this sample's timestamp
        self.drain(timestamp)
        for rule_index in self.alertRulesMetric.get(metric, []):
            rule=self.alerts[rule_index]
            if value > rule.threshold:
                if rule.status is AlertStatus.PENDING or rule.status is AlertStatus.FIRED:
                    # alert already active
                    continue
                heapq.heappush(self.heap, (timestamp+rule.for_seconds, rule.metric, rule_index, rule.version))
                rule.status=AlertStatus.PENDING
            else:
                if rule.status is AlertStatus.FIRED:
                    self.result.append(("RESOLVED", rule.metric, rule.name,timestamp))
                if rule.status is not AlertStatus.IDLE:
                    # invalidate any pending alert/reminder in the heap
                    rule.version+=1
                    rule.status=AlertStatus.IDLE

        # handles for_seconds == 0 right away
        self.drain(timestamp)



    def add_alert_rule(self, name:str, metric:str, threshold:int, for_seconds:int, repeat_seconds:int):
        alert = AlertRule(name, metric, threshold, for_seconds, repeat_seconds)
        self.alerts.append(alert)
        self.alertRulesMetric.setdefault(alert.metric, []).append(len(self.alerts)-1)


    def process_end(self, EndTime):
        self.drain(EndTime)

    def start_process_input(self):
        #R N END_TIME
        R, N, EndTime=map(int, sys.stdin.readline().split())

        for i in range(R):
            rule=sys.stdin.readline().split()
            name,metric,threshold,for_seconds,repeat_seconds=rule[0], rule[1], int(rule[2]), int(rule[3]), int(rule[4])
            self.add_alert_rule(name, metric, threshold, for_seconds, repeat_seconds)

        #timestamp metric value
        for i in range(N):
            samples=sys.stdin.readline().split()
            timestamp,metric,value=int(samples[0]), samples[1], int(samples[2])
            self.process_sample(timestamp, metric, value)

        self.process_end(EndTime)

        # print after all input is read so output doesn't mix with typed/pasted input
        print()
        for event, metric, name, timestamp in self.result:
            print(f"{event} {name} {timestamp}")



if __name__ == "__main__":
    engine=AlertEngine()
    engine.start_process_input()
