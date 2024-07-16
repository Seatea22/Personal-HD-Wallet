import hashlib
import secrets
from typing import List

__doc__ = """seedgen module - Allows the generation of deterministic seeds used in HD wallet creation"""


class SeedGen:
    """
    This class is responsible for generating deterministic seeds that can be used in HD wallet creation.
    The final hash seed and passphrase (if not given) are accessible after instantiation.
    """
    def __init__(self, seed_length=12, salt="", passphrase="", iterations=2048):
        """
        Initializes seed length, salt, passphrase, and iteration values before final
        hash seed is generated.

        :param seed_length: Number of words to be included in the mnemonic phrase. (default value is 12)
        :param salt: Salt to be used in final hash seed generation. (defaults to empty string)
        :param passphrase: A pre-defined passphrase can be provided to initialize the final seed. (defaults to empty string) NOTE: String must include 12 or 24 space separated words that are present in "wordlist.txt".
        :param iterations: The amount of iterations to run during final hash seed generation. (default 2048)
        """
        self._seed_length = seed_length
        self._salt = "mnemonic" + salt
        self._passphrase = passphrase
        self._split_passphrase = passphrase.split(" ")
        self._iterations = iterations

        if len(self._split_passphrase) != self._seed_length:
            raise ValueError("Length of passphrase must equal seed length!")

        self._final_hash_seed = self.__generate_seed(seed_length)

    @property
    def salt(self):
        return self._salt

    @property
    def iterations(self):
        """The number of iterations performed during final hash seed generation."""
        return self._iterations

    @property
    def passphrase(self) -> str:
        """A space separated string containing a mnemonic string of 12 or 24 words."""
        return self._passphrase

    @property
    def final_hash_seed(self) -> str:
        """A string including the hexadecimal representation of the final seed."""
        return self._final_hash_seed


    def __check_seed_length(self, seed_length: int) -> None:
        """
        Raises a ValueError if the seed length provided is not a value of 12 or 24.
        :param seed_length: An integer representing the length of the mnemonic phrase.
        """
        if seed_length != 12 and seed_length != 24:
            raise ValueError("Please provide a seed length of 12 or 24")

    def __generate_seed(self, seed_length: int) -> str:
        """
        Creates a deterministic seed from either a provided passphrase or one generated from random entropy.
        :param seed_length: Number of words in the mnemonic passphrase. (default value is 12)
        :return: A string representation containing the deterministic seed.
        """
        self.__check_seed_length(seed_length)

        # Generate a passphrase if one is not already provided.
        if self._passphrase is None or len(self._passphrase) == 0:
            entropy_bits = self.__generate_entropy(seed_length)
            mnemonic = self.__generate_checksum(entropy_bits)
            self.__generate_phrase(mnemonic)

        return hashlib.pbkdf2_hmac(
            'sha512',
            self._passphrase.encode('utf-8'),
            self._salt.encode('utf-8'),
            self._iterations
        ).hex()

    def __generate_entropy(self, seed_length: int) -> str:
        """
        Generates the entropy bits for the mnemonic passphrase.
        :param seed_length: The mnemonic passphrase can either be 12 or 24 words.
        :return:
        """
        self.__check_seed_length(seed_length)
        # A seed length of 12 will need an entropy length of 128 (256 for 24 words)
        bit_length = 128 if seed_length == 12 else 256
        # Convert to bin str representation (remove '0b') and pad start with leading zeroes
        return bin(secrets.randbits(bit_length))[2:].zfill(bit_length)

    def __generate_checksum(self, entropy_bits: str) -> str:
        """
        Generates and concatenates checksum into the entropy bits.
        :param entropy_bits: A 128 or 256 bit string representing entropy bits.
        :return: A string representation of entropy bits with a checksum.
        """
        entropy_length = len(entropy_bits)
        if entropy_length != 128 or entropy_length != 256:
            raise ValueError("Entropy must be 128 or 256 bits.")

        # In order to extract the checksum, we must first hash the entropy bits.
        sha256_hash = hashlib.sha256(
            int(entropy_bits, 2).to_bytes((entropy_length + 7) // 8, byteorder='big')).digest()
        sha256_bin_hash = ''.join(format(byte, '08b') for byte in sha256_hash) # Convert hex digest to bin representation.

        # There will be a checksum bit added to the end for every 32 bits
        checksum_len = entropy_length // 32
        checksum = sha256_bin_hash[:checksum_len]
        return f"{entropy_bits}{checksum}"

    def __read_words(self) -> List[str]:
        """Reads the word list from the wordlist file. Functionality subject to change."""
        with open("src/wordlist.txt") as f:
            wordlist = [line.strip() for line in f]
        return wordlist

    def __generate_phrase(self, mnemonic: str) -> None:
        """Generates a mnemonic phrase from a bit representation of mnemonic input.
        :param mnemonic: A string representing the mnemonic bits.
        """
        wordlist = self.__read_words()
        self._passphrase = ' '.join([wordlist[int(mnemonic[i:i + 11], 2)] for i in range(0, len(mnemonic), 11)])
