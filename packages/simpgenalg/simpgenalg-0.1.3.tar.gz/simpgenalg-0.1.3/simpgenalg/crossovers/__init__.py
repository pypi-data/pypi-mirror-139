#__name__ = 'simpgenalg.crossovers'

from .onept import onePointCrossover
from .twopt import twoPointCrossover
from .vartwopt import variableTwoPointCrossover

crossovers_dct = {'onept':onePointCrossover,\
                  'twopt':twoPointCrossover,\
                  'vartwopt':variableTwoPointCrossover}
