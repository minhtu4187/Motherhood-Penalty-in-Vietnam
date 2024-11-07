#\ \   / / | | | |   / ___/ ___|                              
# \ \ / /| |_| | |   \___ \___ \                              
#  \ V / |  _  | |___ ___) |__) |                             
# __\_/_ |_|_|_|_____|____/____/____  _   _  ___   ___  ____  
#|  \/  |/ _ \_   _| | | | ____|  _ \| | | |/ _ \ / _ \|  _ \ 
#| |\/| | | | || | | |_| |  _| | |_) | |_| | | | | | | | | | |
#| |  | | |_| || | |  _  | |___|  _ <|  _  | |_| | |_| | |_| |
#|_|__|_|\___/_|_|_|_| |_|_____|_|_\_\_| |_|\___/ \___/|____/ 
#|  _ \| ____| \ | |  / \  | | |_   _\ \ / /                  
#| |_) |  _| |  \| | / _ \ | |   | |  \ V /                   
#|  __/| |___| |\  |/ ___ \| |___| |   | |                    
#|_|   |_____|_| \_/_/   \_\_____|_|   |_|       

import os
os.chdir(r'/Users/professortu/Documents/GFE/11. ATPL/VHLSS/VLSS 2002 _ Vietnamese/')
import sys
sys.path.append(r'/Users/professortu/Documents/GFE/11. ATPL/VHLSS/')
import pandas as pd 
import numpy as np 
import linearmodels as plm
import statsmodels.api as sm
from scipy import stats
from ha_tabulate import tab 
#tab(data_Muc5b2,'m5b2ma_numeric' )
columns_to_keep = ['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'ttnt', 'matv', 
                   'm1ac1', 'm1ac1a', 'ttnt', 'schooling_years', 'dantoc', 'm1ac2', 'relation_to_head', 'm1ac4a', 
                   'm1ac4b', 'm1ac5', 'm4ac1a', 'm4ac2', 'm4ac6', 'm4ac7', 'm4ac8', 
                   'm4ac9', 'm4ac10b', 'total_income', 'm1ac6']

# ╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗#
# ║                                                                                                                        ║#
# ║                                                ✦✦✦  VHLSS 2004 DATA  ✦✦✦                                               ║#
# ║                                                                                                                        ║#
# ║────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────║#
# ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝#

ho1_2004                    = pd.read_stata('/Users/professortu/Documents/GFE/11. ATPL/VHLSS/VLSS 2004 _ Vietnamese/Data/VLSS 2004 _Ho/Ho1.dta', convert_categoricals=False)
ho1_2004                    = ho1_2004[ho1_2004['m1c1'] != 2]
ho1_2004['dup']             = ho1_2004.duplicated(subset=['tinh', 'huyen', 'xa', 'diaban', 'hoso'], keep=False).astype(int)
ho1_2004_cleaned            = ho1_2004[ho1_2004['dup'] == 0]
ho1_2004_cleaned            = ho1_2004_cleaned.drop(columns=['dup'])
ho1_2004_cleaned[['tinh', 'huyen', 'xa', 'diaban', 'hoso']] = ho1_2004_cleaned[['tinh', 'huyen', 'xa', 'diaban', 'hoso']].apply(pd.to_numeric, errors='coerce')
del ho1_2004

muc_123a_2004               = pd.read_stata('/Users/professortu/Documents/GFE/11. ATPL/VHLSS/VLSS 2004 _ Vietnamese/Data/VLSS 2004 _Ho/m1_2_3a.dta', convert_categoricals=False)
muc_123a_2004['dup']        = muc_123a_2004.duplicated(subset=['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv', 'ky'], keep=False).astype(int)
muc_123a_2004_cleaned       = muc_123a_2004[muc_123a_2004['dup'] == 0]
muc_123a_2004_cleaned       = muc_123a_2004_cleaned.drop(columns=['dup'])
del muc_123a_2004

muc_4a_2004                 = pd.read_stata('/Users/professortu/Documents/GFE/11. ATPL/VHLSS/VLSS 2004 _ Vietnamese/Data/VLSS 2004 _Ho/m4a.dta', convert_categoricals=False)
muc_4a_2004['dup']          = muc_4a_2004.duplicated(subset=['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv', 'ky'], keep=False).astype(int)
muc_4a_2004_cleaned         = muc_4a_2004[muc_4a_2004['dup'] == 0]
muc_4a_2004_cleaned         = muc_4a_2004_cleaned.drop(columns=['dup'])
del muc_4a_2004

