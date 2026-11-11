from m5.objects import (
    FUDesc,
    FUPool,
    OpDesc,
)

# FUDesc como puerto funcional, OpDesc son las diferentes "unidades funcionales" que tiene el puerto

# Configuracion bigO3
# Puertos:
class P0(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="FloatAdd"),
        OpDesc(opClass="FloatCmp"),
        OpDesc(opClass="FloatCvt"),
        OpDesc(opClass="FloatMult"),
        OpDesc(opClass="FloatMultAcc"),
        OpDesc(opClass="FloatDiv", opLat=2),
        OpDesc(opClass="FloatMisc"),
        OpDesc(opClass="FloatSqrt", opLat=3),
        OpDesc(opClass="SimdAdd", opLat=2),
        OpDesc(opClass="SimdAddAcc", opLat=2),
        OpDesc(opClass="SimdFloatAdd", opLat=2),
        OpDesc(opClass="SimdAlu", opLat=2),
        OpDesc(opClass="SimdFloatAlu", opLat=2),
        OpDesc(opClass="SimdCmp", opLat=2),
        OpDesc(opClass="SimdFloatCmp", opLat=2),
        OpDesc(opClass="SimdCvt", opLat=2),
        OpDesc(opClass="SimdFloatCvt", opLat=2),
        OpDesc(opClass="SimdMult", opLat=2),
        OpDesc(opClass="SimdFloatMult", opLat=2),
        OpDesc(opClass="SimdMultAcc", opLat=2),
        OpDesc(opClass="SimdFloatMultAcc", opLat=2),
        OpDesc(opClass="SimdDiv", opLat=2),
        OpDesc(opClass="SimdFloatDiv", opLat=2),
        OpDesc(opClass="SimdMisc", opLat=2),
        OpDesc(opClass="SimdFloatMisc", opLat=2),
        OpDesc(opClass="SimdSqrt", opLat=3),
        OpDesc(opClass="SimdFloatSqrt", opLat=3),
        OpDesc(opClass="SimdShift", opLat=2),
        OpDesc(opClass="SimdShiftAcc", opLat=2),
    ]
    count = 1


class P1(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="IntMult"),
        OpDesc(opClass="IntDiv", opLat=2),
        OpDesc(opClass="FloatAdd"),
        OpDesc(opClass="FloatCmp"),
        OpDesc(opClass="FloatCvt"),
        OpDesc(opClass="FloatMult"),
        OpDesc(opClass="FloatMultAcc"),
        OpDesc(opClass="FloatDiv", opLat=2),
        OpDesc(opClass="SimdAdd", opLat=2),
        OpDesc(opClass="SimdAddAcc", opLat=2),
        OpDesc(opClass="SimdFloatAdd", opLat=2),
        OpDesc(opClass="SimdAlu", opLat=2),
        OpDesc(opClass="SimdFloatAlu", opLat=2),
        OpDesc(opClass="SimdCmp", opLat=2),
        OpDesc(opClass="SimdFloatCmp", opLat=2),
        OpDesc(opClass="SimdCvt", opLat=2),
        OpDesc(opClass="SimdFloatCvt", opLat=2),
        OpDesc(opClass="SimdMult", opLat=2),
        OpDesc(opClass="SimdFloatMult", opLat=2),
        OpDesc(opClass="SimdMultAcc", opLat=2),
        OpDesc(opClass="SimdFloatMultAcc", opLat=2),
        OpDesc(opClass="SimdShift", opLat=2),
        OpDesc(opClass="SimdShiftAcc", opLat=2),
    ]
    count = 1


class P2(FUDesc):
    opList = [
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
        OpDesc(opClass="SimdUnitStrideLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideMaskLoad", opLat=2),
        OpDesc(opClass="SimdStridedLoad", opLat=2),
        OpDesc(opClass="SimdIndexedLoad", opLat=2),
        OpDesc(opClass="SimdWholeRegisterLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideFaultOnlyFirstLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideSegmentedLoad", opLat=2),
    ]
    count = 1


class P3(FUDesc):
    opList = [
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
        OpDesc(opClass="SimdUnitStrideLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideMaskLoad", opLat=2),
        OpDesc(opClass="SimdStridedLoad", opLat=2),
        OpDesc(opClass="SimdIndexedLoad", opLat=2),
        OpDesc(opClass="SimdWholeRegisterLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideFaultOnlyFirstLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideSegmentedLoad", opLat=2),
    ]
    count = 1


