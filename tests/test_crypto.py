"""
Unit tests for the crypto module.
"""

import pytest
from crypto import (
    generate_keypair,
    encrypt_value,
    decrypt_value,
    perform_homomorphic_hit_check,
    check_hit
)


class TestKeyGeneration:
    """Tests for key generation."""
    
    def test_generate_keypair(self):
        """Test keypair generation."""
        public_key, private_key = generate_keypair()
        
        assert public_key is not None
        assert private_key is not None
        # Keys are different objects
        assert public_key is not private_key
    
    def test_keypair_different_each_time(self):
        """Test that each keypair generation produces different keys."""
        pub1, priv1 = generate_keypair(n_length=1024)  # Smaller for speed
        pub2, priv2 = generate_keypair(n_length=1024)
        
        # Keys should be different
        assert pub1.n != pub2.n


class TestEncryptionDecryption:
    """Tests for basic encryption/decryption."""
    
    def test_encrypt_decrypt_zero(self):
        """Test encrypting and decrypting 0."""
        public_key, private_key = generate_keypair(n_length=1024)
        
        plaintext = 0
        encrypted = encrypt_value(public_key, plaintext)
        decrypted = decrypt_value(private_key, encrypted)
        
        assert decrypted == plaintext
    
    def test_encrypt_decrypt_one(self):
        """Test encrypting and decrypting 1."""
        public_key, private_key = generate_keypair(n_length=1024)
        
        plaintext = 1
        encrypted = encrypt_value(public_key, plaintext)
        decrypted = decrypt_value(private_key, encrypted)
        
        assert decrypted == plaintext
    
    def test_encrypt_multiple_values(self):
        """Test encrypting multiple values."""
        public_key, private_key = generate_keypair(n_length=1024)
        
        for value in [0, 1, 5, 100, -1, -5]:
            encrypted = encrypt_value(public_key, value)
            decrypted = decrypt_value(private_key, encrypted)
            assert decrypted == value


class TestHomomorphicHitCheck:
    """Tests for homomorphic hit checking."""
    
    def test_hit_check_hit_scenario(self):
        """Test hit detection (cell=1, guess=1)."""
        public_key, private_key = generate_keypair(n_length=1024)
        
        # Cell contains ship (1)
        encrypted_cell = encrypt_value(public_key, 1)
        
        # Perform hit check
        encrypted_result = perform_homomorphic_hit_check(encrypted_cell, 1)
        decrypted_result = decrypt_value(private_key, encrypted_result)
        
        # Should be 0 (hit)
        assert check_hit(decrypted_result)
    
    def test_hit_check_miss_scenario(self):
        """Test miss detection (cell=0, guess=1)."""
        public_key, private_key = generate_keypair(n_length=1024)
        
        # Cell is water (0)
        encrypted_cell = encrypt_value(public_key, 0)
        
        # Perform hit check
        encrypted_result = perform_homomorphic_hit_check(encrypted_cell, 1)
        decrypted_result = decrypt_value(private_key, encrypted_result)
        
        # Should be non-zero (miss)
        assert not check_hit(decrypted_result)
    
    def test_hit_check_multiple_times(self):
        """Test that multiple hit checks on same cell give consistent results."""
        public_key, private_key = generate_keypair(n_length=1024)
        
        encrypted_cell = encrypt_value(public_key, 1)
        
        results = []
        for _ in range(3):
            encrypted_result = perform_homomorphic_hit_check(encrypted_cell, 1)
            decrypted_result = decrypt_value(private_key, encrypted_result)
            results.append(check_hit(decrypted_result))
        
        # All checks should detect hit
        assert all(results)
    
    def test_check_hit_function(self):
        """Test the check_hit utility function."""
        assert check_hit(0) == True
        assert check_hit(1) == False
        assert check_hit(-1) == False
        assert check_hit(999) == False


class TestHomomorphicProperties:
    """Tests for homomorphic properties."""
    
    def test_encryption_preserves_bitlength(self):
        """Test that encrypted values maintain mathematical properties."""
        public_key, private_key = generate_keypair(n_length=1024)
        
        # Encrypt two values
        enc1 = encrypt_value(public_key, 1)
        enc0 = encrypt_value(public_key, 0)
        
        # Addition should work homomorphically
        enc_sum = enc1 + enc0
        result = decrypt_value(private_key, enc_sum)
        assert result == 1
    
    def test_encryption_scalar_multiplication(self):
        """Test scalar multiplication of encrypted values."""
        public_key, private_key = generate_keypair(n_length=1024)
        
        enc_value = encrypt_value(public_key, 5)
        
        # Multiply by plaintext scalar
        enc_result = enc_value * 2
        result = decrypt_value(private_key, enc_result)
        
        assert result == 10
