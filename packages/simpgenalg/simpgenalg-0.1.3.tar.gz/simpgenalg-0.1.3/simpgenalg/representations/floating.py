from .basics import *
import math, random

class floatingBinaryChromo(basicChromo):

    def __init__(self, *args, **kargs):

        super().__init__(self, *args, **kargs)

        self.lenLim = kargs.get('lenLim', None)
        if self.lenLim is None:
            if 'len' in kargs:
                self.lenLim = (kargs.get('len'),kargs.get('len'))
            elif 'len' in self.config:
                self.lenLim = (self.config.get('len', dtype=int, mineq=1),\
                               self.config.get('len', dtype=int, mineq=1))
            elif 'lenmin' in kargs and 'lenmax' in kargs:
                self.lenLim = (kargs.get('lenmin'),kargs.get('lenmax'))
            elif 'lenmin' in self.config and 'lenmax' in self.config:
                self.lenLim = (self.config.get('lenmin', dtype=int, mineq=1),\
                               self.config.get('lenmax', dtype=int, mineq=1))
            else:
                self.log.exception('Need to provide lenLim', err=ValueError)

        self.min, self.max, self.dtype = 0, 1, int

        if 'vals' not in kargs and kargs.get('generate', True):
            self.generate()

        def copy(self):
            return floatingBinaryChromo(vals = self.to_list(return_copy=True),\
                                        lenLim = self.lenLim, \
                                        fit = self.fit, \
                                        hsh = self.hsh)

