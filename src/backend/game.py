from enum import Enum
from itertools import combinations
from dataclasses import dataclass, field
from backend.helper_functions import setup_logger
import pandas as pd

# Configure logger
logger = setup_logger(__name__)
input_logger = setup_logger("points_input", file_name="points_input.log", verbose=False)

class Wind(Enum):
    EAST = "Osten"
    SOUTH = "Süden"
    WEST = "Westen"
    NORTH = "Norden"

    def __str__(self):
        return self.value

def next_wind(current_wind: Wind) -> Wind:
    """Get the next wind in the sequence.
    Args:
        current_wind (Wind): The current wind position.
    """
    if current_wind == Wind.NORTH:
        raise ValueError("Cannot get next wind from NORTH")
    winds = list(Wind)
    current_index = winds.index(current_wind)
    return winds[current_index + 1]

def get_next_round_wind(winner_wind: Wind, round_wind: Wind) -> Wind:
    if winner_wind == round_wind:
        logger.info(f"Round wind stays the same: {round_wind}")
        return round_wind
    next_round_wind = next_wind(round_wind)
    logger.info(f"Next round wind: {next_round_wind}")
    return next_round_wind

@dataclass
class Player:
    name: str
    wind: Wind
    points: int = 0

    @property
    def points_str(self) -> str:
        return f"{self.points:,}".replace(",", ".")

    def __hash__(self):
        return hash((self.name, self.wind))
    
    def __eq__(self, other):
        if not isinstance(other, Player):
            return NotImplemented
        return self.name == other.name and self.wind == other.wind

    def show(self) -> str:
        return f"[{self.wind}] {self.name}"

    def show_with_points(self) -> str:
        return f"{self.show()} - {self.points_str} points"

    def add_points(self, points: int) -> None:
        self.points += points

@dataclass
class Score:
    """Single score of one Wind at one point in time.
    
    Args:
        player: The player who scored.
        points: Gross points inputted by player.
        doublings: How many times the points should be doubled. Defaults to 0.
        net_points: Points after giving and receiving points from other players.
        
    Attributes:
        calculated_points (int): Points after applying doublings.
    """
    player: Player
    points: int
    doublings: int = 0
    net_points: int = None

    @property
    def calculated_points(self) -> int:
        return self.points * (2 ** self.doublings)
    
    def give_net_points_to_player(self) -> None:
        """Apply net points to player."""
        if self.net_points is None:
            raise Exception("Net points not calculated yet")
        self.player.add_points(self.net_points)

@dataclass
class Round:
    round_wind: Wind
    winner: Wind
    scores: list[Score]

    def calculate_point_transfers(self) -> dict[Player, int]:
        """Calculate net scores for the current round."""
        # helper dict to store net points for each player
        net_points_all = {sc.player: 0 for sc in self.scores}

        def adjust_net_points(giver: Player, recipient: Player, points: int) -> None:
            logger.debug(f"{giver.name} gives {points} to {recipient.name}")
            net_points_all[giver] -= points
            net_points_all[recipient] += points

        for score1, score2 in list(combinations(self.scores, 2)):
            player1 = score1.player
            player2 = score2.player
            # being round_wind will double the points you get/lose
            points_factor = 1 + int(player1.wind == self.round_wind or player2.wind == self.round_wind)
            # first handle winner
            if player1.wind == self.winner:
                adjust_net_points(
                    giver=player2,
                    recipient=player1,
                    points=points_factor * score1.calculated_points
                )
            elif player2.wind == self.winner:
                adjust_net_points(
                    giver=player1,
                    recipient=player2,
                    points=points_factor * score2.calculated_points
                )
            # then handle other 3 players
            else:
                adjust_net_points(
                    giver=player2,
                    recipient=player1,
                    points=points_factor * (score1.calculated_points - score2.calculated_points)
                )
        return net_points_all
    
    def apply_net_points(self, net_points_all: dict[Player, int]) -> None:
        """Apply net points to score objects."""
        # apply points to score objects
        for score in self.scores:
            score.net_points = net_points_all[score.player]
            score.give_net_points_to_player()
    
    def process_points(self) -> None:
        """Process points for the current round."""
        net_points_all = self.calculate_point_transfers()
        self.apply_net_points(net_points_all)

