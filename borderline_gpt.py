import random
import copy

class GamePiece:
    def __init__(self, player_color):
        self.player_color = player_color  # 'R' or 'B'
        self.pips = self.generate_random_pips()
    
    def generate_random_pips(self):
        pips = [['_' for _ in range(3)] for _ in range(3)]
        
        # Center pip is always filled
        pips[1][1] = self.player_color
        
        # Ensure at least one PIP in each row
        # Row 0: positions (0,0), (0,1), (0,2)
        # Row 1: center (1,1) already filled, can add (1,0), (1,2)  
        # Row 2: positions (2,0), (2,1), (2,2)
        
        row_positions = [
            [(0, 0), (0, 1), (0, 2)],  # Row 0
            [(1, 0), (1, 2)],          # Row 1 (center already filled)
            [(2, 0), (2, 1), (2, 2)]   # Row 2
        ]
        
        # Add at least one PIP to rows 0 and 2 (row 1 already has center)
        for row_idx in [0, 2]:
            available_positions = row_positions[row_idx]
            selected_pos = random.choice(available_positions)
            pips[selected_pos[0]][selected_pos[1]] = self.player_color
        
        # Now add random additional PIPs with weighted probability
        # We already have 3 PIPs (center + 2 mandatory row PIPs)
        remaining_positions = [(i, j) for i in range(3) for j in range(3) 
                              if pips[i][j] == '_']
        
        if remaining_positions:
            # 80% chance for 0 additional PIPs (3 total), 20% chance for 1-6 additional PIPs (4-9 total)
            if random.random() < 0.8:
                # 80% chance: keep exactly 3 PIPs (no additional PIPs)
                num_additional = 0
            else:
                # 20% chance: add 1-6 additional PIPs
                max_additional = min(6, len(remaining_positions))  # Max 9 total PIPs
                num_additional = random.randint(1, max_additional)
            
            if num_additional > 0:
                selected_positions = random.sample(remaining_positions, num_additional)
                for row, col in selected_positions:
                    pips[row][col] = self.player_color
        
        return pips
    
    def display(self):
        result = " ____\n"
        for row in self.pips:
            result += "|" + "|".join(row) + "|\n"
        return result
    
    def get_filled_positions(self):
        positions = []
        for i in range(3):
            for j in range(3):
                if self.pips[i][j] == self.player_color:
                    positions.append((i, j))
        return positions

