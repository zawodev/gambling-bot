from gambling_bot.models.profile.profile import Profile

def calculate_elo(profile: Profile):
    # calculated overall ranking for a player, where it is good to play risky and play a lot
    # returns elo points, that are calculated onto rank title on profile
    return 2137

def get_title_from_elo(elo: int):
    # returns a title from elo points
    if elo < 1000:
        return "gambling noob"
    elif elo < 2000:
        return "gambling pro"
    elif elo < 3000:
        return "gambling master"
    elif elo < 4000:
        return "gambling legend"
    else:
        return "gambling god"
