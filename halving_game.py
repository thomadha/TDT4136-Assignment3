import math

State = tuple[int, int] # Tuple of player (whose turn it is),
                        # and the number to be decreased
Action = str  # Decrement (number <- number-1) or halve (number <- number / 2)


class Game:
    def __init__(self, N: int):
        self.N = N

    def initial_state(self) -> State:
        return 0, self.N

    def to_move(self, state: State) -> int: #which player's turn it is at state s
        player, _ = state
        return player

    def actions(self, state: State) -> list[Action]: #legal actions at state s
        return ['--', '/2']

    def result(self, state: State, action: Action) -> State: #next state after taking action a at state s
        _, number = state
        if action == '--':
            return (self.to_move(state) + 1) % 2, number - 1
        else:
            return (self.to_move(state) + 1) % 2, number // 2  # Floored division

    def is_terminal(self, state: State) -> bool: #is state s an end state?
        _, number = state
        return number == 0

    def utility(self, state: State, player: int) -> float: #the value of the terminal state s for player p
        assert self.is_terminal(state)
        return 1 if self.to_move(state) == player else -1

    def print(self, state: State):
        _, number = state
        print(f'The number is {number} and ', end='')
        if self.is_terminal(state):
            if self.utility(state, 0) > 0:
                print(f'P1 won')
            else:
                print(f'P2 won')
        else:
            print(f'it is P{self.to_move(state)+1}\'s turn')

def minimax_search(game: Game, state: State) -> Action | None:
    player = game.to_move(state)
    value, move = max_value(game, state) # do a direct call instead. 
    return move


def max_value(game: Game, state: State):
    if game.is_terminal(state):
        return game.utility(state, player), None  #Må huske at utility trenger både state og game sitt state. 
    v = - math.inf     #float('-inf')
    #best_move = None
    for move in game.actions(state):
        value, _ = min_value(game, game.result(state, move))
        if value > v:
            v = value
            best_move = move
    return v, best_move

def min_value(game: Game, state: State):
    if game.is_terminal(state):
        return game.utility(state, player), None #Samme her. 
    v = math.inf       #float('inf')
    #best_move = None
    for move in game.actions(state):
        value, _ = max_value(game, game.result(state, move))
        if value < v:
            v = value
            best_move = move
    return v, best_move





game = Game(5)

state = game.initial_state()
game.print(state)
while not game.is_terminal(state):
    player = game.to_move(state)
    action = minimax_search(game, state) # The player whose turn it is
                                         # is the MAX player
    print(f'P{player+1}\'s action: {action}')
    assert action is not None
    state = game.result(state, action)
    game.print(state)

# Expected output:
# The number is 5 and it is P1's turn
# P1's action: --
# The number is 4 and it is P2's turn
# P2's action: --
# The number is 3 and it is P1's turn
# P1's action: /2
# The number is 1 and it is P2's turn
# P2's action: --
# The number is 0 and P1 won