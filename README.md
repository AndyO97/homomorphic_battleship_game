# Homomorphic Encryption Battleship

A fully interactive two-player Battleship game with **Paillier homomorphic encryption**, where ship positions remain encrypted throughout the entire game.

## Overview

This project implements a secure variant of the classic Battleship game using cryptographic techniques. Unlike traditional Battleship, neither player ever learns the opponent's board layout, even when making guesses. All ship locations are encrypted using Paillier homomorphic encryption, and hit/miss detection is performed mathematically without decrypting the boards.

### Key Features

- **Two Encrypted Boards**: Each player maintains a private 10×10 board with 5 ships
- **Fully Turn-Based Gameplay**: Players alternate guesses with complete game state management
- **Homomorphic Hit Checking**: Hit/miss determination happens without revealing ship positions
- **Secure Communication**: Simulated server coordinates between player instances
- **Distributed Architecture**: Player instances simulate separate computers communicating through a game server

## Installation

### Prerequisites

- Python 3.10 or higher
- `uv` package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/AndyO97/homomorphic_battleship_game.git
cd homomorphic-battleship
```

2. Install dependencies using `uv`:
```bash
uv sync
```

Or install manually:
```bash
uv pip install phe
uv pip install pytest pytest-cov  # For testing
```

## How to Run

### Play the Game

```bash
uv run python -m src.main
```

Or, if you have activated the virtual environment:
```bash
python -m src.main
```

The game will:
1. Generate Paillier keypairs for both players
2. Create and encrypt their boards
3. Prompt players for guesses in turn
4. Display results without revealing the opponent's board
5. End when all ships of one player are sunk

### Example Gameplay

```
Player Alice, enter your guess (format: x y): 5 3
[Server Result] Alice HITS Bob's board at (5, 3)!

Player Bob, enter your guess (format: x y): 2 7
[Server Result] Bob's guess at (2, 7) - MISS
```

### Ship Placement Options

During setup, each player can choose how to place their ships:

1. **Random Placement** - Ships are automatically placed randomly on the board (option 1)
2. **Manual Placement** - You specify the exact coordinates for each ship (option 2)

When selecting manual placement, you'll be prompted to enter coordinates for each cell of your 5 ships in the format `x y` (e.g., `0 0`). The system validates:
- Coordinates are within bounds (0-9)
- No overlapping ships
- No duplicate coordinates within a ship
- Proper error messages for invalid inputs

### Run Tests

```bash
uv run pytest tests/
```

Run specific test module:
```bash
uv run pytest tests/test_board.py -v
uv run pytest tests/test_crypto.py -v
uv run pytest tests/test_game.py -v
```

Run with coverage:
```bash
uv run pytest tests/ --cov=src --cov-report=html
```

## Project Structure

```
.
├── src/
│   ├── __init__.py           # Package initialization
│   ├── main.py               # Main game loop and CLI
│   ├── board.py              # Board management and ship placement
│   ├── crypto.py             # Paillier encryption operations
│   ├── game_logic.py         # Game state and turn management
│   └── server.py             # Server simulation and player instances
├── tests/
│   ├── test_board.py         # Board tests
│   ├── test_crypto.py        # Cryptography tests
│   └── test_game.py          # Game logic tests
├── pyproject.toml            # Project configuration
├── README.md                 # This file
├── PRD.md                    # Product Requirements Document
└── LICENSE
```

## Architecture

### Game Flow

```
┌─────────────────────────────────────────────────────┐
│ Game Initialization                                 │
│ - Generate Paillier keypairs for both players       │
│ - Create and place ships on boards                  │
│ - Encrypt boards using public keys                  │
└──────────────┬──────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────┐
│ Game Server Initialization                          │
│ - Create GameServer instance                        │
│ - Create PlayerInstance for Alice and Bob           │
│ - Both players connected to server                  │
└──────────────┬──────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────┐
│ Turn-Based Gameplay Loop                            │
│ 1. Current player enters guess (x, y)              │
│ 2. Server validates coordinate                      │
│ 3. Homomorphic hit check performed:                │
│    - (E(cell) - 1) * random_blinding                │
│ 4. Opponent decrypts result                         │
│ 5. Result revealed (Hit/Miss/Sunk)                 │
│ 6. Check for victory condition                      │
│ 7. Switch to other player's turn                    │
└──────────────┬──────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────┐
│ Game Over                                           │
│ - Display winner and statistics                     │
└─────────────────────────────────────────────────────┘
```

### Homomorphic Hit Checking

The core security mechanism:

```python
encrypted_difference = encrypted_cell - guess
blinding_factor = random.randint(1, 999999)
encrypted_result = encrypted_difference * blinding_factor

# Opponent decrypts:
decrypted = private_key.decrypt(encrypted_result)

if decrypted == 0:
    print("HIT!")
else:
    print("MISS")  # Decrypted value is random noise
