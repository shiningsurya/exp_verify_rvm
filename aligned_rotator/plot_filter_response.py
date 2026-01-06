
import numpy as np

import matplotlib.pyplot as plt

plt.style.use ('../gmrtr3.mplstyle')

from filter_response import FilterResponseModel
FilterResponse  = FilterResponseModel ("filter_response.npz")

######################################

fig = plt.figure ('fres')

# axp, axm = fig.subplots (2,1,sharex=True, sharey=True)
ax = fig.add_subplot()


_dpa = np.rad2deg ( FilterResponse.filter_pa )
ax.plot ( _dpa, FilterResponse.pfilter, c='b', label='+' )
ax.plot ( _dpa, FilterResponse.mfilter, c='r', label='-' )

# ax.plot ( _dpa, 0.5*np.cos(FilterResponse.filter_pa)**2, c='k' )


ax.legend(loc='best')

ax.set_xlabel ('Mismatch / deg')
ax.set_ylabel('Response')

# ax.set_ylabel('+ orientation')
# ax.set_ylabel('- orientation')

# plt.show()
fig.savefig ('figs/fresponse.pdf', bbox_inches='tight')