class P4(FUDesc):
    opList = [
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemWrite"),
        OpDesc(opClass="SimdUnitStrideStore", opLat=2),
        OpDesc(opClass="SimdUnitStrideMaskStore", opLat=2),
        OpDesc(opClass="SimdStridedStore", opLat=2),
        OpDesc(opClass="SimdIndexedStore", opLat=2),
        OpDesc(opClass="SimdWholeRegisterStore", opLat=2),
        OpDesc(opClass="SimdUnitStrideSegmentedStore", opLat=2),
    ]
    count = 1


class P5(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="IntMult"),
        OpDesc(opClass="FloatAdd"),
        OpDesc(opClass="FloatCmp"),
        OpDesc(opClass="FloatCvt"),
        OpDesc(opClass="FloatMult"),
        OpDesc(opClass="FloatMultAcc"),
        OpDesc(opClass="FloatDiv", opLat=2),
        OpDesc(opClass="Matrix"),
        OpDesc(opClass="MatrixMov"),
        OpDesc(opClass="MatrixOP"),
        OpDesc(opClass="SimdMatMultAcc", opLat=2),
        OpDesc(opClass="SimdFloatMatMultAcc", opLat=2),
        OpDesc(opClass="SimdAdd", opLat=2),
        OpDesc(opClass="SimdAddAcc", opLat=2),
        OpDesc(opClass="SimdFloatAdd", opLat=2),
        OpDesc(opClass="SimdAlu", opLat=2),
        OpDesc(opClass="SimdFloatAlu", opLat=2),
        OpDesc(opClass="SimdCmp", opLat=2),
        OpDesc(opClass="SimdFloatCmp", opLat=2),
        OpDesc(opClass="SimdCvt", opLat=2),
        OpDesc(opClass="SimdFloatCvt", opLat=2),
        OpDesc(opClass="SimdMult", opLat=2),
        OpDesc(opClass="SimdFloatMult", opLat=2),
        OpDesc(opClass="SimdMultAcc", opLat=2),
        OpDesc(opClass="SimdFloatMultAcc", opLat=2),
    ]
    count = 1


class P6(FUDesc):
    opList = [OpDesc(opClass="IntAlu")]
    count = 1

# Puertos STA
# class P7(FUDesc):
#     opList = []
#     count = 1


# class P8(FUDesc):
#     opList = []
#     count = 1


class P9(FUDesc):
    opList = [
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemWrite"),
        OpDesc(opClass="SimdUnitStrideStore", opLat=2),
        OpDesc(opClass="SimdUnitStrideMaskStore", opLat=2),
        OpDesc(opClass="SimdStridedStore", opLat=2),
        OpDesc(opClass="SimdIndexedStore", opLat=2),
        OpDesc(opClass="SimdWholeRegisterStore", opLat=2),
        OpDesc(opClass="SimdUnitStrideSegmentedStore", opLat=2),
    ]
    count = 1


class P10(FUDesc):
    opList = [
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
        OpDesc(opClass="SimdUnitStrideLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideMaskLoad", opLat=2),
        OpDesc(opClass="SimdStridedLoad", opLat=2),
        OpDesc(opClass="SimdIndexedLoad", opLat=2),
        OpDesc(opClass="SimdWholeRegisterLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideFaultOnlyFirstLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideSegmentedLoad", opLat=2),
    ]
    count = 1


class P11(FUDesc):
    opList = [OpDesc(opClass="IntAlu")]
    count = 1


