import random
import copy

class GamePiece:
    def __init__(self, player_color, pip_pattern=None):
        self.player_color = player_color  # 'R' or 'B'
        if pip_pattern is not None:
            # Use provided pip pattern
            self.pips = pip_pattern
        else:
            # Generate random pips (legacy support)
            self.pips = self.generate_random_pips()

    @staticmethod
    def create_fixed_piece_set(player_color):
        """
        Create the fixed set of 16 starting pieces defined in STARTING_PIECES.md
        Returns a list of GamePiece objects
        """
        pieces = []

        # 3 of these: Vertical line (3 pips)
        # | |R|_|
        # |_|R|_|
        # |_|R|_|
        pattern1 = [
            ['_', player_color, '_'],
            ['_', player_color, '_'],
            ['_', player_color, '_']
        ]
        for _ in range(3):
            pieces.append(GamePiece(player_color, [row[:] for row in pattern1]))

        # 3 of these: Diagonal (3 pips)
        # |R| |_|
        # |_|R|_|
        # |_|_|R|
        pattern2 = [
            [player_color, '_', '_'],
            ['_', player_color, '_'],
            ['_', '_', player_color]
        ]
        for _ in range(3):
            pieces.append(GamePiece(player_color, [row[:] for row in pattern2]))

        # 3 of these: T-shape (4 pips)
        # |R| |R|
        # |_|R|_|
        # |_|R|_|
        pattern3 = [
            [player_color, '_', player_color],
            ['_', player_color, '_'],
            ['_', player_color, '_']
        ]
        for _ in range(3):
            pieces.append(GamePiece(player_color, [row[:] for row in pattern3]))

        # 2 of these: X-shape (5 pips)
        # |R| |R|
        # |_|R|_|
        # |R| |R|
        pattern4 = [
            [player_color, '_', player_color],
            ['_', player_color, '_'],
            [player_color, '_', player_color]
        ]
        for _ in range(2):
            pieces.append(GamePiece(player_color, [row[:] for row in pattern4]))

        # 2 of these: Plus-shape (5 pips)
        # | |R| |
        # |R|R|R|
        # | |R| |
        pattern5 = [
            ['_', player_color, '_'],
            [player_color, player_color, player_color],
            ['_', player_color, '_']
        ]
        for _ in range(2):
            pieces.append(GamePiece(player_color, [row[:] for row in pattern5]))

        # 3 of these: Full block (9 pips)
        # |R|R|R|
        # |R|R|R|
        # |R|R|R|
        pattern6 = [
            [player_color, player_color, player_color],
            [player_color, player_color, player_color],
            [player_color, player_color, player_color]
        ]
        for _ in range(3):
            pieces.append(GamePiece(player_color, [row[:] for row in pattern6]))

        return pieces

    def generate_random_pips(self):
        """Legacy random pip generation (kept for backward compatibility)"""
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

    def get_power_level(self):
        """Calculate power level as number of pips / 2 (rounded down)"""
        pip_count = len(self.get_filled_positions())
        return pip_count // 2

    def convert_to_color(self, new_color):
        """Convert all pips on this piece to a new color"""
        old_color = self.player_color
        self.player_color = new_color

        # Update all pips from old color to new color
        for i in range(3):
            for j in range(3):
                if self.pips[i][j] == old_color:
                    self.pips[i][j] = new_color

    def rotate(self, degrees):
        """
        Rotate the piece around its center PIP.
        degrees: 0, 90, 180, or 270 (clockwise rotation)
        Returns a new GamePiece with rotated pip pattern
        """
        if degrees not in [0, 90, 180, 270]:
            raise ValueError("Rotation must be 0, 90, 180, or 270 degrees")

        if degrees == 0:
            # No rotation - return a copy
            rotated = copy.deepcopy(self)
            return rotated

        # Create new piece with same color
        rotated = GamePiece.__new__(GamePiece)
        rotated.player_color = self.player_color
        rotated.pips = [['_' for _ in range(3)] for _ in range(3)]

        # Rotate each pip around the center [1][1]
        for i in range(3):
            for j in range(3):
                if self.pips[i][j] != '_':
                    # Calculate position relative to center
                    rel_i = i - 1
                    rel_j = j - 1

                    # Rotate coordinates
                    if degrees == 90:
                        # 90° clockwise: (x, y) -> (y, -x)
                        new_rel_i = rel_j
                        new_rel_j = -rel_i
                    elif degrees == 180:
                        # 180°: (x, y) -> (-x, -y)
                        new_rel_i = -rel_i
                        new_rel_j = -rel_j
                    elif degrees == 270:
                        # 270° clockwise: (x, y) -> (-y, x)
                        new_rel_i = -rel_j
                        new_rel_j = rel_i

                    # Convert back to absolute coordinates
                    new_i = new_rel_i + 1
                    new_j = new_rel_j + 1

                    rotated.pips[new_i][new_j] = self.player_color

        return rotated

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
        """Check if placing new_piece at (new_row, new_col) has adjacent PIPs with existing pieces

        Adjacency rules:
        - Orthogonal adjacency (up/down/left/right): Always counts
        - Diagonal adjacency: Only counts for corner pips (positions 0,0 / 0,2 / 2,0 / 2,2)
        """
        adjacent_pips = []

        # Corner positions in a 3x3 piece
        corners = {(0, 0), (0, 2), (2, 0), (2, 2)}

        # Get all pips from the new piece with their global coordinates
        new_pips = []
        for pip_row in range(3):
            for pip_col in range(3):
                if new_piece.pips[pip_row][pip_col] == new_piece.player_color:
                    global_pip_row = new_row * 3 + pip_row
                    global_pip_col = new_col * 3 + pip_col
                    is_corner = (pip_row, pip_col) in corners
                    new_pips.append((global_pip_row, global_pip_col, pip_row, pip_col, is_corner))

        # Check against all existing pieces
        for exist_row, exist_col, exist_piece in existing_pieces:
            # Get all pips from this existing piece
            for pip_row in range(3):
                for pip_col in range(3):
                    if exist_piece.pips[pip_row][pip_col] == exist_piece.player_color:
                        exist_global_row = exist_row * 3 + pip_row
                        exist_global_col = exist_col * 3 + pip_col
                        exist_is_corner = (pip_row, pip_col) in corners

                        # Check if any pip in new piece is adjacent to this pip
                        for new_global_row, new_global_col, new_pip_row, new_pip_col, new_is_corner in new_pips:
                            row_diff = abs(new_global_row - exist_global_row)
                            col_diff = abs(new_global_col - exist_global_col)

                            # Skip if same position
                            if row_diff == 0 and col_diff == 0:
                                continue

                            # Check if adjacent
                            is_orthogonal = (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)
                            is_diagonal = (row_diff == 1 and col_diff == 1)

                            # Orthogonal adjacency always counts
                            # Diagonal adjacency only counts if BOTH pips are corners
                            if is_orthogonal or (is_diagonal and new_is_corner and exist_is_corner):
                                adjacent_pips.append({
                                    'new_pos': (new_row, new_col, new_pip_row, new_pip_col),
                                    'exist_pos': (exist_row, exist_col, pip_row, pip_col),
                                    'same_color': new_piece.player_color == exist_piece.player_color
                                })

        return adjacent_pips

    def can_place_piece(self, piece, row, col, player_pieces):
        """Check if a piece can be legally placed according to game rules"""
        if not self.is_empty(row, col):
            return False

        player_color = piece.player_color

        # Rule 1: Players can always place in their starting row
        # Red's starting row is 0 (top), Blue's starting row is 7 (bottom)
        if player_color == 'R' and row == 0:
            return True
        elif player_color == 'B' and row == 7:
            return True

        # Rule 2: Must be adjacent to existing piece with touching PIPs
        if player_pieces:
            adjacent_pips = self.check_pip_adjacency(piece, row, col, player_pieces)
            same_color_adjacent = any(adj['same_color'] for adj in adjacent_pips)
            return same_color_adjacent

        # If no pieces on board and not in starting row, placement is illegal
        return False
    
    def check_victory(self, player_color, debug=False):
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

        if debug:
            print(f"\n=== DEBUG: Victory check for {player_color} ===")
            print(f"Total {player_color} pips: {len(player_pips)}")

        # Check each pip to see if it can reach across the board
        for start_pip in player_pips:
            if start_pip in visited:
                continue

            connected_component = self.flood_fill(start_pip, player_pips, visited.copy())

            # Check if this component spans the board lengthwise
            # Victory requires spanning from top board row to bottom board row
            # Board row 0 = pip rows 0-2, Board row 7 = pip rows 21-23
            rows_with_pips = set(pos[0] for pos in connected_component)
            min_row = min(rows_with_pips)
            max_row = max(rows_with_pips)

            # Check if connection reaches from one end of board to the other
            # Must span from top board row (pips 0-2) to bottom board row (pips 21-23)
            top_end_reached = min_row <= 2  # Touches board row 0
            bottom_end_reached = max_row >= 21  # Touches board row 7

            if debug:
                print(f"Component starting at {start_pip}: size={len(connected_component)}, rows={min_row}-{max_row}")
                if top_end_reached and bottom_end_reached:
                    print(f"  -> VICTORY! Component spans from row {min_row} to {max_row}")

            if top_end_reached and bottom_end_reached:
                return True

            visited.update(connected_component)

        if debug:
            print(f"No winning path found")

        return False
    
    def is_corner_pip(self, global_pip_row, global_pip_col):
        """Check if a pip at global coordinates is a corner pip of its piece"""
        # Get the piece position
        board_row = global_pip_row // 3
        board_col = global_pip_col // 3

        # Get the pip position within the piece
        pip_row = global_pip_row % 3
        pip_col = global_pip_col % 3

        # Corner positions are (0,0), (0,2), (2,0), (2,2)
        return (pip_row, pip_col) in {(0, 0), (0, 2), (2, 0), (2, 2)}

    def flood_fill(self, start, all_pips, visited):
        """
        Find all connected PIPs starting from start position.
        Respects adjacency rules:
        - Orthogonal always valid
        - Diagonal valid if: within same piece OR both pips are corners
        """
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

            row, col = current
            current_board_row = row // 3
            current_board_col = col // 3
            current_is_corner = self.is_corner_pip(row, col)

            # Check orthogonal adjacency (always valid)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (row + dr, col + dc)
                if neighbor not in visited and neighbor in pip_set:
                    stack.append(neighbor)

            # Check diagonal adjacency
            for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                neighbor = (row + dr, col + dc)
                if neighbor not in visited and neighbor in pip_set:
                    neighbor_board_row = neighbor[0] // 3
                    neighbor_board_col = neighbor[1] // 3

                    # Diagonal valid if: same piece OR both are corners
                    same_piece = (current_board_row == neighbor_board_row and
                                current_board_col == neighbor_board_col)
                    both_corners = (current_is_corner and
                                  self.is_corner_pip(neighbor[0], neighbor[1]))

                    if same_piece or both_corners:
                        stack.append(neighbor)

        return connected

    def check_piece_connected_to_home(self, board_row, board_col):
        """
        Check if a piece at (board_row, board_col) has a contiguous pip connection
        back to its home row (Row 0 for Red, Row 7 for Blue)

        Returns True if connected to home, False otherwise
        """
        piece = self.grid[board_row][board_col]
        if not piece:
            return False

        color = piece.player_color
        home_row = 0 if color == 'R' else 7

        # Get all pips of this color on the board
        all_pips = []
        for br in range(self.height):
            for bc in range(self.width):
                p = self.grid[br][bc]
                if p and p.player_color == color:
                    for pip_row in range(3):
                        for pip_col in range(3):
                            if p.pips[pip_row][pip_col] == color:
                                global_pip_row = br * 3 + pip_row
                                global_pip_col = bc * 3 + pip_col
                                all_pips.append((global_pip_row, global_pip_col))

        # Get pips from the current piece
        piece_pips = []
        for pip_row in range(3):
            for pip_col in range(3):
                if piece.pips[pip_row][pip_col] == color:
                    global_pip_row = board_row * 3 + pip_row
                    global_pip_col = board_col * 3 + pip_col
                    piece_pips.append((global_pip_row, global_pip_col))

        if not piece_pips:
            return False

        # Use flood fill from any pip in this piece to see if we can reach home row
        visited = set()
        start_pip = piece_pips[0]
        connected_component = self.flood_fill(start_pip, all_pips, visited)

        # Check if any pip in the connected component reaches the home row
        home_pip_rows = [home_row * 3, home_row * 3 + 1, home_row * 3 + 2]
        for pip_pos in connected_component:
            if pip_pos[0] in home_pip_rows:
                return True

        return False

    def remove_disconnected_pieces(self, losing_color):
        """
        After combat, remove any pieces of the losing color that don't have a contiguous
        connection back to their home row. Returns list of removed pieces.

        Args:
            losing_color: 'R' or 'B' - the color that lost the combat
        """
        removed_pieces = []

        # Check only pieces of the losing color
        pieces_to_check = []
        for board_row in range(self.height):
            for board_col in range(self.width):
                piece = self.grid[board_row][board_col]
                if piece and piece.player_color == losing_color:
                    pieces_to_check.append((board_row, board_col))

        # FIRST: Identify ALL disconnected pieces (before removing any)
        disconnected_positions = []
        for board_row, board_col in pieces_to_check:
            piece = self.grid[board_row][board_col]
            if piece and not self.check_piece_connected_to_home(board_row, board_col):
                disconnected_positions.append((board_row, board_col))

        # SECOND: Remove all disconnected pieces
        for board_row, board_col in disconnected_positions:
            removed_piece = self.remove_piece(board_row, board_col)
            if removed_piece:
                removed_pieces.append({
                    'row': board_row,
                    'col': board_col,
                    'piece': removed_piece
                })

        return removed_pieces

    def resolve_combat(self, new_piece, new_row, new_col, adjacent_pips):
        """Handle combat when different colored PIPs are adjacent

        Returns None if no combat, or a dict with combat results including:
        - All defending pieces and their combined power
        - Die rolls with power bonuses
        - Winner
        """
        if not adjacent_pips:
            return None

        # Filter for enemy contacts only
        enemy_contacts = [adj for adj in adjacent_pips if not adj['same_color']]
        if not enemy_contacts:
            return None

        # Get all unique defending piece positions
        defending_positions = set()
        for contact in enemy_contacts:
            pos = contact['exist_pos']
            defending_positions.add((pos[0], pos[1]))

        # Get all defending pieces
        defending_pieces = []
        total_defender_power = 0
        for row, col in defending_positions:
            piece = self.grid[row][col]
            if piece:
                power = piece.get_power_level()
                defending_pieces.append({
                    'row': row,
                    'col': col,
                    'piece': piece,
                    'power': power
                })
                total_defender_power += power

        # Calculate attacker power
        attacker_power = new_piece.get_power_level()

        # Roll dice
        attacker_roll = random.randint(1, 6)
        defender_roll = random.randint(1, 6)

        # Add power levels
        attacker_total = attacker_roll + attacker_power
        defender_total = defender_roll + total_defender_power

        # Determine winner (attacker wins on tie)
        attacker_color = new_piece.player_color
        defender_color = 'B' if attacker_color == 'R' else 'R'
        winner = attacker_color if attacker_total >= defender_total else defender_color

        return {
            'attacker_pos': (new_row, new_col),
            'attacker_power': attacker_power,
            'attacker_roll': attacker_roll,
            'attacker_total': attacker_total,
            'attacker_color': attacker_color,
            'defenders': defending_pieces,
            'defender_power': total_defender_power,
            'defender_roll': defender_roll,
            'defender_total': defender_total,
            'defender_color': defender_color,
            'winner': winner
        }

