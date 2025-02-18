from constants import TEAMS, PLAYERS
import copy
#The instructions were a bit confusing about the data structures. I could have had everyone go under a team but it would have been a bit annoying so I did it per player instead.

def menupage():
    print('========================================')
    print('------BASKETBALL TEAM STATS TOOL--------')
    print('========================================')

def clean_data():
    #Using the amazing deepcopy function which copys both lists (respectively) but doesnt affect the original TEAMS and PLAYERS.
    teams_copy = copy.deepcopy(TEAMS)
    players_copy = copy.deepcopy(PLAYERS)

    # print("Before cleaning:", players_copy[0]['height'])
    players_copy =[{
        'Name': p['name'],
        'Team': None,
        'Experience': {"yes": True, "no": False}[p['experience'].lower()],
        #Transforming the height into an integer AFTER i first split it into two [42, inches] and only taking the first item.
        'Height': int(p['height'].split()[0]),
        #For this one I split the Guardians by the delimiter ' and ' so that if there are two then its a list of two but if its one then its just the one.
        'Guardians': p['guardians'].split(' and ')

    } for p in players_copy]
#Truth be told for this I had to look up a way to change the experience to true and false in the same list comprehension
#I also looked at how other people format their code in order to make it more readable as it was a one lined garbled mess
    return teams_copy, players_copy

#Now creating a function to split the players up into teams
def balance_teams(players, teams):
    # First getting the number of player per team, I was going to use // but we havent learnt that yet so i did int(len(x)/len(y)) instead
    num_per_team = int(len(players) / len(teams))

    #Sorting players into two different categories as I was not comfortable with and did not learn the whole lambda sort thing
    experienced_players = [p for p in players if p['Experience'] == True]
    inexperienced_players = [p for p in players if p['Experience'] == False]

    #Starting my sort like dealing cards so I dont overshoot or put too many people in one team.
    current_team = 0

    #Doing the experienced players first as that was a requirement
    for player in experienced_players:
        player['Team'] = teams[current_team]
        current_team = (current_team + 1) % len(teams)
    #Doing the rest because YOLO
    for player in inexperienced_players:
        player['Team'] = teams[current_team]
        current_team = (current_team + 1) % len(teams)

   #I might need num_per_team so I will bring it home just in case
    return players, num_per_team


def team_details(team_name, players):
    team_players = [p for p in players if p['Team'] == team_name]
    num_in_team = len(team_players)
    #Turned the players list into a string
    player_names = ", ".join([p['Name'] for p in team_players])
    #This bit was a bit redundant but I couldnt be fucked going and seeing how I could integrate with the balancing of teams.
    experienced = len([p for p in team_players if p['Experience'] == True])
    inexperienced = len([p for p in team_players if p['Experience'] == False])
    #I decided to round the average height to 2dp as it looked ridiculous before.
    average_height = round(sum(p['Height'] for p in team_players)/len(team_players), 2)
    #I also had to flatten the list to a string witht he aforementioned join method.
    guardians = ", ".join([guardian for p in team_players for guardian in p['Guardians']])

#Now to print this bad boy
    print("========================================")
    print(f"There are the {num_in_team} players in the {team_name}'s team: ")
    print(f"{player_names}")
    print("========================================\n")
    print(f"There are {experienced} number of experienced players. ")
    print(f"There are {inexperienced} number of inexperienced players.\n")
    print(f"The team is {average_height} inches tall on average.")
    print(f"These are the guardians for the players on the team: {guardians}")

#I actually had this running not as a function but decided to just do both inputs with the loop as two (nested) functions
def user_selection(teams_copy, players_copy):
    while True:
        print("What would you like to do?:\n    A) Display Team Stats\n    B) QUIT")
        landing_choice = str(input("Enter an option:   "))
        if landing_choice.upper() == "A":
            team_choice(teams_copy, players_copy)
        elif landing_choice.upper() == "B":
            print("Thank you! Have a great day")
            quit()
        else: print("Invalid choice, please type 'A' or 'B'")

    print('========================================')
    #I wanted to use zip and import string to create a dynamic list that would work in case the original file was edited but we havent learnt that yet


def team_choice(teams_copy, players_copy):
    print("A) Panthers\nB) Bandits\nC) Warriors")
    while True:
        team_selection = str(input("Which team do you want to inspect?:    "))
        if team_selection.upper() == "A":
            team_details(teams_copy[0], players_copy)
            break
        if team_selection.upper() == "B":
            team_details(teams_copy[1], players_copy)
            break
        if team_selection.upper() == "C":
            team_details(teams_copy[2], players_copy)
            break
        else:
            print("Invalid choice, please type 'A', 'B' or 'C'")

    print('========================================')


#Dunder Main!
if __name__ == "__main__":
    teams_copy, players_copy = clean_data()
    players, num_per_team = balance_teams(players_copy, teams_copy)

menupage()
user_selection(teams_copy, players_copy)