# Puerto extra con las cosas raras, en principio debería usarse poco
class P12(FUDesc):
    opList = [
        #OpDesc(opClass="IprAccess"),
        OpDesc(opClass="InstPrefetch"),
        OpDesc(opClass="SimdExt", opLat=2),
        OpDesc(opClass="SimdFloatExt", opLat=2),
        OpDesc(opClass="SimdConfig"),
        OpDesc(opClass="SimdReduceAdd", opLat=2),
        OpDesc(opClass="SimdReduceAlu", opLat=2),
        OpDesc(opClass="SimdReduceCmp", opLat=2),
        OpDesc(opClass="SimdFloatReduceAdd", opLat=2),
        OpDesc(opClass="SimdFloatReduceCmp", opLat=2),
        OpDesc(opClass="SimdAes", opLat=2),
        OpDesc(opClass="SimdAesMix", opLat=2),
        OpDesc(opClass="SimdSha1Hash", opLat=2),
        OpDesc(opClass="SimdSha1Hash2", opLat=2),
        OpDesc(opClass="SimdSha256Hash", opLat=2),
        OpDesc(opClass="SimdSha256Hash2", opLat=2),
        OpDesc(opClass="SimdShaSigma2", opLat=2),
        OpDesc(opClass="SimdShaSigma3", opLat=2),
        OpDesc(opClass="SimdPredAlu", opLat=2),
    ]
    count = 1

# Pool con todos los puertos
class FUP_Big(FUPool):
    FUList = [P0(), P1(), P2(),  P3(), P4(), P5(), P6(), P9(), P10(), P11(), P12()]

# -----------------------------------------------------------------------------------------------
# Configuracion smallO3
# Puertos:
class P0(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu")
    ]
    count = 1

class P1(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu")
    ]
    count = 1

class P2(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="IntMult"),
        OpDesc(opClass="IntDiv", opLat=2),
    ]
    count = 1

class P3(FUDesc):
    opList = [
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
    ]
    count = 1

class P4(FUDesc):
    opList = [
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemWrite"),
    ]
    count = 1

class P5(FUDesc):
    opList = [
        OpDesc(opClass="FloatAdd"),
        OpDesc(opClass="FloatCmp"),
        OpDesc(opClass="FloatCvt"),
        OpDesc(opClass="FloatMult"),
        OpDesc(opClass="FloatMultAcc"),
        OpDesc(opClass="SimdAdd", opLat=4),
        OpDesc(opClass="SimdAddAcc", opLat=4),
        OpDesc(opClass="SimdAlu", opLat=4),
        OpDesc(opClass="SimdCmp", opLat=4),
        OpDesc(opClass="SimdCvt", opLat=4),
        OpDesc(opClass="SimdMult", opLat=4),
        OpDesc(opClass="SimdMultAcc", opLat=4),
        OpDesc(opClass="SimdShift", opLat=4),
        OpDesc(opClass="SimdShiftAcc", opLat=4),
        OpDesc(opClass="SimdFloatAdd", opLat=4),
        OpDesc(opClass="SimdFloatAlu", opLat=4),
        OpDesc(opClass="SimdFloatCmp", opLat=4),
        OpDesc(opClass="SimdFloatCvt", opLat=4),
        OpDesc(opClass="SimdFloatMult", opLat=4),
        OpDesc(opClass="SimdFloatMultAcc", opLat=4),
    ]
    count = 1

class P6(FUDesc):
    opList = [
        OpDesc(opClass="FloatAdd"),
        OpDesc(opClass="FloatCmp"),
        OpDesc(opClass="FloatCvt"),
        OpDesc(opClass="FloatMult"),
        OpDesc(opClass="FloatMultAcc"),
        OpDesc(opClass="FloatDiv", opLat=2),
        OpDesc(opClass="FloatMisc"),
        OpDesc(opClass="FloatSqrt", opLat=3),
        OpDesc(opClass="SimdAdd", opLat=4),
        OpDesc(opClass="SimdAddAcc", opLat=4),
        OpDesc(opClass="SimdAlu", opLat=4),
        OpDesc(opClass="SimdCmp", opLat=4),
        OpDesc(opClass="SimdCvt", opLat=4),
        OpDesc(opClass="SimdMult", opLat=4),
        OpDesc(opClass="SimdMultAcc", opLat=4),
        OpDesc(opClass="SimdShift", opLat=4),
        OpDesc(opClass="SimdShiftAcc", opLat=4),
        OpDesc(opClass="SimdFloatAdd", opLat=4),
        OpDesc(opClass="SimdFloatAlu", opLat=4),
        OpDesc(opClass="SimdFloatCmp", opLat=4),
        OpDesc(opClass="SimdFloatCvt", opLat=4),
        OpDesc(opClass="SimdFloatMult", opLat=4),
        OpDesc(opClass="SimdFloatMultAcc", opLat=4),
        OpDesc(opClass="SimdDiv", opLat=4),
        OpDesc(opClass="SimdFloatDiv", opLat=4),
        OpDesc(opClass="SimdSqrt", opLat=4),
        OpDesc(opClass="SimdFloatSqrt", opLat=4),
    ]
    count = 1

