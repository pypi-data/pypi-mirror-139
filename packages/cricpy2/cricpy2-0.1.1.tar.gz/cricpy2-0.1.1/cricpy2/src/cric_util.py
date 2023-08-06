'''
Created on 

Course work: 

@author: raja

Source:
    https://stackoverflow.com/questions/8023306/get-key-by-value-in-dictionary
'''

# Import necessary modules
import time

# Local import
from cricket_constants import *


def get_short_from_full_team_name(team_name):

    short_name = list(team_short_forms.keys())[list(team_short_forms.values()).index(team_name)]

    return short_name

def pgap(count = 1):

    for _count in range(count):
        print('')

def take_5():

    time.sleep(15)

def pline(count = 17):

    '''
        This method will print dotted lines
    '''

    print('-' * count)

def startpy():
    
    # print("Whatsup Toronto")

    print(get_short_from_full_team_name("india"))

    pass


if __name__ == '__main__':
    startpy()