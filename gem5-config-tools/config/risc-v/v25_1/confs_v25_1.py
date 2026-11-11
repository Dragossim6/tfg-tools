# confs.py
# Fábricas de configuración para distintas plataformas (XT-910, etc.)
# Aquí importamos las clases que vamos a instanciar para poder devolver objetos listos.
from pathlib import Path

# importa los componentes específicos que uses
from componentsRiscv.customO3CPU_v25_1 import RiscvO3Processor
from componentsRiscv.customCacheHierarchy import ThreeLevelCacheHierarchy
from gem5.components.memory import DualChannelDDR4_2400
from gem5.components.memory.simple import SingleChannelSimpleMemory
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import (
    PrivateL1SharedL2CacheHierarchy,
)


# constantes por defecto
DEFAULT_MEM_SIZE = 2
DEFAULT_NUM_CORES = 1

def make_bigO3_riscv(num_cores=DEFAULT_NUM_CORES, mem_size_gib=DEFAULT_MEM_SIZE, extra=None):
    """
    Big O3 Parametrization. Inspired by SiFive P870, Xuantie C930, and XiangShan kunminghu.
    """
    processor_config = {
       "frontend_width": 6,
       "backend_width": 12,
       "commitWidth": 8,
       "rob_size": 720,
       "lq_entries": 196,
       "sq_entries": 64,
       "num_int_phys_regs": 228,
       "num_fp_phys_regs": 240,
       "bp": "TAGE_SC_L_Big",
       "numEntriesBtb": 2048,
       "numEntriesRas": 32,
       "iq_config": "big",
       "iq_type": "unified",  # "unified" or "distributed"
       "iq_size": 180,
    #    "iq_int_size": 16, if distributed
    #    "iq_fp_size": 24,
    #    "iq_ls_size": 12,

    }
    if extra:
        processor_config.update(extra.get("processor", {}))
    
    cache_config = {
        "l1i_assoc": 4,
        "l1i_size": "64KiB",
        "l1i_tag_latency": 1,
        "l1i_data_latency": 1,
        "l1i_response_latency": 1,
        "l1d_assoc": 8,
        "l1d_size": "64KiB",
        "l1d_tag_latency": 1,
        "l1d_data_latency": 2,
        "l1d_response_latency": 1,
        "l1d_writeback_clean": True,
        "l2_assoc": 8,
        "l2_size": "1MiB",
        "l2_tag_latency": 3,
        "l2_data_latency": 6,
        "l2_response_latency": 3,
        "l3_assoc": 16,
        "l3_size": "16MiB",
        "l3_tag_latency": 10,
        "l3_data_latency": 20,
        "l3_response_latency": 10,
    }
    if extra:
        cache_config.update(extra.get("cache", {}))

    processor = RiscvO3Processor(numCores=num_cores, **processor_config)
    cache_hierarchy = ThreeLevelCacheHierarchy(**cache_config)
    main_memory = DualChannelDDR4_2400(size=f"{int(mem_size_gib)}GiB")
    return {
        "processor": processor,
        "cache_hierarchy": cache_hierarchy,
        "memory": main_memory,
        "clock": "3GHz",
        "meta": {
            "name": "BigO3_RISCV",
            "processor_config": processor_config,
            "cache_config": cache_config,
        },
    }

def make_smallO3_riscv(num_cores=DEFAULT_NUM_CORES, mem_size_gib=DEFAULT_MEM_SIZE, extra=None):
    """
    Small O3 Parametrization.
    """
    processor_config = {
       "frontend_width": 3,
       "backend_width": 6,
       "commitWidth": 4,
       "rob_size": 192,
       "lq_entries": 36,
       "sq_entries": 18,
       "num_int_phys_regs": 128,
       "num_fp_phys_regs": 119,
       "bp": "TAGE_SC_L_Small", 
       "numEntriesBtb":1024,
       "numEntriesRas":16,
       "iq_config": "small",
       "iq_type": "unified",  # "unified" or "distributed"
       "iq_size": 72,
    #    "iq_int_size": 16, if distributed
    #    "iq_fp_size": 24,
    #    "iq_ls_size": 12,
    }
    if extra:
        processor_config.update(extra.get("processor", {}))
    
    cache_config = {
        "l1i_assoc": 4,
        "l1i_size": "32KiB",
        "l1i_tag_latency": 1,
        "l1i_data_latency": 1,
        "l1i_response_latency": 1,
        "l1d_assoc": 4,
        "l1d_size": "32KiB",
        "l1d_tag_latency": 1,
        "l1d_data_latency": 2,
        "l1d_response_latency": 1,
        "l1d_writeback_clean": True,
        "l2_assoc": 8,
        "l2_size": "256KiB",
        "l2_tag_latency": 3,
        "l2_data_latency": 6,
        "l2_response_latency": 3,
        "l3_assoc": 16,
        "l3_size": "2MiB",
        "l3_tag_latency": 10,
        "l3_data_latency": 20,
        "l3_response_latency": 10,
    }        
    if extra:
        cache_config.update(extra.get("cache", {}))

    processor = RiscvO3Processor(numCores=num_cores, **processor_config)
    cache_hierarchy = ThreeLevelCacheHierarchy(**cache_config)
    main_memory = DualChannelDDR4_2400(size=f"{int(mem_size_gib)}GiB")
    return {
        "processor": processor,
        "cache_hierarchy": cache_hierarchy,
        "memory": main_memory,
        "clock": "2GHz",
        "meta": {
            "name": "SmallO3_RISCV",
            "processor_config": processor_config,
            "cache_config": cache_config,
        },
    }