@dataclass
class Game:
    rounds: list[Round] = field(default_factory=list)
    players: list[Player] = field(default_factory=list)
    round_wind: Wind = Wind.EAST
    
    @property
    def current_round_number(self) -> int:
        return len(self.rounds) + 1

    def _get_player_by_wind(self, wind: Wind) -> Player:
        found_players = [player for player in self.players if player.wind == wind]
        return found_players[0] if found_players else None

    def set_players(self, player_names: list[str]) -> None:
        """Takes list of player names and links them to winds.
        
        Args:
            player_names: List of player names in order of EAST to NORTH.
        """
        self.players = [Player(name, wind) for name, wind in zip(player_names, Wind)]

    def start_new_round(self, winner_wind: Wind) -> None:
        """Sets round wind according to the last wind and winning wind."""
        self.round_wind = get_next_round_wind(winner_wind, self.round_wind)
        logger.debug(f"Starting new round with wind: {self.round_wind}")

    def process_points_input(self, points_dict: dict[Wind, tuple[int, int]], 
                           winner: Wind) -> None:
        logger.debug(f"Processing points input: {points_dict} with winner: {winner}")
        input_logger.debug(f"Round {self.current_round_number} with winner: {winner}")
        scores = []
        for wind, (points, times_doubled) in points_dict.items():
            player = self._get_player_by_wind(wind)
            input_logger.debug(f"{player.name}, {points}, {times_doubled}")
            scores.append(Score(player, points, times_doubled))

        current_round = Round(
            round_wind=self.round_wind,
            winner=winner,
            scores=scores
        )
        current_round.process_points()
        self.rounds.append(current_round)

    def is_game_over(self, winner_wind: Wind) -> bool:
        '''Game is over if current round wind is NORTH and winner is not NORTH.'''
        logger.debug(
            f"Checking if game is over with winner_wind: {winner_wind} "
            f"and round_wind: {self.round_wind}"
        )
        return winner_wind != Wind.NORTH and self.round_wind == Wind.NORTH
    
    def get_round_wind_string(self) -> str:
        return str(self.round_wind)

    def get_standings_from_points(self, points_dict: dict[Player | str, int]) -> list[tuple[Player | str, int]]:
        """Returns list of (player, rank) tuples sorted by points.
        
        Args:
            points_dict: Dictionary mapping players (or player names) to their points
        """
        # Sort players by points in descending order
        sorted_items = sorted(points_dict.items(), key=lambda x: x[1], reverse=True)
        
        # Assign ranks (handling ties)
        standings = []
        current_rank = 1
        previous_points = None
        
        for player, points in sorted_items:
            if previous_points is not None and points < previous_points:
                current_rank = len(standings) + 1
            standings.append((player, current_rank))
            previous_points = points
            
        return standings

    def create_game_dataframe(self) -> pd.DataFrame:
        """Creates DataFrame containing round-by-round game data.
        
        Returns:
            DataFrame: Contains all rounds data with running sums and ranks
        """
        rounds_data = []
        running_sums = {player.name: 0 for player in self.players}
        
        for round_num, round in enumerate(self.rounds, 1):
            # First update all running sums for this round
            round_sums = running_sums.copy()
            for score in round.scores:
                round_sums[score.player.name] += score.net_points
            
            # Calculate ranks using the shared function
            standings = self.get_standings_from_points(round_sums)
            ranks = dict(standings)
            
            # Now create the rows with ranks included
            for score in round.scores:
                running_sums[score.player.name] += score.net_points
                
                round_info = {
                    'round': round_num,
                    'round_wind': round.round_wind.value,
                    'winner': round.winner.value,
                    'player': score.player.name,
                    'wind': score.player.wind.value,
                    'base_points': score.points,
                    'doublings': score.doublings,
                    'calculated_points': score.calculated_points,
                    'net_points': score.net_points,
                    'running_sum': running_sums[score.player.name],
                    'rank': ranks[score.player.name]
                }
                rounds_data.append(round_info)
        
        return pd.DataFrame(rounds_data)
    