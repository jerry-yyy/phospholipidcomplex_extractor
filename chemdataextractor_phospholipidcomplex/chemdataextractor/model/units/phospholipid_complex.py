"""
Property models for phospholipid complex.

"""

from chemdataextractor.model.units import RatioModel, TimeModel, TemperatureModel, DimensionlessModel
from chemdataextractor import Document
from chemdataextractor.model import ModelType, StringType, Compound, BaseModel
from chemdataextractor.doc import Paragraph, Heading
from chemdataextractor.parse import I, W, R, AutoSentenceParser, AutoTableParser, join, OneOrMore, Optional
from chemdataextractor.parse.template_ok import MultiQuantityModelTemplateParser
from chemdataextractor.parse.model_expressions import sovent_model_expression, combine_rate_model_expression, temperature_model_expression, api_model_expression, molar_ratio_model_expression, time_model_expression, solvent_phrase
from chemdataextractor.parse.apparatus import SolventParser
import re


class API(BaseModel):
    """API"""
    specifier = StringType(
        parse_expression=api_model_expression,
        required=True,
        contextual=True,
        updatable=False
    )
    compound = ModelType(Compound, required=False, contextual=True, updatable=False)
    parsers = [AutoSentenceParser(), AutoTableParser()]


class Solvent(BaseModel):
    """Solvent"""
    name = StringType()
    parsers = [SolventParser()]


class EquiMolarRatio(BaseModel):
    """Test if Molar Ratio is 1:1"""
    specifier = StringType(
        parse_expression=(I('equimolar') + Optional(I('ratio') | I('concentration'))).add_action(join),
        required=True,
        contextual=True,
        updatable=False
    )
    compound = ModelType(Compound, required=False, contextual=True, updatable=False)
    parsers = [AutoSentenceParser()]


class MolarRatio(DimensionlessModel):
    """Molar Ratio(Numerical)"""
    specifier = StringType(
        parse_expression=molar_ratio_model_expression,
        required=True,
        contextual=True,
        updatable=False
    )
    compound = ModelType(Compound, required=False, contextual=False, updatable=False)
    parsers = [AutoSentenceParser(), AutoTableParser()]


class Temperature(TemperatureModel):
    """Temperature"""
    specifier = StringType(
        parse_expression = (temperature_model_expression),
        required=True,
        contextual=False,
        updatable=False
    )
    compound = ModelType(Compound, required=False, contextual=True, updatable=False)
    solvent = ModelType(Solvent, required=False, contextual=True, updatable=False)
    parsers = [AutoSentenceParser(), AutoTableParser(), MultiQuantityModelTemplateParser()]


class Time(TimeModel):
    """Time"""
    specifier = StringType(
        parse_expression=(time_model_expression),
        required=True,
        contextual=False,
        updatable=False
    )
    compound = ModelType(Compound, required=False, contextual=True, updatable=False)
    solvent = ModelType(Solvent, required=False, contextual=True, updatable=False)
    parsers = [AutoSentenceParser(), AutoTableParser(), MultiQuantityModelTemplateParser()]


class CombineRate(RatioModel):
    """Combine Rate"""
    specifier = StringType(
        parse_expression=(combine_rate_model_expression),
        required=True,
        contextual=False,
        updatable=False
    )
    compound = ModelType(Compound, required=False, contextual=True, updatable=False)
    time = ModelType(Time, required=False, contextual=True, updatable=False)
    temperature = ModelType(Temperature, required=False, contextual=True, updatable=False)
    parsers = [AutoSentenceParser(), AutoTableParser(), MultiQuantityModelTemplateParser()]
