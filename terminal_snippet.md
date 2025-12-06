============================================================                                                                                                        
  HOMOMORPHIC ENCRYPTION BATTLESHIP - Two Player Secure Game
============================================================

Setting up the game...
============================================================

1. Generating keypairs for both players...
   [OK] Alice's keypair generated
   [OK] Bob's keypair generated

2. Creating boards and placing ships...

Alice, how do you want to place your ships?
[1] Random placement (automatic)
[2] Manual placement (you choose coordinates)
Enter choice (1 or 2): 2

Alice's Manual Ship Placement
============================================================
Enter coordinates for each cell of your ships (format: x y)
Ships must be placed in a straight line (horizontal or vertical)
Board coordinates range from 0-9 for both x and y


Placing Aircraft Carrier (Size: 5)
Please enter 5 coordinates:
  Coordinate 1/5: 1 1
  [OK] 1/5 cells placed at (1, 1)
  Coordinate 2/5: 1 2
  [OK] 2/5 cells placed at (1, 2)
  Coordinate 3/5: 1 3
  [OK] 3/5 cells placed at (1, 3)
  Coordinate 4/5: 1 4
  [OK] 4/5 cells placed at (1, 4)
  Coordinate 5/5: 1 5
  [OK] 5/5 cells placed at (1, 5)
  [OK] Aircraft Carrier placed successfully at: [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]

Placing Battleship (Size: 4)
Please enter 4 coordinates:
  Coordinate 1/4: 2 1
  [OK] 1/4 cells placed at (2, 1)
  Coordinate 2/4: 3 1
  [OK] 2/4 cells placed at (3, 1)
  Coordinate 3/4: 4 1
  [OK] 3/4 cells placed at (4, 1)
  Coordinate 4/4: 5 1
  [OK] 4/4 cells placed at (5, 1)
  [OK] Battleship placed successfully at: [(2, 1), (3, 1), (4, 1), (5, 1)]

Placing Submarine (Size: 3)
Please enter 3 coordinates:
  Coordinate 1/3: 2 2
  [OK] 1/3 cells placed at (2, 2)
  Coordinate 2/3: 3 2
  [OK] 2/3 cells placed at (3, 2)
  Coordinate 3/3: 4 2
  [OK] 3/3 cells placed at (4, 2)
  [OK] Submarine placed successfully at: [(2, 2), (3, 2), (4, 2)]

Placing Destroyer (Size: 2)
Please enter 2 coordinates:
  Coordinate 1/2: 2 3
  [OK] 1/2 cells placed at (2, 3)
  Coordinate 2/2: 2 4
  [OK] 2/2 cells placed at (2, 4)
  [OK] Destroyer placed successfully at: [(2, 3), (2, 4)]

Placing Patrol Boat (Size: 2)
Please enter 2 coordinates:
  Coordinate 1/2: 3 3
  [OK] 1/2 cells placed at (3, 3)
  Coordinate 2/2: 3 4
  [OK] 2/2 cells placed at (3, 4)
  [OK] Patrol Boat placed successfully at: [(3, 3), (3, 4)]

Alice's board setup complete!

Bob, how do you want to place your ships?
[1] Random placement (automatic)
[2] Manual placement (you choose coordinates)
Enter choice (1 or 2): 1
   [OK] Bob's board created with 5 ships (random placement)

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


--- Turn 0 ---
Current Turn: Alice

Alice's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Alice, enter your guess (format: x y): 1 1

[Server Result] Alice's guess at (1, 1) - MISS

--- Turn 1 ---
Current Turn: Bob

Alice's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Bob, enter your guess (format: x y): 1 1

[Server Result] Bob HITS Alice's board at (1, 1)!

--- Turn 2 ---
Current Turn: Alice

Alice's Ships:
  - Aircraft Carrier    :  1/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Alice, enter your guess (format: x y): 1 1

[Server Result] Duplicate guess at (1, 1) - Already attacked this location!
  No damage dealt. Try a different coordinate.

--- Turn 3 ---
Current Turn: Bob

Alice's Ships:
  - Aircraft Carrier    :  1/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits 
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Bob, enter your guess (format: x y): 2 1

[Server Result] Bob HITS Alice's board at (2, 1)!

--- Turn 4 ---
Current Turn: Alice

Alice's Ships:
  - Aircraft Carrier    :  1/ 5 hits
  - Battleship          :  1/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Alice, enter your guess (format: x y): 1 2

[Server Result] Alice's guess at (1, 2) - MISS

