import secrets


class SeedGen:
    def __init__(self, seed: str):
        self.seed = seed

        self.random = secrets.SystemRandom(self.seed) if self.seed is not None or len(
            self.seed) > 0 else secrets.SystemRandom()
        self.phrase = ""

    def generate_phrase(self, seed_length=12):
        if seed_length != 12 and seed_length != 24:
            raise ValueError("Please provide a seed length of 12 or 24")

        bit_length = 128 if seed_length == 12 else 256
        bits = self.random.getrandbits(bit_length)
        bits = bin(bits)[2:].zfill(bit_length)
        print(len(bits), bits)

        checksum_len = int(bit_length / 128)
        checksum = bits[-checksum_len:]
        print(checksum_len, checksum)



