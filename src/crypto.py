"""
Cryptographic utilities for Paillier homomorphic encryption.

This module provides key generation, encryption/decryption, and
homomorphic hit-checking operations.
"""

import random
from typing import Tuple
from phe import paillier
from phe.paillier import PaillierPublicKey, PaillierPrivateKey, EncryptedNumber


def generate_keypair(n_length: int = 2048) -> Tuple[PaillierPublicKey, PaillierPrivateKey]:
    """
    Generate a Paillier public-private keypair.
    
    Args:
        n_length: Bit length of the RSA modulus. Default is 2048.
        
    Returns:
        Tuple of (public_key, private_key)
    """
    public_key, private_key = paillier.generate_paillier_keypair(n_length=n_length)
    return public_key, private_key


def encrypt_value(public_key: PaillierPublicKey, value: int) -> EncryptedNumber:
    """
    Encrypt a single integer value using the public key.
    
    Args:
        public_key: The Paillier public key
        value: The plaintext integer to encrypt (0 or 1 for board cells)
        
    Returns:
        An encrypted number
    """
    return public_key.encrypt(value)


def decrypt_value(private_key: PaillierPrivateKey, encrypted_value: EncryptedNumber) -> int:
    """
    Decrypt an encrypted value using the private key.
    
    Args:
        private_key: The Paillier private key
        encrypted_value: The encrypted number to decrypt
        
    Returns:
        The decrypted integer value
    """
    decrypted = private_key.decrypt(encrypted_value)
    return int(decrypted)


def perform_homomorphic_hit_check(
    encrypted_cell: EncryptedNumber,
    guess_value: int
) -> EncryptedNumber:
    """
    Perform homomorphic hit checking without revealing the cell value.
    
    The logic:
    - encrypted_difference = encrypted_cell - guess_value
    - If cell was 1 (ship) and guess was 1 → difference is 0 (HIT)
    - If cell was 0 (water) and guess was 1 → difference is -1 (MISS)
    - We apply random blinding to hide the miss value
    
    Args:
        encrypted_cell: The encrypted cell value (0 or 1)
        guess_value: The guessed value (typically 1)
        
    Returns:
        The encrypted blinded result
    """
    # Compute encrypted difference
    encrypted_difference = encrypted_cell - guess_value
    
    # Apply random blinding to hide miss values
    # If difference is 0 (hit): 0 * random = 0
    # If difference is non-zero (miss): non-zero * random = random junk
    blinding_factor = random.randint(1, 999999)
    encrypted_result = encrypted_difference * blinding_factor
    
    return encrypted_result


def check_hit(decrypted_result: int) -> bool:
    """
    Determine if a guess was a hit or miss based on the decrypted result.
    
    Args:
        decrypted_result: The decrypted homomorphic result
        
    Returns:
        True if hit (value is 0), False if miss (value is non-zero)
    """
    return decrypted_result == 0
