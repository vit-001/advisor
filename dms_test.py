# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from model.solvers.dms_old import DMquantum

if __name__ == "__main__":
    dm1=DMquantum(2.0,4.0)
    values=[1.0,2.0,3.0,4.0,6.0]
    for v in values:
        dm1.add(v)
        dm1.test_print()

    print(dm1.value)