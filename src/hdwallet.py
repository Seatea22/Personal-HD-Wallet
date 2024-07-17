from abc import ABC, abstractmethod
from typing import Tuple
import hmac
import hashlib

from seedgen import SeedGen


class HDWallet:

    def __init__(self, phrase: str, salt: str):
        seed_length = len(phrase.split(" "))
        self._seedgen = SeedGen(
            seed_length=seed_length,
            passphrase=phrase,
            salt=salt
        )
        self._master_private_key, self._master_chain_code = self._create_master()

    def _create_master(self) -> Tuple[str, str]:
        seed = bytes.fromhex(self._seedgen.final_hash_seed)
        hmac_obj = hmac.new(
            key="Bitcoin seed".encode('utf-8'),
            msg=seed,
            digestmod='sha512'
        )
        hashed_seed = hmac_obj.hexdigest()

        master_pk = hashed_seed[:len(hashed_seed) // 2]
        master_cc = hashed_seed[len(hashed_seed) // 2:]
        return master_pk, master_cc
