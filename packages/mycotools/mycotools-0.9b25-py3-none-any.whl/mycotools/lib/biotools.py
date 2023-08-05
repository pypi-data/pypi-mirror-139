#! /usr/bin/env python3
# parses all fasta files inputted as arguments and stores them as {filename: {genes: {description: }{sequence: }}}

from mycotools.lib.kontools import eprint
import re, sys

aa_weights = {
    'A': 89.1, 'R': 174.2, 'N': 132.1, 'D': 133.1, 'C': 121.2, 'E': 147.1,
    'Q': 146.2, 'G': 75.1, 'H': 155.2, 'I': 131.2, 'L': 131.2, 'K': 146.2,
    'M': 149.2, 'F': 165.2, 'P': 115.1, 'S': 105.1, 'T': 119.1, 'W': 204.2,
    'Y': 181.2, 'V': 117.1
    }
aa_weights['X'] = sum(aa_weights.values())/len(aa_weights)

# codon translation table
translation_table = {
    'GCT':'A', 'GCC':'A', 'GCA':'A', 'GCG':'A',
    'CGT':'R', 'CGC':'R', 'CGA':'R', 'CGG':'R', 'AGA':'R', 'AGG':'R',
    'AAT':'N', 'AAC':'N',
    'GAT':'D', 'GAC':'D',
    'TGT':'C', 'TGC':'C',
    'CAA':'Q', 'CAG':'Q',
    'GAA':'E', 'GAG':'E',
    'GGT':'G', 'GGC':'G', 'GGA':'G', 'GGG':'G',
    'CAT':'H', 'CAC':'H',
    'ATT':'I', 'ATC':'I', 'ATA':'I',
    'TTA':'L', 'TTG':'L', 'CTT':'L', 'CTC':'L', 'CTA':'L', 'CTG':'L',
    'AAA':'K', 'AAG':'K',
    'ATG':'M',
    'TTT':'F', 'TTC':'F',
    'CCT':'P', 'CCC':'P', 'CCA':'P', 'CCG':'P',
    'TCT':'S', 'TCC':'S', 'TCA':'S', 'TCG':'S', 'AGT':'S', 'AGC':'S',
    'ACT':'T', 'ACC':'T', 'ACA':'T', 'ACG':'T',
    'TGG':'W',
    'TAT':'Y', 'TAC':'Y',
    'GTT':'V', 'GTC':'V', 'GTA':'V', 'GTG':'V',
    'TAA':'*', 'TGA':'*', 'TAG':'*'
}

rev_comp_table = {
    'T': 'A', 'G': 'C', 'C': 'G', 'A': 'T',
    'N': 'N', 'Y': 'R', 'R': 'Y', 'K': 'M',
    'M': 'K', 'B': 'V', 'D': 'H', 'H': 'D',
    'V': 'B', 't': 'a', 'g': 'c', 'c': 'g',
    'a': 't', 'n': 'n', 'y': 'r', 'r': 'y',
    'k': 'm', 'm': 'k', 'b': 'v', 'd': 'h',
    'h': 'd', 'v': 'b', 'W': 'W', 'S': 'S',
    'w': 'w', 's': 's'
    }


def calc_weight(seq):
    seq = seq.replace('*','')
    weight = aa_weights[seq[0]]
    for char in seq[1:]:
        weight += aa_weights[char] - 18.01
    return weight



def reverse_complement(seq):

    new_seq = ''
    for i in seq[::-1]:
        new_seq += rev_comp_table[i]

    return new_seq