class GameBoard:
    def __init__(self):
        self.grid = [[None for _ in range(6)] for _ in range(8)]
        self.width = 6
        self.height = 8
    
    def place_piece(self, piece, row, col):
        if self.is_valid_position(row, col):
            self.grid[row][col] = piece
            return True
        return False
    
    def remove_piece(self, row, col):
        if self.is_valid_position(row, col) and self.grid[row][col] is not None:
            piece = self.grid[row][col]
            self.grid[row][col] = None
            return piece
        return None
    
    def is_valid_position(self, row, col):
        return 0 <= row < self.height and 0 <= col < self.width
    
    def is_empty(self, row, col):
        return self.is_valid_position(row, col) and self.grid[row][col] is None
    
    def get_piece(self, row, col):
        if self.is_valid_position(row, col):
            return self.grid[row][col]
        return None
    
    def display(self, highlight_positions=None):
        """Display the board, optionally highlighting pieces at highlight_positions (list of (row, col) tuples)"""
        result = ""

        # Convert single position to list for backward compatibility
        if highlight_positions is not None and not isinstance(highlight_positions, list):
            highlight_positions = [highlight_positions]

        # Create set for faster lookup
        highlight_set = set(highlight_positions) if highlight_positions else set()

        for board_row in range(self.height):
            # Top border for each row of squares
            for board_col in range(self.width):
                result += " ____"
            result += "\n"

            # Display each of the 3 pip rows for this board row
            for pip_row in range(3):
                for board_col in range(self.width):
                    piece = self.grid[board_row][board_col]
                    if piece is None:
                        result += "|_|_|_|"
                    else:
                        # Check if this piece should be highlighted
                        is_highlighted = (board_row, board_col) in highlight_set

                        # Build row content with lowercase for highlighted pieces
                        row_pips = []
                        for pip in piece.pips[pip_row]:
                            if is_highlighted and pip in ['R', 'B']:
                                row_pips.append(pip.lower())
                            else:
                                row_pips.append(pip)
                        row_content = "|" + "|".join(row_pips) + "|"
                        result += row_content
                result += "\n"

        # Final bottom border
        for board_col in range(self.width):
            result += " ____"
        result += "\n"

        return result
    
    def get_adjacent_positions(self, row, col):
        adjacent = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_position(new_row, new_col):
                adjacent.append((new_row, new_col))
        return adjacent
    
    def has_player_pieces_in_row(self, player_color, row):
        for col in range(self.width):
            piece = self.grid[row][col]
            if piece and piece.player_color == player_color:
                return True
        return False
    
    def get_player_pieces(self, player_color):
        pieces = []
        for row in range(self.height):
            for col in range(self.width):
                piece = self.grid[row][col]
                if piece and piece.player_color == player_color:
                    pieces.append((row, col, piece))
        return pieces
    
    def check_pip_adjacency(self, new_piece, new_row, new_col, existing_pieces):
        """Check if placing new_piece at (new_row, new_col) has adjacent PIPs with existing pieces"""
        adjacent_pips = []

        for exist_row, exist_col, exist_piece in existing_pieces:
            # Check if pieces are adjacent and which direction

            # Existing piece is ABOVE new piece
            if exist_row == new_row - 1 and exist_col == new_col:
                # Check all 3 columns where edges touch
                for col in range(3):
                    new_pip = new_piece.pips[0][col]  # Top edge of new piece
                    exist_pip = exist_piece.pips[2][col]  # Bottom edge of existing piece
                    if new_pip == new_piece.player_color and exist_pip == exist_piece.player_color:
                        adjacent_pips.append({
                            'new_pos': (new_row, new_col, 0, col),
                            'exist_pos': (exist_row, exist_col, 2, col),
                            'same_color': new_piece.player_color == exist_piece.player_color
                        })

            # Existing piece is BELOW new piece
            elif exist_row == new_row + 1 and exist_col == new_col:
                # Check all 3 columns where edges touch
                for col in range(3):
                    new_pip = new_piece.pips[2][col]  # Bottom edge of new piece
                    exist_pip = exist_piece.pips[0][col]  # Top edge of existing piece
                    if new_pip == new_piece.player_color and exist_pip == exist_piece.player_color:
                        adjacent_pips.append({
                            'new_pos': (new_row, new_col, 2, col),
                            'exist_pos': (exist_row, exist_col, 0, col),
                            'same_color': new_piece.player_color == exist_piece.player_color
                        })

            # Existing piece is LEFT of new piece
            elif exist_row == new_row and exist_col == new_col - 1:
                # Check all 3 rows where edges touch
                for row in range(3):
                    new_pip = new_piece.pips[row][0]  # Left edge of new piece
                    exist_pip = exist_piece.pips[row][2]  # Right edge of existing piece
                    if new_pip == new_piece.player_color and exist_pip == exist_piece.player_color:
                        adjacent_pips.append({
                            'new_pos': (new_row, new_col, row, 0),
                            'exist_pos': (exist_row, exist_col, row, 2),
                            'same_color': new_piece.player_color == exist_piece.player_color
                        })

            # Existing piece is RIGHT of new piece
            elif exist_row == new_row and exist_col == new_col + 1:
                # Check all 3 rows where edges touch
                for row in range(3):
                    new_pip = new_piece.pips[row][2]  # Right edge of new piece
                    exist_pip = exist_piece.pips[row][0]  # Left edge of existing piece
                    if new_pip == new_piece.player_color and exist_pip == exist_piece.player_color:
                        adjacent_pips.append({
                            'new_pos': (new_row, new_col, row, 2),
                            'exist_pos': (exist_row, exist_col, row, 0),
                            'same_color': new_piece.player_color == exist_piece.player_color
                        })

        return adjacent_pips

    def can_place_piece(self, piece, row, col, player_pieces):
        """Check if a piece can be legally placed according to game rules"""
        if not self.is_empty(row, col):
            return False

        # Rule 1: First piece placement restrictions
        player_color = piece.player_color
        if player_color == 'R':
            if not self.has_player_pieces_in_row(player_color, 0):
                return row == 0
        elif player_color == 'B':
            if not self.has_player_pieces_in_row(player_color, 7):
                return row == 7

        # Rule 2: Must be adjacent to existing piece with touching PIPs
        if player_pieces:
            adjacent_pips = self.check_pip_adjacency(piece, row, col, player_pieces)
            same_color_adjacent = any(adj['same_color'] for adj in adjacent_pips)
            return same_color_adjacent

        return True
    
    def check_victory(self, player_color):
        """Check if player has a contiguous connection across the board lengthwise (8 squares)"""
        # Use flood fill to find all connected PIPs of the player's color
        visited = set()
        
        # Find all PIPs of the player's color
        player_pips = []
        for board_row in range(self.height):
            for board_col in range(self.width):
                piece = self.grid[board_row][board_col]
                if piece and piece.player_color == player_color:
                    for pip_row in range(3):
                        for pip_col in range(3):
                            if piece.pips[pip_row][pip_col] == player_color:
                                global_pip_row = board_row * 3 + pip_row
                                global_pip_col = board_col * 3 + pip_col
                                player_pips.append((global_pip_row, global_pip_col))
        
        # Check each pip to see if it can reach across the board
        for start_pip in player_pips:
            if start_pip in visited:
                continue
            
            connected_component = self.flood_fill(start_pip, player_pips, visited.copy())
            
            # Check if this component spans the board lengthwise (0 to 7*3+2 = 23)
            min_row = min(pos[0] for pos in connected_component)
            max_row = max(pos[0] for pos in connected_component)
            
            # Victory condition: connection spans from top area (0-2) to bottom area (21-23)
            if min_row <= 2 and max_row >= 21:
                return True
            
            visited.update(connected_component)
        
        return False
    
    def flood_fill(self, start, all_pips, visited):
        """Find all connected PIPs starting from start position"""
        stack = [start]
        connected = set()
        pip_set = set(all_pips)
        
        while stack:
            current = stack.pop()
            if current in visited or current in connected:
                continue
            
            if current not in pip_set:
                continue
                
            connected.add(current)
            visited.add(current)
            
            # Check 4-directional adjacency
            row, col = current
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (row + dr, col + dc)
                if neighbor not in visited and neighbor in pip_set:
                    stack.append(neighbor)
        
        return connected
    
    def resolve_combat(self, adjacent_pips):
        """Handle combat when different colored PIPs are adjacent"""
        combats = []
        
        for adj in adjacent_pips:
            if not adj['same_color']:
                # Different colors - combat!
                red_roll = random.randint(1, 6)
                blue_roll = random.randint(1, 6)
                
                new_pos = adj['new_pos']
                exist_pos = adj['exist_pos']
                
                combat_result = {
                    'new_piece_pos': (new_pos[0], new_pos[1]),
                    'existing_piece_pos': (exist_pos[0], exist_pos[1]),
                    'red_roll': red_roll,
                    'blue_roll': blue_roll,
                    'winner': 'R' if red_roll > blue_roll else 'B'
                }
                combats.append(combat_result)
        
        return combats

