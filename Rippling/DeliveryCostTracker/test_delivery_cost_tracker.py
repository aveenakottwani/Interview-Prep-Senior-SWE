import unittest

from Rippling.DeliveryCostTracker.delivery_cost_tracker import DeliveryCostTracker


class TestDeliveryCostTracker(unittest.TestCase):
    def setUp(self) -> None:
        self.t = DeliveryCostTracker()

    # (1) Example 1: one delivery spans a rate change.
    def test_example1_spans_rate_change(self):
        self.t.setDriverRate("A", 0, "36.00")
        self.t.setDriverRate("A", 50, "72.00")
        self.t.recordDelivery("d1", "A", 0, 100)
        # 36.00 * 50/3600 + 72.00 * 50/3600 = 0.50 + 1.00
        self.assertEqual(self.t.getTotalCost(), "1.50")

    # (2) Example 2: round only the final total.
    def test_example2_round_only_final_total(self):
        self.t.setDriverRate("A", 0, "0.18")
        self.t.recordDelivery("d1", "A", 0, 100)    # exactly 0.005
        self.t.recordDelivery("d2", "A", 100, 200)  # exactly 0.005
        self.assertEqual(self.t.getTotalCost(), "0.01")

    # (3) Rate lookup: before the first rate, exactly at a boundary, between rates.
    def test_get_rate_before_at_and_between(self):
        self.t.setDriverRate("A", 10, "36.00")
        self.t.setDriverRate("A", 50, "72.00")
        self.assertIsNone(self.t.getDriverRateAt("A", 9))
        self.assertEqual(self.t.getDriverRateAt("A", 10), "36.00")
        self.assertEqual(self.t.getDriverRateAt("A", 49), "36.00")
        self.assertEqual(self.t.getDriverRateAt("A", 50), "72.00")
        self.assertEqual(self.t.getDriverRateAt("A", 10**12), "72.00")
        self.assertIsNone(self.t.getDriverRateAt("unknown", 100))

    # (4) Setting a rate at an existing timestamp replaces it, including for recorded deliveries.
    def test_replace_rate_same_timestamp(self):
        self.t.setDriverRate("A", 0, "36.00")
        self.t.recordDelivery("d1", "A", 0, 3600)
        self.assertEqual(self.t.getTotalCost(), "36.00")
        self.t.setDriverRate("A", 0, "40.00")
        self.assertEqual(self.t.getDriverRateAt("A", 0), "40.00")
        self.assertEqual(self.t.getTotalCost(), "40.00")
        self.assertEqual(len(self.t.rates["A"]), 1)

    # (5) A rate inserted out of order, into the past, retroactively changes an existing delivery.
    def test_out_of_order_historical_insert_is_retroactive(self):
        self.t.setDriverRate("A", 100, "72.00")
        self.t.setDriverRate("A", 0, "36.00")  # inserted out of order
        self.t.recordDelivery("d1", "A", 0, 200)
        # 36.00 * 100/3600 + 72.00 * 100/3600 = 1.00 + 2.00
        self.assertEqual(self.t.getTotalCost(), "3.00")
        self.t.setDriverRate("A", 50, "0.00")  # historical insert in the middle
        # [0,50) at 36.00 = 0.50, [50,100) at 0.00 = 0, [100,200) at 72.00 = 2.00
        self.assertEqual(self.t.getTotalCost(), "2.50")

    # (6) Overlapping deliveries for the same driver are billed independently.
    def test_overlapping_deliveries_same_driver(self):
        self.t.setDriverRate("A", 0, "36.00")
        self.t.recordDelivery("d1", "A", 0, 100)   # 1.00
        self.t.recordDelivery("d2", "A", 50, 150)  # 1.00
        self.assertEqual(self.t.getTotalCost(), "2.00")
        self.t.setDriverRate("A", 100, "72.00")    # changes only d2's [100,150)
        self.assertEqual(self.t.getTotalCost(), "2.50")

    # (7) Very large values: Python ints never overflow.
    def test_large_values_no_overflow(self):
        self.t.setDriverRate("A", 0, "1000000.00")
        self.t.recordDelivery("d1", "A", 0, 10**12)
        # 10^6 * 10^12 / 3600 = 277777777777777.777... -> .78
        self.assertEqual(self.t.getTotalCost(), "277777777777777.78")

    # (8) Exactly half a cent rounds up; just under half a cent rounds down.
    def test_half_cent_rounds_up(self):
        self.t.setDriverRate("A", 0, "0.18")
        self.t.recordDelivery("d1", "A", 0, 100)  # exactly 0.005
        self.assertEqual(self.t.getTotalCost(), "0.01")

    def test_just_under_half_cent_rounds_down(self):
        self.t.setDriverRate("A", 0, "0.17")
        self.t.recordDelivery("d1", "A", 0, 100)  # 0.004722...
        self.assertEqual(self.t.getTotalCost(), "0.00")

    # Extra: a delivery that ends exactly at effective_time is not affected ([start, end)).
    def test_delivery_ending_at_effective_time_unaffected(self):
        self.t.setDriverRate("A", 0, "36.00")
        self.t.recordDelivery("d1", "A", 0, 50)
        self.t.setDriverRate("A", 50, "72.00")
        self.assertEqual(self.t.getTotalCost(), "0.50")

    # Extra: one driver's rate change doesn't touch another driver's deliveries.
    def test_drivers_isolated(self):
        self.t.setDriverRate("A", 0, "36.00")
        self.t.setDriverRate("B", 0, "10.00")
        self.t.recordDelivery("a1", "A", 0, 3600)
        self.t.recordDelivery("b1", "B", 0, 3600)
        self.t.setDriverRate("A", 0, "0.00")
        self.assertEqual(self.t.getTotalCost(), "10.00")

    # Extra: an empty tracker totals to zero.
    def test_empty_total(self):
        self.assertEqual(self.t.getTotalCost(), "0.00")


if __name__ == "__main__":
    unittest.main()
