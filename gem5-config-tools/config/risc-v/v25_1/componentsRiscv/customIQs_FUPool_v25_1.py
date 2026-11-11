from m5.objects import (
    FUDesc,
    FUPool,
    OpDesc,
    IQUnit,
)

# Misc operations added to every port
def _simd_misc_ops():
    """Common SIMD/misc operations added to many ports."""
    return [
        OpDesc(opClass="SimdAdd"),
        OpDesc(opClass="SimdAddAcc"),
        OpDesc(opClass="SimdAlu"),
        OpDesc(opClass="SimdCmp"),
        OpDesc(opClass="SimdCvt"),
        OpDesc(opClass="SimdMult"),
        OpDesc(opClass="SimdMultAcc"),
        OpDesc(opClass="SimdShift"),
        OpDesc(opClass="SimdShiftAcc"),
        OpDesc(opClass="SimdFloatAdd"),
        OpDesc(opClass="SimdFloatAlu"),
        OpDesc(opClass="SimdFloatCmp"),
        OpDesc(opClass="SimdFloatCvt"),
        OpDesc(opClass="SimdFloatMult"),
        OpDesc(opClass="SimdFloatMultAcc"),
        OpDesc(opClass="SimdDiv"),
        OpDesc(opClass="SimdFloatDiv"),
        OpDesc(opClass="SimdSqrt"),
        OpDesc(opClass="SimdFloatSqrt"),
        OpDesc(opClass="SimdMisc"),
        OpDesc(opClass="SimdFloatMisc"),
        OpDesc(opClass="SimdFloatMatMultAcc"),
        OpDesc(opClass="SimdReduceAdd"),
        OpDesc(opClass="SimdReduceAlu"),
        OpDesc(opClass="SimdReduceCmp"),
        OpDesc(opClass="SimdFloatReduceAdd"),
        OpDesc(opClass="SimdFloatReduceCmp"),
        OpDesc(opClass="SimdAes"),
        OpDesc(opClass="SimdAesMix"),
        OpDesc(opClass="SimdSha1Hash"),
        OpDesc(opClass="SimdSha1Hash2"),
        OpDesc(opClass="SimdSha256Hash"),
        OpDesc(opClass="SimdSha256Hash2"),
        OpDesc(opClass="SimdShaSigma2"),
        OpDesc(opClass="SimdShaSigma3"),
        OpDesc(opClass="SimdSha3"),
        OpDesc(opClass="SimdSm4e"),
        OpDesc(opClass="SimdCrc"),
        OpDesc(opClass="SimdPredAlu"),
        OpDesc(opClass="SimdDotProd"),
        OpDesc(opClass="Matrix"),
        OpDesc(opClass="MatrixMov"),
        OpDesc(opClass="MatrixOP"),
        OpDesc(opClass="InstPrefetch"),
        OpDesc(opClass="SimdUnitStrideLoad"),
        OpDesc(opClass="SimdUnitStrideStore"),
        OpDesc(opClass="SimdUnitStrideMaskLoad"),
        OpDesc(opClass="SimdUnitStrideMaskStore"),
        OpDesc(opClass="SimdStridedLoad"),
        OpDesc(opClass="SimdStridedStore"),
        OpDesc(opClass="SimdIndexedLoad"),
        OpDesc(opClass="SimdIndexedStore"),
        OpDesc(opClass="SimdWholeRegisterLoad"),
        OpDesc(opClass="SimdWholeRegisterStore"),
        OpDesc(opClass="SimdUnitStrideFaultOnlyFirstLoad"),
        OpDesc(opClass="SimdUnitStrideSegmentedLoad"),
        OpDesc(opClass="SimdUnitStrideSegmentedStore"),
        OpDesc(opClass="SimdUnitStrideSegmentedFaultOnlyFirstLoad"),
        OpDesc(opClass="SimdStrideSegmentedLoad"),
        OpDesc(opClass="SimdStrideSegmentedStore"),
        OpDesc(opClass="SimdExt"),
        OpDesc(opClass="SimdFloatExt"),
        OpDesc(opClass="SimdConfig"),
        OpDesc(opClass="SimdBf16Add"),
        OpDesc(opClass="SimdBf16Cmp"),
        OpDesc(opClass="SimdBf16Cvt"),
        OpDesc(opClass="SimdBf16DotProd"),
        OpDesc(opClass="SimdBf16MatMultAcc"),
        OpDesc(opClass="SimdBf16Mult"),
        OpDesc(opClass="SimdBf16MultAcc"),
        OpDesc(opClass="Bf16Cvt"),
        OpDesc(opClass="System"),
    ]

