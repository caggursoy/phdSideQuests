# # Ref: https://towardsdatascience.com/introduction-to-power-analysis-in-python-e7b748dfa26
# import statsmodels.stats.power as sm
# import matplotlib.pyplot as plt
# import numpy as np
# # parameters for the analysis
# effect_size = 0.9
# alpha = 0.05 # significance level
# power = 0.25
#
# power_analysis = sm.TTestIndPower()
# sample_size = power_analysis.solve_power(effect_size = effect_size,
#                                          power = power,
#                                          alpha = alpha)
#
# print('Required sample size: {0:.2f}'.format(sample_size))
#
# # power vs. number of observations
#
# fig = plt.figure()
# ax = fig.add_subplot(2,1,1)
# fig = sm.TTestIndPower().plot_power(dep_var='nobs',
#                                  nobs= np.arange(2, 200),
#                                  effect_size=np.array([0.2, 0.5, 0.8]),
#                                  alpha=0.01,
#                                  ax=ax, title='Power of t-Test' + '\n' + r'$\alpha = 0.01$')
# ax.get_legend().remove()
# ax = fig.add_subplot(2,1,2)
# fig = sm.TTestIndPower().plot_power(dep_var='nobs',
#                                  nobs= np.arange(2, 200),
#                                  effect_size=np.array([0.2, 0.5, 0.8]),
#                                  alpha=0.05,
#                                  ax=ax, title=r'$\alpha = 0.05$')
# #fig.subplots_adjust(top = .9)
# plt.show(fig)
#

# Ref: https://machinelearningmastery.com/statistical-power-and-power-analysis-in-python/
import statsmodels.stats.power as sm
import matplotlib.pyplot as plt
import numpy as np
# parameters for power analysis
effect = 0.25
alph = 0.05
pwr = 0.9
# perform power analysis
# analysis = TTestIndPower()
# analysis = sm.FTestPower()
result = sm.FTestPower().solve_power(effect_size=effect, alpha=alph, power=pwr, nobs=None, df_num=None ,df_denom=1)
print('Sample Size: %.3f' % result)
