
import m5
import os
import argparse
import sys

from pathlib import Path
from gem5.resources.resource import *
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator

from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.components.boards.riscv_board import RiscvBoard
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import (
    PrivateL1SharedL2CacheHierarchy,
)
from gem5.components.memory import DualChannelDDR4_2400

# Add parent directory to sys.path to import confs.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from confs_v25_1 import CONFIG_FACTORIES

parser = argparse.ArgumentParser(
    description="Restore and run from a RISC-V checkpoint"
)
parser.add_argument(
    "--config",
    type=str,
    required=True,
    help=f"Available configurations: {list(CONFIG_FACTORIES.keys())}",
)
parser.add_argument(
    "--ckpt_path",
    type=str,
    required=True,
    help="Full path to checkpoint directory",
)
parser.add_argument(
    "--disk_image",
    type=str,
    required=True,
    help="Full path to disk image",
)
parser.add_argument(
    "--mem_size",
    type=int,
    required=False,
    default=4,
    help="Memory size in GB (must match checkpoint)"
)
parser.add_argument(
    "--num_cores", 
    type=int, 
    required=False, 
    default=1, 
    help="Number of cores (must match checkpoint)"
)
parser.add_argument(
    "--iq_size",
    type=int,
    required=False,
    help="IQ size in the O3 processor"
)
parser.add_argument(
    "--works",
    type=int,
    default=1,
    help="Number of workend events until exit"
)
parser.add_argument(
    "--num_ticks",
    type=int,
    default=10000000000,
    help="Maximum number of ticks to simulate"
)

args = parser.parse_args()

# Get configuration factory
factory = CONFIG_FACTORIES.get(args.config)
if factory is None:
    print(f"ERROR: Unknown configuration '{args.config}'")
    print(f"Available configurations: {list(CONFIG_FACTORIES.keys())}")
    exit(1)

# Create components from factory
extra = {
    "processor": {"iq_size": args.iq_size} if args.iq_size else {},
    "cache": {},
}
components = factory(num_cores=args.num_cores, mem_size_gib=args.mem_size, extra=extra)

processor = components["processor"]
cache_hierarchy = components["cache_hierarchy"]
memory = components["memory"]
clk_freq = components["clock"]

# Build board
board = RiscvBoard(
    clk_freq=clk_freq,
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy
)

# Checkpoint path
ckpt_path = Path(args.ckpt_path)
if not ckpt_path.exists():
    print(f"ERROR: Checkpoint path does not exist: {ckpt_path}")
    exit(1)

# Event handlers
def handle_workend():
    num_works = 0
    while True:
        num_works += 1
        print(f"Workend event #{num_works}")
        if num_works < args.works:
            yield False
        else:
            print(f"Reached {args.works} workend events, exiting...")
            yield True

def handle_workbegin():
    print("WARNING: Unexpected WORKBEGIN event (should already be past ROI start)")
    yield False

def exit_event_handler():
    print("Exit event: Application execution finished")
    yield True

# Set workload (restore from checkpoint)
board.set_kernel_disk_workload(
    bootloader=obtain_resource(resource_id="riscv-bootloader-opensbi-1.3.1"),
    kernel=obtain_resource(resource_id="riscv-linux-6.8.12-kernel"),
    disk_image=DiskImageResource(
        args.disk_image,
        root_partition="1"
    ),
    checkpoint=ckpt_path,
)

# ==============================================================================
# PARCHE DE CONFIGURACIÓN RISC-V: Desactivar PMP
# Evita el bucle infinito de "pmp access fault" al restaurar con procesadores O3
# ==============================================================================
for core in processor.get_cores():
    core.get_mmu().pmp.pmp_entries = 0
# ==============================================================================

# Create simulator
sim = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.WORKBEGIN: handle_workbegin(),
        ExitEvent.WORKEND: handle_workend(),
        ExitEvent.EXIT: exit_event_handler(),
    },
)

# Run simulation
print(f"Starting simulation from checkpoint: {ckpt_path}")
print(f"Configuration: {args.config}")
print(f"Running for maximum {args.num_ticks} ticks or {args.works} workend events")

sim.run(args.num_ticks)

print(f"\nSimulation finished:")
print(f"  Final tick: {sim.get_current_tick()}")
print(f"  Exit cause: {sim.get_last_exit_event_cause()}")
