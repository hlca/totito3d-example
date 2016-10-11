import itertools
import random
import copy
import operator

board = [
  [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
  ],
  [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
  ],
  [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
  ],
  [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
  ]
]

iterations = 50

p1_token = 1
p2_token = -1
draw_token = 0

allPositions = list(itertools.product([0,1,2,3], repeat=3))
#print random.sample(allPositions, len(allPositions)/2)

def slice_winner(state_slice):
  slice_size = len(state_slice)
  sums = [sum(row) for row in state_slice]
  sums.extend([sum([row[i] for row in state_slice]) for i in range(slice_size)])

  if (p1_token * slice_size) in sums:
    return p1_token
  elif (p2_token * slice_size) in sums:
    return p2_token

  return 0


def winner(state):
  for state_slice in state:
    winner_in_slice = slice_winner(state_slice)
    if winner_in_slice != draw_token:
      return winner_in_slice

  state_size = len(state)

  for i in range(state_size):
    state_slice = []
    for j in range(state_size):
      state_slice.append([state[j][i][k] for k in range(state_size)])
    winner_in_slice = slice_winner(state_slice)

    if winner_in_slice != draw_token:
      return winner_in_slice

  diagonals = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  for i in range(state_size):
    diagonals[0] += state[i][i][i]
    diagonals[1] += state[state_size - 1 - i][i][i]
    diagonals[2] += state[i][state_size - 1 - i][i]
    diagonals[3] += state[state_size - 1 - i][state_size - 1 - i][i]
    for j in range(state_size):
      diagonals[4+j] += state[i][i][j]
      diagonals[8+j] += state[j][i][i]
      diagonals[12+j] += state[state_size - 1 - i][i][j]
      diagonals[16+j] += state[i][state_size - 1 - i][j]
      diagonals[20+j] += state[state_size - 1 - i][state_size - 1 - i][j]
    
  if (p1_token * state_size) in diagonals:
    return p1_token

  elif (p2_token * state_size) in diagonals:
    return p2_token

  return draw_token


def str_token(cell):
  if cell == p1_token:
    return "X"
  elif cell == p2_token:
    return "O"

  return "."


def draw_board(state):
  result = ""
  state_size = len(state)
  for y in range(state_size):
    for z in range(state_size):
      for x in range(state_size):
        result += str_token(state[x][y][z]) + " "
      result += "\t"
    result += "\n"
  return result


player_1_turn = True
while winner(board) == draw_token:

  # Print board state
  print ""
  print "Board:"
  print draw_board(board)
  print ""
  
  # Print 
  print "Player %s turn:" % (1 if player_1_turn else 2)

  # Get input

  if player_1_turn:
    x = int(raw_input("x: "))
    y = int(raw_input("y: "))
    z = int(raw_input("z: "))
  else:
    choises = {}
    #isForced = False
    #forcedPosition = (0, 0, 0)
    for position in allPositions:
      #Tomamos una de las posiciones y obtenemos los valores.
      tempX = position[0]
      tempY = position[1]
      tempZ = position[2]

      virtualBoard = copy.deepcopy(board)

      virtualBoard[tempX][tempY][tempZ] = -1

      jugadas = len(allPositions)

      for i in range(iterations):

        tempVirtualBoard = copy.deepcopy(virtualBoard)
        tempPositions = copy.deepcopy(allPositions)

        quienGano = winner(tempVirtualBoard) 
        tempJugadas = 0
        turn = 1
        while( quienGano == 0 and tempJugadas < jugadas):
          tempJugadas = tempJugadas + 1
          #print random.choise(tempPositions)
          thePosition = tempPositions[random.randrange(len(tempPositions))]
          tempVirtualBoard[thePosition[0]][thePosition[1]][thePosition[2]] = turn
          quienGano = winner(tempVirtualBoard) 
          if(turn == 1):
            turn = -1
          else:
            turn = 1


        if(quienGano == -1):
          #No va a perder
          if (tempX, tempY, tempZ) in choises:
            for i, j in choises.items():       
              if i == (tempX, tempY, tempZ) :
                  choises[i] = choises[i] + 2
          else:
            choises[position] =  2
        elif(quienGano == 0):
          #No va a perder
          if (tempX, tempY, tempZ) in choises:
            for i, j in choises.items():       
              if i == (tempX, tempY, tempZ) :
                  choises[i] = choises[i] + 1
          else:
            choises[position] =  1
        else:
          if (tempX, tempY, tempZ) in choises:
            for i, j in choises.items():       
              if i == (tempX, tempY, tempZ) :
                  choises[i] = choises[i] - 2
          else:
            choises[position] =  -2
          

    maxResult = (0,0,0)
    maxSum = 0
    worstMaxSum = iterations
    print choises
    maxResult = max(choises.iteritems(), key=operator.itemgetter(1))[0]
    print maxResult
    maxSum = j

    x = maxResult[0]
    y = maxResult[1]
    z = maxResult[2]
  if board[x][y][z] == draw_token:
    board[x][y][z] = 1 if player_1_turn else -1
    player_1_turn = not player_1_turn
    allPositions.remove((x,y,z))
  else:
    print ""
    print "ERROR: occupied position, please retry in a new position"
    print ""

print "Player %s is the winner!" % (1 if winner(board) == 1 else 2)
print draw_board(board)
