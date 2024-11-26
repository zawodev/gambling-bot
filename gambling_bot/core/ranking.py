import random


def calculate_elo(profile1, profile2):
    from gambling_bot.models.profile.profile import Profile
    profile1: Profile
    profile2: Profile
    # calculated overall ranking for a player, where it is good to play risky and play a lot
    # returns elo points, that are calculated onto rank title on profile

    # elo points are calculated from enemy elo points, player's win rate, player's games played and player's games won
    # elo formula:
    # elo = elo + K * (W - E)
    # where:
    # elo - player's elo points
    # K - K factor (depends on games played)
    # W - player's win rate
    # E - expected win rate
    # --------------------------------
    # E = 1 / (1 + 10 ^ ((enemy_elo - player_elo) / 400))
    # elo points are calculated from 0 to 999
    # K factor is calculated from games played:
    # K = 100 / (1 + games_played / 10)
    # win rate is calculated from games played and games won:
    # W = games_won / games_played

    #random.seed(profile.profile_data['name']) # seed for random
    #return random.randint(0, 999)

def get_title_from_elo(elo: int):
    # returns a title from elo points
    # pierwsza cyfra to tytuł
    # druga cyfra to dywizja (od I do X (po rzymsku)
    title = elo // 100
    division = elo // 10 % 10
    result = ""

    match title:
        case 0:
            result = "Bronze"
        case 1:
            result = "Silver"
        case 2:
            result = "Gold"
        case 3:
            result = "Platinum"
        case 4:
            result = "Diamond"
        case 5:
            result = "Master"
        case 6:
            result = "Grandmaster"
        case 7:
            result = "Challenger"
        case 8:
            result = "Legend"
        case 9:
            result = "God"

    match division:
        case 0:
            result += " I"
        case 1:
            result += " II"
        case 2:
            result += " III"
        case 3:
            result += " IV"
        case 4:
            result += " V"
        case 5:
            result += " VI"
        case 6:
            result += " VII"
        case 7:
            result += " VIII"
        case 8:
            result += " IX"
        case 9:
            result += " X"

    return result
