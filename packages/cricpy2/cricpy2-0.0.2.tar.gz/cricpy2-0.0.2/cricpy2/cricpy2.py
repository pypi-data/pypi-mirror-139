'''
Created on 
Course work: 
@author: raja
Source:
    
'''

# Import necessary modules


# Local import
import cricket
import cricket_constants as ccon
import cric_util
from cric_util import pgap, take_5

def play_game(team_1, team_2):

    team_a = ccon.get_teamname_from_short(team_1)
    team_b = ccon.get_teamname_from_short(team_2)

    print(f"team_a : {team_a}, team_b : {team_b}")

    return cricket.play_game(team_a, team_b)

def play_knockout_tournament():

    print('Knockout 2022')
    pgap()

    # 4 teams

    # league matches
    print('Knockout Match 1: ')
    game_1_winner = play_game(
        "sri",
        "eng"
    )
    print(f'winner: {game_1_winner}')
    pgap()
    take_5()

    print('Knockout Match 2: ')
    game_2_winner = play_game(
        "ind",
        "aus"
    )
    print(f'winner: {game_2_winner}')
    pgap()
    take_5()

    game_1_winner_short = cric_util.get_short_from_full_team_name(game_1_winner)
    game_2_winner_short = cric_util.get_short_from_full_team_name(game_2_winner)
    
    # # final
    print(f'Final Match:')
    play_game(
        game_1_winner_short,
        game_2_winner_short
    )


def startpy():
    
    # print("Whatsup Toronto")

    play_knockout_tournament()


if __name__ == '__main__':
    startpy()