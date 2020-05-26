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
def readItem(item,itemname):
    if itemname not in item['donneesNationales']:
        return 0

    return item['donneesNationales'][itemname]


# Argument options
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path",	help="Git repo Path")
args = vars(ap.parse_args())

################################
# Read opencovid19 YAML datas
################################

# Get yaml files list
searchpath=args['path']
files = [os.path.join(searchpath, f) for f in os.listdir(searchpath) if f.rfind('.yaml')>=0 and os.path.isfile(os.path.join(searchpath, f))]
files = sorted(files)

# Generate data lists
deltas = []
datas = []
for filename in files:
    with open(filename, 'r') as f:
        # Get Yaml item
        item = yaml.safe_load(f)

        # Add to datas array
        data = (
            item['date'],
            readItem(item,'casConfirmes'),
            readItem(item,'hospitalises'),
            readItem(item,'gueris'),
            readItem(item,'reanimation'),
            readItem(item,'deces'),
            readItem(item,'casEhpad'),
            readItem(item,'casConfirmesEhpad'),
            readItem(item,'decesEhpad')
            )
        datas.append(data)

days = [1,3,7,15]
fieldscolumn = OrderedDict()
fieldscolumn={
    'casConfirmes':{
        'total':True,
    },
    'hospitalises':{
        'total':False
    },
    'gueris':{
        'total':True
    },
    'reanimation':{
        'total':False
    },
    'deces':{
        'total':True
    },
    'casEhpad':{
        'total':True
    },
    'casConfirmesEhpad':{
        'total':True
    },
    'decesEhpad':{
        'total':True
    }
}

# Convert to dataframe
columns = ['date']
columns.extend(fieldscolumn)
df=pd.DataFrame(
    datas,
    columns=columns
)
df = df.set_index('date')

# Compute fields
for field in fieldscolumn:
    for d in days :
        if not fieldscolumn[field]['total'] and d>1:
            df[f'avg_{field}_{d}j'] = df[field].rolling(window=d).mean().round(4)

        df[f'diff_{field}_{d}j'] = df[field].diff(periods=d)
        df[f'var_{field}_{d}j'] = df[field].pct_change(periods=d).round(4)
        df[f'var_diff_{field}_{d}j'] = df[f'diff_{field}_{d}j'].pct_change(periods=1).round(4)


# Order columns
dfcolumns=[]
for field in fieldscolumn:
    dfcolumns.append(field)

    # Avg
    if not fieldscolumn[field]['total']:
        for d in days :
            if d > 1:
                dfcolumns.append(f'avg_{field}_{d}j')

    # Global Variation
    for d in days :
        # Keep only positive value
        if not fieldscolumn[field]['total']:
            mask = df[f'var_{field}_{d}j']<0
            df[mask][f'var_{field}_{d}j'] = np.nan

        dfcolumns.append(f'var_{field}_{d}j')

    # Diff
    for d in days :
        dfcolumns.append(f'diff_{field}_{d}j')

    # differential variation
    for d in days :
        dfcolumns.append(f'var_diff_{field}_{d}j')


# Save to CSV Raw
df = df[dfcolumns]
df.to_csv('/tmp/summary.csv',sep=';')


####################
# Compute trend
####################


# Add trend column
for column in df.columns:
    if 'var_' in column:
        # Convert to percent
        df[column] = (df[column]*100.0).round(4)

        # Compute trend
        trendcol = column.replace('var_','trend_')

        # positive=['⬌','⬈','⬈⬈','⬈⬈⬈']
        # negative=['⬌','⬊','⬊⬊','⬊⬊⬊']

        notrend='⬌'
        positive=[notrend,'⬈','⬈','⬈']
        negative=[notrend,'⬊','⬊','⬊']

        # Init new colmn
        unknow='?'
        df[trendcol]=unknow

        # Negative values
        # mask = df[column] == -np.inf
        # df[trendcol][mask] = 'X'

        # mask = (df[column]<=0) & (df[column]>-5)
        # df[trendcol][mask] = negative[0]

        mask = (df[column]<=-5) & (df[column]>-25)
        df[trendcol][mask] = negative[1]

        mask = (df[column]<=-25) & (df[column]>-50)
        df[trendcol][mask] = negative[2]

        mask = df[column]<=-50
        df[trendcol][mask] = negative[3]

        mask = (df[column]>=-5) & (df[column]<5)
        df[trendcol][mask] = positive[0]

        mask = (df[column]>=5) & (df[column]<25)
        df[trendcol][mask] = positive[1]

        mask = (df[column]>=25) & (df[column]<50)
        df[trendcol][mask] = positive[2]

        mask = df[column]>=50
        df[trendcol][mask] = positive[3]


    # No mouvement
for field in fieldscolumn:
    for d in days :
        mask = (df[f'diff_{field}_{d}j'] == 0) & (df[f'trend_diff_{field}_{d}j'] == unknow)
        df[f'var_diff_{field}_{d}j'][mask] = 0
        df[f'trend_diff_{field}_{d}j'][mask] = notrend


