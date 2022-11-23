#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Print the acknowledgements sentence with all the project references!
See acknowledgements.py -h or run acknowledgements.py ? for help or simply use as 
acknowledgements.py Author1 Author2
"""

import sys
from collections import OrderedDict
import argparse
import textwrap
import inflect


p = inflect.engine()

name = 'acknowledgements'
FCT = r'Funda\c{c}\~ao para a Ci\^encia e a Tecnologia (FCT, Portugal)'
FEDER = r'FEDER - Fundo Europeu de Desenvolvimento Regional'
COMPETE2020 = r'COMPETE2020 - Programa Operacional Competitividade e Internacionaliza\c{c}\~ao'
POCH = 'POCH/FSE (EC)'

def from_tex(s):
    s = s.replace(r'\c{c}', 'ç')
    s = s.replace(r'\~a', 'ã')
    s = s.replace(r'\^e', 'ê')
    return s


def _parser():
    parser = argparse.ArgumentParser(description='Print %s' % name)
    parser.add_argument('authors', metavar='authors', type=str, nargs='+',
                        help='authors for the current paper')
    parser.add_argument('--sort', dest='sortalpha', action='store_true',
                        default=False, help='sort the authors alphabetically?')
    parser.add_argument('--notex', action='store_true', default=False,
                        help='no LaTeX output')
    parser.add_argument('-w', '--width', type=int, default=80,
                        help='width of lines in output (default=80)')
    parser.add_argument('--noGEANES', action='store_true', default=False,
                        help='remove G.EANES project from acknowledgements')
    parser.add_argument('--noEPIC', action='store_true', default=False,
                        help='remove EPIC project from acknowledgements')

    args = parser.parse_args()
    # print args
    return args


def flatten(lst):
    return [item for sublist in lst for item in sublist]


def comma_separator(sequence, end_with_and=True):
    if not sequence:
        return ''
    if isinstance(sequence, dict):
        sequence = list(sequence.values())

    for i, item in enumerate(sequence):
        if isinstance(item, list):
            sequence[i] = comma_separator(item, end_with_and=False)

    if len(sequence) == 1:
        return sequence[0]
    elif len(sequence) == 2:
        return ' and '.join(sequence)

    if end_with_and:
        return '{}, and {}'.format(', '.join(sequence[:-1]), sequence[-1])
    else:
        return ', '.join(sequence)


def justy(text, width=80, ret=False):
    """ Print text limiting the number of characters per line to `width` """
    broken = textwrap.wrap(text, width, break_long_words=False)
    if ret:
        return '\n'.join(broken)
    else:
        print('\n'.join(broken))


def individual(initials, normal=True, dl57=False, ifct=False, width=80,
               ret=False):
    if dl57 or ifct:
        normal = False

    n = len(initials)  # how many?

    if n == 0:
        return ''

    if len(initials) == 1:
        t1, t2, t3, t4 = 'is', 'acknowledges', 'contract', 'reference'
    else:
        t1, t2, t3, t4 = 'are', 'acknowledge', 'contracts', 'references'

    # list the initials
    msg = p.join(list(initials.keys())) + ' '
    if normal:
        msg += p.plural_verb('acknowledges ', n)
        msg += f'support from FCT through '
        msg += p.plural('contract ', n)
        msg += 'with '
        msg += p.plural('reference ', n)

    elif dl57:
        msg += p.plural_verb('is ', n)
        msg += 'supported in the form of '
        msg += 'a ' if n == 1 else ''
        msg += p.plural('work contract ', n)
        msg += 'funded by national funds through FCT with '
        msg += p.plural('reference ', n)

    elif ifct:
        msg += p.plural_verb('acknowledges ', n)
        msg += 'support from FCT through Investigador FCT '
        msg += p.plural('contract ', n)

    msg += p.join(flatten(list(initials.values())))

    if ret:
        return msg + '. '
    else:
        justy(msg + '. ', width)


IA_akn = {
    'IA': [
        # 'UID/FIS/04434/2019',
        'UIDB/04434/2020',
        'UIDP/04434/2020',
        # 'UIDB/04564/2020',
        # 'UIDP/04564/2020',
        # 'PTDC/FIS-AST/7002/2020',
        # 'POCI-01-0145-FEDER-022217',
        # 'POCI-01-0145-FEDER029932',
    ],
}

team_akn = {
    # 'GEANES': 'PTDC/FIS-AST/32113/2017 & POCI-01-0145-FEDER-032113',
    # 'EPIC': 'PTDC/FIS-AST/28953/2017 & POCI-01-0145-FEDER-028953',
    # 'unk1': 'PTDC/FIS-AST/28987/2017 & POCI-01-0145-FEDER-028987',
    'SAM': 'EXPL/FIS-AST/0615/2021',
    'CSI': 'EXPL/FIS-AST/XXXX/XXXX',
}

erc_akn = {
    'ERC': "The research leading to these results has received funding from the European Research Council through the grant agreement 101052347 (FIERCE)."
}

# 'UID/FIS/04434/2013',
# 'POCI-01-0145-FEDER-007672',
# 'PTDC/FIS-AST/1526/2014',
# 'POCI-01-0145-FEDER-016886'

# Vardan_project = [
#     'PTDC/FIS-AST/7073/2014',
#     'POCI-01-0145-FEDER-016880',
# ]

acknow = {
    ('Elisa Delgado Mena', 'E.D.M.', 'Elisa'):           ['IF/00849/2015/CP1273/CT0003'], #['IF/00849/2015',],
    ('João P. S. Faria', 'J.P.F.', 'Faria'):             ['DL57/2016/CP1364/CT0005'],  #['SFRH/BD/93848/2013',],
    ('Jorge H. C. Martins', 'J.H.C.M.', 'Jorge'):        ['DL57/2016/CP1364/CT0007'],
    ('João Gomes da Silva', 'J.G.dS.', 'GomesDaSilva'):  [],
    ('L. Filipe Pereira', 'F.P.', 'Filipe'):             [], #['PD/BD/135227/2017'],
    ('Nuno C. Santos', 'N.C.S.', 'Nuno'):                [],  #['IF/00169/2012/CP0150/CT0002',],
    ('Nuno Peixinho', 'N.', 'Peixinho'):                 [],
    ('Olivier D. S. Demangeon', 'O.D.', 'Olivier'):      ['DL57/2016/CP1364/CT0004'],
    ('Pedro Figueira', 'P.F.', 'PedroF'):                [], #['IF/01037/2013CP1191/CT0001',],
    ('Pedro Machado', 'P.M.', 'PedroM'):                 [],
    ('Pedro T. P. Viana', 'P.T.P.V.', 'PedroV'):         [],
    ('Pedro Pina', 'P.P.', 'PedroPina'):                   [],
    ('Sérgio A. G. Sousa', 'S.G.S.', 'Sergio'):          ['IF/00028/2014/CP1215/CT0002',],
    ('Susana C. C. Barros', 'S.C.C.B.', 'Susana'):       ['IF/01312/2014/CP1215/CT0004',],
    ('Tiago Campante', 'T.C.', 'Tiago'):                 [], #  ['IF/00650/2015/CP1273/CT0001'],  #['IF/00650/2015',],
    ('Vardan Zh. Adibekyan', 'V.A.', 'Vardan'):          ['IF/00650/2015/CP1273/CT0001'],  #['IF/00650/2015',],
    #
    ('Alexandros Antoniadis Karnavas', 'A.A.K.', 'Alexandros'): [],
    ('Ana Rita Silva', 'A.R.S.', 'AnaRita'): [],
    ('André Silva', 'A.M.S.', 'Andre'): [],
    ('Bárbara M. T. B. Soares', 'B.M.T.B.S.', 'Barbara'): [],
    ('Daniela Espadinha', 'D.E.', 'Daniela'): [],
    ('Eduardo Cristo', 'E.C.', 'Eduardo'): [],
    ('Francisco Brasil', 'F.B.', 'Franciso'): [],
    ('José Ribeiro', 'J.R.', 'JoseRibeiro'): [],
    ('José Rodrigues', 'J.R.', 'JoseRodrigues'): [],
    ('Nuno Rosário', 'N.R.', 'NunoRosario'): [],
    ('Tomás de Azevedo Silva', 'T.S.', 'Tomas'): [],
    #
    # no longer in the team:
    # ('Ruben Gonçalves', 'R.G.', 'Ruben')                    : [],
    # ('Luisa M. Serrano', 'L.M.S.', 'Luisa')                 : ['SFRH/BD/120518/2016'],
    # ('Pedro I. T. K. Sarmento', 'P.I.T.K.S.', 'PedroS')     : [],
    # ('Saeed Hojjatpanah', 'S.H.', 'Saeed')                  : [],
    # ('Solène C. Ulmer-Moll', 'S.C.M.', 'Solene')            : [],
    # ('Gabriella Gilli', 'G.G.', 'Gabriella')                : [],
    # ('Andressa C. S. Ferreira', 'A.C.S.F.', 'Andressa')     : [],
    # ('Daniel Thaagaard Andreasen', 'D.T.A.', 'Daniel')      : [],
    # ('Jason J. Neal', 'J.J.N.', 'Jason')                    : [],
}

DL57 = ('Olivier', 'Faria', 'Jorge')
iFCT = ('Sergio', 'Susana', 'Vardan', 'Elisa')


def acknowledgements(authors, noGEANES=False, noEPIC=False, ERC=True,
                     SAM=False, CSI=False, notex=False, width=80):
    # build a dict with the acknowledgements for these authors only
    ThisPaperAcknow = OrderedDict()
    for author in authors:
        for k, v in acknow.items():
            if author in k:
                ThisPaperAcknow[k] = v

    # print the damn thing!!!
    # print('\n\n')
    # print(name)
    # print('='*len(name) + '\n')

    team_akn_copy = team_akn.copy()
    if noGEANES:
        team_akn_copy.pop('GEANES')
    if noEPIC:
        team_akn_copy.pop('EPIC')
    if not SAM:
        team_akn_copy.pop('SAM')
    if not CSI:
        team_akn_copy.pop('CSI')

    # if 'Vardan' in authors:
    # add Vardan's project

    if notex:
        detex = from_tex
    else:
        detex = lambda x: x

    IA = IA_akn['IA']

    msg = f'This work was supported by {detex(FCT)} '
    msg += f'through the research grants {comma_separator(IA)}'

    if len(team_akn_copy) > 0:
        msg += ' '
        # msg += f'and by {detex(FEDER)} '
        # msg += f'through {detex(COMPETE2020)} '
        msg += f'and by {detex(POCH)} '
        msg += p.plural('through the grant ', len(team_akn_copy))
        msg += comma_separator(team_akn_copy)
    
    msg += '. '

    if ERC:
        msg += '\n'
        msg += detex(erc_akn['ERC'])
        msg += '\n'

    initials = [n[1] for n in list(ThisPaperAcknow.keys())]
    dl57 = {}
    ifct = {}
    other = {}
    for i, (initial,
            (k, v)) in enumerate(zip(initials, list(ThisPaperAcknow.items()))):
        if k[2] in DL57:
            dl57[initial] = v
        elif k[2] in iFCT:
            ifct[initial] = v
        else:
            if v:
                other[initial] = v
        # if len(v)==0:
        #     initials.pop(i)
        #     ThisPaperAcknow.pop(k)

    msg += '\n'
    msg += individual(dl57, dl57=True, width=width, ret=True)
    msg += individual(ifct, ifct=True, width=width, ret=True)
    msg += individual(other, width=width, ret=True)

    return msg


if __name__ == '__main__':

    args = _parser()
    print(args)
    list_authors = args.authors

    if '?' in list_authors:
        print('Possible names for authors are (space-separated):')
        [print('  ' + n[2]) for n in list(acknow.keys())]
        sys.exit(0)

    print('There are %d team members with known %s' % (len(acknow), name))
    nauthors = len(list_authors)
    if nauthors == 1:
        print('There is 1 author:')
    else:
        print('There are %d authors:' % len(list_authors))
    print('\t', list_authors)

    # should we sort alphabetically?
    # otherwise use the same order as input
    if args.sortalpha:
        print('Sorting authors alphabetically by first name:')
        list_authors = sorted(list_authors)
        print(list_authors)

    akn = acknowledgements(list_authors)
    print(akn)