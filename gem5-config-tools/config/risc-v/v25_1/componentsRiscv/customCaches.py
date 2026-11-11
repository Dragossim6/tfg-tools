# Import the SimObjects we are going to extend: Cache
from m5.objects import Cache, StridePrefetcher

# Los valores que pongo directamente aqui es xq no quiero cambiarlos en ningun momento


# Create an L1 cache
class L1Cache(Cache):
    def __init__(
        self, size, assoc, tag_latency, data_latency, response_latency
    ):
        super().__init__()
        self.size = size
        self.assoc = assoc
        self.tag_latency = tag_latency
        self.data_latency = data_latency
        self.response_latency = response_latency
        self.clusivity = "mostly_incl"


# Subclasses of L1 cache: Instruction and Data caches
class L1ICache(L1Cache):
    def __init__(
        self,
        size,
        assoc,
        tag_latency,
        data_latency,
        response_latency,
    ):
        super().__init__(
            size, assoc, tag_latency, data_latency, response_latency
        )
        self.is_read_only = True
        self.mshrs = 16
        self.tgts_per_mshr = 8


class L1DCache(L1Cache):
    def __init__(
        self, size, assoc, tag_latency, data_latency, response_latency, writeback_clean
    ):
        super().__init__(
            size, assoc, tag_latency, data_latency, response_latency
        )
        self.writeback_clean = writeback_clean
        self.mshrs = 32
        self.tgts_per_mshr = 16
        self.write_buffers = 8


# Create an L2 cache
class L2Cache(Cache):
    def __init__(
        self, size, assoc, tag_latency, data_latency, response_latency
    ):
        super().__init__()
        self.size = size
        self.assoc = assoc
        self.tag_latency = tag_latency
        self.data_latency = data_latency
        self.response_latency = response_latency
        self.mshrs = 32
        self.tgts_per_mshr = 16
        self.clusivity = "mostly_incl"
        self.prefetcher = StridePrefetcher(degree=1, latency=1, prefetch_on_access=True)


# Create an L3 cache
class L3Cache(Cache):
    def __init__(
        self, size, assoc, tag_latency, data_latency, response_latency
    ):
        super().__init__()
        self.size = size
        self.assoc = assoc
        self.tag_latency = tag_latency
        self.data_latency = data_latency
        self.response_latency = response_latency
        self.mshrs = 32
        self.tgts_per_mshr = 16
        self.writeback_clean = False
        self.clusivity = "mostly_incl"
        self.prefetcher = StridePrefetcher(degree=8, latency=1, prefetch_on_access=True)