--- Turn 5 ---
Current Turn: Bob

Alice's Ships:
  - Aircraft Carrier    :  1/ 5 hits
  - Battleship          :  1/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Bob, enter your guess (format: x y): 1 2

[Server Result] Bob HITS Alice's board at (1, 2)!

--- Turn 6 ---
Current Turn: Alice

Alice's Ships:
  - Aircraft Carrier    :  2/ 5 hits
  - Battleship          :  1/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Alice, enter your guess (format: x y): 1 3

[Server Result] Alice's guess at (1, 3) - MISS

--- Turn 7 ---
Current Turn: Bob

Alice's Ships:
  - Aircraft Carrier    :  2/ 5 hits
  - Battleship          :  1/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Bob, enter your guess (format: x y): 1 3

[Server Result] Bob HITS Alice's board at (1, 3)!

--- Turn 8 ---
Current Turn: Alice

Alice's Ships:
  - Aircraft Carrier    :  3/ 5 hits
  - Battleship          :  1/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Alice, enter your guess (format: x y): 1 4

[Server Result] Alice's guess at (1, 4) - MISS

--- Turn 9 ---
Current Turn: Bob

Alice's Ships:
  - Aircraft Carrier    :  3/ 5 hits
  - Battleship          :  1/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Bob, enter your guess (format: x y): 1 4

[Server Result] Bob HITS Alice's board at (1, 4)!

--- Turn 10 ---
Current Turn: Alice

Alice's Ships:
  - Aircraft Carrier    :  4/ 5 hits
  - Battleship          :  1/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Alice, enter your guess (format: x y): 1 5

[Server Result] Alice's guess at (1, 5) - MISS

--- Turn 11 ---
Current Turn: Bob

Alice's Ships:
  - Aircraft Carrier    :  4/ 5 hits
  - Battleship          :  1/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Bob, enter your guess (format: x y): 1 5

[Server Result] Bob HITS Alice's board at (1, 5)!
*** Bob sunk Alice's Aircraft Carrier! ***

--- Turn 12 ---
Current Turn: Alice

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  1/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Alice, enter your guess (format: x y): 9 9

[Server Result] Alice's guess at (9, 9) - MISS

--- Turn 13 ---
Current Turn: Bob

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  1/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Bob, enter your guess (format: x y): 1 5

[Server Result] Duplicate guess at (1, 5) - Already attacked this location!
  No damage dealt. Try a different coordinate.

--- Turn 14 ---
Current Turn: Alice

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  1/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits 
  - Patrol Boat         :  0/ 2 hits


Alice, enter your guess (format: x y): 2 1

[Server Result] Alice's guess at (2, 1) - MISS

--- Turn 15 ---
Current Turn: Bob

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  1/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Bob, enter your guess (format: x y): 2 1

[Server Result] Duplicate guess at (2, 1) - Already attacked this location!
  No damage dealt. Try a different coordinate.

--- Turn 16 ---
Current Turn: Alice

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  1/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Alice, enter your guess (format: x y): 3 1

[Server Result] Alice's guess at (3, 1) - MISS

--- Turn 17 ---
Current Turn: Bob

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  1/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Bob, enter your guess (format: x y): 3 1

[Server Result] Bob HITS Alice's board at (3, 1)!

--- Turn 18 ---
Current Turn: Alice

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  2/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Alice, enter your guess (format: x y): 4 1

[Server Result] Alice's guess at (4, 1) - MISS

--- Turn 19 ---
Current Turn: Bob

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  2/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Bob, enter your guess (format: x y): 4 1

[Server Result] Bob HITS Alice's board at (4, 1)!

--- Turn 20 ---
Current Turn: Alice

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  3/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Alice, enter your guess (format: x y): 5 1

[Server Result] Alice's guess at (5, 1) - MISS

--- Turn 21 ---
Current Turn: Bob

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  3/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Bob, enter your guess (format: x y): 5 1

[Server Result] Bob HITS Alice's board at (5, 1)!
*** Bob sunk Alice's Battleship! ***

--- Turn 22 ---
Current Turn: Alice

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  4/ 4 hits [SUNK]
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Alice, enter your guess (format: x y): 2 2

[Server Result] Alice's guess at (2, 2) - MISS

--- Turn 23 ---
Current Turn: Bob

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  4/ 4 hits [SUNK]
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Bob, enter your guess (format: x y): 2 2

[Server Result] Bob HITS Alice's board at (2, 2)!

