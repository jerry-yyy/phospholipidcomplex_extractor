# -*- coding: utf-8 -*-
"""
Parser for sentences that provide contextual information, such as apparatus, solvent, and temperature.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import re
from lxml import etree

from .common import optdelim, hyphen, slash
from ..utils import first
from ..parse.base import BaseSentenceParser
from .actions import join, merge, fix_whitespace
from .cem import cem, chemical_name
from .elements import I, T, R, W, ZeroOrMore, Optional, Group, OneOrMore, Any, Not

log = logging.getLogger(__name__)

dt = T('DT')

apparatus_type = R('^\d{2,}$') + W('MHz')
brands = I('HORIBA') + I('Jobin') + I('Yvon') | I('Hitachi') | I('Bruker') | I('Cary') | I('Jeol') | I('PerkinElmer') | I('Agilent') | I('Shimadzu') | I('Varian')
models = I('FluoroMax-4') | I('F-7000') | I('AVANCE') | I('Digital') | R('\d\d\d+') | I('UV–vis-NIR') | I('Mercury') | I('Avatar') | I('thermonicolet') | I('pulsed') | I('Fourier') | I('transform')
instrument = I('spectrofluorimeter') | I('spectrophotometer') | Optional(I('fluorescence')) + I('spectrometer') | Optional(I('nmr')) + I('workstation') | W('NMR') | I('instrument') | I('spectrometer')
apparatus = (ZeroOrMore(T('JJ')) + Optional(apparatus_type) + OneOrMore(T('NNP') | T('NN') | brands) + ZeroOrMore(T('NNP') | T('NN') | T('HYPH') | T('CD') | brands | models) + Optional(instrument))('apparatus').add_action(join).add_action(fix_whitespace)
apparatus_blacklist = R('^(following|usual|equation|standard|accepted|method|point|temperature|melting|boiling)$', re.I)
apparatus_phrase = (W('with') | W('using') | W('on')).hide() + Optional(dt).hide() + Not(apparatus_blacklist) + apparatus
solvent_phrase = (I('in').hide() + cem|chemical_name)('solvent')

class ApparatusParser(BaseSentenceParser):

    root = apparatus_phrase

    def interpret(self, result, start, end):
        log.debug(etree.tostring(result))
        apparatus = self.model(name=first(result.xpath('./text()')))
        log.debug(apparatus.serialize())
        yield apparatus


from .cem import solvent_name
complex_solvent = (I('ethanol') | I('methanol') | I('tetrahydrofuran') | I('chloroform') | I('ethanol:tetrahydrofuran') | I('1, 4-dioxane:methanol') | I('dichloromethane') | I('ethanol:dichloromethane') | I('n-hexane') | I('ethanol:water') | I('ethyl acetate') | I('acetic ether') | I('acetone') | I('dichloromethane:methanol') | I('ethyl acetate'))('solvent')
solvent_phrase =Optional(I('dissolved')).hide() + (I('in') | I('with') | I('using')).hide() + complex_solvent|solvent_name

class SolventParser(BaseSentenceParser):
    root = solvent_phrase

    def interpret(self, result, start, end):
        log.debug(etree.tostring(result))
        solvent = self.model(name=first(result.xpath('./text()')))
        log.debug(solvent.serialize())
        yield solvent
