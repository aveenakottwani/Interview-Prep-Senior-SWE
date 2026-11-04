"""
Rippling: AI-assisted coding round. Delivery Cost Tracker.

Implement a Python class DeliveryCostTracker for a food delivery company. Use dictionaries
to manage driver rates and delivery records, supporting effective timestamps, historical rate
queries, and delivery cost calculation.

Interface
- setDriverRate(driver_id, effective_time, hourly_rate)
    Set a driver's hourly rate effective from the Unix timestamp effective_time (seconds).
    hourly_rate is a nonnegative decimal string with at most two fractional digits ("36.00").
    Historical rates may be inserted out of order. Same driver + effective timestamp replaces
    the previous rate. Updates are retroactive: affected recorded deliveries for that driver
    must be recalculated.
- getDriverRateAt(driver_id, timestamp)
    Return the hourly rate effective at that timestamp as a string with two fractional digits.
    Return null if no rate is effective yet.
- recordDelivery(delivery_id, driver_id, start_time, end_time)
    Record a delivery with a globally unique ID. Interval is [start_time, end_time), charged by
    elapsed seconds. If the delivery spans rate changes, charge each segment at its effective
    rate. A rate is guaranteed to be effective at the delivery's start. Deliveries may overlap
    and are billed independently.
- getTotalCost()
    Return the total cost of all recorded deliveries as a string with two fractional digits.
    Do not round intermediate values; round only the final total to cents, exact halves up.
    Must run in O(1) without scanning delivery records.

Also explain why using float and rounding every delivery charge to two decimals does not
guarantee a correct final total.

Input/output: stdin is a JSON object with an "operations" array; each operation has an "op"
field naming a method, other fields match its parameter names. Print a JSON array with the
results of getDriverRateAt and getTotalCost, in order.

Example 1: rates A@0 = "36.00", A@50 = "72.00"; delivery d1 A [0, 100); getTotalCost -> ["1.50"]
Example 2: rate A@0 = "0.18"; deliveries [0, 100) and [100, 200); getTotalCost -> ["0.01"]
           (each costs exactly 0.005; do not round them separately before summing)

Constraints: <= 10^4 operations; <= 10^3 rate timestamps per driver; timestamps are integers
in [0, 10^12] with start_time < end_time; rates in [0, 10^6] with <= 2 fractional digits.
All operations are valid. Only getTotalCost() has a mandatory complexity bound.

Follow-ups: driver rate updates with effective timestamps, your own test cases, historical
rate queries, floating-point precision for currency, getTotalCost() from O(n) to O(1).
"""
import json
import sys
from bisect import bisect_left, bisect_right
from typing import Dict, List, Optional, Set, Tuple


