import sys, os
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss

plt.ion()

# Read the summary file
with open('summary.dat', 'r') as foo:
    lines = foo.readlines()

# Extract out number of shares
nshares = np.zeros(len(lines)-1, dtype=int)
for i, line in enumerate(lines[1:]):
    nshares[i] = int(line.split(';')[-1])

# Uncomment this if you want to omit the giant whales
#nshares = nshares[nshares<2500] # this ~doubles the probability
# Uncomment this if you want to omit all whales w/ > 1000 shares
#nshares = nshares[nshares<1000] # this ~triples the probability
# For clarity, if you use either of the above trimmings, then the probability density is a measure of the probability that an ape with under 2500 (or 1000) shares is holding X shares

# Plot the histogram
nbins = 1000
ncount, bins, patches = plt.hist(nshares, bins=nbins, 
                                 density=True, log=True, 
                                 label='Histogram')
plt.xlabel('Number of shares')
plt.ylabel('Probability density')
plt.title('Distribution of $GME Shareholders')
plt.savefig('histogram.png')

# KDE to determine the underlying dist'n
rep = ss.gaussian_kde(nshares)
val = rep.evaluate(bins) # Evaluate the KDE according to the histogram bins

plt.plot(bins, val, label='KDE')
plt.legend(loc='best')
plt.savefig('histogram_with_kde_log.png')
# Trim to under 1000 shares for prettier plots
plt.xlim(-10, 1000)
plt.ylim(1e-5, 1e-1)
plt.savefig('histogram_with_kde_log_under1k.png')
plt.yscale('linear')
plt.ylim(0, 0.02) # so that the plot looks reasonable...
plt.savefig('histogram_with_kde_linear_under1k.png')
plt.ylim(0, 0.007)
plt.xlim(-850, 17500) # back to orignial scale
plt.savefig('histogram_with_kde_linear.png')
plt.close()



