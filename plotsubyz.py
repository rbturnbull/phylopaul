#!/usr/bin/env python

import matplotlib.pyplot as plt
import pandas as pd
import argparse
from matplotlib import rcParams
import arviz

rcParams['font.family'] = 'Linux Libertine O'
rcParams.update({'font.size': 14})

parser = argparse.ArgumentParser(description='Makes a plot of the rates to the Byz text and from the Byz text.')
parser.add_argument("log", help="The Beast 2 log file.")
parser.add_argument("output", help="The output file.")

args = parser.parse_args()

fig, ax = plt.subplots(1, 1, figsize=(16, 5))

df = pd.read_csv(args.log, sep='\t', comment='#', )
df = df.truncate(before=int(len(df.index)*0.5))

df['MULTIPLIER'] = df['TO_BYZ_RATE']/df['FROM_BYZ_RATE']

bins = 50

to_byz_hpdi = arviz.hdi(df['TO_BYZ_RATE'].values, 0.95)
to_byz_hpdi_centre = 0.5*(to_byz_hpdi[1]+to_byz_hpdi[0])
to_byz_hpdi_uncert = to_byz_hpdi[1] - to_byz_hpdi_centre

from_byz_hpdi = arviz.hdi(df['FROM_BYZ_RATE'].values, 0.95)
from_byz_hpdi_centre = 0.5*(from_byz_hpdi[1]+from_byz_hpdi[0])
from_byz_hpdi_uncert = from_byz_hpdi[1] - from_byz_hpdi_centre

plt.hist(df['TO_BYZ_RATE'], density=True, bins=bins, alpha=0.5, color="dodgerblue", label="To Byzantine Text")
plt.hist(df['FROM_BYZ_RATE'], density=True, bins=bins, alpha=0.5, color="red", label="From Byzantine Text")
plt.axvline(to_byz_hpdi[0], color='dodgerblue', linestyle='dashed', linewidth=1)
plt.axvline(to_byz_hpdi[1], color='dodgerblue', linestyle='dashed', linewidth=1)

plt.axvline(from_byz_hpdi[0], color='red', linestyle='dashed', linewidth=1)
plt.axvline(from_byz_hpdi[1], color='red', linestyle='dashed', linewidth=1)

min_ylim, max_ylim = plt.ylim()
min_xlim, max_xlim = plt.xlim()

to_byz_label = "%.2g ± %.2g" % (to_byz_hpdi_centre, to_byz_hpdi_uncert )
from_byz_label = "%.2g ± %.2g" % (from_byz_hpdi_centre, from_byz_hpdi_uncert )
plt.text(to_byz_hpdi_centre, max_ylim*0.9, to_byz_label, color="dodgerblue", ha='center')
plt.text(from_byz_hpdi_centre, max_ylim*0.9, from_byz_label, color="red")

multiplier_label = "Relative Rate To/From Byz: %.1f ± %.1f" % (df['MULTIPLIER'].mean(), 2.0*df['MULTIPLIER'].std() )
plt.text(0.98*max_xlim, 0.1*max_ylim, multiplier_label, horizontalalignment='right')
leg = ax.legend()
ax.set_xlabel("Rate (relative to transitions not involving Byzantine text)")
ax.set_ylabel("Density")

show = False
if show:
    plt.show()

# fig.tight_layout()
fig.savefig(args.output) 
print(f"Saved to {args.output}")