class DeliveryCostTracker:
    """Tracks driver hourly rates and delivery records, and computes total delivery cost.

    Money is held exactly as integers, never floats:
      - Rates are stored as integer cents ("36.00" -> 3600).
      - A delivery's cost is stored as cost_units = sum(rate_cents * seconds) over
        its rate segments, so cost_units / 3600 is the exact cost in cents.
      - Rounding happens once, only when getTotalCost() formats the total.

    Deliveries cover the half-open interval [start_time, end_time). A rate applies
    from its effective_time onward, including effective_time itself.
    """

    def __init__(self) -> None:
        # driver_id -> [(effective_time, rate_cents)], kept sorted by effective_time.
        self.rates: Dict[str, List[Tuple[int, int]]] = {}
        # delivery_id -> (driver_id, start_time, end_time, cost_units)
        self.deliveries: Dict[str, Tuple[str, int, int, int]] = {}
        # driver_id -> ids of that driver's deliveries (used for retroactive recalculation)
        self.driver_deliveries: Dict[str, Set[str]] = {}
        # Sum of cost_units over all deliveries, kept current so getTotalCost is O(1).
        self.total_units: int = 0

    def setDriverRate(self, driver_id: str, effective_time: int, hourly_rate: str) -> None:
        """Set driver_id's hourly rate from effective_time onward.

        hourly_rate is a nonnegative decimal string with at most two fractional
        digits, such as "36.00". Rates may be set out of order. Setting a rate at an
        existing (driver_id, effective_time) replaces it. Changes are retroactive:
        the cost of every recorded delivery the change affects is recalculated, and
        total_units is adjusted by the difference.
        """
        rate_cents = self._parse_cents(hourly_rate)
        driver_rates = self.rates.setdefault(driver_id, [])
        i = bisect_left(driver_rates, effective_time, key=lambda r: r[0])
        if i < len(driver_rates) and driver_rates[i][0] == effective_time:
            driver_rates[i] = (effective_time, rate_cents)  # same timestamp: replace
        else:
            driver_rates.insert(i, (effective_time, rate_cents))

        # Retroactive recalculation: only time in [effective_time, next_effective) changed rate.
        window_end = driver_rates[i + 1][0] if i + 1 < len(driver_rates) else float("inf")
        for delivery_id in self.driver_deliveries.get(driver_id, ()):
            _, start, end, old_cost = self.deliveries[delivery_id]
            if start < window_end and end > effective_time:  # [start, end) overlaps the window
                new_cost = self._cost_units(driver_id, start, end)
                self.total_units += new_cost - old_cost
                self.deliveries[delivery_id] = (driver_id, start, end, new_cost)

    def getDriverRateAt(self, driver_id: str, timestamp: int) -> Optional[str]:
        """Return the rate in effect at timestamp as a two-decimal string, such as "36.00".

        The rate in effect is the one with the latest effective_time <= timestamp.
        Returns None if driver_id has no rate in effect at timestamp.
        """
        driver_rates = self.rates.get(driver_id)
        if not driver_rates:
            return None
        i = bisect_right(driver_rates, timestamp, key=lambda r: r[0]) - 1
        if i < 0:
            return None
        return self._format_cents(driver_rates[i][1])

    def recordDelivery(self, delivery_id: str, driver_id: str, start_time: int, end_time: int) -> None:
        """Record a delivery over [start_time, end_time), billed per elapsed second.

        If the interval crosses a rate change, each segment is charged at the rate in
        effect for it. A rate is guaranteed to be in effect at start_time. Deliveries
        may overlap, and each is billed on its own. The delivery's cost_units are
        added to total_units.
        """
        cost = self._cost_units(driver_id, start_time, end_time)
        self.deliveries[delivery_id] = (driver_id, start_time, end_time, cost)
        self.driver_deliveries.setdefault(driver_id, set()).add(delivery_id)
        self.total_units += cost

    def getTotalCost(self) -> str:
        """Return the total cost of all deliveries as a two-decimal string.

        Runs in O(1): reads the running total_units rather than scanning deliveries.
        Rounds to the nearest cent, with exact half cents rounded up, and rounds only
        here, never on individual deliveries.
        """
        # total_units / 3600 = cents; adding 1800 (half of 3600) before // rounds half up.
        cents = (self.total_units + 1800) // 3600
        return self._format_cents(cents)

    # ---- helpers ----

    def _cost_units(self, driver_id: str, start: int, end: int) -> int:
        """Return sum(rate_cents * overlap_seconds) over the rate segments that overlap [start, end)."""
        driver_rates = self.rates[driver_id]
        i = bisect_right(driver_rates, start, key=lambda r: r[0]) - 1  # rate in effect at start
        total = 0
        seg_start = start
        while seg_start < end:
            seg_end = driver_rates[i + 1][0] if i + 1 < len(driver_rates) else end
            seg_end = min(seg_end, end)
            total += driver_rates[i][1] * (seg_end - seg_start)
            seg_start= seg_end
            i += 1
        return total

    @staticmethod
    def _parse_cents(s: str) -> int:
        """Parse a decimal string such as "36.00", "36.5" or "36" into integer cents, without float."""
        whole, _, frac = s.strip().partition(".")
        return int(whole or "0") * 100 + int(frac.ljust(2, "0")[:2])

    @staticmethod
    def _format_cents(cents: int) -> str:
        """Format integer cents as a two-decimal string: 3600 -> "36.00", 5 -> "0.05"."""
        return f"{cents // 100}.{cents % 100:02d}"


# Only these ops are allowed; True means the op returns a value for the output array.
_OPS = {
    "setDriverRate": False,
    "getDriverRateAt": True,
    "recordDelivery": False,
    "getTotalCost": True,
}


def main() -> None:
    data = json.load(sys.stdin)
    tracker = DeliveryCostTracker()
    results = []
    for operation in data["operations"]:
        args = dict(operation)
        op = args.pop("op")
        if op not in _OPS:
            raise ValueError(f"unknown op: {op}")
        result = getattr(tracker, op)(**args)  # remaining fields match parameter names
        if _OPS[op]:
            results.append(result)  # None serializes to null
    print(json.dumps(results))


if __name__ == "__main__":
    main()
