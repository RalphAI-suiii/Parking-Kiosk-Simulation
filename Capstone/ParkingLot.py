import json
import random

class ParkingLot:
    def __init__(self, spot_ids, filename="parking_data.json"):
        self.filename = filename
        # Force fresh start every time
        data = {spot: 'free' for spot in spot_ids}
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)

    def _load_data(self):
        with open(self.filename, 'r') as f:
            return json.load(f)

    def _save_data(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)

    def assign_random_spot(self):
        data = self._load_data()
        free_spots = [spot for spot, status in data.items() if status == 'free']
        if not free_spots:
            return None
        chosen = random.choice(free_spots)
        data[chosen] = 'occupied'
        self._save_data(data)
        return chosen

    def free_spot(self, spot_id):
        data = self._load_data()
        if data.get(spot_id) == 'occupied':
            data[spot_id] = 'free'
            self._save_data(data)
            return True
        return False

    def free_count(self):
        data = self._load_data()
        return list(data.values()).count('free')