class Player:
    def __init__(self, color, name):
        self.color = color  # 'R' or 'B'
        self.name = name
        self.pieces = [GamePiece(color) for _ in range(15)]
        self.pieces_on_board = []
    
    def has_pieces(self):
        return len(self.pieces) > 0
    
    def get_piece(self):
        if self.pieces:
            return self.pieces.pop()
        return None
    
    def add_piece_back(self, piece):
        self.pieces.append(piece)
    
    def display_remaining_pieces(self):
        if not self.pieces:
            return f"{self.name}: No pieces remaining"
        
        result = f"{self.name} ({len(self.pieces)} pieces):\n"
        
        # Display pieces in rows of up to 8 pieces each (with gaps, fewer fit)
        pieces_per_row = 8
        for start_idx in range(0, len(self.pieces), pieces_per_row):
            end_idx = min(start_idx + pieces_per_row, len(self.pieces))
            row_pieces = self.pieces[start_idx:end_idx]
            
            # Display top borders for this row with gaps
            for i, piece in enumerate(row_pieces):
                if i > 0:
                    result += "  "  # Gap between pieces
                result += " ____"
            result += "\n"
            
            # Display each of the 3 PIP rows with gaps
            for pip_row in range(3):
                for i, piece in enumerate(row_pieces):
                    if i > 0:
                        result += "  "  # Gap between pieces
                    row_content = "|" + "|".join(piece.pips[pip_row]) + "|"
                    result += row_content
                result += "\n"
        
        return result

