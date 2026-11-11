from components.customBranchPredictor import (
    PerceptBP,
    TournBP,
    TAGE_SC_L_Big,
)
from components.customFUPool import FUP_Big, FUP_Small, FUP_General, FUP_Different

from m5.objects import (
    X86O3CPU,
    DefaultX86FUPool,
    TournamentBP,
)

from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.isas import ISA


# O3Core extiende X86O3CPU. X86O3CPU es uno de los modelos internos de gem5 que implementa
# un pipeline fuera de orden para la arquitectura x86.
class O3Core(X86O3CPU):
    def __init__(
        self,
        frontend_width,
        backend_width,
        rob_size,
        iq_size,
        lsq_size,
        num_int_phys_regs,
        num_fp_phys_regs,
        fu_pool,
        bp,
        numEntriesBtb,
        numEntriesRas,
        tagBitsBtb=None,
        num_filter_entries=None,
        num_local_histories=None,
        local_history_length=None,
        num_ports=None,  # Optional parameter for "General" fu_pool
        num_IQs=None,
        num_DividedIQ_entries=None,
    ):
        super().__init__()
        self.fetchWidth = frontend_width
        self.decodeWidth = frontend_width
        self.renameWidth = frontend_width
        self.issueWidth = backend_width
        self.dispatchWidth = backend_width
        self.commitWidth = backend_width
        self.wbWidth = backend_width

        self.numROBEntries = rob_size
        #self.numIQEntries = iq_size
        self.LQEntries = lsq_size
        self.SQEntries = lsq_size

        self.numPhysIntRegs = num_int_phys_regs
        self.numPhysFloatRegs = num_fp_phys_regs

        valid_fu_pools = ["Big", "Small", "General","Different", "Default"]
        if fu_pool not in valid_fu_pools:
            raise ValueError(f"Invalid fu_pool '{fu_pool}'. Valid options are: {valid_fu_pools}")

        valid_bps = ["TournBP", "PerceptBP", "Default", "TAGE_SC_L_Big"]
        if bp not in valid_bps:
            raise ValueError(f"Invalid bp '{bp}'. Valid options are: {valid_bps}")

        if fu_pool == "Big":
            self.fuPool = FUP_Big()
        elif fu_pool == "Small":
            self.fuPool = FUP_Small()
        elif fu_pool == "General":
            if num_ports is None:
                raise ValueError("num_ports must be specified for 'General' fu_pool")
            self.fuPool = FUP_General(num_ports)
        elif fu_pool == "Different":
            self.fuPool = FUP_Different()
        else:
            self.fuPool = DefaultX86FUPool()

        if bp == "TournBP":
            self.branchPred = TournBP(
                numEntriesBtb, 
                numEntriesRas, 
            )
        elif bp == "PerceptBP":
            self.branchPred = PerceptBP(
                numEntriesBtb,
                tagBitsBtb,
                numEntriesRas,
                num_filter_entries,
                num_local_histories,
                local_history_length,
            )
        elif bp == "TAGE_SC_L_Big":
            self.branchPred = TAGE_SC_L_Big(numEntriesBtb, numEntriesRas)
        #else:
          #  self.branchPred = TournamentBP()

        if num_IQs and num_DividedIQ_entries:
            self.numIQs = num_IQs
            self.numEntriesDividedIQ = num_DividedIQ_entries


# O3StdCore hace wrap de O3CPUCore a un core compatible con la libreria estandar de gem5.
class O3StdCore(BaseCPUCore):
    def __init__(
        self,
        frontend_width,
        backend_width,
        rob_size,
        iq_size,
        lsq_size,
        num_int_phys_regs,
        num_fp_phys_regs,
        fu_pool,
        bp,
        numEntriesBtb,
        numEntriesRas,
        tagBitsBtb=None,        
        num_filter_entries=None,
        num_local_histories=None,
        local_history_length=None,
        num_ports=None,  # Optional parameter for "General" fu_pool
        num_IQs=None,
        num_DividedIQ_entries=None,
    ):
        core = O3Core(
            frontend_width,
            backend_width,
            rob_size,
            iq_size,
            lsq_size,
            num_int_phys_regs,
            num_fp_phys_regs,
            fu_pool,
            bp,
            numEntriesBtb,
            tagBitsBtb,
            numEntriesRas,
            num_filter_entries,
            num_local_histories,
            local_history_length,
            num_ports,  # Optional parameter for "General" fu_pool
            num_IQs,
            num_DividedIQ_entries,
        )
        super().__init__(core, ISA.X86)


# O3Processor, junto con BaseCPUProcessor, hace wrap de O3Core a un procesador compatible con la libreria estandar de gem5.
class O3Processor(BaseCPUProcessor):
    def __init__(
        self,
        numCores,
        frontend_width,
        backend_width,
        rob_size,
        iq_size,
        lsq_size,
        num_int_phys_regs,
        num_fp_phys_regs,
        fu_pool,
        bp,
        numEntriesBtb,
        numEntriesRas,
        tagBitsBtb=None,        
        num_filter_entries=None,
        num_local_histories=None,
        local_history_length=None,
        num_ports=None,  # Optional parameter for "General" fu_pool
        num_IQs=None,
        num_DividedIQ_entries=None,
    ):
        cores = [
            O3StdCore(
                frontend_width,
                backend_width,
                rob_size,
                iq_size,
                lsq_size,
                num_int_phys_regs,
                num_fp_phys_regs,
                fu_pool,
                bp,
                numEntriesBtb,
                tagBitsBtb,
                numEntriesRas,
                num_filter_entries,
                num_local_histories,
                local_history_length,
                num_ports,  # Optional parameter for "General" fu_pool
                num_IQs,
                num_DividedIQ_entries,
            )
            for _ in range(numCores)
        ]
        super().__init__(cores)
