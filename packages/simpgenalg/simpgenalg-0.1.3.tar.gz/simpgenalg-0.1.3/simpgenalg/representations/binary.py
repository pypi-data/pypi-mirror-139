from .basics import *
from random import choices

class fixedBinaryChromo(basicChromo):

    __slots__ = ('num_genes', 'gene_size')

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        # Get number of genes
        self.num_genes = kargs.get('num_genes', None)
        if self.num_genes is None:
            self.num_genes = kargs.get('num_genes',\
                                self.config.get('num_genes', dtype=int, min=1))
        # Get gene size
        self.gene_size = kargs.get('gene_size', None)
        if self.gene_size is None:
            self.gene_size = kargs.get('gene_size',\
                                    self.config.get('gene_size', dtype=int, min=1))
        # Determine length
        length = self.num_genes*self.gene_size

        # If passed a lenmin or a lenmax raise errors
        if 'len_min' in kargs or 'len_max' in kargs:
            raise ValueError('Should not include len_min or len_max for '+\
                             'fixedBinaryChromo')

        # Determine length limit
        if self.lenLim is not None:
            if self.lenLim[0] != length and lenLim[1] != self.length:
                self.log.exception('lenLim should be equal to length')
        else:
            self.lenLim = (length, length)

        # These values are always true
        self.min, self.max, self.dtype = 0, 1, int

        if 'vals' not in kargs and kargs.get('generate', True):
            self.generate()



    def get_split(self):
        return [self.vals[x:x+self.gene_size] for x in \
                    range(0, self.num_genes*self.gene_size, self.gene_size)]

    # Returns a copy of this chromosome
    def copy(self):
        return fixedBinaryChromo(vals = self.to_list(return_copy=True),\
                                    lenLim = self.lenLim, \
                                    fit = self.fit, \
                                    hsh = self.hsh, \
                                    num_genes = self.num_genes, \
                                    gene_size = self.gene_size)

    def generate(self):
        self.set_chromo(choices((0,1), k=self.lenLim[0]))

    def append(self, item):
        self.log.exception('Cannot append to a fixedBinaryChromo',\
                           err=NotImplementedError)

    def extend(self, item):
        self.log.exception('Cannot extend to a fixedBinaryChromo',\
                           err=NotImplementedError)

    def insert(self, item):
        self.log.exception('Cannot insert to a fixedBinaryChromo',\
                           err=NotImplementedError)

    def pop(self, indx):
        self.log.exception('Cannot pop from a fixedBinaryChromo',\
                           err=NotImplementedError)

class binaryRepresentation(basicRepresentation):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        self.dtype = kargs.get('dtype',\
                    self.config.get('dtype', int, options=(int, float, None)))

        if 'chromo' not in kargs:
            self.chromo = fixedBinaryChromo(*args, **kargs)

    def _cnvrt_to_float(self, lst):
        return sum([1/(2**indx) if x==1 else 0 for indx, x in enumerate(lst)])

    def _cnvrt_to_int(self, lst):
        return sum([(2**indx) if x==1 else 0 \
                                    for indx, x in enumerate(lst[::-1])])

    def _map(self, chromo):
        if self.dtype is int:
            return [self._cnvrt_to_int(lst) for lst in chromo.get_split()]
        elif self.dtype is float:
            return [self._cnvrt_to_float(lst) for lst in chromo.get_split()]
        elif self.dtype is None:
            return chromo.to_list(return_copy=True)