class AIPlayer(Player):
    def __init__(self, color, name):
        super().__init__(color, name)
    
    def choose_move(self, board):
        """AI decision making for piece placement"""
        if not self.has_pieces():
            return None, None, None
        
        current_pieces = board.get_player_pieces(self.color)
        valid_moves = []
        
        # Try each piece and position
        for piece_idx, piece in enumerate(self.pieces):
            for row in range(board.height):
                for col in range(board.width):
                    if board.can_place_piece(piece, row, col, current_pieces):
                        score = self.evaluate_move(board, piece, row, col, current_pieces)
                        valid_moves.append((score, piece_idx, row, col))
        
        if not valid_moves:
            return None, None, None
        
        # Sort by score (highest first) and choose best move
        valid_moves.sort(reverse=True)
        best_score, piece_idx, row, col = valid_moves[0]
        
        chosen_piece = self.pieces[piece_idx]
        return chosen_piece, row, col
    
    def evaluate_move(self, board, piece, row, col, current_pieces):
        """Evaluate the quality of a potential move"""
        score = 0
        
        # Create temporary board state to evaluate
        temp_board = copy.deepcopy(board)
        temp_board.place_piece(piece, row, col)
        temp_current_pieces = current_pieces + [(row, col, piece)]
        
        # Priority 1: Win condition (highest priority)
        if temp_board.check_victory(self.color):
            score += 1000
        
        # Priority 2: Block opponent win (high priority)
        opponent_color = 'B' if self.color == 'R' else 'R'
        if temp_board.check_victory(opponent_color):
            score -= 800
        
        # Priority 3: Progress toward victory (connection building)
        connection_score = self.evaluate_connection_progress(temp_board)
        score += connection_score * 10
        
        # Priority 4: Strategic positioning
        # Prefer central positions
        center_distance = abs(row - 3.5) + abs(col - 2.5)
        score += (10 - center_distance) * 2
        
        # Priority 5: Piece efficiency (more PIPs = better)
        pip_count = len(piece.get_filled_positions())
        score += pip_count
        
        return score
    
    def evaluate_connection_progress(self, board):
        """Evaluate how close the player is to winning"""
        player_pips = []
        for board_row in range(board.height):
            for board_col in range(board.width):
                piece = board.grid[board_row][board_col]
                if piece and piece.player_color == self.color:
                    for pip_row in range(3):
                        for pip_col in range(3):
                            if piece.pips[pip_row][pip_col] == self.color:
                                global_pip_row = board_row * 3 + pip_row
                                global_pip_col = board_col * 3 + pip_col
                                player_pips.append((global_pip_row, global_pip_col))
        
        if not player_pips:
            return 0
        
        # Find largest connected component
        visited = set()
        max_component_size = 0
        best_span = 0
        
        for start_pip in player_pips:
            if start_pip in visited:
                continue
            
            connected_component = board.flood_fill(start_pip, player_pips, visited.copy())
            
            if len(connected_component) > max_component_size:
                max_component_size = len(connected_component)
                
                # Calculate span
                min_row = min(pos[0] for pos in connected_component)
                max_row = max(pos[0] for pos in connected_component)
                best_span = max_row - min_row
            
            visited.update(connected_component)
        
        # Reward large connected components and good span
        return max_component_size + (best_span * 2)

