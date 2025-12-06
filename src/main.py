"""
Main game loop for Homomorphic Battleship.

This module brings together all components to run the game with
two players communicating through a simulated server.
"""

import sys
from src.crypto import generate_keypair
from src.board import Board
from src.game_logic import GameLogic
from src.server import GameServer, PlayerInstance


def print_header() -> None:
    """Print the game header."""
    print("=" * 60)
    print("  HOMOMORPHIC ENCRYPTION BATTLESHIP - Two Player Secure Game")
    print("=" * 60)
    print()


def get_placement_choice(player_name: str) -> bool:
    """
    Ask a player if they want manual or random ship placement.
    
    Args:
        player_name: Name of the player
        
    Returns:
        True for manual placement, False for random placement
    """
    while True:
        choice = input(f"\n{player_name}, how do you want to place your ships?\n"
                      "[1] Random placement (automatic)\n"
                      "[2] Manual placement (you choose coordinates)\n"
                      "Enter choice (1 or 2): ").strip()
        
        if choice == "1":
            return False
        elif choice == "2":
            return True
        else:
            print("Invalid choice. Please enter 1 or 2.")


def place_player_board(player_name: str, board: Board) -> None:
    """
    Place ships on a player's board based on their preference.
    
    Args:
        player_name: Name of the player
        board: Board object to place ships on
    """
    manual = get_placement_choice(player_name)
    
    if manual:
        board.place_ships_manual()
    else:
        board.place_ships()
        print(f"   [OK] {player_name}'s board created with 5 ships (random placement)")


def print_game_status(server: GameServer) -> None:
    """Print the current game status."""
    status = server.get_game_state()
    print(f"\n--- Turn {status['total_turns']} ---")
    print(f"Current Turn: {server.get_whose_turn()}")
    print()
    
    # Print Alice's ship status
    alice_status = status["alice_status"]
    print(f"{alice_status['player']}'s Ships:")
    for ship in alice_status["ships"]:
        sunk_str = "[SUNK]" if ship["sunk"] else ""
        print(f"  - {ship['name']:20s}: {ship['hits']:2d}/{ship['size']:2d} hits {sunk_str}")
    
    print()
    
    # Print Bob's ship status
    bob_status = status["bob_status"]
    print(f"{bob_status['player']}'s Ships:")
    for ship in bob_status["ships"]:
        sunk_str = "[SUNK]" if ship["sunk"] else ""
        print(f"  - {ship['name']:20s}: {ship['hits']:2d}/{ship['size']:2d} hits {sunk_str}")
    
    print()


def get_player_guess(player_name: str) -> tuple:
    """
    Get a guess from a player.
    
    Args:
        player_name: Name of the player
        
    Returns:
        Tuple of (x, y) coordinates
    """
    while True:
        try:
            guess_input = input(f"\n{player_name}, enter your guess (format: x y): ")
            parts = guess_input.strip().split()
            if len(parts) != 2:
                print("Invalid format. Please enter two numbers separated by a space.")
                continue
            
            x, y = int(parts[0]), int(parts[1])
            
            if not (0 <= x < 10 and 0 <= y < 10):
                print("Coordinates out of bounds. Please use 0-9.")
                continue
            
            return x, y
        
        except ValueError:
            print("Invalid input. Please enter two integers (0-9).")


def process_guess_result(result: dict, player_name: str, opponent_name: str) -> None:
    """
    Process and display the result of a guess.
    
    Args:
        result: Result dictionary from the server
        player_name: Name of the guessing player
        opponent_name: Name of the defending player
    """
    if result["status"] == "error":
        print(f"Error: {result['message']}")
        return
    
    x, y = result["coordinate"]
    is_duplicate = result.get("is_duplicate", False)
    
    if is_duplicate:
        print(f"\n[Server Result] Duplicate guess at ({x}, {y}) - Already attacked this location!")
        print(f"  No damage dealt. Try a different coordinate.")
        return
    
    if result["is_hit"]:
        print(f"\n[Server Result] {player_name} HITS {opponent_name}'s board at ({x}, {y})!")
        
        if result["ship_sunk"]:
            print(f"*** {player_name} sunk {opponent_name}'s {result['ship_sunk']}! ***")
    else:
        print(f"\n[Server Result] {player_name}'s guess at ({x}, {y}) - MISS")