--- Turn 24 ---
Current Turn: Alice

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  4/ 4 hits [SUNK]
  - Submarine           :  1/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Alice, enter your guess (format: x y): 3 2

[Server Result] Alice's guess at (3, 2) - MISS

--- Turn 25 ---
Current Turn: Bob

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  4/ 4 hits [SUNK]
  - Submarine           :  1/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Bob, enter your guess (format: x y): 3 2

[Server Result] Bob HITS Alice's board at (3, 2)!

--- Turn 26 ---
Current Turn: Alice

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  4/ 4 hits [SUNK]
  - Submarine           :  2/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Alice, enter your guess (format: x y): 4 2

[Server Result] Alice's guess at (4, 2) - MISS

--- Turn 27 ---
Current Turn: Bob

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  4/ 4 hits [SUNK]
  - Submarine           :  2/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Bob, enter your guess (format: x y): 4 2

[Server Result] Bob HITS Alice's board at (4, 2)!
*** Bob sunk Alice's Submarine! ***

--- Turn 28 ---
Current Turn: Alice

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  4/ 4 hits [SUNK]
  - Submarine           :  3/ 3 hits [SUNK]
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Alice, enter your guess (format: x y): 2 3

[Server Result] Alice's guess at (2, 3) - MISS

--- Turn 29 ---
Current Turn: Bob

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  4/ 4 hits [SUNK]
  - Submarine           :  3/ 3 hits [SUNK]
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Bob, enter your guess (format: x y): 2 3

[Server Result] Bob HITS Alice's board at (2, 3)!

--- Turn 30 ---
Current Turn: Alice

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  4/ 4 hits [SUNK]
  - Submarine           :  3/ 3 hits [SUNK]
  - Destroyer           :  1/ 2 hits
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  0/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Alice, enter your guess (format: x y): 2 4

[Server Result] Alice HITS Bob's board at (2, 4)!

--- Turn 31 ---
Current Turn: Bob

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  4/ 4 hits [SUNK]
  - Submarine           :  3/ 3 hits [SUNK]
  - Destroyer           :  1/ 2 hits
  - Patrol Boat         :  0/ 2 hits 

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  1/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Bob, enter your guess (format: x y): 2 4

[Server Result] Bob HITS Alice's board at (2, 4)!
*** Bob sunk Alice's Destroyer! ***

--- Turn 32 ---
Current Turn: Alice

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  4/ 4 hits [SUNK]
  - Submarine           :  3/ 3 hits [SUNK]
  - Destroyer           :  2/ 2 hits [SUNK]
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  1/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Alice, enter your guess (format: x y): 3 3

[Server Result] Alice's guess at (3, 3) - MISS

--- Turn 33 ---
Current Turn: Bob

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  4/ 4 hits [SUNK]
  - Submarine           :  3/ 3 hits [SUNK]
  - Destroyer           :  2/ 2 hits [SUNK]
  - Patrol Boat         :  0/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  1/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Bob, enter your guess (format: x y): 3 3

[Server Result] Bob HITS Alice's board at (3, 3)!

--- Turn 34 ---
Current Turn: Alice

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  4/ 4 hits [SUNK]
  - Submarine           :  3/ 3 hits [SUNK]
  - Destroyer           :  2/ 2 hits [SUNK]
  - Patrol Boat         :  1/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  1/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Alice, enter your guess (format: x y): 3 4

[Server Result] Alice HITS Bob's board at (3, 4)!

--- Turn 35 ---
Current Turn: Bob

Alice's Ships:
  - Aircraft Carrier    :  5/ 5 hits [SUNK]
  - Battleship          :  4/ 4 hits [SUNK]
  - Submarine           :  3/ 3 hits [SUNK]
  - Destroyer           :  2/ 2 hits [SUNK]
  - Patrol Boat         :  1/ 2 hits

Bob's Ships:
  - Aircraft Carrier    :  0/ 5 hits
  - Battleship          :  0/ 4 hits
  - Submarine           :  2/ 3 hits
  - Destroyer           :  0/ 2 hits
  - Patrol Boat         :  0/ 2 hits


Bob, enter your guess (format: x y): 3 4

[Server Result] Bob HITS Alice's board at (3, 4)!
*** Bob sunk Alice's Patrol Boat! ***

============================================================
GAME OVER! Bob wins after 35 turns!
============================================================


Final Game Statistics:
============================================================
Total turns: 36
Alice's hits: 2
Bob's hits: 18