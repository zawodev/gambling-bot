from random import random, randint
from gambling_bot.data.json_manager import save_data, load_data
from gambling_bot.models.dict_data.dict_data import DictData

class ProfileData(DictData):

    def __init__(self, data, path):
        random_color = lambda: ((randint(128, 255) << 16) + (randint(128, 255) << 8) + randint(128, 255))
        default_data = {
            "name": 'Profile',
            "title": 'gambling noob', # ranga from elo points
            "color": random_color(),
            "chips": 1000,
            "freechips": 0,

            "blackjacks": 0, #done
            "wins": 0, #done
            "pushes": 0, #done
            "losses": 0, #done
            "busts": 0, #done

            "cards_drawn": 0, #done
            "hands_played": 0, #done

            "doubles": 0, #done
            "splits": 0, #done
            "stands": 0, #done
            "hits": 0, #done
            "forfeits": 0, #done

            "total_won_chips": 0, #done
            "total_lost_chips": 0, #done
            "biggest_win": 0, #done
            "biggest_loss": 0, #done
            "max_chips": 1000, #done

            "loans_taken": 0,
            "loans_returned": 0,
            "biggest_loan_taken": 0,
            "biggest_loan_returned": 0,

            "freechips_claimed": 0, #done
            "last_freechips_claim_hour": -1, #done
            "games_played_by_date": {} # date: total games played, if more than 0 it is a login
        }
        super().__init__(default_data, data, path)


    def __str__(self):
        return (
            f"👤 Name: {self.data.get('name')}\n"
            f"🪙 Hajs: {self.chips}$\n"
            f"🏆 Wygrane: {self.wins}\n"
            f"🤝 Remisy: {self.pushes}\n"
            f"🥺 Porażki: {self.losses}\n"
            f"🃏 Karty: {self.cards_drawn}\n"
            f"🤲 Ręce: {self.hands_played}\n"
            f"🔥 Blackjacks: {self.blackjacks}\n"
            f"💥 Busts: {self.busts}\n"
            f"🔁 Double: {self.doubles}\n"
            f"🔀 Split: {self.splits}\n"
            f"🛑 Stand: {self.stands}\n"
            f"👊 Hit: {self.hits}\n"
            f"🏦 Max hajs: {self.max_chips}$\n"
            f"🏧 Pożyczki: {self.loans}\n"
            f"💸 Pożyczki spłacone: {self.loans_paid}\n"
            f"🎰 Freebety: {self.total_freebets}\n"
            f"🎰 Freebety wygrane: {self.freebets_won}\n"
            f"🎰 Freebety przegrane: {self.freebets_lost}\n"
            f"📅 Gry: {sum(self.total_games_dates)}\n"
            f"📅 Freebety: {len(self.freebet_dates)}\n"
        )

    def increment(self, path):
        """
        Increments the value at the specified path in a nested dictionary.
        Creates intermediate dictionaries and initializes the value at 0 if it doesn't exist.
        """
        data = load_data(self.path)
        keys = path.split('/')

        current = data
        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]

        final_key = keys[-1]
        if final_key not in current:
            current[final_key] = 0
        current[final_key] += 1

        save_data(self.path, data)
