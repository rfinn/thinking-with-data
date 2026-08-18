#!/usr/bin/env python

import sys

from astropy.table import Table
import pandas as pd

infile = sys.argv[1]



planets = pd.read_csv(infile, comment='#')

# remove planets with orbital_distance_au > 20
flag = planets['pl_orbsmax'] < 20.

planets = planets[flag]

# rename columns
planets = planets.rename(columns={'pl_name': 'planet_name',
                            'discoverymethod' : 'discovery_method',
                            'disc_year' : 'discovery_year',
                            'soltype': 'solution_type',
                            'pl_orbper': 'orbital_period_days',
                            'pl_orbsmax': 'orbital_distance_au',
                            'pl_bmasse': 'planet_mass_earth',
                            'pl_bmassj': 'planet_mass_jupiter'
                            }
                            )

print(planets.columns)


# write out results as planets_2026.csv
planets.to_csv('exoplanets_2026.csv', index=False)
