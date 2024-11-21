from gambling_bot.models.profile.profile_data import ProfileData
from datetime import datetime

class Profile:
    def __init__(self, data, path):
        self.profile_data = ProfileData(data, path)

    def __str__(self):
        return f'{self.profile_data['name']} has {self.profile_data['chips']}$'

    def __eq__(self, other):
        if isinstance(other, str):
            return self.profile_data.path == other
        elif isinstance(other, Profile):
            return self.profile_data.path == other.profile_data.path
        return False

    def claim_free_chips(self, amount):
        if not self.has_claimed_free_chips():
            self.profile_data['freechips'] += amount
            self.profile_data['last_freechips_claim_hour'] = datetime.now().hour

    def has_claimed_free_chips(self):
        return self.profile_data['last_freechips_claim_hour'] == datetime.now().hour

    def has_chips(self, amount):
        return self.profile_data['chips'] + self.profile_data['freechips'] >= amount

    def transfer_chips(self, other, amount):
        freechips = self.profile_data['freechips']
        chips = self.profile_data['chips']
        other_chips = other.profile_data['chips']

        if freechips > amount:
            chips += amount
            freechips -= amount
        else:
            chips += freechips
            freechips = 0

        self.profile_data['freechips'] = freechips
        self.profile_data['chips'] = chips - amount
        other.profile_data['chips'] = other_chips + amount