class Player:
    def __init__(self, color, name):
        self.color = color  # 'R' or 'B'
        self.name = name
        # Use fixed piece set instead of random generation
        self.pieces = GamePiece.create_fixed_piece_set(color)
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
            return None, None, None, None, None

        current_pieces = board.get_player_pieces(self.color)
        valid_moves = []

        # Try each piece, rotation, and position
        for piece_idx, piece in enumerate(self.pieces):
            for rotation in [0, 90, 180, 270]:
                rotated_piece = piece.rotate(rotation)
                for row in range(board.height):
                    for col in range(board.width):
                        if board.can_place_piece(rotated_piece, row, col, current_pieces):
                            score = self.evaluate_move(board, rotated_piece, row, col, current_pieces)
                            valid_moves.append((score, piece_idx, row, col, rotation))

        if not valid_moves:
            return None, None, None, None, None

        # Sort by score (highest first) and choose best move
        valid_moves.sort(reverse=True)
        best_score, piece_idx, row, col, rotation = valid_moves[0]

        # Get the piece and apply the chosen rotation
        chosen_piece = self.pieces[piece_idx]
        rotated_piece = chosen_piece.rotate(rotation)

        return rotated_piece, row, col, rotation, piece_idx
    
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

class AggressiveConnectorAI(AIPlayer):
    """Red Strategy: Aggressive path builder focusing on direct vertical connection"""
    def __init__(self, color, name):
        super().__init__(color, name)

    def evaluate_move(self, board, piece, row, col, current_pieces):
        """Aggressive strategy: prioritize vertical progress and direct paths"""
        score = 0

        # Create temporary board state
        temp_board = copy.deepcopy(board)
        temp_board.place_piece(piece, row, col)

        # Priority 1: Win condition (ULTIMATE)
        if temp_board.check_victory(self.color):
            score += 100000  # MASSIVE - winning is everything!

        # Priority 2: Check if this move creates a battle opportunity that could win the game
        battle_value = self.evaluate_battle_opportunity(board, piece, row, col, current_pieces)
        score += battle_value

        # Priority 3: Path continuity - ensure we're building a continuous path
        pieces_remaining = len([p for p in current_pieces if p is not None])
        if pieces_remaining < 8:  # Running low on pieces!
            # Be VERY selective - only build on existing path
            path_continuity = self.evaluate_path_continuity(temp_board, row, col)
            score += path_continuity * 300  # HUGE bonus for staying on path

        # GEN 30: Improved with battle awareness, lookahead, and path continuity
        # Focus on vertical progress but also exploit battle opportunities and ensure continuous paths

        if self.color == 'R':
            vertical_progress = row
            score += vertical_progress * 200  # EXTREME vertical priority!
        else:
            vertical_progress = 7 - row
            score += vertical_progress * 200

        # Connection is EVERYTHING - maximize this above all else
        connection_score = self.evaluate_vertical_connection(temp_board)
        score += connection_score * 150  # Up from 100!

        all_pieces = temp_board.get_player_pieces('R') + temp_board.get_player_pieces('B')
        adjacent_pips = temp_board.check_pip_adjacency(piece, row, col, all_pieces)
        enemy_adjacent = sum(1 for adj in adjacent_pips if not adj['same_color'])
        if enemy_adjacent > 0:
            score += enemy_adjacent * 5  # MINIMAL - avoid all combat unless strategic!

        pip_count = len(piece.get_filled_positions())
        score += pip_count * 30  # Bigger pieces = better connections

        # ULTRA-FOCUSED: Stick to column 2 or 3 (center columns)
        # Try column 2 this time for variety
        preferred_col = 2
        col_distance = abs(col - preferred_col)
        score -= col_distance * 100  # MASSIVE penalty for deviation!

        return score

    def evaluate_battle_opportunity(self, board, piece, row, col, current_pieces):
        """Evaluate if winning a battle at this position could lead to victory

        Strategy:
        1. Check which enemy pieces would be in combat
        2. Simulate winning the combat and removing disconnected enemy pieces
        3. Check if that would create a winning path
        """
        # Check if this move would trigger combat
        all_pieces = board.get_player_pieces('R') + board.get_player_pieces('B')
        adjacent_pips = board.check_pip_adjacency(piece, row, col, all_pieces)
        enemy_contacts = [adj for adj in adjacent_pips if not adj['same_color']]

        if not enemy_contacts:
            return 0  # No combat, no opportunity

        # Get enemy color
        enemy_color = 'B' if self.color == 'R' else 'R'

        # Simulate placing the piece and winning the combat
        temp_board = copy.deepcopy(board)
        temp_board.place_piece(piece, row, col)

        # Simulate removing disconnected enemy pieces if we win
        # (We'll check what would happen if enemy loses)
        removed_positions = []
        for board_row in range(temp_board.height):
            for board_col in range(temp_board.width):
                enemy_piece = temp_board.grid[board_row][board_col]
                if enemy_piece and enemy_piece.player_color == enemy_color:
                    if not temp_board.check_piece_connected_to_home(board_row, board_col):
                        removed_positions.append((board_row, board_col))

        # Create a board state with those pieces removed
        victory_test_board = copy.deepcopy(temp_board)
        for r, c in removed_positions:
            victory_test_board.remove_piece(r, c)

        # Check if removing those pieces gives us victory
        if victory_test_board.check_victory(self.color):
            # This battle could win the game!
            return 50000  # Very high but less than immediate win

        # Even if it doesn't win immediately, check if it improves our connection significantly
        old_connection = self.evaluate_vertical_connection(temp_board)
        new_connection = self.evaluate_vertical_connection(victory_test_board)
        connection_improvement = new_connection - old_connection

        if connection_improvement > 5:  # Significant improvement
            return connection_improvement * 500  # Reward proportional to improvement

        return 0

    def evaluate_path_continuity(self, board, new_row, new_col):
        """Check if the new piece connects well to existing pieces

        This prevents leaving gaps when running low on pieces.
        Returns a score based on how well this piece extends the existing path.
        """
        # Get all our existing pieces
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
            return 0  # First piece, can't evaluate continuity

        # Check if this new piece's position has pips that connect to existing pips
        new_piece = board.grid[new_row][new_col]
        if not new_piece:
            return 0

        new_pips = []
        for pip_row in range(3):
            for pip_col in range(3):
                if new_piece.pips[pip_row][pip_col] == self.color:
                    global_pip_row = new_row * 3 + pip_row
                    global_pip_col = new_col * 3 + pip_col
                    new_pips.append((global_pip_row, global_pip_col))

        # Count how many of the new pips are adjacent to existing pips
        connected_count = 0
        for new_pip in new_pips:
            for existing_pip in player_pips:
                # Check if adjacent (orthogonal or diagonal)
                dr = abs(new_pip[0] - existing_pip[0])
                dc = abs(new_pip[1] - existing_pip[1])
                if dr <= 1 and dc <= 1 and not (dr == 0 and dc == 0):
                    connected_count += 1
                    break  # Count each new pip only once

        # Return score based on how many connections we made
        return connected_count

    def evaluate_vertical_connection(self, board):
        """Calculate the longest vertical span of connected pips"""
        player_pips = []
        for board_row in range(board.height):
            for board_col in range(board.width):
                piece = board.grid[board_row][board_col]
                if piece and piece.player_color == self.color:
                    for pip_row in range(3):
                        for pip_col in range(3):
                            if piece.pips[pip_row][pip_col] == self.color:
                                global_pip_row = board_row * 3 + pip_row
                                player_pips.append((global_pip_row, board_col * 3 + pip_col))

        if not player_pips:
            return 0

        # Find connected components and measure vertical span
        visited = set()
        best_vertical_span = 0

        for start_pip in player_pips:
            if start_pip in visited:
                continue

            component = board.flood_fill(start_pip, player_pips, visited.copy())
            visited.update(component)

            if component:
                min_row = min(pos[0] for pos in component)
                max_row = max(pos[0] for pos in component)
                vertical_span = max_row - min_row
                best_vertical_span = max(best_vertical_span, vertical_span)

        return best_vertical_span


