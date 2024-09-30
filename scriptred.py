from random import randint

name = 'sample4'

def moveTo(x, y, pirate):
    position = pirate.getPosition()
    if position[0] == x and position[1] == y:
        return 0
    if position[0] == x:
        return (position[1] < y) * 2 + 1
    if position[1] == y:
        return (position[0] > x) * 2 + 2
    if randint(1, 2) == 1:
        return (position[0] > x) * 2 + 2
    else:
        return (position[1] < y) * 2 + 1

def checkfriends(pirate, quad):
    friends_count = 0
    directions = {
        'up': pirate.investigate_up()[1],
        'down': pirate.investigate_down()[1],
        'left': pirate.investigate_left()[1],
        'right': pirate.investigate_right()[1],
        'ne': pirate.investigate_ne()[1],
        'nw': pirate.investigate_nw()[1],
        'se': pirate.investigate_se()[1],
        'sw': pirate.investigate_sw()[1],
    }
    
    # Check friends in the given quadrant
    if quad == 'ne':
        friends_count += directions['up'] == 'friend'
        friends_count += directions['ne'] == 'friend'
        friends_count += directions['right'] == 'friend'
    elif quad == 'se':
        friends_count += directions['down'] == 'friend'
        friends_count += directions['se'] == 'friend'
        friends_count += directions['right'] == 'friend'
    elif quad == 'sw':
        friends_count += directions['down'] == 'friend'
        friends_count += directions['sw'] == 'friend'
        friends_count += directions['left'] == 'friend'
    elif quad == 'nw':
        friends_count += directions['up'] == 'friend'
        friends_count += directions['nw'] == 'friend'
        friends_count += directions['left'] == 'friend'

    return friends_count

def spread(pirate):
    friends_count = {
        'sw': checkfriends(pirate, 'sw'),
        'se': checkfriends(pirate, 'se'),
        'ne': checkfriends(pirate, 'ne'),
        'nw': checkfriends(pirate, 'nw'),
    }
    
    # Prioritize directions based on friend count
    best_direction = max(friends_count, key=friends_count.get)
    x, y = pirate.getPosition()

    if friends_count[best_direction] == 0:
        return randint(1, 4)

    if best_direction == 'sw':
        return moveTo(x - 1, y + 1, pirate)
    elif best_direction == 'se':
        return moveTo(x + 1, y + 1, pirate)
    elif best_direction == 'ne':
        return moveTo(x + 1, y - 1, pirate)
    elif best_direction == 'nw':
        return moveTo(x - 1, y - 1, pirate)

def ActPirate(pirate):
    up = pirate.investigate_up()[0]
    down = pirate.investigate_down()[0]
    left = pirate.investigate_left()[0]
    right = pirate.investigate_right()[0]
    x, y = pirate.getPosition()
    pirate.setSignal("")
    s = pirate.trackPlayers()

    islands = {
        'island1': (up, s[0]),
        'island2': (down, s[1]),
        'island3': (left, s[2]),
        'island4': (right, s[3])
    }

    for island, (direction, signal) in islands.items():
        if direction == island and signal != "myCaptured":
            pirate.setTeamSignal(f"{island[-1]}{x},{y + 1 if direction == up else y - 1 if direction == down else y if direction == left else y + 1}")

    if pirate.getTeamSignal():
        s = pirate.getTeamSignal()
        x, y = map(int, s[1:].split(','))
        return moveTo(x, y, pirate)
    else:
        return spread(pirate)

def ActTeam(team):
    l = team.trackPlayers()
    s = team.getTeamSignal()

    team.buildWalls(1)
    team.buildWalls(2)
    team.buildWalls(3)

    if s:
        island_no = int(s[0])
        signal = l[island_no - 1]
        if signal == "myCaptured":
            team.setTeamSignal("")
