'''
Created on 
    Feb 19, 2022 - Sunday 

Course work: 
    Python for Cricket Lovers

@author: Raja CSP

Source:
    
    https://www.espncricinfo.com/series/icc-cricket-world-cup-2010-11-381449/sri-lanka-squad-495852/series-squads

    https://pythonexamples.org/python-find-index-of-item-in-list/

    https://www.espncricinfo.com/series/icc-cricket-world-cup-2010-11-381449/england-squad-497407/series-squads

    
'''

# Import necessary modules
import os
from dotenv import load_dotenv

load_dotenv()

# Hard Constants
BALLS_PER_OVER  = 6
TOTAL_WICKETS   = 10

# Soft Constants
TOTAL_OVERS     = int(os.getenv('TOTAL_OVERS', 2))
QUICK_TESTING   = int(os.getenv('QUICK_TESTING', "0"))
SLEEP_TIME_SECONDS   = float(os.getenv('SLEEP_TIME_SECONDS', "1"))

CURRENT_MATCH   = {
    "first"     : os.getenv('FIRST', "ind"),
    "second"    : os.getenv('SECOND', "eng")
}

total_teams = [
    "india",
    "australia",
    "srilanka",
    "england",
    "westindies",
    "pakistan"
    "bangladesh"
]

team_short_forms = {
    "ind"  : "india",
    "sri"  : "srilanka",
    "eng"  : "england",
    "aus"  : "australia",
    "wind" : "westindies",
    "newz" : "newzealand",
    "pak"  : "pakistan",
    "bang" : "bangladesh "
}

indian_players = [
    "Gautam Gambhir",
    "Virender Sehwag",
    "Sachin Tendulkar",
    "Suresh Raina ",
    "Yuvraj Singh",
    "Yusuf Pathan",
    "Virat Kohli",
    "MS Dhoni",
    "Zaheer Khan",
    "Harbhajan Singh",
    "Ravichandran Ashwin",
]

australian_players = [
    "Ricky Ponting",
    "Michael Clarke",
    "David Hussey",
    "Michael Hussey",
    "Callum Ferguson",
    "Shane Watson",
    "Cameron White",
    "Jason Krejza",
    "Brett Lee",
    "Shaun Tait",
    "Doug Bollinger",
]

srilankan_players = [
    "Kumar Sangakkara",
    "Mahela Jayawardene",
    "Tillakaratne Dilshan",
    "Dilhara Fernando",
    "Rangana Herath",
    "Chamara Kapugedera",
    "Upul Tharanga",
    "Thisara Perera",
    "Ajantha Mendis",
    "Muthiah Muralidaran",
    "Nuwan Kulasekara"
]

england_players = [
    "Kevin Pietersen",
    "James Tredwell",
    "Ian Bell",
    "Adil Rashid",
    "Paul Collingwood",
    "Eoin Morgan",
    "Matt Prior",
    "Ravi Bopara",
    "James Anderson",
    "Jade Dernbach",
    "Graeme Swann"
]

westindies_players = [
    "Daren Sammy ",
    "Devendra Bishoo ",
    "Sulieman Benn ",
    "Darren Bravo  ",
    "Chris Gayle ",
    "Nikita Miller ",
    "Devon Smith ",
    "Dwayne Bravo ",
    "Zaheer Khan",
    "Andre Russell ",
    "Kemar Roach ",
]

newzealand_players = [
    "James Franklin  ",
    "Daniel Vettori  ",
    "Jamie How  ",
    "Brendon McCullum  ",
    "Andy McKay ",
    "Jacob Oram  ",
    "Tim Southee  ",
    "Ross Taylor  ",
    "Kyle Mills ",
    "Luke Woodcock  ",
    "Scott Styris  ",
]

pakistan_players = [
    "Abdullah Shafique", 
    "Abid Ali", 
    "Arshad Iqbal", 
    "Azhar Ali",
    "Babar Azam", 
    "Danish Aziz",   
    "Faheem Ashraf",
    "Fawad Alam" , 
    "Haris Rauf", 
    "Imad Wasim",
    "Imran Butt"
]

bangladesh_players = [
    "Shakib Al Hasan",
    "Abdur Razzak",
    "Junaid Siddique",
    "Mohammad Ashraful",
    "Naeem Islam",
    "Raqibul Hasan",
    "Shafiul Islam",
    "Sohrawordi Shuvo",
    "Tamim Iqbal",
    "Imrul Kayes",
    "Mahmudullah"
]


def get_teamname_from_short(short_form):

    team_name = team_short_forms[short_form]
    index = total_teams.index(team_name)

    team_name = total_teams[index]
    # print(team_name)

    return team_name

all_team_players = {
    "india"      : indian_players,
    "australia"  : australian_players,
    "srilanka"   : srilankan_players,
    "england"    : england_players,
    "westindies" : westindies_players,
    "newzealand" : newzealand_players,
    "pakistan"   : pakistan_players,
    "bangladesh" : bangladesh_players
}

# team_a_players = all_team_players[get_teamname_from_short(CURRENT_MATCH["first"])]
# team_b_players = all_team_players[get_teamname_from_short(CURRENT_MATCH["second"])]

CURRENT_TEAMS   = [
    get_teamname_from_short(CURRENT_MATCH["first"]),
    get_teamname_from_short(CURRENT_MATCH["second"]),
]

def startpy():

    short_form = "aus"
    print(get_teamname_from_short(short_form))
    
if __name__ == '__main__':
    startpy()