def _apply_extra_cycles(iq_list, extra_cycles):
    """
    Helper to apply extra latency to all ops in the IQ list,
    excluding those found in _simd_misc_ops.
    """
    if not extra_cycles or extra_cycles == 0:
        return iq_list

    # Define the list of OpClasses to exclude (those from _simd_misc_ops)
    # as strings to avoid instantiating orphan SimObjects.
    excluded_op_classes = {
        "SimdAdd", "SimdAddAcc", "SimdAlu", "SimdCmp", "SimdCvt", "SimdMult",
        "SimdMultAcc", "SimdShift", "SimdShiftAcc", "SimdFloatAdd",
        "SimdFloatAlu", "SimdFloatCmp", "SimdFloatCvt", "SimdFloatMult",
        "SimdFloatMultAcc", "SimdDiv", "SimdFloatDiv", "SimdSqrt",
        "SimdFloatSqrt", "SimdMisc", "SimdFloatMisc", "SimdFloatMatMultAcc",
        "SimdReduceAdd", "SimdReduceAlu", "SimdReduceCmp", "SimdFloatReduceAdd",
        "SimdFloatReduceCmp", "SimdAes", "SimdAesMix", "SimdSha1Hash",
        "SimdSha1Hash2", "SimdSha256Hash", "SimdSha256Hash2", "SimdShaSigma2",
        "SimdShaSigma3", "SimdSha3", "SimdSm4e", "SimdCrc", "SimdPredAlu",
        "SimdDotProd", "Matrix", "MatrixMov", "MatrixOP", "InstPrefetch",
        "SimdUnitStrideLoad", "SimdUnitStrideStore", "SimdUnitStrideMaskLoad",
        "SimdUnitStrideMaskStore", "SimdStridedLoad", "SimdStridedStore",
        "SimdIndexedLoad", "SimdIndexedStore", "SimdWholeRegisterLoad",
        "SimdWholeRegisterStore", "SimdUnitStrideFaultOnlyFirstLoad",
        "SimdUnitStrideSegmentedLoad", "SimdUnitStrideSegmentedStore",
        "SimdUnitStrideSegmentedFaultOnlyFirstLoad", "SimdStrideSegmentedLoad",
        "SimdStrideSegmentedStore", "SimdExt", "SimdFloatExt", "SimdConfig",
        "SimdBf16Add", "SimdBf16Cmp", "SimdBf16Cvt", "SimdBf16DotProd",
        "SimdBf16MatMultAcc", "SimdBf16Mult", "SimdBf16MultAcc", "Bf16Cvt",
        "System"
    }

    for iq in iq_list:
        if not iq.fuPool:
            continue
            
        for fu in iq.fuPool.FUList:
            for op in fu.opList:
                if str(op.opClass) not in excluded_op_classes:
                    # It's a target op: add extra latency
                    # Default latency is 1 if not specified
                    current_lat = int(getattr(op, 'opLat', 1))
                    op.opLat = current_lat + extra_cycles

    return iq_list

# -----------------------------------------------------------------------------------
# BigO3 riscv distributed port configuration 
# Integer

#ALU, Div
class P1_Big_Riscv_Distributed(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="IntDiv", opLat=3, pipelined=False),
    ] + _simd_misc_ops()
    count = 1

# Alu, Mult
class P2_Big_Riscv_Distributed(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="IntMult"),
    ] + _simd_misc_ops()
    count = 1

# Alu, Mult
class P3_Big_Riscv_Distributed(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="IntMult"),
    ] + _simd_misc_ops()
    count = 1

# ALU
class P4_Big_Riscv_Distributed(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
    ] + _simd_misc_ops()
    count = 1

# ALU, Branch
class P5_Big_Riscv_Distributed(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        #Branch unit is not modelled in gem5 o3 cpu
    ] + _simd_misc_ops()
    count = 1

