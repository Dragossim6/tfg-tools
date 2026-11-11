from typing import List
from componentsRiscv.customBranchPredictor import (
    BiMode_BP,
    Local_BP,
    PerceptBP,
    TournBP,
    TAGE_SC_L_Big,
    TAGE_SC_L_Small
)

from componentsRiscv.customIQs_FUPool_v25_1 import (
    make_bigO3_distributed_IQs,
    make_bigO3_unified_IQ,
    make_smallO3_distributed_IQs,
    make_smallO3_unified_IQ,
    make_replicated_IQs,
)

from m5.objects import (
    RiscvO3CPU, 
    DefaultFUPool, 
    TournamentBP 
)

from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.isas import ISA


# O3Core extiende X86O3CPU. X86O3CPU es uno de los modelos internos de gem5 que implementa
# un pipeline fuera de orden para la arquitectura x86.
class RiscvO3Core(RiscvO3CPU):
    def __init__(
        self,
        frontend_width,
        backend_width,
        rob_size,
        iq_size,
        num_int_phys_regs,
        num_fp_phys_regs,
        bp,
        numEntriesBtb=None,
        numEntriesRas=None,
        tagBitsBtb=None,
        num_filter_entries=None,
        num_local_histories=None,
        local_history_length=None,
        iq_config="big",
        iq_type="unified",
        num_ports=None,
        iq_replicated_size=None,
        iq_int_size=16,
        iq_fp_size=24,
        iq_ls_size=12,
        fetchWidth=None,
        decodeWidth=None,
        renameWidth=None,
        issueWidth=None,
        dispatchWidth=None,
        commitWidth=None,
        wbWidth=None,
        lsq_size=None,
        lq_entries=None,
        sq_entries=None,
        issueToExecuteDelay=1,
        fwd_delay=0,
        #steering_less_full=False,
    ):
        super().__init__()

        # Set pipeline widths, defaulting to frontend_width or backend_width if not specified
        self.fetchWidth = fetchWidth if fetchWidth is not None else frontend_width
        self.decodeWidth = decodeWidth if decodeWidth is not None else frontend_width
        self.renameWidth = renameWidth if renameWidth is not None else frontend_width
        self.dispatchWidth = dispatchWidth if dispatchWidth is not None else backend_width
        self.issueWidth = issueWidth if issueWidth is not None else backend_width        
        self.commitWidth = commitWidth if commitWidth is not None else backend_width
        self.wbWidth = wbWidth if wbWidth is not None else backend_width

        # Set delays
        self.issueToExecuteDelay = issueToExecuteDelay

        # Set sizes of ROB, LQ, SQ and reg files
        self.numROBEntries = rob_size
        # Ensure LSQ sizing is valid: either a common lsq_size is provided
        # or both lq_entries and sq_entries are specified separately.
        if lsq_size is None and (lq_entries is None or sq_entries is None):
            raise ValueError(
                "Either 'lsq_size' must be provided or both 'lq_entries' and 'sq_entries' must be provided"
            )
        self.LQEntries = lq_entries if lq_entries is not None else lsq_size
        self.SQEntries = sq_entries if sq_entries is not None else lsq_size

        self.numPhysIntRegs = num_int_phys_regs
        self.numPhysFloatRegs = num_fp_phys_regs

        # Enable steering to less full IQs when requested
        #self.steeringLessFull = steering_less_full

        # IQ and FU Pool configuration
        if iq_type == "replicated":
            self.instQueues = make_replicated_IQs(iq_replicated_size, num_ports, fwd_delay)
        else:
            if iq_config == "big":
                if iq_type == "distributed":
                    self.instQueues = make_bigO3_distributed_IQs(iq_int_size, iq_fp_size, iq_ls_size, fwd_delay)
                elif iq_type == "unified":
                    self.instQueues = make_bigO3_unified_IQ(iq_size, fwd_delay)
                else:
                    raise ValueError(f"Invalid iq_type '{iq_type}'. Valid options are: 'replicated', 'unified', 'distributed'")
            elif iq_config == "small":
                if iq_type == "distributed":
                    self.instQueues = make_smallO3_distributed_IQs(iq_int_size, iq_fp_size, iq_ls_size, fwd_delay)
                elif iq_type == "unified":
                    self.instQueues = make_smallO3_unified_IQ(iq_size, fwd_delay)
                else:
                    raise ValueError(f"Invalid iq_type '{iq_type}'. Valid options are: 'replicated', 'unified', 'distributed'")
            else :
                raise ValueError(f"Invalid iq_config '{iq_config}'. Valid options are: 'big', 'small'")
        
        # Configure Branch Predictor
        valid_bps = ["TournBP", "PerceptBP", "TAGE_SC_L_Big", "TAGE_SC_L_Small", "Local_BP", "BiMode_BP"]

        if bp == "TournBP":
            self.branchPred = TournBP(numEntriesBtb, numEntriesRas)

        elif bp == "TAGE_SC_L_Big":
            self.branchPred = TAGE_SC_L_Big(numEntriesBtb, numEntriesRas)

        elif bp == "TAGE_SC_L_Small":
            self.branchPred = TAGE_SC_L_Small(numEntriesBtb, numEntriesRas)

        elif bp == "PerceptBP":
            self.branchPred = PerceptBP(
                numEntriesBtb,
                tagBitsBtb,
                numEntriesRas,
                num_filter_entries,
                num_local_histories,
                local_history_length,
            )
        elif bp == "Local_BP":
            self.branchPred = Local_BP(numEntriesBtb, numEntriesRas, num_local_histories*local_history_length)

        elif bp == "BiMode_BP":
            self.branchPred = BiMode_BP(numEntriesBtb, numEntriesRas)

        else:
            raise ValueError(f"Invalid bp '{bp}'. Valid options are: {valid_bps}")


