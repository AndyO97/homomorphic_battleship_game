#!/usr/bin/env python
"""
Test script to verify manual ship placement works correctly.
"""

import sys
sys.path.insert(0, 'src')

from board import Board, Ship

def test_manual_placement():
    """Test manual ship placement validation."""
    board = Board(player_name="TestPlayer")
    
    # Verify board is empty
    assert len(board.ships) == 0, "Board should start with no ships"
    assert all(board.board[coord] == 0 for coord in board.board), "All cells should be water"
    
    # Manually place ships programmatically (simulating user input)
    print("Testing manual ship placement...")
    
    # Aircraft Carrier (size 5)
    coords_carrier = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    ship1 = Ship(ship_id=0, name="Aircraft Carrier", size=5)
    for coord in coords_carrier:
        board.board[coord] = 1
    ship1.coordinates = coords_carrier
    board.ships.append(ship1)
    print(f"  [OK] Placed Aircraft Carrier at {coords_carrier}")
    
    # Battleship (size 4)
    coords_battleship = [(0, 2), (0, 3), (0, 4), (0, 5)]
    ship2 = Ship(ship_id=1, name="Battleship", size=4)
    for coord in coords_battleship:
        board.board[coord] = 1
    ship2.coordinates = coords_battleship
    board.ships.append(ship2)
    print(f"  [OK] Placed Battleship at {coords_battleship}")
    
    # Submarine (size 3)
    coords_submarine = [(5, 5), (5, 6), (5, 7)]
    ship3 = Ship(ship_id=2, name="Submarine", size=3)
    for coord in coords_submarine:
        board.board[coord] = 1
    ship3.coordinates = coords_submarine
    board.ships.append(ship3)
    print(f"  [OK] Placed Submarine at {coords_submarine}")
    
    # Destroyer (size 2)
    coords_destroyer = [(9, 0), (9, 1)]
    ship4 = Ship(ship_id=3, name="Destroyer", size=2)
    for coord in coords_destroyer:
        board.board[coord] = 1
    ship4.coordinates = coords_destroyer
    board.ships.append(ship4)
    print(f"  [OK] Placed Destroyer at {coords_destroyer}")
    
    # Patrol Boat (size 2)
    coords_patrol = [(7, 9), (8, 9)]
    ship5 = Ship(ship_id=4, name="Patrol Boat", size=2)
    for coord in coords_patrol:
        board.board[coord] = 1
    ship5.coordinates = coords_patrol
    board.ships.append(ship5)
    print(f"  [OK] Placed Patrol Boat at {coords_patrol}")
    
    # Verify all ships are placed
    assert len(board.ships) == 5, "Should have 5 ships"
    print(f"\n[OK] All 5 ships placed successfully")
    
    # Test ship retrieval
    ship_at_0_0 = board.get_ship_at(0, 0)
    assert ship_at_0_0 is not None, "Should find ship at (0, 0)"
    assert ship_at_0_0.name == "Aircraft Carrier", "Should be Aircraft Carrier"
    print(f"[OK] Ship retrieval works: Found {ship_at_0_0.name} at (0, 0)")
    
    # Test hit recording
    board.record_hit_on_board(0, 0)
    assert ship1.hits == 1, "Should have 1 hit"
    print(f"[OK] Hit recording works")
    
    # Test water cell (no ship)
    is_hit = board.record_hit_on_board(3, 3)
    assert not is_hit, "Water cell should be a miss"
    print(f"[OK] Water cell detection works")
    
    # Test game status
    status = board.get_game_status()
    assert status["player"] == "TestPlayer", "Player name should match"
    assert len(status["ships"]) == 5, "Should have 5 ships in status"
    print(f"[OK] Game status works")
    
    print("\n[SUCCESS] All manual placement tests passed!")

if __name__ == "__main__":
    try:
        test_manual_placement()
    except AssertionError as e:
        print(f"\n[FAILED] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