# ALU, Branch
class P6_Big_Riscv_Distributed(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
    ] + _simd_misc_ops()
    count = 1

# FP
#Alu, Mult, MAC, Div, Sqrt
class P7_Big_Riscv_Distributed(FUDesc):
    opList = [
        OpDesc(opClass="FloatAdd", opLat=3),
        OpDesc(opClass="FloatCmp", opLat=3),
        OpDesc(opClass="FloatCvt", opLat=3),
        OpDesc(opClass="FloatMult", opLat=3),
        OpDesc(opClass="FloatMultAcc", opLat=5),
        OpDesc(opClass="FloatMisc", opLat=3),
        OpDesc(opClass="FloatDiv", opLat=5, pipelined=False),
        OpDesc(opClass="FloatSqrt", opLat=5, pipelined=False),
    ] + _simd_misc_ops()
    count = 1

# Alu, Mult, MAC
class P8_Big_Riscv_Distributed(FUDesc):
    opList = [
        OpDesc(opClass="FloatAdd", opLat=3),
        OpDesc(opClass="FloatCmp", opLat=3),
        OpDesc(opClass="FloatCvt", opLat=3),
        OpDesc(opClass="FloatMult", opLat=3),
        OpDesc(opClass="FloatMultAcc", opLat=5),
    ] + _simd_misc_ops()
    count = 1

# Alu, Mult, MAC
class P9_Big_Riscv_Distributed(FUDesc):
    opList = [
        OpDesc(opClass="FloatAdd", opLat=3),
        OpDesc(opClass="FloatCmp", opLat=3),
        OpDesc(opClass="FloatCvt", opLat=3),
        OpDesc(opClass="FloatMult", opLat=3),
        OpDesc(opClass="FloatMultAcc", opLat=5),
    ] + _simd_misc_ops()
    count = 1

# Memory
# Load
class P10_Big_Riscv_Distributed(FUDesc):
    opList = [
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
    ] + _simd_misc_ops()
    count = 1

# Load-Store
class P11_Big_Riscv_Distributed(FUDesc):
    opList = [
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemWrite"),
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
    ] + _simd_misc_ops()
    count = 1

# Load-Store
class P12_Big_Riscv_Distributed(FUDesc):
    opList = [
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemWrite"),
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
    ] + _simd_misc_ops()
    count = 1

# -----------------------------------------------------------------------------------
# BigO3 riscv UNIFIED port configuration (sin misc ops duplicadas)
# Integer

#ALU, Div
class P1_Big_Riscv_Unified(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="IntDiv", opLat=3, pipelined=False),
    ]
    count = 1

# Alu, Mult
class P2_Big_Riscv_Unified(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="IntMult"),
    ]
    count = 1

# Alu, Mult
class P3_Big_Riscv_Unified(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="IntMult"),
    ]
    count = 1

# ALU
class P4_Big_Riscv_Unified(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
    ]
    count = 1

# ALU, Branch
class P5_Big_Riscv_Unified(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
    ]
    count = 1

# ALU, Branch
class P6_Big_Riscv_Unified(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
    ]
    count = 1

# FP - Alu, Mult, MAC, Div, Sqrt
class P7_Big_Riscv_Unified(FUDesc):
    opList = [
        OpDesc(opClass="FloatAdd", opLat=3),
        OpDesc(opClass="FloatCmp", opLat=3),
        OpDesc(opClass="FloatCvt", opLat=3),
        OpDesc(opClass="FloatMult", opLat=3),
        OpDesc(opClass="FloatMultAcc", opLat=5),
        OpDesc(opClass="FloatMisc", opLat=3),
        OpDesc(opClass="FloatDiv", opLat=5, pipelined=False),
        OpDesc(opClass="FloatSqrt", opLat=5, pipelined=False),
    ]
    count = 1

# Alu, Mult, MAC
class P8_Big_Riscv_Unified(FUDesc):
    opList = [
        OpDesc(opClass="FloatAdd", opLat=3),
        OpDesc(opClass="FloatCmp", opLat=3),
        OpDesc(opClass="FloatCvt", opLat=3),
        OpDesc(opClass="FloatMult", opLat=3),
        OpDesc(opClass="FloatMultAcc", opLat=5),
    ]
    count = 1