def fa2dict(fasta_file):
    fasta_dict = {}

    with open(fasta_file, 'r') as fasta:
        str_fasta = ''
        for line in fasta:
            # rstrips if it's not a sequence line and isn't a line with only \n
            if line[0] != '>' and line[0] != '\n':
                line = line.rstrip()
            # concatenates a new line character if it is the first sequence line
            if line[0] == '>' and str_fasta != '':
                str_fasta = str_fasta + '\n'
            # concatenates the prep string with the prepped line from the fasta file
            str_fasta = str_fasta + line

        # extracts 0) seq ID and description and 1) sequence
        extracted = re.findall( r'(^>[^\n]*)\n([^>]*)', str_fasta, re.M)

        # adds a new dictionary for each gene
        for index in range(len(extracted)):
            step1 = extracted[index][0]
            step2 = re.search(r'^>([^ ]*)', step1)
            gene = step2[1]
            step3 = re.search(r' (.*)', step1)
            if step3:
                descrip = step3[1]
            else:
                descrip = ''

            seq = extracted[index][1]
            if seq[-1] == '\n' or seq[-1] == '\r':
                seq = seq.rstrip()

            # prepares dictionaries for each gene with description, seq, rvcmpl_seq, and codons
            fasta_dict[gene] = {}
            if descrip != '\n':
                fasta_dict[gene]['description'] = descrip
            fasta_dict[gene]['sequence'] = seq

    return fasta_dict


# truncates sequences based on inputted lenght
def dnatrunc(fasta_dict,trunc_length):
    for gene in fasta_dict:
        if len(fasta_dict[gene]['sequence']) >= trunc_length:
            fasta_dict[gene]['sequence'] = fasta_dict[gene]['sequence'][:(trunc_length - 1)]
            # I should be able to do this in one line
            fasta_dict[gene]['reverse_complement'] = fasta_dict[gene]['reverse_complement'][-1:(0-trunc_length):-1]
            fasta_dict[gene]['reverse_complement'] = fasta_dict[gene]['reverse_complement'][::-1]
    return(fasta_dict)

# takes output dict from fasta2Dict and extracts codons from all 6 reading frames
def dict2codon(fasta_dict):

    fasta_dict[gene]['codons'] = {}

    # outputs a dictionary of reading frames and the possible codons for each
    for index in range(3):
        fasta_dict[gene]['codons']['reading_frame_' + str(index)] = []
        codon = ''
        for nt in fasta_dict[gene]['sequence'][index:]:
            if len(codon) < 3:
                codon = codon + nt
            if len(codon) == 3:
                fasta_dict[gene]['codons']['reading_frame_' + str(index)].append(codon)
                codon = ''

    # let's extract codons from all reading frames for the reverse sequences too
    for index in range(3):
        fasta_dict[gene]['codons']['reverse_reading_frame_' + str(index)] = []
        codon = ''
        for nt in fasta_dict[gene]['reverse_complement'][index:]:
            if len(codon) < 3:
                codon = codon + nt
            if len(codon) == 3:
                fasta_dict[gene]['codons']['reverse_reading_frame_' + str(index)].append(codon)
                codon = ''

    return codondict


def dict2fa(fasta_dict, description = True):

    fasta_string = ''
    if description:
        for gene in fasta_dict:
            fasta_string += '>' + gene.rstrip()
            if 'description' in fasta_dict[gene]:
                fasta_string += (' ' + fasta_dict[gene]['description']).rstrip() + '\n'
            else:
                fasta_string += '\n'
            fasta_string += fasta_dict[gene]['sequence'].rstrip() + '\n'

    else:
        for gene in fasta_dict:
            fasta_string += '>' + gene.rstrip() + '\n' + \
            fasta_dict[ gene ][ 'sequence' ].rstrip() + '\n'

    return fasta_string.rstrip()

# need to turn these into classes and class functions
def calc_gc(gene):

    G = gene['sequence'].count('G')
    C = gene['sequence'].count('C')
    GC = (G + C)/len(gene['sequence'])
    GC_con = '{:.2%}'.format(GC)

    return(GC_con)



# need to change into a class
def gff2list( gff_path, insert = False, error = True ):

    gff_list_dict = []
    with open( gff_path, 'r' ) as raw_gff:
        try:
            for line in raw_gff:
                if not line.startswith('#') and len(line) > 5: 
                    if line.endswith('\n'):
                        line = line.rstrip()
                    col_list = line.split(sep='\t')
                    if len(col_list) == 8 and insert:
                        col_list.insert(2, 'CDS')
                    gff_list_dict.append({
                        'seqid': col_list[0], 'source': col_list[1], 'type': col_list[2],
                        'start': col_list[3], 'end': col_list[4], 'score': col_list[5],
                        'strand': col_list[6], 'phase': col_list[7], 'attributes': col_list[8]
                        })
        except IndexError:
            if not error:
                gff_list_dict = None
            else:
                eprint( line , flush = True)
                raise IndexError
            
    return gff_list_dict