class BorderlineGPT:
    def __init__(self):
        self.board = GameBoard()
        self.red_player = AIPlayer('R', 'Red AI')
        self.blue_player = AIPlayer('B', 'Blue AI')
        self.current_player = self.red_player
        self.turn_count = 0
        self.game_over = False
        self.winner = None
        self.last_placed_pos = None  # Track last placed piece for highlighting
    
    def switch_player(self):
        self.current_player = self.blue_player if self.current_player == self.red_player else self.red_player
    
    def play_turn(self):
        """Execute one turn of the game"""
        if self.game_over:
            return
        
        print(f"\n=== Turn {self.turn_count + 1}: {self.current_player.name} ===")
        
        # Check if current player has pieces
        if not self.current_player.has_pieces():
            print(f"{self.current_player.name} has no pieces left - skipping turn")
            if not self.red_player.has_pieces() and not self.blue_player.has_pieces():
                self.game_over = True
                print("Game Over: Both players out of pieces!")
                return
            self.switch_player()
            self.turn_count += 1
            return
        
        # AI chooses move
        piece, row, col = self.current_player.choose_move(self.board)
        
        if piece is None:
            print(f"{self.current_player.name} has no valid moves - skipping turn")
            self.switch_player()
            self.turn_count += 1
            return
        
        # Remove piece from player's hand
        self.current_player.pieces.remove(piece)
        
        # Check for combat before placing
        current_pieces = self.board.get_player_pieces(self.current_player.color)
        all_pieces = self.board.get_player_pieces('R') + self.board.get_player_pieces('B')
        adjacent_pips = self.board.check_pip_adjacency(piece, row, col, all_pieces)
        
        # Place piece
        self.board.place_piece(piece, row, col)
        print(f"{self.current_player.name} places piece at ({row}, {col})")

        # Track this position for highlighting
        self.last_placed_pos = (row, col)

        # Handle combat
        if adjacent_pips:
            combats = self.board.resolve_combat(adjacent_pips)
            for combat in combats:
                # Get positions of both combatants
                attacker_pos = combat['new_piece_pos']
                defender_pos = combat['existing_piece_pos']

                # Show both pieces highlighted during combat
                print(f"COMBAT! Red rolls {combat['red_roll']}, Blue rolls {combat['blue_roll']}")
                print(self.board.display(highlight_positions=[attacker_pos, defender_pos]))

                if combat['winner'] != self.current_player.color:
                    # Current player loses, remove their piece
                    lost_piece = self.board.remove_piece(row, col)
                    if lost_piece:
                        self.current_player.add_piece_back(lost_piece)
                        print(f"{self.current_player.name} loses combat and piece is returned!")
                        # Clear highlight since piece was removed
                        self.last_placed_pos = None
                else:
                    # Opponent loses, remove their piece
                    loser_row, loser_col = combat['existing_piece_pos']
                    lost_piece = self.board.remove_piece(loser_row, loser_col)
                    if lost_piece:
                        loser_player = self.red_player if lost_piece.player_color == 'R' else self.blue_player
                        loser_player.add_piece_back(lost_piece)
                        print(f"Opponent loses combat and their piece is returned!")

        # Check victory
        if self.board.check_victory(self.current_player.color):
            self.winner = self.current_player
            self.game_over = True
            print(f"\n🎉 VICTORY! {self.current_player.name} wins! 🎉")
            return

        self.switch_player()
        self.turn_count += 1
    
    def display_game_state(self):
        """Display the complete game state including board and remaining pieces"""
        print(self.board.display(highlight_positions=self.last_placed_pos))
        print(self.red_player.display_remaining_pieces())
        print(self.blue_player.display_remaining_pieces())
    
    def play_game(self):
        """Main game loop"""
        print("🎮 Starting Borderline GPT! 🎮")
        self.display_game_state()
        
        while not self.game_over and self.turn_count < 100:  # Safety limit
            self.play_turn()
            if not self.game_over:
                self.display_game_state()
        
        if not self.game_over:
            print("Game ended due to turn limit!")
        
        print(f"\nFinal board state:")
        self.display_game_state()
        
        if self.winner:
            print(f"Winner: {self.winner.name}!")
        else:
            print("Game ended in a draw!")

if __name__ == "__main__":
    game = BorderlineGPT()
    game.play_game()