def make_smallO3_riscv(num_cores=DEFAULT_NUM_CORES, mem_size_gib=DEFAULT_MEM_SIZE, extra=None):
    """
    Small O3 Parametrization.
    """
    processor_config = {
       "frontend_width": 3,
       "backend_width": 6,
       "commitWidth": 4,
       "rob_size": 192,
       "lq_entries": 36,
       "sq_entries": 18,
       "num_int_phys_regs": 128,
       "num_fp_phys_regs": 119,
       "bp": "TAGE_SC_L_Small", 
       "numEntriesBtb":1024,
       "numEntriesRas":16,
       "iq_config": "small",
       "iq_type": "unified",  # "unified" or "distributed"
       "iq_size": 72,
    #    "iq_int_size": 16, if distributed
    #    "iq_fp_size": 24,
    #    "iq_ls_size": 12,
    }
    if extra:
        processor_config.update(extra.get("processor", {}))
    
    cache_config = {
        "l1i_assoc": 4,
        "l1i_size": "32KiB",
        "l1i_tag_latency": 1,
        "l1i_data_latency": 1,
        "l1i_response_latency": 1,
        "l1d_assoc": 4,
        "l1d_size": "32KiB",
        "l1d_tag_latency": 1,
        "l1d_data_latency": 2,
        "l1d_response_latency": 1,
        "l1d_writeback_clean": True,
        "l2_assoc": 8,
        "l2_size": "256KiB",
        "l2_tag_latency": 3,
        "l2_data_latency": 6,
        "l2_response_latency": 3,
        "l3_assoc": 16,
        "l3_size": "2MiB",
        "l3_tag_latency": 10,
        "l3_data_latency": 20,
        "l3_response_latency": 10,
    }        
    if extra:
        cache_config.update(extra.get("cache", {}))

    processor = RiscvO3Processor(numCores=num_cores, **processor_config)
    cache_hierarchy = ThreeLevelCacheHierarchy(**cache_config)
    main_memory = DualChannelDDR4_2400(size=f"{int(mem_size_gib)}GiB")
    return {
        "processor": processor,
        "cache_hierarchy": cache_hierarchy,
        "memory": main_memory,
        "clock": "2GHz",
        "meta": {
            "name": "SmallO3_RISCV",
            "processor_config": processor_config,
            "cache_config": cache_config,
        },
    }

def make_beaglev_ahead_riscv(num_cores=4, mem_size_gib=4, extra=None):
    """
    BeagleV-Ahead Parametrization. 
    Based on the Alibaba T-Head TH1520 SoC (Quad-core XuanTie C910 RV64GCV).
    """
    # Parámetros aproximados para la microarquitectura XuanTie C910 (Out-of-Order, 12 stages)
    processor_config = {
        "frontend_width": 3,   # Decode de hasta 3 instrucciones por ciclo
        "renameWidth": 4, 
        "dispatchWidth": 4,    # Despacho de hasta 4 instrucciones
        "backend_width": 8,    # Puertos de ejecución (issue)
        "commitWidth": 3,      # Commit de hasta 3 instrucciones
        "rob_size": 192,       # ROB aproximado para el C910
        "lq_entries": 12,
        "sq_entries": 24,
        "num_int_phys_regs": 96,
        "num_fp_phys_regs": 64,
        "bp": "BiMode_BP",  # Predictor local para un diseño más simple
        "numEntriesBtb": 1024, # BTB más grande para compensar el pipeline
        "numEntriesRas": 12,
        "iq_config": "small",
        "iq_type": "distributed",
        "iq_size": 80, 
        "iq_int_size": 12,
        "iq_fp_size": 8,
        "iq_ls_size": 8,
    }
    if extra:
        processor_config.update(extra.get("processor", {}))
    
    # Jerarquía típica del TH1520: L1I/L1D de 64KB y L2 compartida de 1MB a 2MB
    cache_config = {
        "l1i_size": "64KiB",
        "l1i_assoc": 2,
        "l1d_size": "64KiB",
        "l1d_assoc": 2,
        "l2_size": "1MiB", # o "2MiB" dependiendo del binning del TH1520
        "l2_assoc": 16,
    }
    if extra:
        cache_config.update(extra.get("cache", {}))

    processor = RiscvO3Processor(numCores=num_cores, **processor_config)
    
    # El TH1520 carece de L3, por lo que instanciamos la jerarquía estándar de 2 niveles importada arriba
    cache_hierarchy = PrivateL1SharedL2CacheHierarchy(
        l1d_size=cache_config["l1d_size"],
        l1d_assoc=cache_config["l1d_assoc"],
        l1i_size=cache_config["l1i_size"],
        l1i_assoc=cache_config["l1i_assoc"],
        l2_size=cache_config["l2_size"],
        l2_assoc=cache_config["l2_assoc"]
    )
    
    # BeagleV-Ahead utiliza memoria LPDDR4 a 4266 MT/s. 
    # Como fallback en tu entorno actual, usaremos tu DDR4, 
    # pero puedes cambiarlo a LPDDR4 de gem5 si lo tienes disponible.
    main_memory = DualChannelDDR4_2400(size=f"{int(mem_size_gib)}GiB")
    
    return {
        "processor": processor,
        "cache_hierarchy": cache_hierarchy,
        "memory": main_memory,
        "clock": "1.85GHz", # Reloj típico del TH1520 en la BeagleV-Ahead
        "meta": {
            "name": "BeagleV_Ahead_TH1520",
            "processor_config": processor_config,
            "cache_config": cache_config,
        },
    }


# Diccionario público de configuraciones. Añade nuevas fábricas aquí.
CONFIG_FACTORIES = {
    "BeagleV-Ahead": make_beaglev_ahead_riscv,
    "BigO3": make_bigO3_riscv,
    "SmallO3": make_smallO3_riscv,
}
