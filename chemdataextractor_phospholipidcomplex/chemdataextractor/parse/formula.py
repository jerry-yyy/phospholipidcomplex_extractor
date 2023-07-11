from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import re

from .base import BaseSentenceParser
from .cem import chemical_name
from ..utils import first

log = logging.getLogger(__name__)

solvent = chemical_name('solvent')

class FormulaParser(BaseSentenceParser):
    """"""
    root = solvent

    def interpret(self, result, start, end):
        compound = self.model.fields['compound'].model_class()
        s = self.model(
            solvent=first(result.xpath('./solvent/text()'))
        )
        s.compound = compound
        yield s
