import m5
import os
import argparse
import sys

from pathlib import Path
from gem5.resources.resource import obtain_resource, DiskImageResource
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator

from gem5.components.boards.x86_board import X86Board

# Añadimos el directorio padre para importar confs_v25_1.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from confs_v25_1 import CONFIG_FACTORIES

parser = argparse.ArgumentParser(
    description="Restore and run from an x86 SPEC checkpoint"
)
parser.add_argument(
    "--config",
    type=str,
    default="Xeon4514Y",
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
    required=False,
    default="/nfs/home/ce/simciucd/full_system/x86-ubuntu-24.04-20250515",
    help="Full path to disk image",
)
parser.add_argument(
    "--mem_size",
    type=int,
    required=False,
    default=3,
    help="Memory size in GB (must match the 3GB used in checkpoint)"
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
    default=100000000000,
    help="Maximum number of ticks to simulate"
)

args = parser.parse_args()

# Obtener la configuración (Xeon4514Y)
factory = CONFIG_FACTORIES.get(args.config)
if factory is None:
    print(f"ERROR: Unknown configuration '{args.config}'")
    exit(1)

# Crear componentes desde la factoría
extra = {
    "processor": {"iq_size": args.iq_size} if args.iq_size else {},
    "cache": {},
}
components = factory(num_cores=args.num_cores, mem_size_gib=args.mem_size, extra=extra)

# Construir la placa X86
board = X86Board(
    clk_freq=components["clock"],
    processor=components["processor"],
    memory=components["memory"],
    cache_hierarchy=components["cache_hierarchy"]
)

# Verificar ruta del checkpoint
ckpt_path = Path(args.ckpt_path)
if not ckpt_path.exists():
    print(f"ERROR: Checkpoint path does not exist: {ckpt_path}")
    exit(1)

# Manejadores de eventos
def handle_workbegin():
    print("WARNING: Reached a WORKBEGIN event. Resetting stats again...")
    m5.stats.reset()
    yield False

def handle_workend():
    num_works = 0
    while True:
        num_works += 1
        print(f"Workend event #{num_works} reached")
        
        if num_works < args.works:
            yield False
        else:
            print(f"Reached {args.works} workend events. Dumping stats and exiting simulation!")
            m5.stats.dump()
            yield True

def exit_event_handler():
    print("Exit event: Application execution finished or m5 exit reached")
    yield True

# Cargar el Workload (Restaurando el checkpoint)
board.set_kernel_disk_workload(
    kernel=obtain_resource(resource_id="x86-linux-kernel-5.15.180"),
    disk_image=DiskImageResource(
        args.disk_image,
        root_partition="2"
    ),
    kernel_args=["root=/dev/sda2", "console=ttyS0", "earlyprintk=serial"],
    checkpoint=ckpt_path,
)

# Crear el simulador
sim = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.WORKBEGIN: handle_workbegin(),
        ExitEvent.WORKEND: handle_workend(),
        ExitEvent.EXIT: exit_event_handler(),
    },
)

# Ejecutar simulación
print(f"Starting simulation from checkpoint: {ckpt_path}")
print(f"Configuration: {args.config}")
print("Warming up caches and starting detailed simulation...")

# Reseteamos estadísticas aquí para que el calentamiento inicial no ensucie los resultados
m5.stats.reset() 

sim.run(args.num_ticks)

print(f"\nSimulation finished:")
print(f"  Final tick: {sim.get_current_tick()}")
print(f"  Exit cause: {sim.get_last_exit_event_cause()}")