class DefensiveTerritoryAI(AIPlayer):
    """Blue Strategy: Defensive territory control, methodical expansion"""
    def __init__(self, color, name):
        super().__init__(color, name)

    def evaluate_move(self, board, piece, row, col, current_pieces):
        """GEN 1: MAJOR CHANGES - Blue lost, switching to balanced aggression"""
        score = 0

        # Create temporary board state
        temp_board = copy.deepcopy(board)
        temp_board.place_piece(piece, row, col)

        # Priority 1: Win condition
        if temp_board.check_victory(self.color):
            score += 10000

        # GEN 26: HYPER-AGGRESSIVE EDGE DOMINANCE
        # Blue goes ALL-IN on edges and combat to beat Red at its own game!

        # Vertical progress (MASSIVE increase - must match Red!)
        if self.color == 'B':
            vertical_progress = 7 - row
            score += vertical_progress * 75  # HUGE jump from 65!
        else:
            vertical_progress = row
            score += vertical_progress * 75

        # EDGE WARFARE: Contest edges even harder!
        if col in [0, 5]:  # Extreme edges - Blue wants these MORE than Red!
            score += 70  # HIGHER than Red's 65!
        elif col in [1, 4]:  # Near edges
            score += 35  # Increased from 25
        else:  # Center (still de-prioritized)
            score += 5  # Even lower - edges only!

        # Row bonuses (still reduced, edges matter more)
        if row in [3, 4]:
            score += 15  # Further reduced
        elif row in [2, 5]:
            score += 8  # Further reduced

        # Vertical connection (even higher)
        connection_score = self.evaluate_vertical_connection(temp_board)
        score += connection_score * 45  # Big increase from 35

        # Territory control (minimal - not the focus)
        territory_score = self.evaluate_territory_control(temp_board)
        score += territory_score * 10  # Further reduced from 15

        # Combat bonus (MAXIMUM - must dominate edge battles!)
        all_pieces = temp_board.get_player_pieces('R') + temp_board.get_player_pieces('B')
        adjacent_pips = temp_board.check_pip_adjacency(piece, row, col, all_pieces)
        enemy_adjacent = sum(1 for adj in adjacent_pips if not adj['same_color'])
        if enemy_adjacent > 0:
            score += enemy_adjacent * 45  # Big increase from 38

        # Piece power (MAX for winning edge combat!)
        pip_count = len(piece.get_filled_positions())
        score += pip_count * 18  # Increased from 14

        return score

    def evaluate_vertical_connection(self, board):
        """GEN 1: Added - Calculate the longest vertical span of connected pips"""
        player_pips = []
        for board_row in range(board.height):
            for board_col in range(board.width):
                piece = board.grid[board_row][board_col]
                if piece and piece.player_color == self.color:
                    for pip_row in range(3):
                        for pip_col in range(3):
                            if piece.pips[pip_row][pip_col] == self.color:
                                global_pip_row = board_row * 3 + pip_row
                                player_pips.append((global_pip_row, board_col * 3 + pip_col))

        if not player_pips:
            return 0

        visited = set()
        best_vertical_span = 0

        for start_pip in player_pips:
            if start_pip in visited:
                continue

            component = board.flood_fill(start_pip, player_pips, visited.copy())
            visited.update(component)

            if component:
                min_row = min(pos[0] for pos in component)
                max_row = max(pos[0] for pos in component)
                vertical_span = max_row - min_row
                best_vertical_span = max(best_vertical_span, vertical_span)

        return best_vertical_span

    def evaluate_territory_control(self, board):
        """Measure how many rows we have strong presence in"""
        row_counts = [0] * board.height
        for board_row in range(board.height):
            for board_col in range(board.width):
                piece = board.grid[board_row][board_col]
                if piece and piece.player_color == self.color:
                    row_counts[board_row] += 1

        # Reward having multiple pieces in rows
        territory_score = sum(min(count * 2, 10) for count in row_counts)
        return territory_score

    def count_friendly_adjacent(self, board, row, col, current_pieces):
        """Count how many friendly pieces are adjacent"""
        adjacent_count = 0
        for piece_row, piece_col, _ in current_pieces:
            if abs(piece_row - row) + abs(piece_col - col) == 1:
                adjacent_count += 1
        return adjacent_count

    def evaluate_row_expansion(self, board):
        """Reward methodical row-by-row expansion"""
        rows_with_pieces = set()
        for board_row in range(board.height):
            for board_col in range(board.width):
                piece = board.grid[board_row][board_col]
                if piece and piece.player_color == self.color:
                    rows_with_pieces.add(board_row)

        if not rows_with_pieces:
            return 0

        # Reward contiguous row control
        if rows_with_pieces:
            min_row = min(rows_with_pieces)
            max_row = max(rows_with_pieces)
            row_span = max_row - min_row + 1
            contiguous_bonus = row_span if len(rows_with_pieces) == row_span else 0
            return len(rows_with_pieces) * 2 + contiguous_bonus * 3

        return 0

    def evaluate_column_diversity(self, board):
        """Reward spreading across multiple columns"""
        columns_with_pieces = set()
        for board_row in range(board.height):
            for board_col in range(board.width):
                piece = board.grid[board_row][board_col]
                if piece and piece.player_color == self.color:
                    columns_with_pieces.add(board_col)

        return len(columns_with_pieces)


