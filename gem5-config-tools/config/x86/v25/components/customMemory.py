from typing import Optional

from gem5.components.memory.abstract_memory_system import AbstractMemorySystem
from gem5.components.memory.dram_interfaces.ddr4 import DDR4_2400_8x8
from gem5.components.memory.memory import ChanneledMemory

# NO funciona

# DRAM interface type
class CustomDDR4(DDR4_2400_8x8):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tCL = "14"  # Si intento añadir parametros casca


# Memory system
def MiMemoria(
    size: Optional[str] = None,
    num_channels: Optional[int] = 1,
) -> AbstractMemorySystem:
    """
    A single channel memory system using custom DIMM
    """
    return ChanneledMemory(
        CustomDDR4, num_channels=num_channels, interleaving_size=64, size=size
    )