data_2004                   = ho1_2004_cleaned.merge(muc_123a_2004_cleaned, on=['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'ky'], how='inner').merge(muc_4a_2004_cleaned, on=['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv'], how='left')

data_2004.rename(columns={'m2c1': 'schooling_years'}, inplace=True)
data_2004.rename(columns={'m1ac3': 'relation_to_head'}, inplace=True)

data_2004['m4ac11']         = pd.to_numeric(data_2004['m4ac11'], errors='coerce')
data_2004['m4ac12e']        = pd.to_numeric(data_2004['m4ac12e'], errors='coerce')
data_2004['m4ac21']         = pd.to_numeric(data_2004['m4ac21'], errors='coerce')
data_2004['m4ac22e']        = pd.to_numeric(data_2004['m4ac22e'], errors='coerce')
data_2004['m4ac25']         = pd.to_numeric(data_2004['m4ac25'], errors='coerce')

data_2004['total_income']   = data_2004[['m4ac11', 'm4ac12e', 'm4ac21', 'm4ac22e', 'm4ac25']].sum(axis=1, skipna=True)

data_2004                   = data_2004[columns_to_keep]

# ╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗#
# ║                                                                                                                        ║#
# ║                                                ✦✦✦  VHLSS 2006 DATA  ✦✦✦                                               ║#
# ║                                                                                                                        ║#
# ║────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────║#
# ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝#

ttchung_2006                 = pd.read_stata('/Users/professortu/Documents/GFE/11. ATPL/VHLSS/VLSS 2006 _ Vietnamese/Data/VLSS 2006 _ Ho/Income/ttchung.dta', convert_categoricals=False)
ttchung_2006                 = ttchung_2006.drop(columns=['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'ttnt'])
columns_to_rename            = ['tinh04', 'huyen04', 'xa04', 'diaban04', 'hoso04', 'ttnt04']
columns_to_move              = ['tinh', 'huyen', 'xa', 'diaban', 'hoso','ttnt']
ttchung_2006                 = ttchung_2006.rename(columns={col: col[:-2] for col in columns_to_rename})
ttchung_2006                 = ttchung_2006.reindex(columns=columns_to_move + [col for col in ttchung_2006.columns if col not in columns_to_move])
ttchung_2006['dup']          = ttchung_2006.duplicated(subset=['tinh', 'huyen', 'xa', 'diaban', 'hoso'], keep=False).astype(int)
ttchung_2006_cleaned         = ttchung_2006[ttchung_2006['dup'] == 0]
ttchung_2006_cleaned         = ttchung_2006_cleaned.drop(columns=['dup'])
ttchung_2006_cleaned[['tinh', 'huyen', 'xa', 'diaban', 'hoso']] = ttchung_2006_cleaned[['tinh', 'huyen', 'xa', 'diaban', 'hoso']].apply(pd.to_numeric, errors='coerce')
del columns_to_move, columns_to_rename, ttchung_2006

muc_2a_2006                 = pd.read_stata('/Users/professortu/Documents/GFE/11. ATPL/VHLSS/VLSS 2006 _ Vietnamese/Data/VLSS 2006 _ Ho/Income/muc2a.dta', convert_categoricals=False)
muc_2a_2006['dup']          = muc_2a_2006.duplicated(subset=['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv'], keep=False).astype(int)
muc_2a_2006_cleaned         = muc_2a_2006[muc_2a_2006['dup'] == 0]
muc_2a_2006_cleaned         = muc_2a_2006_cleaned.drop(columns=['dup'])
muc_2a_2006_cleaned[['tinh', 'huyen', 'xa', 'diaban', 'hoso']] = muc_2a_2006_cleaned[['tinh', 'huyen', 'xa', 'diaban', 'hoso']].apply(pd.to_numeric, errors='coerce')
del muc_2a_2006

muc_1a_2006                 = pd.read_stata('/Users/professortu/Documents/GFE/11. ATPL/VHLSS/VLSS 2006 _ Vietnamese/Data/VLSS 2006 _ Ho/Income/muc1a.dta', convert_categoricals=False)
muc_1a_2006['dup']          = muc_1a_2006.duplicated(subset=['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv'], keep=False).astype(int)
muc_1a_2006_cleaned         = muc_1a_2006[muc_1a_2006['dup'] == 0]
muc_1a_2006_cleaned         = muc_1a_2006_cleaned.drop(columns=['dup'])
muc_1a_2006_cleaned[['tinh', 'huyen', 'xa', 'diaban', 'hoso']] = muc_1a_2006_cleaned[['tinh', 'huyen', 'xa', 'diaban', 'hoso']].apply(pd.to_numeric, errors='coerce')
del muc_1a_2006

muc_4a_2006                 = pd.read_stata('/Users/professortu/Documents/GFE/11. ATPL/VHLSS/VLSS 2006 _ Vietnamese/Data/VLSS 2006 _ Ho/Income/muc4a.dta', convert_categoricals=False)
muc_4a_2006['dup']          = muc_4a_2006.duplicated(subset=['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv'], keep=False).astype(int)
muc_4a_2006_cleaned         = muc_4a_2006[muc_4a_2006['dup'] == 0]
muc_4a_2006_cleaned         = muc_4a_2006_cleaned.drop(columns=['dup'])
muc_4a_2006_cleaned[['tinh', 'huyen', 'xa', 'diaban', 'hoso']] = muc_4a_2006_cleaned[['tinh', 'huyen', 'xa', 'diaban', 'hoso']].apply(pd.to_numeric, errors='coerce')
del muc_4a_2006

data_2006                   = (  ttchung_2006_cleaned            
                               .merge(muc_1a_2006_cleaned, on=['tinh', 'huyen', 'xa', 'diaban', 'hoso'], how='inner')
                               .merge(muc_2a_2006_cleaned, on=['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv'], how='left')
                               .merge(muc_4a_2006_cleaned, on=['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv'], how='left')     
                               )


data_2006['m4ac11']         = pd.to_numeric(data_2006['m4ac11'], errors='coerce')
data_2006['m4ac12f']        = pd.to_numeric(data_2006['m4ac12f'], errors='coerce')
data_2006['m4ac21']         = pd.to_numeric(data_2006['m4ac21'], errors='coerce')
data_2006['m4ac22f']        = pd.to_numeric(data_2006['m4ac22f'], errors='coerce')
data_2006['m4ac25']         = pd.to_numeric(data_2006['m4ac25'], errors='coerce')

data_2006['total_income'] = data_2006[['m4ac11', 'm4ac12f', 'm4ac21', 'm4ac22f', 'm4ac25']].sum(axis=1, skipna=True)

data_2006.rename(columns={'m2ac1': 'schooling_years'}, inplace=True)
data_2006.rename(columns={'m1ac3': 'relation_to_head'}, inplace=True)

data_2006                   = data_2006[columns_to_keep]

# ╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗#
# ║                                                                                                                        ║#
# ║                                                ✦✦✦  VHLSS 2008 DATA  ✦✦✦                                               ║#
# ║                                                                                                                        ║#
# ║────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────║#
# ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝#

ho_2008                      = pd.read_stata('/Users/professortu/Documents/GFE/11. ATPL/VHLSS/VLSS 2008 _ Vietnamese/Data/VLSS 2008 _ Ho/ho.dta', convert_categoricals=False)
ho_2008                      = ho_2008.drop(columns=['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'ttnt'])
columns_to_rename            = ['tinh06', 'huyen06', 'xa06', 'diaban06', 'hoso06', 'ttnt06']
columns_to_move              = ['tinh', 'huyen', 'xa', 'diaban', 'hoso','ttnt']
ho_2008                      = ho_2008.rename(columns={col: col[:-2] for col in columns_to_rename})
ho_2008                      = ho_2008.reindex(columns=columns_to_move + [col for col in ho_2008.columns if col not in columns_to_move])
ho_2008['dup']               = ho_2008.duplicated(subset=['tinh', 'huyen', 'xa', 'diaban', 'hoso'], keep=False).astype(int)
ho_2008_cleaned              = ho_2008[ho_2008['dup'] == 0]
ho_2008_cleaned              = ho_2008_cleaned.drop(columns=['dup'])
del columns_to_move,columns_to_rename, ho_2008

ho11_2008                     = pd.read_stata('/Users/professortu/Documents/GFE/11. ATPL/VHLSS/VLSS 2008 _ Vietnamese/Data/VLSS 2008 _ Ho/ho11.dta', convert_categoricals=False)
ho11_2008['dup']              = ho11_2008.duplicated(subset=['tinh', 'huyen', 'xa', 'diaban', 'hoso'], keep=False).astype(int)
ho11_2008_cleaned             = ho11_2008[ho11_2008['dup'] == 0]
ho11_2008_cleaned             = ho11_2008_cleaned.drop(columns=['dup'])
del ho11_2008

muc_123a_2008               = pd.read_stata('/Users/professortu/Documents/GFE/11. ATPL/VHLSS/VLSS 2008 _ Vietnamese/Data/VLSS 2008 _ Ho/muc123a.dta', convert_categoricals=False)
muc_123a_2008['dup']        = muc_123a_2008.duplicated(subset=['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv'], keep=False).astype(int)
muc_123a_2008_cleaned       = muc_123a_2008[muc_123a_2008['dup'] == 0]
muc_123a_2008_cleaned       = muc_123a_2008_cleaned.drop(columns=['dup'])
del muc_123a_2008


muc_4a_2008                 = pd.read_stata('/Users/professortu/Documents/GFE/11. ATPL/VHLSS/VLSS 2008 _ Vietnamese/Data/VLSS 2008 _ Ho/muc4a.dta', convert_categoricals=False)
muc_4a_2008['dup']          = muc_4a_2008.duplicated(subset=['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv'], keep=False).astype(int)
muc_4a_2008_cleaned         = muc_4a_2008[muc_4a_2008['dup'] == 0]
muc_4a_2008_cleaned         = muc_4a_2008_cleaned.drop(columns=['dup'])
del muc_4a_2008

data_2008                   = (ho_2008_cleaned  
                               .merge(muc_123a_2008_cleaned, on=['tinh', 'huyen', 'xa', 'diaban', 'hoso'], how='inner')
                               .merge(muc_4a_2008_cleaned, on=['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv'], how='left')
                               )

data_2008['m4ac11']         = pd.to_numeric(data_2008['m4ac11'], errors='coerce')
data_2008['m4ac12f']        = pd.to_numeric(data_2008['m4ac12f'], errors='coerce')
data_2008['m4ac21']         = pd.to_numeric(data_2008['m4ac21'], errors='coerce')
data_2008['m4ac22f']        = pd.to_numeric(data_2008['m4ac22f'], errors='coerce')
data_2008['m4ac25']         = pd.to_numeric(data_2008['m4ac25'], errors='coerce')


data_2008['total_income']   = data_2008[['m4ac11', 'm4ac12f', 'm4ac21', 'm4ac22f', 'm4ac25']].sum(axis=1, skipna=True)

data_2008.rename(columns={'m2ac1': 'schooling_years'}, inplace=True)
data_2008.rename(columns={'m1ac3': 'relation_to_head'}, inplace=True)

data_2008                   = data_2008[columns_to_keep]

# ╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗#
# ║                                                                                                                        ║#
# ║                                                   ✦✦✦  PANEL DATA  ✦✦✦                                                 ║#
# ║                                                                                                                        ║#
# ║────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────║#
# ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝#

data_2004['year']            = 2004
data_2006['year']            = 2006
data_2008['year']            = 2008

panel_data                   = pd.concat([data_2004, data_2006, data_2008], axis=0)
panel_data.sort_values(by=['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv', 'year'], inplace=True)
panel_data.reset_index(drop=True, inplace=True)

panel_data['ethnic']        = panel_data['dantoc'].apply(lambda x: 1 if x == 1 else 0)
panel_data['marital_status'] = panel_data['m1ac6'].apply(lambda x: 1 if x==2 else 0)
panel_data['working?']       = panel_data['m4ac1a'].apply(lambda x: 1 if x == 1 else 0)
panel_data['canbo?']         = panel_data['m4ac10b'].apply(lambda x: 1 if x == 1 else 0)


zero_income_rows = panel_data[panel_data['total_income'] == 0]

# ╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗#
# ║                                                                                                                        ║#
# ║                                        ✦✦✦  MOTHER OF SMALL CHILD  ✦✦✦                                                 ║#
# ║                                                                                                                        ║#
# ║────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────║#
# ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝#

females_panel               = panel_data[panel_data['m1ac2'] == 2]
children_panel              = panel_data[panel_data['m1ac5'] < 3]
mothers_head_wife           = females_panel[females_panel['relation_to_head'].isin([1, 2])]
mothers_daughter            = females_panel[females_panel['relation_to_head'] == 3]
matched_head_wife           = pd.merge(children_panel[children_panel['relation_to_head'] == 3],
                              mothers_head_wife,
                              on=['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'year'],
                              suffixes=('_child', '_mother'))
matched_daughters           = pd.merge(children_panel[children_panel['relation_to_head'] == 6],
                              mothers_daughter,
                              on=['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'year'],
                              suffixes=('_child', '_mother'))
all_mothers_panel           = pd.concat([matched_head_wife, matched_daughters])

panel_data['mother_of_small_child'] = 0
panel_data.loc[panel_data[['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv', 'year']].apply(tuple, axis=1).isin(
    all_mothers_panel[['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv_mother', 'year']].apply(tuple, axis=1)),
    'mother_of_small_child'] = 1

del females_panel, children_panel, mothers_head_wife, mothers_daughter, matched_head_wife, matched_daughters, all_mothers_panel

# ╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗#
# ║                                                                                                                        ║#
# ║                                       ✦✦✦ DROPPING NAN AND CLEANNING THE PANEL ✦✦✦                                     ║#
# ║                                                                                                                        ║#
# ║────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────║#
# ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝#

panel_data                  = panel_data.dropna()
panel_data                  = panel_data[panel_data['total_income'] > 0]
panel_data                  = panel_data.drop(columns=['dantoc','m1ac2', 'm1ac6', 'm4ac1a', 'm4ac10b', 'relation_to_head'])


unique_years_per_individual = panel_data.groupby(['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv'])['year'].nunique()
valid_individuals           = unique_years_per_individual[unique_years_per_individual > 1].index
panel_data                  = panel_data[panel_data.set_index(['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv']).index.isin(valid_individuals)]
panel_data.reset_index(drop=True, inplace=True)

year_pairs                  = [(2004, 2006), (2006, 2008)]
grouped                     = panel_data.groupby(['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv'])
panel_data                  = grouped.filter(lambda x: len(x['year'].unique()) == 2 and tuple(sorted(x['year'].unique())) in year_pairs)
del valid_individuals, unique_years_per_individual 

# ╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗#
# ║                                                                                                                        ║#
# ║                                       ✦✦✦ RENAME AND ADDING CONTROL VARIABLES ✦✦✦                                      ║#
# ║                                                                                                                        ║#
# ║────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────║#
# ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝#

panel_data.rename(columns={'m1ac5': 'age'}, inplace=True)
panel_data.rename(columns={'m1ac2': 'gender'}, inplace=True)
panel_data['age_sq']        = panel_data['age']**2
panel_data['log_income']    = np.log(panel_data['total_income'])
panel_data['id']            = panel_data.groupby(['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv']).ngroup() + 1 

columns_order               = [
                                'tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv', 'm1ac1', 'm1ac1a', 'year', 'id',
                                'mother_of_small_child', 'log_income', 'age', 'age_sq', 'schooling_years', 'ttnt', 
                                'ethnic', 'marital_status', 'working?', 'canbo?, total_income'
                                    ]
panel_data                  = panel_data[columns_order]

# ╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗#
# ║                                                                                                                        ║#
# ║                                             ✦✦✦ MODEL: FIRST DIFFERENCE ✦✦✦                                            ║#
# ║                                                                                                                        ║#
# ║────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────║#
# ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝#

X                           = panel_data[['mother_of_small_child', 'age', 'age_sq', 'schooling_years', 'ttnt', 'ethnic',
                                          'marital_status', 'working?', 'canbo?']]
Y                           = panel_data['log_income']

first_diff                  = pd.concat([panel_data['id'], X], axis=1)
first_diff                  = first_diff.groupby('id').diff()

first_diff.dropna(inplace=True)
first_diff.reset_index(drop=True, inplace=True)
first_diff = first_diff.loc[:, (first_diff != 0).any(axis=0)]
del first_diff

X_after                     = panel_data[['mother_of_small_child', 'age', 'age_sq', 'schooling_years', 'ethnic',
                                          'marital_status', 'canbo?']]

panel_data.set_index(['id', 'year'], drop=False, inplace=True)

firstdf_regress = plm.FirstDifferenceOLS.from_formula(
    formula='log_income ~ mother_of_small_child + age + age_sq + ttnt + schooling_years + ethnic + marital_status + `canbo?`',
    data=panel_data
)
results_fd                 = firstdf_regress.fit(cov_type='clustered',cluster_entity=True)
table_fd                   = pd.DataFrame({
                                'b': round(results_fd.params, 4),
                                'se': round(results_fd.std_errors, 4),
                                't': round(results_fd.tstats, 4),
                                'pval': round(results_fd.pvalues, 4)
                                })