# Alu, Mult, MAC
class P9_Big_Riscv_Unified(FUDesc):
    opList = [
        OpDesc(opClass="FloatAdd", opLat=3),
        OpDesc(opClass="FloatCmp", opLat=3),
        OpDesc(opClass="FloatCvt", opLat=3),
        OpDesc(opClass="FloatMult", opLat=3),
        OpDesc(opClass="FloatMultAcc", opLat=5),
    ]
    count = 1

# Memory - Load
class P10_Big_Riscv_Unified(FUDesc):
    opList = [
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
    ]
    count = 1

# Store
class P11_Big_Riscv_Unified(FUDesc):
    opList = [
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemWrite"),
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
    ]
    count = 1

# Store
class P12_Big_Riscv_Unified(FUDesc):
    opList = [
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemWrite"),
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
    ]
    count = 1

# Dedicated port for SIMD/misc in unified configuration
class P_Misc_Riscv_Unified(FUDesc):
    opList = _simd_misc_ops()
    count = 1

# -----------------------------------------------------------------------------------
# FUPools for distributed configuration
class BigO3_P1_FUP_Distributed(FUPool):
    FUList = [P1_Big_Riscv_Distributed(count=1)]

class BigO3_P2_FUP_Distributed(FUPool):
    FUList = [P2_Big_Riscv_Distributed(count=1)]

class BigO3_P3_FUP_Distributed(FUPool):
    FUList = [P3_Big_Riscv_Distributed(count=1)]

class BigO3_P4_FUP_Distributed(FUPool):
    FUList = [P4_Big_Riscv_Distributed(count=1)]

class BigO3_P5_FUP_Distributed(FUPool):
    FUList = [P5_Big_Riscv_Distributed(count=1)]

class BigO3_P6_FUP_Distributed(FUPool):
    FUList = [P6_Big_Riscv_Distributed(count=1)]

class BigO3_P7_FUP_Distributed(FUPool):
    FUList = [P7_Big_Riscv_Distributed(count=1)]

class BigO3_P8_FUP_Distributed(FUPool):
    FUList = [P8_Big_Riscv_Distributed(count=1)]

class BigO3_P9_FUP_Distributed(FUPool):
    FUList = [P9_Big_Riscv_Distributed(count=1)]

class BigO3_P10_FUP_Distributed(FUPool):
    FUList = [P10_Big_Riscv_Distributed(count=1)]

class BigO3_P11_FUP_Distributed(FUPool):
    FUList = [P11_Big_Riscv_Distributed(count=1)]

class BigO3_P12_FUP_Distributed(FUPool):
    FUList = [P12_Big_Riscv_Distributed(count=1)]

# -----------------------------------------------------------------------------------
# BigO3 Riscv unified port configuration
class FUP_Big_Riscv_Unified(FUPool):
    FUList = [
        P1_Big_Riscv_Unified(count=1),
        P2_Big_Riscv_Unified(count=1),
        P3_Big_Riscv_Unified(count=1),
        P4_Big_Riscv_Unified(count=1),
        P5_Big_Riscv_Unified(count=1),
        P6_Big_Riscv_Unified(count=1),
        P7_Big_Riscv_Unified(count=1),
        P8_Big_Riscv_Unified(count=1),
        P9_Big_Riscv_Unified(count=1),
        P10_Big_Riscv_Unified(count=1),
        P11_Big_Riscv_Unified(count=1),
        P12_Big_Riscv_Unified(count=1),
        P_Misc_Riscv_Unified(count=1),
    ]

# -----------------------------------------------------------------------------------
# IQ CONFIGURATIONS - Distributed

class BigO3_IQ0(IQUnit):
    """Scheduler 0: Integer ALU, Div"""
    numEntries = 16
    fuPool = BigO3_P1_FUP_Distributed()

class BigO3_IQ1(IQUnit):
    """Scheduler 1: Integer ALU, Mult"""
    numEntries = 16
    fuPool = BigO3_P2_FUP_Distributed()

class BigO3_IQ2(IQUnit):
    """Scheduler 2: Integer ALU, Mult"""
    numEntries = 16
    fuPool = BigO3_P3_FUP_Distributed()

