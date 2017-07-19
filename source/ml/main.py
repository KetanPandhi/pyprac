#!/usr/bin/python3.5
"""ml runner"""

import regression

a = regression.linearRegression()

#use linearRegression or SVR for classifiers choice
a.runLinearReg('SVR')