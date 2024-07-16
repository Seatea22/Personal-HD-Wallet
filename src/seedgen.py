import hashlib
import secrets
from typing import List

import pyperclip


class SeedGen:
    def __init__(self, seed="", passphrase=None, iterations=100000):
        self.seed = "mnemonic" + seed
        self.passphrase = passphrase
        self.iterations = iterations

    def generate_entropy(self, seed_length: int) -> str:
        bit_length = 128 if seed_length == 12 else 256
        return bin(secrets.randbits(bit_length))[2:].zfill(bit_length)

    def generate_checksum(self, entropy_bits: str, ):
        sha256_hash = hashlib.sha256(
            int(entropy_bits, 2).to_bytes((len(entropy_bits) + 7) // 8, byteorder='big')).digest()
        sha256_bin_hash = ''.join(format(byte, '08b') for byte in sha256_hash)

        checksum_len = len(entropy_bits) // 32
        checksum = sha256_bin_hash[:checksum_len]

        return entropy_bits + checksum

    def read_words(self) -> List[str]:
        with open("src/wordlist.txt") as f:
            wordlist = [line.strip() for line in f]
        return wordlist

    def generate_phrase(self, mnemonic: str) -> None:
        wordlist = self.read_words()
        self.passphrase = ' '.join([wordlist[int(mnemonic[i:i + 11], 2)] for i in range(0, len(mnemonic), 11)])

    def generate_seed(self, seed_length=12):
        if seed_length != 12 and seed_length != 24:
            raise ValueError("Please provide a seed length of 12 or 24")

        if self.passphrase is None or len(self.passphrase) == 0:
            entropy_bits = self.generate_entropy(seed_length)

            mnemonic = self.generate_checksum(entropy_bits)

            self.generate_phrase(mnemonic)
            pyperclip.copy(self.passphrase)

        hash = hashlib.pbkdf2_hmac(
            'sha512',
            self.passphrase.encode('utf-8'),
            self.seed.encode('utf-8'),
            2048
        )

        hash_hex = hash.hex()
        print(len(hash_hex), hash_hex)
        print(self.passphrase, self.seed)