def play_game() -> None:
    """Main game loop."""
    print_header()
    
    print("Setting up the game...")
    print("=" * 60)
    
    # SETUP PHASE
    print("\n1. Generating keypairs for both players...")
    alice_public_key, alice_private_key = generate_keypair()
    bob_public_key, bob_private_key = generate_keypair()
    print("   [OK] Alice's keypair generated")
    print("   [OK] Bob's keypair generated")
    
    print("\n2. Creating boards and placing ships...")
    alice_board = Board(player_name="Alice")
    place_player_board("Alice", alice_board)
    
    bob_board = Board(player_name="Bob")
    place_player_board("Bob", bob_board)
    
    print("\n3. Encrypting boards...")
    alice_encrypted = alice_board.encrypt_board(alice_public_key)
    print(f"   [OK] Alice's board encrypted ({len(alice_encrypted)} cells)")
    
    bob_encrypted = bob_board.encrypt_board(bob_public_key)
    print(f"   [OK] Bob's board encrypted ({len(bob_encrypted)} cells)")
    
    print("\n4. Initializing game logic...")
    game_logic = GameLogic(
        alice_board, bob_board,
        alice_public_key, bob_public_key,
        alice_private_key, bob_private_key
    )
    print("   [OK] Game logic initialized")
    
    print("\n5. Creating game server...")
    server = GameServer(game_logic)
    start_info = server.start_game()
    print(f"   [OK] {start_info['message']}")
    
    print("\n6. Initializing player instances...")
    alice_player = PlayerInstance("Alice", alice_board, alice_public_key, alice_private_key, server)
    bob_player = PlayerInstance("Bob", bob_board, bob_public_key, bob_private_key, server)
    print("   [OK] Alice player instance created")
    print("   [OK] Bob player instance created")
    
    print("\n" + "=" * 60)
    print("Game ready! Let the battle begin!\n")
    
    # GAME LOOP
    turn_count = 0
    max_turns = 200  # Safety limit
    
    while not server.is_game_over() and turn_count < max_turns:
        print_game_status(server)
        
        current_player_name = server.get_whose_turn()
        opponent_name = "Bob" if current_player_name == "Alice" else "Alice"
        current_player = alice_player if current_player_name == "Alice" else bob_player
        
        # Get guess from current player
        x, y = get_player_guess(current_player_name)
        
        # Process through server
        result = current_player.make_guess(x, y)
        process_guess_result(result, current_player_name, opponent_name)
        
        # Check for game over
        if result.get("game_over"):
            winner = result.get("winner")
            print(f"\n{'=' * 60}")
            print(f"GAME OVER! {winner} wins after {server.get_game_state()['total_turns']} turns!")
            print(f"{'=' * 60}\n")
            break
        
        turn_count += 1
    
    if turn_count >= max_turns:
        print(f"Game ended due to turn limit ({max_turns} turns reached)")
    
    # Print final statistics
    print("\nFinal Game Statistics:")
    print("=" * 60)
    history = server.get_game_history()
    print(f"Total turns: {len(history)}")
    
    alice_hits = sum(1 for turn in history if turn['player'] == 'Alice' and turn['is_hit'])
    bob_hits = sum(1 for turn in history if turn['player'] == 'Bob' and turn['is_hit'])
    
    print(f"Alice's hits: {alice_hits}")
    print(f"Bob's hits: {bob_hits}")
    print()


def debug_show_boards(alice_board: Board, bob_board: Board) -> None:
    """Show plaintext boards (debug only - don't do this in production!)"""
    print("\n" + "=" * 60)
    print("DEBUG: Plaintext Board States (WOULD NEVER HAPPEN IN REAL GAME)")
    print("=" * 60)
    alice_board.print_board_state()
    bob_board.print_board_state()


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