outcolumns = [
    'casConfirmes',
    'diff_casConfirmes_1j',
    'var_diff_casConfirmes_1j',
    'trend_diff_casConfirmes_1j',
    'diff_casConfirmes_7j',
    'var_diff_casConfirmes_7j',
    'trend_diff_casConfirmes_7j',

    'hospitalises',
    'diff_hospitalises_1j',
    'var_diff_hospitalises_1j',
    'trend_diff_hospitalises_1j',
    'diff_hospitalises_7j',
    'var_diff_hospitalises_7j',
    'trend_diff_hospitalises_7j',

    'gueris',
    'diff_gueris_1j',
    'var_diff_gueris_1j',
    'trend_diff_gueris_1j',
    'diff_gueris_7j',
    'var_diff_gueris_7j',
    'trend_diff_gueris_7j',

    'reanimation',
    'diff_reanimation_1j',
    'var_diff_reanimation_1j',
    'trend_diff_reanimation_1j',
    'diff_reanimation_7j',
    'var_diff_reanimation_7j',
    'trend_diff_reanimation_7j',

    'deces',
    'diff_deces_1j',
    'var_diff_deces_1j',
    'trend_diff_deces_1j',
    'diff_deces_7j',
    'var_diff_deces_7j',
    'trend_diff_deces_7j',
]


df = df[outcolumns]
df.to_csv('/tmp/trend.csv',sep=';')

######################
# Generate HTML pages
######################
html="""<html lang="fr">
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
      <th class='center' scope="col" rowspan="2" colspan="1">Date</th>
      <th class='center' scope="col" colspan="3">Cas confirmés</th>
      <th class='center' scope="col" colspan="3">Hospitalises</th>
      <th class='center' scope="col" colspan="3">Guéris</th>
      <th class='center' scope="col" colspan="3">Réanimations</th>
      <th class='center' scope="col" colspan="3">Décès</th>
    </tr>
    <tr>
      <th class='center' scope="col">Nb</th>
      <th class='left' scope="col">1j</th>
      <th class='left' scope="col">7j</th>
      <th class='center' scope="col">Nb</th>
      <th class='left' scope="col">1j</th>
      <th class='left' scope="col">7j</th>
      <th class='center' scope="col">Nb</th>
      <th class='left' scope="col">1j</th>
      <th class='left' scope="col">7j</th>
      <th class='center' scope="col">Nb</th>
      <th class='left' scope="col">1j</th>
      <th class='left' scope="col">7j</th>
      <th class='center' scope="col">Nb</th>
      <th class='left' scope="col">1j</th>
      <th class='left' scope="col">7j</th>
    </tr>
  </thead>
  <tbody>
"""

htmlcolumn=['casConfirmes','hospitalises','gueris','reanimation','deces']

for idx, item in df.iterrows():
    html += f"""
    <tr>
      <td class="center" scope="row" data-label="cas_confirmes">{idx}</td>
"""

    for column in htmlcolumn:

        diff_1j = str(item[f'diff_{column}_1j'])
        diff_1j = diff_1j.replace('nan','')
        if diff_1j!='' and '-' not in diff_1j:
            diff_1j = f'+{item[f"diff_{column}_1j"]}'
            diff_1j = diff_1j.replace('.0','')


        var_diff_1j = str(item[f'var_diff_{column}_1j'])
        var_diff_1j = var_diff_1j.replace('nan','')
        if var_diff_1j!='' and '-' not in var_diff_1j:
            var_diff_1j = f'+{item[f"var_diff_{column}_1j"]}'

        if var_diff_1j != '':
            var_diff_1j += '%'


        diff_7j = str(item[f'diff_{column}_7j'])
        diff_7j = diff_7j.replace('nan','')
        if diff_7j!='' and '-' not in diff_7j:
            diff_7j = f'+{item[f"diff_{column}_7j"]}'
            diff_7j = diff_7j.replace('.0','')


        var_diff_7j = str(item[f'var_diff_{column}_7j'])
        var_diff_7j = var_diff_7j.replace('nan','')
        if var_diff_7j!='' and '-' not in var_diff_7j:
            var_diff_7j = f'+{item[f"var_diff_{column}_7j"]}'

        if var_diff_7j != '':
            var_diff_7j += '%'

        ###############
        # casConfirmes
        ###############

        # 1j
        stylecolor=""
        if item[f'trend_diff_{column}_1j'] in positive[1:]:
            stylecolor1j="good"
        elif item[f'trend_diff_{column}_1j'] in negative[1:]:
            stylecolor1j="bad"
        else:
            stylecolor1j="unknow"

        # 7j
        stylecolor=""
        if item[f'trend_diff_{column}_7j'] in positive[1:]:
            stylecolor7j="good"
        elif item[f'trend_diff_{column}_7j'] in negative[1:]:
            stylecolor7j="bad"
        else:
            stylecolor7j="unknow"


        # html += f"""
        #   <td class="center" data-label="confirmes_nb">{item[f'{column}']}</td>
        #   <td class="left" data-label="{column}_1j"><span class="{stylecolor1j}">{item[f'trend_diff_{column}_1j']} {eval(f'var_diff_{column}_1j')}</span> ({eval(f'diff_{column}_1j')})</td>
        #   <td class="left" data-label="{column}_7j"><span class="{stylecolor1j}">{item[f'trend_diff_{column}_7j']} {eval(f'var_diff_{column}_7j')}</span> ({eval(f'diff_{column}_7j')})</td>
        # """

        html += f"""
        <td class="center" data-label="{column}_nb">{item[f'{column}']}</td>
        <td class="left" data-label="{column}_1j"><span class="{stylecolor1j}">{item[f'trend_diff_{column}_1j']} {eval(f'var_diff_1j')}</span> ({eval(f'diff_1j')})</td>
        <td class="left" data-label="{column}_1j"><span class="{stylecolor7j}">{item[f'trend_diff_{column}_7j']} {eval(f'var_diff_7j')}</span> ({eval(f'diff_7j')})</td>
        """

    html += """
    </tr>"""

html+="""
</tbody>
</table>"""


print(html)
