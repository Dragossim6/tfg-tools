from m5.objects import *
# from m5.objects import SimpleBTB, TournamentBP, ReturnAddrStack, MultiperspectivePerceptron8KB

# Branch prediction 36-bit history, 512-entry weight table perceptron,
# 2K-set, 4-way BTB, 15-cycle misprediction penalty 

class BTB(SimpleBTB):
    def __init__(self, numEntries, tagBits):
        super(BTB, self).__init__()
        self.numEntries = numEntries
        self.tagBits = tagBits

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