class BigO3_IQ3(IQUnit):
    """Scheduler 3: Integer ALU"""
    numEntries = 16
    fuPool = BigO3_P4_FUP_Distributed()

class BigO3_IQ4(IQUnit):
    """Scheduler 4: Integer ALU, Branch"""
    numEntries = 16
    fuPool = BigO3_P5_FUP_Distributed()

class BigO3_IQ5(IQUnit):
    """Scheduler 5: Integer ALU, Branch"""
    numEntries = 16
    fuPool = BigO3_P6_FUP_Distributed()

class BigO3_IQ6(IQUnit):
    """Scheduler 6: Floating Point ALU, Mult, MAC, Div, Sqrt"""
    numEntries = 24
    fuPool = BigO3_P7_FUP_Distributed()

class BigO3_IQ7(IQUnit):
    """Scheduler 7: Floating Point ALU, Mult, MAC"""
    numEntries = 24
    fuPool = BigO3_P8_FUP_Distributed()

class BigO3_IQ8(IQUnit):
    """Scheduler 8: Floating Point ALU, Mult, MAC"""
    numEntries = 24
    fuPool = BigO3_P9_FUP_Distributed()

class BigO3_IQ9(IQUnit):
    """Scheduler 9: Load"""
    numEntries = 12
    fuPool = BigO3_P10_FUP_Distributed()

class BigO3_IQ10(IQUnit):
    """Scheduler 10: Store"""
    numEntries = 12
    fuPool = BigO3_P11_FUP_Distributed()

class BigO3_IQ11(IQUnit):
    """Scheduler 11: Store"""
    numEntries = 12
    fuPool = BigO3_P12_FUP_Distributed()

# -------------------------------------------------------------------------
# Big O3 Riscv Unified IQ configuration
class BigO3_Uni_IQ(IQUnit):
    """Unified Scheduler: All Functional Units"""
    numEntries = 180
    fuPool = FUP_Big_Riscv_Unified()

# -------------------------------------------------------------------------
# Factory functions for parameterized IQ configurations

def make_bigO3_distributed_IQs(iq_int_size=16, iq_fp_size=24, iq_ls_size=12, extraCycles=0):
    """Create distributed IQ configuration with custom sizes."""
    iq0 = BigO3_IQ0()
    iq0.numEntries = iq_int_size
    
    iq1 = BigO3_IQ1()
    iq1.numEntries = iq_int_size
    
    iq2 = BigO3_IQ2()
    iq2.numEntries = iq_int_size
    
    iq3 = BigO3_IQ3()
    iq3.numEntries = iq_int_size
    
    iq4 = BigO3_IQ4()
    iq4.numEntries = iq_int_size
    
    iq5 = BigO3_IQ5()
    iq5.numEntries = iq_int_size
    
    iq6 = BigO3_IQ6()
    iq6.numEntries = iq_fp_size
    
    iq7 = BigO3_IQ7()
    iq7.numEntries = iq_fp_size
    
    iq8 = BigO3_IQ8()
    iq8.numEntries = iq_fp_size
    
    iq9 = BigO3_IQ9()
    iq9.numEntries = iq_ls_size
    
    iq10 = BigO3_IQ10()
    iq10.numEntries = iq_ls_size
    
    iq11 = BigO3_IQ11()
    iq11.numEntries = iq_ls_size
    
    return _apply_extra_cycles([iq0, iq1, iq2, iq3, iq4, iq5, iq6, iq7, iq8, iq9, iq10, iq11], extraCycles)

def make_bigO3_unified_IQ(iq_size=180, extraCycles=0):
    """Create unified IQ configuration with custom size."""
    iq = BigO3_Uni_IQ()
    iq.numEntries = iq_size
    return _apply_extra_cycles([iq], extraCycles)

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
# Small O3 Riscv distributed port configuration
# Integer

#ALU, Div
class P1_Small_Riscv_Distributed(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="IntDiv", opLat=3, pipelined=False),
    ]  + _simd_misc_ops()
    count = 1

# Alu, Mult
class P2_Small_Riscv_Distributed(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="IntMult"),
    ] + _simd_misc_ops()
    count = 1