# O3StdCore hace wrap de O3CPUCore a un core compatible con la libreria estandar de gem5.
class RiscvO3StdCore(BaseCPUCore):
    def __init__(
        self,
        frontend_width,
        backend_width,
        rob_size,
        iq_size,
        num_int_phys_regs,
        num_fp_phys_regs,
        bp,
        numEntriesBtb=None,
        numEntriesRas=None,
        tagBitsBtb=None,        
        num_filter_entries=None,
        num_local_histories=None,
        local_history_length=None,
        iq_config="big",
        iq_type="unified",
        num_ports=None,
        iq_replicated_size=None,
        iq_int_size=16,
        iq_fp_size=24,
        iq_ls_size=12,
        fetchWidth=None,
        decodeWidth=None,
        renameWidth=None,
        issueWidth=None,
        dispatchWidth=None,
        commitWidth=None,
        wbWidth=None,
        lsq_size=None,
        lq_entries=None,
        sq_entries=None,
        issueToExecuteDelay=1,
        fwd_delay=0,
        #steering_less_full=False,
    ):
        core = RiscvO3Core(
            frontend_width,
            backend_width,
            rob_size,
            iq_size,
            num_int_phys_regs,
            num_fp_phys_regs,
            bp,
            numEntriesBtb,
            numEntriesRas,
            tagBitsBtb,
            num_filter_entries,
            num_local_histories,
            local_history_length,
            iq_config,
            iq_type,
            num_ports,
            iq_replicated_size,
            iq_int_size,
            iq_fp_size,
            iq_ls_size,
            fetchWidth,
            decodeWidth,
            renameWidth,
            issueWidth,
            dispatchWidth,
            commitWidth,
            wbWidth,
            lsq_size,
            lq_entries,
            sq_entries,
            issueToExecuteDelay,
            fwd_delay,
            #steering_less_full,
        )
        super().__init__(core, ISA.RISCV)


# O3Processor, junto con BaseCPUProcessor, hace wrap de O3Core a un procesador compatible con la libreria estandar de gem5.
class RiscvO3Processor(BaseCPUProcessor):
    def __init__(
        self,
        numCores,
        frontend_width,
        backend_width,
        rob_size,
        iq_size,
        num_int_phys_regs,
        num_fp_phys_regs,
        bp,
        numEntriesBtb=None,
        numEntriesRas=None,
        tagBitsBtb=None,        
        num_filter_entries=None,
        num_local_histories=None,
        local_history_length=None,
        iq_config="big",
        iq_type="unified",
        num_ports=None,
        iq_replicated_size=None,
        iq_int_size=16,
        iq_fp_size=24,
        iq_ls_size=12,
        fetchWidth=None,
        decodeWidth=None,
        renameWidth=None,
        issueWidth=None,
        dispatchWidth=None,
        commitWidth=None,
        wbWidth=None,
        lsq_size=None,
        lq_entries=None,
        sq_entries=None,
        issueToExecuteDelay=1,
        fwd_delay=0,
        #steering_less_full=False,
    ):
        cores: List[BaseCPUCore] = [
            RiscvO3StdCore(
                frontend_width,
                backend_width,
                rob_size,
                iq_size,
                num_int_phys_regs,
                num_fp_phys_regs,
                bp,
                numEntriesBtb,
                numEntriesRas,
                tagBitsBtb,
                num_filter_entries,
                num_local_histories,
                local_history_length,
                iq_config,
                iq_type,
                num_ports,
                iq_replicated_size,
                iq_int_size,
                iq_fp_size,
                iq_ls_size,
                fetchWidth,
                decodeWidth,
                renameWidth,
                issueWidth,
                dispatchWidth,
                commitWidth,
                wbWidth,
                lsq_size,
                lq_entries,
                sq_entries,
                issueToExecuteDelay,
                fwd_delay,   
                #steering_less_full,
            )
            for _ in range(numCores)
        ]
        super().__init__(cores)