class P7(FUDesc):
    opList = [
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
        OpDesc(opClass="SimdPredAlu"),
        OpDesc(opClass="Matrix"),
        OpDesc(opClass="MatrixMov"),
        OpDesc(opClass="MatrixOP"),
        #OpDesc(opClass="IprAccess"),
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
        OpDesc(opClass="SimdExt"),
        OpDesc(opClass="SimdFloatExt"),
        OpDesc(opClass="SimdConfig"),
    ]
    count = 1

# Pool con todos los puertos
class FUP_Small(FUPool):
    FUList = [P0(), P1(), P2(),  P3(), P4(), P5(), P6(), P7()]


# ------------------------------------------------------------------------------------------------------------
# Configuracion generalizada
# Puerto general con todas las unidades funcionales:
class PGeneral(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="IntMult"),
        OpDesc(opClass="IntDiv", opLat=2),
        OpDesc(opClass="FloatAdd"),
        OpDesc(opClass="FloatCmp"),
        OpDesc(opClass="FloatCvt"),
        OpDesc(opClass="FloatMult"),
        OpDesc(opClass="FloatMultAcc"),
        OpDesc(opClass="FloatDiv", opLat=2),
        OpDesc(opClass="FloatMisc"),
        OpDesc(opClass="FloatSqrt", opLat=3),
        OpDesc(opClass="SimdAdd", opLat=2),
        OpDesc(opClass="SimdAddAcc", opLat=2),
        OpDesc(opClass="SimdAlu", opLat=2),
        OpDesc(opClass="SimdCmp", opLat=2),
        OpDesc(opClass="SimdCvt", opLat=2),
        OpDesc(opClass="SimdMisc", opLat=2),
        OpDesc(opClass="SimdMult", opLat=2),
        OpDesc(opClass="SimdMultAcc", opLat=2),
        OpDesc(opClass="SimdMatMultAcc", opLat=2),
        OpDesc(opClass="SimdShift", opLat=2),
        OpDesc(opClass="SimdShiftAcc", opLat=2),
        OpDesc(opClass="SimdDiv", opLat=2),
        OpDesc(opClass="SimdSqrt", opLat=3),
        OpDesc(opClass="SimdFloatAdd", opLat=2),
        OpDesc(opClass="SimdFloatAlu", opLat=2),
        OpDesc(opClass="SimdFloatCmp", opLat=2),
        OpDesc(opClass="SimdFloatCvt", opLat=2),
        OpDesc(opClass="SimdFloatDiv", opLat=2),
        OpDesc(opClass="SimdFloatMisc", opLat=2),
        OpDesc(opClass="SimdFloatMult", opLat=2),
        OpDesc(opClass="SimdFloatMultAcc", opLat=2),
        OpDesc(opClass="SimdFloatMatMultAcc", opLat=2),
        OpDesc(opClass="SimdFloatSqrt", opLat=3),
        OpDesc(opClass="SimdReduceAdd", opLat=2),
        OpDesc(opClass="SimdReduceAlu", opLat=2),
        OpDesc(opClass="SimdReduceCmp", opLat=2),
        OpDesc(opClass="SimdFloatReduceAdd", opLat=2),
        OpDesc(opClass="SimdFloatReduceCmp", opLat=2),
        OpDesc(opClass="SimdAes", opLat=2),
        OpDesc(opClass="SimdAesMix", opLat=2),
        OpDesc(opClass="SimdSha1Hash", opLat=2),
        OpDesc(opClass="SimdSha1Hash2", opLat=2),
        OpDesc(opClass="SimdSha256Hash", opLat=2),
        OpDesc(opClass="SimdSha256Hash2", opLat=2),
        OpDesc(opClass="SimdShaSigma2", opLat=2),
        OpDesc(opClass="SimdShaSigma3", opLat=2),
        OpDesc(opClass="SimdPredAlu", opLat=2),
        OpDesc(opClass="Matrix"),
        OpDesc(opClass="MatrixMov"),
        OpDesc(opClass="MatrixOP"),
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemRead"),
        OpDesc(opClass="FloatMemWrite"),
        #OpDesc(opClass="IprAccess"),
        OpDesc(opClass="InstPrefetch"),
        OpDesc(opClass="SimdUnitStrideLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideStore", opLat=2),
        OpDesc(opClass="SimdUnitStrideMaskLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideMaskStore", opLat=2),
        OpDesc(opClass="SimdStridedLoad", opLat=2),
        OpDesc(opClass="SimdStridedStore", opLat=2),
        OpDesc(opClass="SimdIndexedLoad", opLat=2),
        OpDesc(opClass="SimdIndexedStore", opLat=2),
        OpDesc(opClass="SimdWholeRegisterLoad", opLat=2),
        OpDesc(opClass="SimdWholeRegisterStore", opLat=2),
        OpDesc(opClass="SimdUnitStrideFaultOnlyFirstLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideSegmentedLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideSegmentedStore", opLat=2),
        OpDesc(opClass="SimdExt", opLat=2),
        OpDesc(opClass="SimdFloatExt", opLat=2),
        OpDesc(opClass="SimdConfig"),
    ]
    count = 1