```

**Security Properties:**
- If cell=1 (ship) and guess=1: `(1-1) * random = 0` → HIT
- If cell=0 (water) and guess=1: `(0-1) * random = random junk` → MISS
- Random blinding prevents reverse-engineering missed guesses
- Neither player ever sees the opponent's plaintext board

## Module Details

### `crypto.py`
Handles all Paillier cryptographic operations:
- `generate_keypair()` - Generate public/private keypair
- `encrypt_value()` - Encrypt a single value
- `decrypt_value()` - Decrypt an encrypted value
- `perform_homomorphic_hit_check()` - Compute hit/miss homomorphically
- `check_hit()` - Determine if result is a hit

### `board.py`
Manages board state and ship placement:
- `Board` class - Represents a player's 10×10 board
- `Ship` class - Represents individual ships (size 2-5)
- Ship placement with validation (no overlap, fits on board)
- Hit tracking and sinking detection

### `game_logic.py`
Controls game flow and rules:
- `GameLogic` class - Manages game state and turns
- `GameState` dataclass - Tracks turn history and victory conditions
- Turn management and validation
- Ship sinking and victory detection

### `server.py`
Simulates server and player instances:
- `GameServer` class - Coordinates communication between players
- `PlayerInstance` class - Represents a single player
- Guess processing and result distribution
- Game state queries

### `main.py`
Interactive game loop:
- Setup phase (key generation, board creation)
- Main game loop with CLI interface
- Result display and statistics
- Error handling

## Testing

The project includes comprehensive unit tests:

### `test_board.py`
- Board initialization and dimensions
- Ship placement validation
- Hit recording and ship sinking
- Boundary checking

### `test_crypto.py`
- Keypair generation
- Encryption/decryption correctness
- Homomorphic operations
- Hit detection logic

### `test_game.py`
- Game initialization
- Turn management
- Hit/miss detection
- Victory conditions
- Game history tracking

### `test_manual_placement.py`
- Standalone test script (not part of unit tests)
- Tests the manual ship placement feature validation
- Verifies coordinate bounds checking, overlap detection, and duplicate prevention
- Run with: `uv run python tests/test_manual_placement.py`
- Useful for verifying the manual placement feature works correctly before playing the game

## Security Considerations

### What is Encrypted
- Every cell on each player's board is encrypted
- Encrypted boards are transmitted to the game server
- Hit checking occurs on encrypted data

### What is Revealed
- Hit or Miss results (but never the ship location)
- Ship names when sunk (not position)
- Game statistics (total guesses, etc.)
- Never the plaintext board

### Cryptographic Assumptions
- Paillier encryption is semantically secure
- RSA modulus is sufficiently large (2048 bits minimum)
- Random blinding values are truly random
- Each player keeps their private key secret

## Example Game Session

```
$ uv run python -m src.main

============================================================
  HOMOMORPHIC ENCRYPTION BATTLESHIP - Two Player Secure Game
============================================================

Setting up the game...
============================================================

1. Generating keypairs for both players...
   [OK] Alice's keypair generated
   [OK] Bob's keypair generated

2. Creating boards and placing ships...
   [OK] Alice's board created with 5 ships
   [OK] Bob's board created with 5 ships

3. Encrypting boards...
   [OK] Alice's board encrypted (100 cells)
   [OK] Bob's board encrypted (100 cells)

4. Initializing game logic...
   [OK] Game logic initialized

5. Creating game server...
   [OK] Alice will go first.

6. Initializing player instances...
   [OK] Alice player instance created
   [OK] Bob player instance created

============================================================
Game ready! Let the battle begin!

--- Turn 1 ---
Current Turn: Alice
...
[Game continues with interactive play]
```

## Development

### Adding New Features

1. **Custom Ship Sizes**: Modify `SHIP_SIZES` in `board.py`
2. **Larger Boards**: Change `BOARD_SIZE` in `board.py`
3. **Different Encryption**: Substitute Paillier with other schemes (supports additive homomorphism)
4. **Network Support**: Replace `GameServer` with actual network calls

### Running Locally

```bash
# Install in development mode with test dependencies
uv sync --all-extras

# Run tests with coverage
uv run pytest tests/ --cov=src --cov-report=term-missing
```

## License

This project is provided as part of the Applied Cryptography course.

## References

### Paillier Cryptosystem
- [Paillier PHE Library Documentation](https://python-phe.readthedocs.io/)
- P. Paillier: "Public-Key Cryptosystems Based on Composite Degree Residuosity Classes"

### Homomorphic Encryption
- Additive homomorphic property: `E(m1) + E(m2) = E(m1 + m2)`
- Scalar multiplication: `k * E(m) = E(k * m)`

## Troubleshooting

### Import Errors
If you see "Import 'phe' could not be resolved", run:
```bash
uv pip install phe
```

### Test Failures
For slow machines, tests may timeout. Run with longer timeout:
```bash
pytest tests/ --timeout=60
```

### KeyError in Game Logic
Ensure both players' boards are properly initialized with `place_ships()` before starting the game.

## FAQ

**Q: Can a player cheat by revealing their board?**
A: Not without the private key. The board is encrypted on their local machine.

**Q: How does blinding prevent attacks?**
A: Random blinding masks non-zero values as noise. Attackers cannot distinguish between different miss values.

**Q: Why is this better than traditional Battleship?**
A: In traditional Battleship, a player must trust the opponent with their board. Here, the board never needs to be revealed - the opponent can verify hits without seeing ship locations.

**Q: Can this scale to larger boards?**
A: Yes, but Paillier encryption becomes slower with larger boards. For very large boards, consider more efficient protocols.

---

**Happy playing! 🚢**
