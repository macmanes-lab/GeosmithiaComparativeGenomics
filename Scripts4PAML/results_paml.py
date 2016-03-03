#!/usr/bin/python

from __future__ import division
from Bio.Phylo.PAML import codeml
import sys
import os
import shutil
import time
import glob
from math import sqrt
from rpy2 import robjects

r = robjects.r
len = len(glob.glob1(".","*.out"))

def compare_models(null_lnl, alt_lnl, df):
    likelihood = 2*(abs(null_lnl-alt_lnl))
    p = 1 - robjects.r.pchisq(likelihood, df)[0]
    return p


null_results = codeml.read(sys.argv[1])
alt_results = codeml.read(sys.argv[2])

null_nssites = null_results.get("NSsites")
alt_nssites = alt_results.get("NSsites")

#null_model = null_results.get("model")
#alt_model = alt_results.get("model")

null_value = null_nssites.get(2)
null_lnl = null_value.get("lnL")

alt_value = alt_nssites.get(2)
alt_lnl = alt_value.get("lnL")

bs_p_pos = compare_models(null_lnl,alt_lnl,1)
# m8_p_pos = compare_models(m7_lnl,m8_lnl,2)

r.assign('bs_p_pos', bs_p_pos)
# r.assign('m8_p_pos', m8_p_pos)
r.assign('len', len)


paBS = robjects.r('p.adjust(bs_p_pos, "BH", len)')
# paM8 = robjects.r('p.adjust(m8_p_pos, "BH", len)')


print 'Ajusted p-val for null vs. alt of orthogroup {} is {}'.format(sys.argv[1][0:13], paBS[0])

# print 'M7vM8_pajust-value {} {}'.format(sys.argv[1], paM8[0])