# ALU
class P3_Small_Riscv_Distributed(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
    ] + _simd_misc_ops()
    count = 1

# FP
#Alu, Mult, MAC, Div, Sqrt
class P4_Small_Riscv_Distributed(FUDesc):
    opList = [
        OpDesc(opClass="FloatAdd", opLat=3),
        OpDesc(opClass="FloatCmp", opLat=3),
        OpDesc(opClass="FloatCvt", opLat=3),
        OpDesc(opClass="FloatMult", opLat=3),
        OpDesc(opClass="FloatMultAcc", opLat=5),
        OpDesc(opClass="FloatMisc", opLat=3),
        OpDesc(opClass="FloatDiv", opLat=5, pipelined=False),
        OpDesc(opClass="FloatSqrt", opLat=5, pipelined=False),
    ] + _simd_misc_ops()
    count = 1

# Memory
# Load
class P5_Small_Riscv_Distributed(FUDesc):
    opList = [
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
    ] + _simd_misc_ops()
    count = 1

# Load, store
class P6_Small_Riscv_Distributed(FUDesc):
    opList = [
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemWrite"),
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
    ] + _simd_misc_ops()
    count = 1

# -----------------------------------------------------------------------------------
# SmallO3 riscv UNIFIED port configuration (sin misc ops duplicadas)
#ALU, Div
class P1_Small_Riscv_Unified(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="IntDiv", opLat=3, pipelined=False),
    ]
    count = 1

# Alu, Mult
class P2_Small_Riscv_Unified(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="IntMult"),
    ]
    count = 1

# ALU
class P3_Small_Riscv_Unified(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
    ]
    count = 1

# FP
#Alu, Mult, MAC, Div, Sqrt
class P4_Small_Riscv_Unified(FUDesc):
    opList = [
        OpDesc(opClass="FloatAdd", opLat=3),
        OpDesc(opClass="FloatCmp", opLat=3),
        OpDesc(opClass="FloatCvt", opLat=3),
        OpDesc(opClass="FloatMult", opLat=3),
        OpDesc(opClass="FloatMultAcc", opLat=5),
        OpDesc(opClass="FloatMisc", opLat=3),
        OpDesc(opClass="FloatDiv", opLat=5, pipelined=False),
        OpDesc(opClass="FloatSqrt", opLat=5, pipelined=False),
    ]
    count = 1

# Memory
# Load
class P5_Small_Riscv_Unified(FUDesc):
    opList = [
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
    ]
    count = 1

# Load, store
class P6_Small_Riscv_Unified(FUDesc):
    opList = [
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemWrite"),
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
    ]
    count = 1

# -----------------------------------------------------------------------------------
# FUPools for distributed configuration
class SmallO3_P1_FUP_Distributed(FUPool):
    FUList = [P1_Small_Riscv_Distributed(count=1)]

class SmallO3_P2_FUP_Distributed(FUPool):
    FUList = [P2_Small_Riscv_Distributed(count=1)]

class SmallO3_P3_FUP_Distributed(FUPool):
    FUList = [P3_Small_Riscv_Distributed(count=1)]

class SmallO3_P4_FUP_Distributed(FUPool):
    FUList = [P4_Small_Riscv_Distributed(count=1)]

class SmallO3_P5_FUP_Distributed(FUPool):
    FUList = [P5_Small_Riscv_Distributed(count=1)]

class SmallO3_P6_FUP_Distributed(FUPool):
    FUList = [P6_Small_Riscv_Distributed(count=1)]

# -----------------------------------------------------------------------------------
# SmallO3 Riscv unified port configuration
class FUP_Small_Riscv_Unified(FUPool):
    FUList = [
        P1_Small_Riscv_Unified(count=1),
        P2_Small_Riscv_Unified(count=1),
        P3_Small_Riscv_Unified(count=1),
        P4_Small_Riscv_Unified(count=1),
        P5_Small_Riscv_Unified(count=1),
        P6_Small_Riscv_Unified(count=1),
        P_Misc_Riscv_Unified(count=1),
    ]

# -----------------------------------------------------------------------------------
# IQ CONFIGURATIONS - Distributed

class SmallO3_IQ0(IQUnit):
    """Scheduler 0: Integer ALU, Div"""
    numEntries = 8
    fuPool = SmallO3_P1_FUP_Distributed()