class floatingRepresentation(basicRepresentation):

    __slots__ = ('template', 'g_id_len', 'gene_ids','gene_size', 'num_genes',\
                    'start_tag', 'end_tag', 'dtype')

    def __init__(self, *args, **kargs):

        super().__init__(*args, **kargs)
        # Get number of genes
        self.num_genes = kargs.get('num_genes', None)
        if self.num_genes is None:
            self.num_genes = self.config.get('num_genes')
        # Get gene size
        self.gene_size = kargs.get('gene_size',None)
        if self.gene_size is None:
            self.gene_size = self.config.get('gene_size', dtype=int, mineq=1)
        # Get dtype
        self.dtype = kargs.get('dtype',None)
        if self.dtype is None:
            self.dtype = self.config.get('dtype', int, options=(int, float, None))

        # Determine start tag
        self.start_tag = kargs.get('start_tag', self.config.get('start_tag', \
                            self._generate_tag(self.config.get('start_tag_len',\
                                                        3, dtype=int, mineq=1))))

        # Determine end tag (if applicable)
        if ('end_tag' in kargs or self.config.get('has_end_tag', True, dtype=bool)):
            self.end_tag = kargs.get('end_tag',self.config.get('end_tag', \
                    self._generate_tag(self.config.get('end_tag_len',3,\
                                                    dtype=int, mineq=1))))

        # Figure out gene ids
        self.gene_ids = kargs.get('gene_ids', self._generate_gene_ids())
        self.g_id_len = None
        # Template
        self.template = kargs.get('template', None)
        if self.template is None:
            self.config.get('template', [0]*self.num_genes, dtype=list)


        if 'chromo' not in kargs:
            self.chromo = floatingBinaryChromo(*args, **kargs)

    def _cnvrt_to_float(self, lst):
        return sum([1/(2**indx) if x==1 else 0 for indx, x in enumerate(lst)])

    def _cnvrt_to_int(self, lst):
        return sum([(2**indx) if x==1 else 0 \
                                    for indx, x in enumerate(lst[::-1])])

    def _generate_tag(self, length):
        tag = random.choices((0,1), k=length)

        if length == 1 and hasattr(self, 'start_tag') and \
                self.start_tag is not None and hasattr(self, 'end_tag') and \
                self.end_tag is not None and self.start_tag != self.end_tag:
            self.log.exception('No other tag option available', err=Exception)

        if not hasattr(self, 'start_tag') and not hasattr(self, 'end_tag'):
            return random.choices((0,1), k=length)

        if hasattr(self, 'start_tag'):
            while (tag == self.start_tag):
                tag = random.choices((0,1), k=length)
            return tag

        if hasattr(self, 'end_tag'):
            while (tag == self.end_tag):
                tag = random.choices((0,1), k=length)
            return tag

        # Keep making new one
        while (tag == self.start_tag or tag == self.end_tag):
            tag = random.choices((0,1), k=length)
        # Return tag
        return tag

    def _generate_gene_ids(self, length=None):
        min_length = math.log2(self.num_genes)
        if length is None:
            length = min_length
        elif length < min_length:
            self.log.exception('Given length is too small')
        if self.start_tag is not None and len(self.start_tag) == length:
            length += 1
        if self.end_tag is not None and len(self.end_tag) == length:
            length += 1
        self.g_id_len = length
        # Function for generating ids
        def genbin(lst, length):
            if len(lst) == 0:
                lst = [[0], [1]]
            elif len(lst[0]) >= length:
                return lst
            newlst = []
            for sublst in lst:
                newlst.append(sublst.copy()+[0])
                newlst.append(sublst.copy()+[1])
            return genbin(newlst, length)

        # Generate all possible ids
        ids = genbin([], length)
        random.shuffle(ids)
        ids = [id for id in ids if id != self.start_tag and id != self.end_tag]\
                    [:self.num_genes]

        dct = {}
        for gene_num, id in enumerate([id for id in ids \
                                             if id != self.start_tag and \
                                             id != self.end_tag]\
                                             [:self.num_genes]):
            dct[gene_num] = tuple(id)
            dct[dct[gene_num]] = gene_num

        return dct

    def _map(self, chromo):

        # Create map lst and lbls
        map, lbls, extractions = [None]*self.num_genes, \
                                 [set() for x in range(self.num_genes)], \
                                 dict.fromkeys(range(0, self.num_genes), [])
        # Get start tag info and gene info
        strt, strt0, strt_len, g_id_len, gene_size, chr_len = \
                        self.start_tag, self.start_tag[0], len(self.start_tag),\
                        self.g_id_len, self.gene_size, len(chromo)
        tot_len = strt_len + g_id_len + gene_size


        stats = dict.from_labels(('n_starts', 'n_bad_starts', 'n_ends',\
                    'n_encoded_genes', 'n_unique_encoded_genes',\
                    'meaningful_bits', 'meaningful_bits_pct',\
                    'gene_len_avg', 'gene_len_stdev',
                    'meaningful_bit_overlap_avg'), 0)

        # Find end tags
        if end_tag is not None:
            # Get end tag info
            end, end0, end_len = self.end_tag, self.end_tag[0], len(self.end_tag)
            # Enumerate through and find all end tags
            for indx, b in enumerate(chromo):
                # If cannot fit an end tag, end it
                if indx+end_len > chr_len:
                    break
                if b == end0 and end == chromo[indx:indx+end_len]:
                    stats['n_ends'] += 1
                    for lbl in lbls[indx:indx+end_len]:
                        lbl.add('E')

        # Enumerate through binary values
        for indx, b in enumerate(chromo):
            # If cannot fit a start tag, end it
            if indx+strt_len > chr_len:
                break
            # If at start of a start tag, extract it
            if b == strt0 and strt == chromo[indx:indx+strt_len]:
                stats['n_starts'] += 1
                for lbl in lbls[indx:indx+strt_len]:
                    lbl.add('S')

                # If can fit gene ID too, get the ID
                if indx+strt_len+g_id_len < chr_len:
                    gID = self.gene_ids.get(chromo[indx+strt_len:\
                                                   indx+strt_len+g_id_len],
                                                   None)
                    if gID is None:
                        stats['n_bad_starts'] += 1
                        continue
                    for lbl in lbls[indx+strt_len:indx+strt_len+g_id_len]:
                        lbl.add('ID')
                else:
                    stats['n_bad_starts'] += 1
                    continue

                # Record extraction
                gene = []
                for cur_indx, lbl in enumerate(lbl[indx+strt_len+g_id_len:\
                                min(chr_len, indx+strt_len+g_id_len+tot_len)]):
                    # If an end label, stop there
                    if 'E' in lbl:
                        break
                    # Otherwise, add int for gene id
                    lbl.add(gID)
                    gene.append(chromo[indx+srt_len+g_id_len+cur_indx])
                extractions[gID].append(gene)
                stats['n_encoded_genes'] += 1

        # Find gene values through averaging
        gene_len_sum = 0
        for gene_num, genes in extractions.items():

            if len(genes) == 0:
                continue

            stats['n_unique_encoded_genes'] += 1

            if self.dtype is int:
                nums = self._cnvrt_to_int(genes)
            elif self.dtype is float:
                nums = self._cnvrt_to_float(genes)

            map[gene_num] = mean(nums)

        # Get some final stats
        glens = [len(value) for item in extractions.values]
        bit_use = [len(lbl) for lbl in lbls]
        num_bits_used = sum([1 if uses > 0 else 0 for uses in bit_use])
        bit_overlap = mean([use for use in bit_use if use!=0])
        stats.update({'gene_len_avg':mean(glens),\
                      'gene_len_stdev':stdev(glens),\
                      'meaningful_bits':num_bits_used,\
                      'meaningful_bits_pct':num_bits_used/len(chromo),\
                      'meaningful_bit_overlap_avg':bit_overlap,\
                      'pct_template':\
                            stats['n_unique_encoded_genes']/self.num_genes})

        map = [chrval if chrval is not None else tempval \
                    for chrval, tempval in zip(map, self.template)]

        return map, stats

    # Returns chromosome mapped
    def get_mapped(self, return_copy=True):
        if self.mapped is None or \
                            self.get_chromo(return_copy=False).get_fit() is None:
            self.mapped, mapstats = self._map(self.get_chromo())
            self.update_attrs(map_stats)
        if return_copy:
            return self.mapped.copy()
        return self.mapped
