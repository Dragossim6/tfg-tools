# confs.py (Versión para x86)
from pathlib import Path

# Volvemos a los imports de tu primer script (x86)
from components.customO3CPU import O3Processor
from components.customCacheHierarchy import ThreeLevelCacheHierarchy
from gem5.components.memory import DualChannelDDR4_2400

DEFAULT_MEM_SIZE = 4
DEFAULT_NUM_CORES = 1

def make_xeon4514Y_x86(num_cores=DEFAULT_NUM_CORES, mem_size_gib=DEFAULT_MEM_SIZE, extra=None):
    """
    Intel Xeon Silver 4514Y (Redwood Cove) Parametrization para x86 O3.
    """
    processor_config = {
        "frontend_width": 6,
        "backend_width": 8,
        "rob_size": 512,
        "lsq_size": 306,              # LSQ unificado (192 Load + 114 Store)
        "num_int_phys_regs": 280, #320
        "num_fp_phys_regs": 332,
        "fu_pool": "Big",            
        "bp": "TAGE_SC_L_Big",           
        "numEntriesBtb": 8192, #4096
        "tagBitsBtb": 18,
        "numEntriesRas": 96,
        "num_filter_entries": 0,
        "num_local_histories": 512,
        "local_history_length": 36,
        "iq_size": 192, #256
    }
    
    # Inyectar parámetros extra de la línea de comandos (ej. --iq_size)
    if extra:
        processor_config.update(extra.get("processor", {}))
    
    cache_config = {
        "l1i_assoc": 8,
        "l1i_size": "64kB",           
        "l1i_tag_latency": 1,
        "l1i_data_latency": 2,
        "l1i_response_latency": 1,
        "l1d_assoc": 12, 
        "l1d_size": "48kB",
        "l1d_tag_latency": 1,
        "l1d_data_latency": 4,
        "l1d_response_latency": 1,
        "l1d_writeback_clean": False,
        "l2_assoc": 16,
        "l2_size": "2MB",             # 2MB por core para este Xeon
        "l2_tag_latency": 4,
        "l2_data_latency": 12,
        "l2_response_latency": 4,
        "l3_assoc": 15, #12
        "l3_size": "30MB",            # 30MB L3 Compartida
        "l3_tag_latency": 15,
        "l3_data_latency": 35,
        "l3_response_latency": 15, 
    }        
    if extra:
        cache_config.update(extra.get("cache", {}))

    processor = O3Processor(numCores=num_cores, **processor_config)
    cache_hierarchy = ThreeLevelCacheHierarchy(**cache_config)
    main_memory = DualChannelDDR4_2400(size=f"{int(mem_size_gib)}GB") # GB en vez de GiB
    
    return {
        "processor": processor,
        "cache_hierarchy": cache_hierarchy,
        "memory": main_memory,
        "clock": "2GHz", # Frecuencia base Xeon Silver 4514Y
        "meta": {
            "name": "Xeon4514Y_Redwood_x86",
            "processor_config": processor_config,
            "cache_config": cache_config,
        },
    }

# Actualizamos el diccionario
CONFIG_FACTORIES = {
    # Puedes conservar tus otras configuraciones aquí si las migras a x86
    "Xeon4514Y": make_xeon4514Y_x86,
}