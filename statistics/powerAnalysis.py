# Ref: https://machinelearningmastery.com/statistical-power-and-power-analysis-in-python/
import statsmodels.stats.power as sm
import matplotlib.pyplot as plt
import numpy as np
# parameters for power analysis: 4x2 Two-way ANOVA (4 recording time points x 2 conditions)
effect = 0.25
alph = 0.05
pwr = 0.9
dof_1 = 3
dof_2 = 1
# perform power analysis
# analysis = TTestIndPower()
# analysis = sm.FTestPower()
# result = sm.FTestPower().solve_power(effect_size=effect, alpha=alph, power=pwr, nobs=None, df_num=dof_1 ,df_denom=dof_2)
result = sm.FTestAnovaPower().solve_power(effect_size=effect, nobs=None, alpha=alph, power=pwr, k_groups=2)
print('Sample Size: %.3f' % result)