class SmallO3_IQ1(IQUnit):
    """Scheduler 1: Integer ALU, Mult"""
    numEntries = 8
    fuPool = SmallO3_P2_FUP_Distributed()

class SmallO3_IQ2(IQUnit):
    """Scheduler 2: Integer ALU"""
    numEntries = 8
    fuPool = SmallO3_P3_FUP_Distributed()


class SmallO3_IQ3(IQUnit):
    """Scheduler 3: Floating Point ALU, Mult, MAC, Div, Sqrt"""
    numEntries = 12
    fuPool = SmallO3_P4_FUP_Distributed()


class SmallO3_IQ4(IQUnit):
    """Scheduler 4: Load"""
    numEntries = 6
    fuPool = SmallO3_P5_FUP_Distributed()

class SmallO3_IQ5(IQUnit):
    """Scheduler 5: Load, Store"""
    numEntries = 6
    fuPool = SmallO3_P6_FUP_Distributed()

# -------------------------------------------------------------------------
# SmallO3 Riscv Unified IQ configuration
class SmallO3_Uni_IQ(IQUnit):
    """Unified Scheduler: All Functional Units"""
    numEntries = 48
    fuPool = FUP_Small_Riscv_Unified()

# -------------------------------------------------------------------------
# Factory functions for parameterized IQ configurations

def make_smallO3_distributed_IQs(iq_int_size=12, iq_fp_size=12, iq_ls_size=12, extraCycles=0):
    """Create distributed IQ configuration with custom sizes."""
    iq0 = SmallO3_IQ0()
    iq0.numEntries = iq_int_size
    
    iq1 = SmallO3_IQ1()
    iq1.numEntries = iq_int_size
    
    iq2 = SmallO3_IQ2()
    iq2.numEntries = iq_int_size

    iq3 = SmallO3_IQ2()
    iq3.numEntries = iq_int_size
    
    iq4 = SmallO3_IQ3()
    iq4.numEntries = iq_fp_size

    iq5 = SmallO3_IQ3()
    iq5.numEntries = iq_fp_size
    
    iq6 = SmallO3_IQ4()
    iq6.numEntries = iq_ls_size
    
    iq7 = SmallO3_IQ5()
    iq7.numEntries = iq_ls_size
    
    return _apply_extra_cycles([iq0, iq1, iq2, iq3, iq4, iq5, iq6, iq7], extraCycles)

def make_smallO3_unified_IQ(iq_size=72, extraCycles=0):
    """Create unified IQ configuration with custom size."""
    iq = SmallO3_Uni_IQ()
    iq.numEntries = iq_size
    return _apply_extra_cycles([iq], extraCycles)


# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
# Replicated riscv port configuration - all ports have all the operations
def _replicated_ops():
    """All operations replicated on every port."""
    return [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="IntMult"),
        OpDesc(opClass="IntDiv", opLat=3, pipelined=False),
        OpDesc(opClass="FloatAdd", opLat=3),
        OpDesc(opClass="FloatCmp", opLat=3),
        OpDesc(opClass="FloatCvt", opLat=3),
        OpDesc(opClass="FloatMult", opLat=3),
        OpDesc(opClass="FloatMultAcc", opLat=5),
        OpDesc(opClass="FloatMisc", opLat=3),
        OpDesc(opClass="FloatDiv", opLat=5, pipelined=False),
        OpDesc(opClass="FloatSqrt", opLat=5, pipelined=False),
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemRead"),
        OpDesc(opClass="FloatMemWrite"),

        # SIMD and misc ops
        OpDesc(opClass="SimdAdd"),
        OpDesc(opClass="SimdAddAcc"),
        OpDesc(opClass="SimdAlu"),
        OpDesc(opClass="SimdCmp"),
        OpDesc(opClass="SimdCvt"),
        OpDesc(opClass="SimdMisc"),
        OpDesc(opClass="SimdMult"),
        OpDesc(opClass="SimdMultAcc"),
        OpDesc(opClass="SimdMatMultAcc"),
        OpDesc(opClass="SimdShift"),
        OpDesc(opClass="SimdShiftAcc"),
        OpDesc(opClass="SimdDiv"),
        OpDesc(opClass="SimdSqrt"),
        OpDesc(opClass="SimdFloatAdd"),
        OpDesc(opClass="SimdFloatAlu"),
        OpDesc(opClass="SimdFloatCmp"),
        OpDesc(opClass="SimdFloatCvt"),
        OpDesc(opClass="SimdFloatDiv"),
        OpDesc(opClass="SimdFloatMisc"),
        OpDesc(opClass="SimdFloatMult"),
        OpDesc(opClass="SimdFloatMultAcc"),
        OpDesc(opClass="SimdFloatMatMultAcc"),
        OpDesc(opClass="SimdFloatSqrt"),
        OpDesc(opClass="SimdReduceAdd"),
        OpDesc(opClass="SimdReduceAlu"),
        OpDesc(opClass="SimdReduceCmp"),
        OpDesc(opClass="SimdFloatReduceAdd"),
        OpDesc(opClass="SimdFloatReduceCmp"),
        OpDesc(opClass="SimdAes"),
        OpDesc(opClass="SimdAesMix"),
        OpDesc(opClass="SimdSha1Hash"),
        OpDesc(opClass="SimdSha1Hash2"),
        OpDesc(opClass="SimdSha256Hash"),
        OpDesc(opClass="SimdSha256Hash2"),
        OpDesc(opClass="SimdShaSigma2"),
        OpDesc(opClass="SimdShaSigma3"),
        OpDesc(opClass="SimdSha3"),
        OpDesc(opClass="SimdSm4e"),
        OpDesc(opClass="SimdCrc"),
        OpDesc(opClass="SimdPredAlu"),
        OpDesc(opClass="SimdDotProd"),
        OpDesc(opClass="Matrix"),
        OpDesc(opClass="MatrixMov"),
        OpDesc(opClass="MatrixOP"),
        OpDesc(opClass="InstPrefetch"),
        OpDesc(opClass="SimdUnitStrideLoad"),
        OpDesc(opClass="SimdUnitStrideStore"),
        OpDesc(opClass="SimdUnitStrideMaskLoad"),
        OpDesc(opClass="SimdUnitStrideMaskStore"),
        OpDesc(opClass="SimdStridedLoad"),
        OpDesc(opClass="SimdStridedStore"),
        OpDesc(opClass="SimdIndexedLoad"),
        OpDesc(opClass="SimdIndexedStore"),
        OpDesc(opClass="SimdWholeRegisterLoad"),
        OpDesc(opClass="SimdWholeRegisterStore"),
        OpDesc(opClass="SimdUnitStrideFaultOnlyFirstLoad"),
        OpDesc(opClass="SimdUnitStrideSegmentedLoad"),
        OpDesc(opClass="SimdUnitStrideSegmentedStore"),
        OpDesc(opClass="SimdUnitStrideSegmentedFaultOnlyFirstLoad"),
        OpDesc(opClass="SimdStrideSegmentedLoad"),
        OpDesc(opClass="SimdStrideSegmentedStore"),
        OpDesc(opClass="SimdExt"),
        OpDesc(opClass="SimdFloatExt"),
        OpDesc(opClass="SimdConfig"),
        OpDesc(opClass="SimdBf16Add"),
        OpDesc(opClass="SimdBf16Cmp"),
        OpDesc(opClass="SimdBf16Cvt"),
        OpDesc(opClass="SimdBf16DotProd"),
        OpDesc(opClass="SimdBf16MatMultAcc"),
        OpDesc(opClass="SimdBf16Mult"),
        OpDesc(opClass="SimdBf16MultAcc"),
        OpDesc(opClass="Bf16Cvt"),
    ]

# -------------------------------------------------------------------------
# Factory functions for parameterized IQ configurations
def make_replicated_IQs(iq_size, num_ports, extraCycles=0):
    """Create replicated IQ configuration with custom size and number of ports."""
    iq_list = []
    for i in range(num_ports):
        iq = IQUnit()
        iq.numEntries = iq_size
        iq.fuPool = FUPool(FUList=[FUDesc(opList=_replicated_ops(), count=1)])
        iq_list.append(iq)
    return _apply_extra_cycles(iq_list, extraCycles)