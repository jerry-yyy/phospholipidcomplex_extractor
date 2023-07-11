"""
Parses articles for the phospholipid complex project.

"""

import os
import json
from chemdataextractor import Document
from chemdataextractor.model.units.phospholipid_complex import API, Solvent, CombineRate, Temperature, Time, MolarRatio, EquiMolarRatio
from chemdataextractor.errors import ReaderError

chosen_model = Time  # API, Solvent, MolarRatio, CombineRate, Temperature, Time
model_name = chosen_model.__name__

extract_results = {}

for filename in os.listdir('example_articles'):
    if filename.endswith('.pdf'):
        try:

            with open(os.path.join('example_articles', filename), 'rb') as f:
                doc = Document.from_file(f)

            doc.models = [chosen_model]

            extract_results[filename] = doc.records.serialize()
            print(f'"{chosen_model.__name__}" is processing on {filename}')
        except ReaderError:
            print(f'Error reading file: {filename}')
        finally:

            with open(f'{chosen_model.__name__}_extract_results.json', 'w') as f:
                json.dump(extract_results, f)
