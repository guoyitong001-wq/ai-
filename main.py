class GameOfLife:
    def __init__(self):
        self.game_state = []
        self.game_ui = None
        self.current_mode = 'play'

    def initialize_game(self):
        # Initialize the game engine and UI
        self.game_state = self.create_initial_state()
        self.game_ui = self.create_ui()

    def create_initial_state(self):
        # Initialize the game grid state
        return [[0 for _ in range(20)] for _ in range(20)]

    def create_ui(self):
        # Create the UI elements
        print("UI Initialized.")

    def main_loop(self):
        while True:
            self.update_game_state()
            self.render()
            # Handle user inputs and transitions

    def update_game_state(self):
        # Update the game state based on rules
        pass

    def render(self):
        # Draw the current game state to the UI
        print(self.game_state)

    def switch_mode(self, new_mode):
        self.current_mode = new_mode
        print(f'Switched to {new_mode} mode.')

if __name__ == '__main__':
    game = GameOfLife()
    game.initialize_game()
    game.main_loop()