class FUP_General(FUPool):
    def __init__(self, num_ports):
        super().__init__()
        self.FUList = [PGeneral() for _ in range(num_ports)]

# ---------------------------------------------------------------------------------
# Config with different ports for divided IQ  -> trying to cause a blocking scenario
# If both Mem ports are full, the one with high latencies is the one blocking,
# and the other one frees fast and could be taken as alternative
# Similarly for ALU ports
class OnlyALU(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu")
    ]
    count = 1

class CompleteALU(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="IntMult", opLat=2),
        OpDesc(opClass="IntDiv", opLat=2),
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
        OpDesc(opClass="SimdPredAlu"),
        OpDesc(opClass="Matrix"),
        OpDesc(opClass="MatrixMov"),
        OpDesc(opClass="MatrixOP"),
        #OpDesc(opClass="IprAccess"),
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
        OpDesc(opClass="SimdExt"),
        OpDesc(opClass="SimdFloatExt"),
        OpDesc(opClass="SimdConfig"),
    ]
    count = 1

class OnlyMem(FUDesc):
    opList = [
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemWrite"),
    ]
    count = 1

class StoreAndBlocking(FUDesc):
    opList = [
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemWrite"),
        OpDesc(opClass="FloatAdd", opLat=2),
        OpDesc(opClass="FloatCmp", opLat=2),
        OpDesc(opClass="FloatCvt", opLat=2),
        OpDesc(opClass="FloatMult", opLat=2),
        OpDesc(opClass="FloatMultAcc", opLat=2),
        OpDesc(opClass="FloatDiv", opLat=2),
        OpDesc(opClass="FloatMisc", opLat=2),
        OpDesc(opClass="FloatSqrt", opLat=3),
        OpDesc(opClass="SimdAdd", opLat=4),
        OpDesc(opClass="SimdAddAcc", opLat=4),
        OpDesc(opClass="SimdAlu", opLat=4),
        OpDesc(opClass="SimdCmp", opLat=4),
        OpDesc(opClass="SimdCvt", opLat=4),
        OpDesc(opClass="SimdMult", opLat=4),
        OpDesc(opClass="SimdMultAcc", opLat=4),
        OpDesc(opClass="SimdShift", opLat=4),
        OpDesc(opClass="SimdShiftAcc", opLat=4),
        OpDesc(opClass="SimdFloatAdd", opLat=4),
        OpDesc(opClass="SimdFloatAlu", opLat=4),
        OpDesc(opClass="SimdFloatCmp", opLat=4),
        OpDesc(opClass="SimdFloatCvt", opLat=4),
        OpDesc(opClass="SimdFloatMult", opLat=4),
        OpDesc(opClass="SimdFloatMultAcc", opLat=4),
        OpDesc(opClass="SimdDiv", opLat=4),
        OpDesc(opClass="SimdFloatDiv", opLat=4),
        OpDesc(opClass="SimdSqrt", opLat=4),
        OpDesc(opClass="SimdFloatSqrt", opLat=4),
    ]
    count = 1

# Pool con todos los puertos
class FUP_Different(FUPool):
    FUList = [OnlyALU(), CompleteALU(), OnlyMem(), StoreAndBlocking()]