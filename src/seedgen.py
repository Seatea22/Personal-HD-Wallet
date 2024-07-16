import hashlib
import secrets
from typing import List

import pyperclip


class SeedGen:
    def __init__(self, seed="", passphrase=None, iterations=100000):
        self._seed = "mnemonic" + seed
        self._passphrase = passphrase
        self._iterations = iterations
        self._final_hash_seed = ""

    @property
    def final_hash_seed(self) -> str:
        return self._final_hash_seed

    def generate_seed(self, seed_length=12) -> None:
        if seed_length != 12 and seed_length != 24:
            raise ValueError("Please provide a seed length of 12 or 24")

        if self._passphrase is None or len(self._passphrase) == 0:
            entropy_bits = self.__generate_entropy(seed_length)
            mnemonic = self.__generate_checksum(entropy_bits)
            self.__generate_phrase(mnemonic)

        self._final_hash_seed = hashlib.pbkdf2_hmac('sha512', self._passphrase.encode('utf-8'),
                                                    self._seed.encode('utf-8'), 2048).hex()

    def __generate_entropy(self, seed_length: int) -> str:
        bit_length = 128 if seed_length == 12 else 256
        return bin(secrets.randbits(bit_length))[2:].zfill(bit_length)

    def __generate_checksum(self, entropy_bits: str, ):
        sha256_hash = hashlib.sha256(
            int(entropy_bits, 2).to_bytes((len(entropy_bits) + 7) // 8, byteorder='big')).digest()
        sha256_bin_hash = ''.join(format(byte, '08b') for byte in sha256_hash)

        checksum_len = len(entropy_bits) // 32
        checksum = sha256_bin_hash[:checksum_len]

        return entropy_bits + checksum

    def __read_words(self) -> List[str]:
        with open("src/wordlist.txt") as f:
            wordlist = [line.strip() for line in f]
        return wordlist

    def __generate_phrase(self, mnemonic: str) -> None:
        wordlist = self.__read_words()
        self._passphrase = ' '.join([wordlist[int(mnemonic[i:i + 11], 2)] for i in range(0, len(mnemonic), 11)])
