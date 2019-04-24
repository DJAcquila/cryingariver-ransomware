import Crypto.Random, base64


def generate_randomKey(bits, encode64 = False):
	gen = Crypto.Random.OSRNG.posix.DevURandomRNG()
	gen_bits = gen.read(bits)

	if encode64:
		return base64.b64encode(gen_bits)

	return gen_bits

if __name__ == '__main__':
	print(rand.generate_key(64))