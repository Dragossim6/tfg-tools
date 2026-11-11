from m5.objects import *

class BTB(SimpleBTB):
    def __init__(self, numEntries, tagBits):
        super(BTB, self).__init__()
        self.numEntries = numEntries
        self.tagBits = tagBits
        self.associativity = 4
        self.instShiftAmt = 2
        self.btbReplPolicy = LRURP()
        self.btbIndexingPolicy = BTBSetAssociative(
            num_entries=Parent.numEntries,
            set_shift=Parent.instShiftAmt,
            assoc=Parent.associativity,
            tag_bits=Parent.tagBits,
        )

class TournBP(TournamentBP):
    def __init__(self, numEntriesBtb, numEntriesRas):
        super(TournBP, self).__init__()
        self.btb = BTB(numEntries=numEntriesBtb, tagBits=10)
        self.ras = ReturnAddrStack(numEntries=numEntriesRas)

class PerceptBP(MultiperspectivePerceptron8KB):
    def __init__(self, numEntriesBtb, tagBitsBtb, numEntriesRas, num_filter_entries, num_local_histories, local_history_length):
        super(PerceptBP, self).__init__()
        self.btb = BTB(numEntries=numEntriesBtb, tagBits=tagBitsBtb)
        self.ras = ReturnAddrStack(numEntries=numEntriesRas)
        self.num_filter_entries = num_filter_entries
        self.num_local_histories = num_local_histories
        self.local_history_length = local_history_length

class TAGE_SC_L_Big(BranchPredictor):
    def __init__(self, numEntriesBtb, numEntriesRas):
        super(TAGE_SC_L_Big, self).__init__()
        self.conditionalBranchPred = TAGE_SC_L_64KB()
        self.btb = BTB(numEntries=numEntriesBtb, tagBits=18)
        self.ras = ReturnAddrStack(numEntries=numEntriesRas)
        self.instShiftAmt = 2
        self.requiresBTBHit = True
        self.takenOnlyHistory = True

class TAGE_SC_L_Small(BranchPredictor):
    def __init__(self, numEntriesBtb, numEntriesRas):
        super(TAGE_SC_L_Small, self).__init__()
        self.conditionalBranchPred = TAGE_SC_L_8KB()
        self.btb = BTB(numEntries=numEntriesBtb, tagBits=10)
        self.ras = ReturnAddrStack(numEntries=numEntriesRas)
        self.instShiftAmt = 2
        self.requiresBTBHit = True
        self.takenOnlyHistory = True

class Local_BP(LocalBP):
    def __init__(self, numEntriesBtb, numEntriesRas, predictorSize):
        super(Local_BP, self).__init__()
        self.btb = BTB(numEntries=numEntriesBtb, tagBits=10)
        self.localPredictorSize = predictorSize
        self.ras = ReturnAddrStack(numEntries=numEntriesRas)

class BiMode_BP(BranchPredictor):
    def __init__(self, numEntriesBtb, numEntriesRas):
        super(BiMode_BP, self).__init__()
        # Instantiate the conditional predictor logic here
        self.conditionalBranchPred = BiModeBP(
            globalPredictorSize = 16384,
            globalCtrBits = 2,
            choicePredictorSize = 1024,
            choiceCtrBits = 2
        )
        
        # Assign BTB and RAS to the top-level BranchPredictor wrapper
        self.btb = BTB(numEntries=numEntriesBtb, tagBits=10)
        self.ras = ReturnAddrStack(numEntries=numEntriesRas)