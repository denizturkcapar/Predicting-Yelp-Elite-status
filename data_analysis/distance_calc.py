# Code for determining how to build distance formula. We use basic summary 
# statistics to assess this.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def summary_stats(series):
	'''
	Computes summary statistics and histogram of a pandas series.

	Inputs:
		series: a pandas series.

	Returns:
		stats: (list) A list of summary statistics including min, max, mean,
		  and standard deviation.
	'''

	s1 = min(series)
	s2 = max(series)
	s3 = np.mean(series)
	s4 = np.std(series)
	stats = [s1, s2, s3, s4]

	plt.hist(x=np.array(series), bins=20)
	plt.show()

	return stats

'''
NOTES

# Formula 1: Our starting formula. Will changes
S = a*(1 - score) + b*(1 - review) + c*()
'''