class HumanPlayer(Player):
    """Human player with interactive input"""
    def __init__(self, color, name):
        super().__init__(color, name)

    def display_hand(self):
        """Display all pieces in hand with indices"""
        print(f"\n{self.name}'s Hand ({len(self.pieces)} pieces remaining):")
        print("=" * 60)
        for idx, piece in enumerate(self.pieces):
            pip_count = len(piece.get_filled_positions())
            print(f"  [{idx}] {pip_count} PIPs -")
            # Add indentation to piece display and blank line after
            for line in piece.display().strip().split('\n'):
                print(f"      {line}")
            print()  # Blank line between pieces
        print("=" * 60)

    def preview_piece(self, piece, rotation):
        """Show what a piece looks like after rotation"""
        rotated = piece.rotate(rotation)
        print(f"\nPiece after {rotation}° rotation:")
        print(rotated.display())

    def get_valid_positions(self, board, piece, rotation):
        """Get list of valid (row, col) positions for a piece/rotation"""
        current_pieces = board.get_player_pieces(self.color)
        rotated = piece.rotate(rotation)
        valid_positions = []

        for row in range(board.height):
            for col in range(board.width):
                if board.can_place_piece(rotated, row, col, current_pieces):
                    valid_positions.append((row, col))

        return valid_positions

    def show_legal_moves(self, board, valid_positions):
        """Display board with legal move positions marked"""
        if not valid_positions:
            print("\nNo legal moves available for this piece/rotation!")
            return

        print(f"\nLegal positions (row, col): {valid_positions}")
        print("\nBoard with legal positions marked as 'X':")

        # Create a visual representation
        grid = [[' ' for _ in range(board.width)] for _ in range(board.height)]
        for row, col in valid_positions:
            grid[row][col] = 'X'

        # Display grid
        print("  " + " ".join(str(c) for c in range(board.width)))
        for row in range(board.height):
            print(f"{row} " + " ".join(grid[row]))

    def choose_move(self, board):
        """Interactive move selection for human player"""
        if not self.has_pieces():
            return None, None, None, None, None

        print(f"\n{'='*60}")
        print(f"{self.name}'s Turn")
        print(f"{'='*60}")

        while True:
            # Show hand
            self.display_hand()

            # Get piece selection
            while True:
                piece_input = input(f"\nSelect piece (0-{len(self.pieces)-1}) or 'quit': ").strip().lower()
                if piece_input == 'quit':
                    print("Exiting game...")
                    exit(0)

                try:
                    piece_idx = int(piece_input)
                    if 0 <= piece_idx < len(self.pieces):
                        break
                    else:
                        print(f"Invalid piece index. Must be 0-{len(self.pieces)-1}")
                except ValueError:
                    print("Invalid input. Enter a number or 'quit'")

            piece = self.pieces[piece_idx]
            pip_count = len(piece.get_filled_positions())
            print(f"\nSelected piece with {pip_count} PIPs")
            print(piece.display())

            # Get rotation
            while True:
                rotation_input = input("\nRotation (0, 90, 180, 270): ").strip()
                try:
                    rotation = int(rotation_input)
                    if rotation in [0, 90, 180, 270]:
                        break
                    else:
                        print("Invalid rotation. Must be 0, 90, 180, or 270")
                except ValueError:
                    print("Invalid input. Enter a number")

            # Show preview
            self.preview_piece(piece, rotation)

            # Get valid positions
            valid_positions = self.get_valid_positions(board, piece, rotation)
            self.show_legal_moves(board, valid_positions)

            if not valid_positions:
                print("\nNo legal moves for this piece/rotation. Try again.")
                continue

            # Get position
            while True:
                pos_input = input("\nEnter position as 'row col' (e.g., '3 2') or 'back': ").strip().lower()

                if pos_input == 'back':
                    break  # Go back to piece selection

                try:
                    parts = pos_input.split()
                    if len(parts) != 2:
                        print("Invalid format. Use 'row col' (e.g., '3 2')")
                        continue

                    row, col = int(parts[0]), int(parts[1])

                    if not (0 <= row < board.height and 0 <= col < board.width):
                        print(f"Position out of bounds. Row: 0-{board.height-1}, Col: 0-{board.width-1}")
                        continue

                    if (row, col) not in valid_positions:
                        print("Illegal move! Choose from the legal positions shown above.")
                        continue

                    # Valid move found!
                    rotated_piece = piece.rotate(rotation)
                    return rotated_piece, row, col, rotation, piece_idx

                except ValueError:
                    print("Invalid input. Use 'row col' format with numbers")

            # If we get here, user typed 'back'
            continue


