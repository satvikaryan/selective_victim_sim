class Cache:
    def __init__(self, size):
        self.size = size
        self.data = {}
        self.hit_bits = {i: 0 for i in range(size)}  # Initialize hit bits with default value 0
        self.sticky_bits = {i: 0 for i in range(size)}  # Initialize sticky bits with default value 0

    def read(self, address):
        if address in self.data:
            self.hit_bits[address] = 1  # Update hit bit to 1
            self.sticky_bits[address] = 1  # Update sticky bit to 1
            return self.data[address]
        return None

    def write(self, address, data):
        self.data[address] = data
        self.hit_bits[address] = 1  # Update hit bit to 1
        self.sticky_bits[address] = 1  # Update sticky bit to 1

    def evict(self):
        # Find a victim block based on sticky bits
        victim = min(self.sticky_bits, key=self.sticky_bits.get)
        del self.data[victim]
        del self.hit_bits[victim]
        del self.sticky_bits[victim]

    def access(self, address):
        if address in self.data:  # Case 1: Hit in main cache
            self.hit_bits[address] = 1
            self.sticky_bits[address] = 1
            print(f"Case 1: Access to line {address}, hit in main cache")
        elif address in self.sticky_bits:  # Case 2: Hit in victim cache
            a = min(self.sticky_bits, key=self.sticky_bits.get)
            if self.sticky_bits[a] == 0:
                self.data[address], self.data[a] = self.data.get(a, None), self.data.get(address, None)
                self.sticky_bits[address] += 1
                self.hit_bits[address] += 1
            else:
                if self.hit_bits[address] == 0:
                    self.sticky_bits[a] = 0
                else:
                    self.data[address], self.data[a] = self.data.get(a, None), self.data.get(address, None)
                    self.sticky_bits[address] = 1
                    self.hit_bits[address] = 0
            print(f"Case 2: Access to line {address}, hit in victim cache")
        else:  # Case 3: Miss in both main and victim caches
            a = min(self.sticky_bits, key=self.sticky_bits.get)
            if self.sticky_bits[a] == 0:
                self.data[address] = self.data.get(a, None)
                self.sticky_bits[address] = 1
                self.hit_bits[address] += 1
            else:
                if self.hit_bits[address] == 0:
                    self.data[address] = "Data for line " + str(address)
                    self.sticky_bits[a] = 0
                else:
                    self.data[address] = self.data.get(a, None)
                    self.sticky_bits[address] = 1
                    self.hit_bits[address] = 0
            print(f"Case 3: Access to line {address}, miss in both main and victim caches")
        
        self.print_cache_state()  # Print cache state after access

    def print_cache_state(self):
        print("Main Cache:")
        for address, data in self.data.items():
            print(f"Address: {address}, Data: {data}, Hit Bit: {self.hit_bits.get(address, 0)}, Sticky Bit: {self.sticky_bits.get(address, 0)}")
        print("")


def test_selective_victim_caching():
    cache_size = 4
    cache = Cache(cache_size)

    # Test cases
    cache.access(0)  # Case 1
    cache.access(1)  # Case 2
    cache.access(2)  # Case 3

if __name__ == "__main__":
    test_selective_victim_caching()
