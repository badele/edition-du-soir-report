#!/usr/bin/python
import os
import yaml
import argparse
import numpy as np
import pandas as pd
from collections import OrderedDict

# Set pandas options
pd.set_option('mode.chained_assignment', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

# ReadItem, if not exists, set 0 value


def readItem(item, itemname):
    if itemname not in item['donneesNationales']:
        return 0

    return item['donneesNationales'][itemname]


# Argument options
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path",	help="Git repo Path")
args = vars(ap.parse_args())

# Init columns informations
days = [1,  7]
fieldscolumn = OrderedDict()
fieldscolumn = {
    'cas_confirmes': {
        'total': True,
    },
    'hospitalises': {
        'total': False
    },
    'nouvelles_hospitalisations': {
        'total': False
    },
    'gueris': {
        'total': True,
        'reverse': True

    },
    'reanimation': {
        'total': False
    },
    'nouvelles_reanimations': {
        'total': False
    },
    'deces': {
        'total': True

    },
    'cas_ehpad': {
        'total': True

    },
    'cas_confirmes_ehpad': {
        'total': True

    },
    'deces_ehpad': {
        'total': True

    }
}


# Read OpenCovid19 datas
orig = pd.read_csv(
    'https://raw.githubusercontent.com/opencovid19-fr/data/master/dist/chiffres-cles.csv',
    sep=','
)
orig = orig.set_index('date')

# Create mask
mask_MSS = (orig['source_type'] ==
            'ministere-sante') & (orig['granularite'] == 'pays')

mask_OC19 = (orig['source_type'] ==
             'opencovid19-fr') & (orig['granularite'] == 'pays')

df_MSS = orig[mask_MSS]
df_OC19 = orig[mask_OC19]

# Merge datas
df = df_MSS
df['nouvelles_hospitalisations'] = df_OC19['nouvelles_hospitalisations']
df['nouvelles_reanimations'] = df_OC19['nouvelles_reanimations']

# Compute fields
for field in fieldscolumn:
    for d in days:
        if not fieldscolumn[field]['total'] and d > 1:
            df[f'avg_{field}_{d}j'] = df[field].rolling(
                window=d).mean().round(4)

        df[f'diff_{field}_{d}j'] = df[field].diff(periods=d)
        df[f'var_{field}_{d}j'] = df[field].pct_change(periods=d).round(4)
        df[f'var_diff_{field}_{d}j'] = df[f'diff_{field}_{d}j'].pct_change(
            periods=1).round(4)


# Order columns
dfcolumns = []
subfields = ['var', 'diff', 'avg', 'var_diff']
for field in fieldscolumn:
    dfcolumns.append(field)

for subfield in subfields:
    for d in days:
        for field in fieldscolumn:

            # Avg
            if subfield == 'avg':
                if not fieldscolumn[field]['total']:
                    if d > 1:
                        dfcolumns.append(f'{subfield}_{field}_{d}j')

            # Global Variation
            if subfield == 'var':
                # Keep only positive value
                if not fieldscolumn[field]['total']:
                    mask = df[f'{subfield}_{field}_{d}j'] < 0
                    df[mask][f'{subfield}_{field}_{d}j'] = np.nan

                dfcolumns.append(f'{subfield}_{field}_{d}j')

            # Diff
            if subfield == 'diff':
                dfcolumns.append(f'{subfield}_{field}_{d}j')

            # differential variation
            if subfield == 'var_diff':
                dfcolumns.append(f'{subfield}_{field}_{d}j')


# Save to CSV Raw
df = df[dfcolumns]
df.to_csv('/tmp/summary.csv', sep=';')

####################
# Compute trend
####################

# Add trend column
for column in df.columns:
    if 'var_' in column:
        # Convert to percent
        df[column] = (df[column]*100.0).round(4)

        # Compute trend
        trendcol = column.replace('var_', 'trend_')

        # positive=['⬌','⬈','⬈⬈','⬈⬈⬈']
        # negative=['⬌','⬊','⬊⬊','⬊⬊⬊']

        notrend = '⬌'
        positive = [notrend, '⬈', '⬈', '⬈']
        negative = [notrend, '⬊', '⬊', '⬊']

        # Init new colmn
        unknow = '?'
        df[trendcol] = unknow

        mask = (df[column] <= -5) & (df[column] > -25)
        df[trendcol][mask] = negative[1]

        mask = (df[column] <= -25) & (df[column] > -50)
        df[trendcol][mask] = negative[2]

        mask = df[column] <= -50
        df[trendcol][mask] = negative[3]

        mask = (df[column] >= -5) & (df[column] < 5)
        df[trendcol][mask] = positive[0]

        mask = (df[column] >= 5) & (df[column] < 25)
        df[trendcol][mask] = positive[1]

        mask = (df[column] >= 25) & (df[column] < 50)
        df[trendcol][mask] = positive[2]

        mask = df[column] >= 50
        df[trendcol][mask] = positive[3]


# No mouvement
for field in fieldscolumn:
    for d in days:
        mask = (df[f'diff_{field}_{d}j'] == 0) & (
            df[f'trend_diff_{field}_{d}j'] == unknow)
        df[f'var_diff_{field}_{d}j'][mask] = 0
        df[f'trend_diff_{field}_{d}j'][mask] = notrend

outfieldcolumns = [
    'cas_confirmes',
    'hospitalises',
    'nouvelles_hospitalisations',
    'gueris',
    'reanimation',
    'nouvelles_reanimations',
    'deces',
    'cas_confirmes_ehpad',
    'cas_ehpad',
    'deces_ehpad']

outstatscolumns = ['diff', 'var_diff', 'trend_diff']

outcolumns = outfieldcolumns.copy()
for outfield in outfieldcolumns:
    for d in days:
        for statcolumn in outstatscolumns:
            outcolumns.append(f'{statcolumn}_{outfield}_{d}j')


df = df[outcolumns]
df.to_csv('/tmp/trend.csv', sep=';')

######################
# Generate HTML pages
######################
htmlcolumn = ['cas_confirmes', 'hospitalises', 'nouvelles_hospitalisations',
              'gueris', 'reanimation', 'nouvelles_reanimations', 'deces',
              'cas_ehpad', 'cas_confirmes_ehpad', 'deces_ehpad']


def GetHhtmlInfo(item, column):
    diff_1j = str(item[f'diff_{column}_1j'])
    diff_1j = diff_1j.replace('nan', '')
    if diff_1j != '' and '-' not in diff_1j:
        diff_1j = f'+{item[f"diff_{column}_1j"]}'
        diff_1j = diff_1j.replace('.0', '')

    var_diff_1j = str(item[f'var_diff_{column}_1j'])
    var_diff_1j = var_diff_1j.replace('nan', '')
    if var_diff_1j != '' and '-' not in var_diff_1j:
        var_diff_1j = f'+{item[f"var_diff_{column}_1j"]}'

    if var_diff_1j != '':
        var_diff_1j += '%'

    diff_7j = str(item[f'diff_{column}_7j'])
    diff_7j = diff_7j.replace('nan', '')
    if diff_7j != '' and '-' not in diff_7j:
        diff_7j = f'+{item[f"diff_{column}_7j"]}'
        diff_7j = diff_7j.replace('.0', '')

    var_diff_7j = str(item[f'var_diff_{column}_7j'])
    var_diff_7j = var_diff_7j.replace('nan', '')
    if var_diff_7j != '' and '-' not in var_diff_7j:
        var_diff_7j = f'+{item[f"var_diff_{column}_7j"]}'

    if var_diff_7j != '':
        var_diff_7j += '%'

    state = ['bad', 'good', 'unknow']

    # 1j
    if item[f'trend_diff_{column}_1j'] in positive[1:]:
        # Bad
        styleidx = 0
    elif item[f'trend_diff_{column}_1j'] in negative[1:]:
        # Good
        styleidx = 1
    else:
        # Unknow
        styleidx = 2

    # Reverse trend if needed
    if 'reverse' in fieldscolumn[column] and fieldscolumn[column]['reverse'] and styleidx <= 1:
        styleidx = styleidx ^ 1

    stylecolor1j = state[styleidx]

    # 7j
    if item[f'trend_diff_{column}_7j'] in positive[1:]:
        # Good
        styleidx = 0
    elif item[f'trend_diff_{column}_7j'] in negative[1:]:
        # Bad
        styleidx = 1
    else:
        # Unknow
        styleidx = 2

    # Reverse trend if needed
    if 'reverse' in fieldscolumn[column] and fieldscolumn[column]['reverse'] and styleidx <= 1:
        styleidx = styleidx ^ 1

    stylecolor7j = state[styleidx]

    line = f"""<span class="{stylecolor1j}">{item[f'trend_diff_{column}_1j']}</span></br>"""
    line += f"""<span class="{stylecolor1j}">{var_diff_1j}</span> ({diff_1j})</br>"""
    line += "<br>"
    line += f"""<span class="{stylecolor7j}">{item[f'trend_diff_{column}_7j']}</span></br>"""
    line += f"""<span class="{stylecolor7j}">{var_diff_7j}</span> ({diff_7j})</br>"""

    line = f"""<span class="{stylecolor1j}">{item[f'trend_diff_{column}_1j']}&nbsp;{var_diff_1j}</span>&nbsp;({diff_1j})</br>"""
    line += f"""<span class="{stylecolor7j}">{item[f'trend_diff_{column}_7j']}&nbsp;{var_diff_7j}</span>&nbsp;({diff_7j})</br>"""

    return line


html = """<html lang="fr">
<head>
  <meta charset="utf-8">

  <title>Report</title>
  <meta name="description" content="Covid report">
  <link rel="stylesheet" href="./style.css">

</head>

<body>

<table>
  <caption>Rapport</caption>
  <thead>
    <tr>
      <th class='center' scope="col" >Date</th>
"""
for column in htmlcolumn:
    html += f"""<th class='center' scope="col" colspan=2 >{column}</th>"""

html += f"""
    </tr>
  </thead>
  <tbody>
"""


df = df.iloc[::-1]

for idx, item in df.iterrows():
    html += f"""
    <tr>
      <td class="center" scope="row" data-label="date">{idx}</td>
"""

    for column in htmlcolumn:
        html += f"""<td class="center field" scope="row" data-label="{column}">{item[column]}</td>"""
        html += f"""<td class="center" scope="row" data-label="{column}_trend">"""
        html += GetHhtmlInfo(item, column)
        html += "</td>"

    html += "</tr>"

html += """</tbody>
</table>"""


print(html)
