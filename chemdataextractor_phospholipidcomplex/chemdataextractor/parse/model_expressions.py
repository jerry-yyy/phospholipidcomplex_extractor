'''
Expressions for models about phosphlipid complex

'''

from chemdataextractor.parse import I, W, R, join, OneOrMore, Optional
import re


api_model_expression_1 = R('^.+[–-]PC$')

api_model_expression_2 = (R('^.+[–-]phospholipid$') + I('complex')).add_action(join)

api_model_expression_3 = (I('phospholipid') + I('complex')).add_action(join)

api_model_expression = (api_model_expression_1 | api_model_expression_2)

solvent = (I('water') | I('ethanol') | I('methanol') | I('acetone') | I('chloroform') | I('hexane') | I('toluene') | I('dichloromethane'))('solvent')

solvent_phrase = (W('in') | W('with') | W('using')).hide() + solvent

sovent_model_expression = (I('solvent'))

molar_ratio_model_expression = (Optional(I('molar')) + OneOrMore(I('ratio') | I('ratios'))).add_action(join)

combine_rate_model_expression = (OneOrMore(I('combine') | I('combination') | I('complex') | I('complexation') | I('binding') | I('incorporation') | I('concentration') | I('concentrations') | I('encapsulation')) + Optional(I('efficiency') | I('rate') | I('rates') | I('percentage') | I('extent'))).add_action(join)

temperature_model_expression_1 = (Optional(I('was') | I('were')) + OneOrMore(I('reflux') | I('reﬂux') |  I('refluxed') | I('reﬂuxed') | I('refluxing') | I('reﬂuxing') |I('dissolved') | I('dissolved')) + Optional(I('at'))).add_action(join)

temperature_model_expression_2 = (Optional(I('was') | I('were') | I('in') | I('under') | I('with')) + Optional(I('a')) + Optional(I('magnetic')) + OneOrMore(I('stirring') | I('stirred') | I('stirrer')) + Optional(I('at'))).add_action(join)

temperature_model_expression_3 = (I('mixture'))

temperature_model_expression_4 = (I('reaction') + Optional((I('temperature') | I('temperatures')))).add_action(join)

temperature_model_expression = (temperature_model_expression_1 | temperature_model_expression_2 | temperature_model_expression_3 | temperature_model_expression_4)

time_model_expression_1 = (Optional(I('was') | I('were')) + OneOrMore(I('reflux') | I('reﬂux') |  I('refluxed') | I('reﬂuxed') | I('refluxing') | I('reﬂuxing') | I('dissolved') | I('dissolved')) + Optional(I('at'))).add_action(join)

time_model_expression_2 = (Optional(I('was') | I('were') | I('in') | I('under') | I('with')) + Optional(I('a')) + Optional(I('magnetic')) + OneOrMore(I('stirring') | I('stirred') | I('stirrer')) + Optional(I('at'))).add_action(join)

time_model_expression_3 = (I('mixture'))

time_model_expression_4 = (I('reaction') + Optional((I('time') | I('times')))).add_action(join)

time_model_expression = (time_model_expression_1 | time_model_expression_2 | time_model_expression_3 | time_model_expression_4)
