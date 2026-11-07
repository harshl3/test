import unittest

from app import app


class TankerSlotTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_says_ready(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "Tanker dispatch ready")

    def test_river_road(self):
        response = self.client.get("/slot/river%20road")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {"street": "river road", "slot": "06:30", "tanker": "T1"},
        )

    def test_hill_lane(self):
        response = self.client.get("/slot/hill%20lane")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {"street": "hill lane", "slot": "08:00", "tanker": "T1"},
        )

    def test_unknown_street_is_unassigned(self):
        response = self.client.get("/slot/unknown%20street")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {"street": "unknown street", "slot": "unassigned", "tanker": "none"},
        )

    def test_mixed_case_is_lowered(self):
        response = self.client.get("/slot/Market%20Square")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {"street": "market square", "slot": "07:15", "tanker": "T2"},
        )

    def test_surrounding_spaces_are_trimmed(self):
        response = self.client.get("/slot/%20%20River%20Road%20")
        self.assertEqual(
            response.get_json(),
            {"street": "river road", "slot": "06:30", "tanker": "T1"},
        )

    def test_exactly_three_keys(self):
        for street in ("river%20road", "unknown%20street"):
            with self.subTest(street=street):
                data = self.client.get(f"/slot/{street}").get_json()
                self.assertEqual(sorted(data.keys()), ["slot", "street", "tanker"])


if __name__ == "__main__":
    unittest.main()