class RandomPlayer(Player):
    """Random player that makes random legal moves"""
    def __init__(self, color, name):
        super().__init__(color, name)

    def choose_move(self, board):
        """Randomly select a legal move"""
        if not self.has_pieces():
            return None, None, None, None, None

        # Try pieces in random order
        piece_indices = list(range(len(self.pieces)))
        random.shuffle(piece_indices)

        for piece_idx in piece_indices:
            piece = self.pieces[piece_idx]

            # Try rotations in random order
            rotations = [0, 90, 180, 270]
            random.shuffle(rotations)

            for rotation in rotations:
                rotated_piece = piece.rotate(rotation)
                current_pieces = board.get_player_pieces(self.color)

                # Get all valid positions for this piece/rotation
                valid_positions = []
                for row in range(board.height):
                    for col in range(board.width):
                        if board.can_place_piece(rotated_piece, row, col, current_pieces):
                            valid_positions.append((row, col))

                # If we found valid positions, pick one randomly
                if valid_positions:
                    row, col = random.choice(valid_positions)
                    print(f"{self.name} randomly places piece at ({row}, {col}) with {rotation}° rotation")
                    return rotated_piece, row, col, rotation, piece_idx

        # No legal moves found
        return None, None, None, None, None


class BorderlineGPT:
    def __init__(self, red_strategy='default', blue_strategy='default', blue_human=False, blue_random=False):
        self.board = GameBoard()

        # Select strategy for Red
        if red_strategy == 'aggressive':
            self.red_player = AggressiveConnectorAI('R', 'Red AI (Aggressive)')
        else:
            self.red_player = AIPlayer('R', 'Red AI')

        # Select strategy for Blue (can be human, random, or AI)
        if blue_human:
            self.blue_player = HumanPlayer('B', 'Human Player (Blue)')
        elif blue_random:
            self.blue_player = RandomPlayer('B', 'Random Player (Blue)')
        elif blue_strategy == 'defensive':
            self.blue_player = DefensiveTerritoryAI('B', 'Blue AI (Defensive)')
        else:
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
        result = self.current_player.choose_move(self.board)

        if result[0] is None:
            print(f"{self.current_player.name} has no valid moves - skipping turn")
            self.switch_player()
            self.turn_count += 1
            return

        piece, row, col, rotation, piece_idx = result

        # Remove the original piece from player's hand using the index
        original_piece = self.current_player.pieces.pop(piece_idx)

        # Display rotation info if piece was rotated
        if rotation != 0:
            print(f"{self.current_player.name} rotates piece {rotation}° clockwise")
        
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
        combat = self.board.resolve_combat(piece, row, col, adjacent_pips)
        if combat:
            # Build list of all pieces involved in combat for highlighting
            highlight_positions = [combat['attacker_pos']]
            for defender in combat['defenders']:
                highlight_positions.append((defender['row'], defender['col']))

            # Display combat information
            print(f"\nCOMBAT!")
            print(f"  Attacker ({combat['attacker_color']}): Roll={combat['attacker_roll']} + Power={combat['attacker_power']} = {combat['attacker_total']}")
            print(f"  Defender ({combat['defender_color']}): Roll={combat['defender_roll']} + Power={combat['defender_power']} = {combat['defender_total']}")
            if len(combat['defenders']) > 1:
                print(f"  Defending pieces: {len(combat['defenders'])} (combined power: {combat['defender_power']})")
            print(self.board.display(highlight_positions=highlight_positions))

            if combat['winner'] != self.current_player.color:
                # Attacker loses - remove piece from board, convert it, and give to defender
                attacking_piece = self.board.remove_piece(row, col)
                if attacking_piece:
                    attacking_piece.convert_to_color(combat['defender_color'])
                    # Give the converted piece to the winning player
                    winner_player = self.red_player if combat['defender_color'] == 'R' else self.blue_player
                    winner_player.add_piece_back(attacking_piece)
                    print(f"{self.current_player.name} loses combat! Piece is captured and converted to {combat['defender_color']}!")
                    # Clear highlight since piece was removed
                    self.last_placed_pos = None
            else:
                # Defender(s) lose - remove all defending pieces, convert them, and give to attacker
                for defender in combat['defenders']:
                    defending_piece = self.board.remove_piece(defender['row'], defender['col'])
                    if defending_piece:
                        defending_piece.convert_to_color(combat['attacker_color'])
                        self.current_player.add_piece_back(defending_piece)

                if len(combat['defenders']) > 1:
                    print(f"All {len(combat['defenders'])} defending pieces are captured and converted to {combat['attacker_color']}!")
                else:
                    print(f"Defending piece is captured and converted to {combat['attacker_color']}!")

                # POST-COMBAT: Check if any remaining defending pieces became disconnected
                # (only when defender loses)
                defender_color = combat['defender_color']
                disconnected = self.board.remove_disconnected_pieces(defender_color)
                if disconnected:
                    print(f"\nPOST-COMBAT CONNECTIVITY CHECK:")
                    print(f"  {len(disconnected)} {defender_color} piece(s) disconnected from home row - returned to hand")
                    for piece_info in disconnected:
                        print(f"    Disconnected piece at ({piece_info['row']}, {piece_info['col']})")
                    defender_player = self.red_player if defender_color == 'R' else self.blue_player
                    for piece_info in disconnected:
                        defender_player.add_piece_back(piece_info['piece'])
                else:
                    print(f"\nPOST-COMBAT CONNECTIVITY CHECK:")
                    print(f"  No defending pieces are disconnected from the home row")

        # Check victory
        victory = self.board.check_victory(self.current_player.color, debug=True)
        if victory:
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
    import argparse

    parser = argparse.ArgumentParser(description='Borderline - A strategic board game')
    parser.add_argument('--human_vs_ai', action='store_true',
                        help='Play as Human (Blue) against AI (Red)')
    parser.add_argument('--blue_random', action='store_true',
                        help='Blue makes random legal moves, Red uses AI')
    args = parser.parse_args()

    if args.human_vs_ai:
        print("=" * 60)
        print("BORDERLINE: Human vs AI Mode")
        print("You are playing as Blue against Red AI")
        print("=" * 60)
        game = BorderlineGPT(red_strategy='aggressive', blue_human=True)
    elif args.blue_random:
        print("=" * 60)
        print("BORDERLINE: AI vs Random Mode")
        print("Red AI (Aggressive) vs Random Blue")
        print("=" * 60)
        game = BorderlineGPT(red_strategy='aggressive', blue_random=True)
    else:
        game = BorderlineGPT()

    game.play_game()