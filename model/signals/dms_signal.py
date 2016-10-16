# -*- coding: utf-8 -*-
__author__ = 'Vit'

from model.base_classes import AbstractSolver

class DMSSignal(AbstractSolver):
    def __init__(self, dms_solver):
        self.dms=dms_solver
        self.old_pdi_ndi_diff=0.0
        self.old_adxi=1.0
        self.buy_signal=0.0

    def on_bid_change(self, time, bid, ask):
        self.buy_signal=0.0

        pdi_ndi_diff=self.dms.get_pdi(14)-self.dms.get_ndi(14)
        adxi=self.dms.get_adxi(14)

        if pdi_ndi_diff>0.0:# and self.old_pdi_ndi_diff<0.0:
            if adxi > self.old_adxi:
                self.buy_signal=1.0

        self.old_pdi_ndi_diff=pdi_ndi_diff
        self.old_adxi=adxi


if __name__ == "__main__":
    pass