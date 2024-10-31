import logging
from enum import Enum
from logging import getLogger, DEBUG
from dataclasses import dataclass, field

# Configure the default logger to save logs to a file
logging.basicConfig(
    level=DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='app.log',  # Specify the log file name
    filemode='w'  # Overwrite the log file each time the program runs
)

logger = getLogger(__name__)
logger.setLevel(DEBUG)

class Wind(Enum):
    EAST = "Osten"
    SOUTH = "Süden"
    WEST = "Westen"
    NORTH = "Norden"

    def __str__(self):
        return self.value

def next_wind(current_wind: Wind) -> Wind:
    """
    Get the next wind in the sequence. Should never be called with Wind.NORTH.
    """
    if current_wind == Wind.NORTH:
        raise ValueError("Cannot get next wind from NORTH")
    winds = list(Wind)
    current_index = winds.index(current_wind)
    return winds[current_index + 1]


@dataclass
class Player:
    name: str
    wind: Wind
    points: int = 0

    @property
    def points_str(self) -> str:
        return f"{self.points:,}".replace(",", ".")

    def show(self) -> str:
        return f"[{self.wind}] {self.name}"

    def show_with_points(self) -> str:
        return f"{self.show()} - {self.points_str} points"

    def add_points(self, points: int) -> None:
        self.points += points


@dataclass
class Round:
    round_wind: Wind
    winner: Wind
    scores: dict[Wind, int]


@dataclass
class Game:
    rounds: list[Round] = field(default_factory=list)
    players: list[Player] = field(default_factory=list)
    round_wind: Wind = Wind.EAST


    def _get_player_by_wind(self, wind: Wind) -> Player:
        found_players = [player for player in self.players if player.wind == wind]
        return found_players[0] if found_players else None

    def _get_next_round_wind(self, last_winner: Wind, last_round_wind: Wind) -> Wind:
        # The round_wind stays the same until the round_wind loses
        # draws are not handled as they cannot be selected in the UI
        if last_winner == last_round_wind:
            logger.debug(f"Round wind stays the same: {last_round_wind}")
            return last_round_wind

        next_round_wind = next_wind(last_round_wind)
        logger.debug(f"Next round wind: {next_round_wind}")
        return next_round_wind

    # TODO: set random names if left out
    def set_players(self, player_names: list[str]) -> None:
        """ Takes list of player names and links them to EAST - SOUTH ... """
        self.players = [Player(name, wind) for name, wind in zip(player_names, Wind)]

    def start_new_round(self, winner_wind: Wind) -> None:
        """ Sets round wind according to the last wind and winning wind """
        self.round_wind = self._get_next_round_wind(winner_wind, self.round_wind)
        logger.debug(f"Starting new round with wind: {self.round_wind}")

    def process_points_input(self, points_dict: dict[Wind, tuple[int, int]], winner: Wind) -> None:
        logger.debug(f"Processing points input: {points_dict} with winner: {winner}")
        scores = {}
        for wind, (points, times_doubled) in points_dict.items():
            points_gross = calculate_gross_points(points, times_doubled)
            scores[wind] = points_gross
            player = self._get_player_by_wind(wind)
            player.add_points(points_gross)

        current_round = Round(
            round_wind=self.round_wind,
            winner=winner,
            scores=scores
        )
        self.rounds.append(current_round)

    def is_game_over(self, winner_wind: Wind) -> bool:
        logger.debug(f"Checking if game is over with winner_wind: {winner_wind} and round_wind: {self.round_wind}")
        return winner_wind != Wind.NORTH and self.round_wind == Wind.NORTH
    
    def get_round_wind_string(self) -> str:
        return str(self.round_wind)

def calculate_gross_points(points: int, times_doubled: int) -> int:
    return points * (2 ** times_doubled)


