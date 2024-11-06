from gambling_bot.models.profile.profile_data import ProfileData

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

    def has_chips(self, amount):
        return self.profile_data['chips'] >= amount

    def transfer_chips(self, other, amount):
        self.profile_data['chips'] = self.profile_data['chips'] - amount
        other.profile_data['chips'] = other.profile_data['chips'] + amount