def list2gff( gff_dict ):

    gff_str = ''
    for line in gff_dict:
        add_str = '\t'.join( str(line[x]) for x in line )
        gff_str += add_str + '\n'

    return gff_str.rstrip()

def gff3Comps( source = None ):

    comps = {}
    comps['par'] = r'Parent=([^;]+)'
    comps['id'] = r'ID=([^;]+)'
    comps['Alias'] = r'Alias=([^;]+)'
    comps['product'] = r'product="([^"]*)' 
    comps['ver'] = 'gff3'

    if source == 'ncbi':
        comps['prot'] = r';protein_id=([^;]+)'
    elif source == 'jgi':
        comps['prot'] = r'proteinId=([^;]+)'
        comps['transcript'] = r'transcriptId=([^;])'
   
    return comps

def gff2Comps():

    comps = {}
    comps['id'] = r'name "([^"]+)"'
    comps['prot'] = r'proteinId ([^;]+)'
    comps['transcript'] = r'transcriptId ([^;]+)'
    comps['alias'] = r'alias "([^"]+)"'
    comps['product'] = r'product_name "([^"]+)'
    comps['ver'] = 'gff2'

    return comps

def gtfComps():

    comps = {}
    comps['id'] = r'gene_id "([^"]+)"'
    comps['transcript'] = r'transcript_id "([^"]+)"'
    comps['alias'] = r'alias "([^"]+)"'
    comps['ver'] = 'gtf'

    return comps

def grabGffAcc( gff_list, acc ):

    if ';Alias=' in gff_list[0]['attributes']:
        alias = 'Alias=' + acc
        alias_on = alias + ';'
    elif ' alias "' in gff_list[0]['attributes']:
        alias = 'alias "' + acc + '"'
        alias_on = 'alias "' + acc + '"'
    out_list = [ 
        x for x in gff_list \
        if x['attributes'].endswith(alias) or \
            alias_on in x['attributes'] 
# timed slower        if re.search(alias + r'(?:;|$)', x['attributes'])
        ]
    return out_list


def grabGffAccs(gff_list, acc_list):

    aliases, ends = set(), set()
    for acc in acc_list:
        aliases.add('Alias=' + acc)
        ends.add('Alias=' + acc + ';')
    out_list = []
    for i in gff_list:
        if any(i['attributes'].endswith(x) for x in aliases):
            out_list.append(i)
        elif any(x in i['attributes'] for x in ends):
            out_list.append(i)

    return out_list

def compileExon( gff ):
	
    exon_dict = {}

    for index in range(len(gff)):
        if gff[index]['type'].lower() == 'exon':
            break

    protComp = re.compile( r';Parent\=([^;]*)' )
    if not protComp.search( gff[index]['attributes'] ):
        protComp = re.compile( r'gene_id "(.*?)"' )
        if not protComp.search( gff[index]['attributes'] ):
            protComp = re.compile( r'name "(.*?)"\;' )
            if not protComp.search( gff[index]['attributes'] ):
                protComp = re.compile( r'ID=(.*?);' )

    for line in gff:
        if line['type'].lower() == 'exon':
            prot = protComp.search( line['attributes'] )[1]
            if prot not in exon_dict:
                exon_dict[ prot ] = []
            if line['strand'] == '+':
                exon_dict[prot].append( [int(line['start'] ) - 1, int( line['end'] )] )
            else:
                if int(line['start']) > int(line['end']):
                    exon_dict[prot].append( [int (line['end'] ) - 1, int( line['start'])])
                else:
                    exon_dict[prot].append( [int (line['start'] ) - 1, int( line['end'])])

    for prot in exon_dict:
        exon_dict[ prot ] = sorted(exon_dict[ prot ], key = lambda i: i[0])

    return exon_dict
