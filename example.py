# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2017  SysMedOs_team @ AG Bioanalytik, University of Leipzig:
# SysMedOs_team: Zhixu Ni, Georgia Angelidou, Maria Fedorova
# LipidCircos is licensed under `GPLv2 License`. Please read more information by the following link:
# [The GNU General Public License version 2] (https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
# Please cite our publication in an appropriate form.
#
# LibCircos.LipidCircos.py was forked from Circos for python3 on github (MIT License).
# The Circos repository is: https://github.com/ericmjl/Circos
# We acknowledge to the developers of Circos project.
#
# For more info please contact:
#     SysMedOs_team: oxlpp@bbz.uni-leipzig.de
#     LipidCircos repository: https://bitbucket.org/SysMedOs/lipidcircos
#     Developer Zhixu Ni zhixu.ni@uni-leipzig.de
#
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xlrd

from LibCircos.LipidCircos import CircosPlot

# Please go to line 215 - 218 to set output image parameters

filename = r'SampleData\CM_unox_pl_to_lpp.xlsx'
book = xlrd.open_workbook(filename)

lpp_t = r'SampleData\CM_LPP_Ident_list.xlsx'
lpp_df = pd.read_excel(lpp_t)

quant_lpp_t = r'SampleData\CM_LPP_Quant_list.xlsx'
quant_lpp_df = pd.read_excel(quant_lpp_t)

norm_t = r'SampleData\CM_unox_all_reversed.xlsx'
norm_df = pd.read_excel(norm_t)

quant_norm_t = r'SampleData\CM_PL_Quant_list.xlsx'
quant_norm_df = pd.read_excel(quant_norm_t)

plt_dct = {}
# color names from https://matplotlib.org/examples/color/named_colors.html
plot_lst = ['PC(16:0/18:1)', 'PC(18:0/18:2)', 'PE(18:0/20:3)']
plt_dct['PC(16:0/18:1)'] = {'PL': 'PC(16:0/18:1)', 'nodecolor': 'limegreen', 'edgecolor': 'limegreen'}
# plt_dct['PC(16:0/20:3)'] = {'PL': 'PC(16:0/20:3)', 'nodecolor': 'navy', 'edgecolor': 'navy'}
plt_dct['PC(18:0/18:2)'] = {'PL': 'PC(18:0/18:2)', 'nodecolor': 'blue', 'edgecolor': 'blue'}
plt_dct['PE(18:0/20:3)'] = {'PL': 'PE(18:0/20:3)', 'nodecolor': 'red', 'edgecolor': 'red'}
# plt_dct['PS(16:1/18:1)'] = {'PL': 'PS(16:1/18:1)', 'nodecolor': 'lawngreen', 'edgecolor': 'lawngreen'}

pa_df = norm_df.query('Class == "PA"').sort_values(by='Proposed_structures')
pc_df = norm_df.query('Class == "PC"').sort_values(by='Proposed_structures')
pe_df = norm_df.query('Class == "PE"').sort_values(by='Proposed_structures')
pg_df = norm_df.query('Class == "PG"').sort_values(by='Proposed_structures')
ps_df = norm_df.query('Class == "PS"').sort_values(by='Proposed_structures')

oap_df = lpp_df.query('Type == "OAP"').sort_values(by='Proposed_structures')
ocp_df = lpp_df.query('Type == "OCP"').sort_values(by='Proposed_structures')
lyso_df = lpp_df.query('Type == "Lyso"').sort_values(by='Proposed_structures')
prostane_df = lpp_df.query('Type == "Prostane"').sort_values(by='Proposed_structures')

# print(lyso_df.head(10))

pa_lst = pa_df['Proposed_structures'].tolist()
pc_lst = pc_df['Proposed_structures'].tolist()
pe_lst = pe_df['Proposed_structures'].tolist()
pg_lst = pg_df['Proposed_structures'].tolist()
ps_lst = ps_df['Proposed_structures'].tolist()
oap_lst = oap_df['Proposed_structures'].tolist()
ocp_lst = ocp_df['Proposed_structures'].tolist()
lyso_lst = lyso_df['Proposed_structures'].tolist()
prostane_lst = prostane_df['Proposed_structures'].tolist()

print('File loaded!')

nrows = book.sheet_by_name('Sheet1').nrows
header = book.sheet_by_name('Sheet1').row_values(0)
data = [book.sheet_by_name('Sheet1').row_values(i) for i in range(1, nrows)]
df = pd.DataFrame(data, columns=header)
df[df == ''] = np.nan

df_dict = {}
for i in df.columns.tolist():
    df_dict[i] = list(df.loc[:, i].dropna())

pre_all_nodes = []
for key in df_dict.keys():
    pre_all_nodes.extend(df_dict[key])
pre_all_nodes = list(pre_all_nodes)

headers = list(df.columns)

lpp_node_lst = []
for header in headers:
    lpp_node_lst.append(header)
pre_all_nodes.extend(lpp_node_lst)

pa_nodes = []
pc_nodes = []
pe_nodes = []
pg_nodes = []
ps_nodes = []
oap_nodes = []
ocp_nodes = []
lyso_nodes = []
prostane_nodes = []

for n in pre_all_nodes:
    if n in pa_lst:
        pa_nodes.append(n)
    if n in pc_lst:
        pc_nodes.append(n)
    if n in pe_lst:
        pe_nodes.append(n)
    if n in pg_lst:
        pg_nodes.append(n)
    if n in ps_lst:
        ps_nodes.append(n)
    if n in oap_lst:
        oap_nodes.append(n)
    if n in ocp_lst:
        ocp_nodes.append(n)
    if n in lyso_lst:
        lyso_nodes.append(n)
    if n in prostane_lst:
        prostane_nodes.append(n)

all_nodes = []
all_lst = [sorted(set(pa_nodes)), sorted(set(pc_nodes)), sorted(set(pe_nodes)),
           sorted(set(pg_nodes)), sorted(set(ps_nodes)),
           sorted(set(lyso_nodes)), sorted(set(prostane_nodes)), sorted(set(ocp_nodes)), sorted(set(oap_nodes))]
for part_nodes in all_lst:
    all_nodes.extend(part_nodes)

print(all_nodes)

node_data_dct = {}

for _idx, _row in quant_lpp_df.iterrows():
    tmp_lst = []
    if _row['Proposed_structures'] in all_nodes:
        tmp_lst = [_row['Control'], _row['15min'], _row['30min'], _row['70min'], _row['16h']]
        node_data_dct[_row['Proposed_structures']] = tmp_lst

# for _i, _n_row in quant_norm_df.iterrows():
#     tmp_lst = []
#     if _n_row['Proposed_structures'] in all_nodes:
#         print('Found Normal PL', _n_row['Proposed_structures'])
#         tmp_lst = [_n_row['Control'], _n_row['15min'], _n_row['30min'], _n_row['70min'], _n_row['16h']]
#         node_data_dct[_n_row['Proposed_structures']] = tmp_lst
#     else:
#         print('NO Normal PL', _n_row['Proposed_structures'])

print(len(all_nodes))
print(len(set(pa_nodes)), len(set(pc_nodes)), len(set(pe_nodes)), len(set(pg_nodes)), len(set(ps_nodes)),
      len(set(oap_nodes)), len(set(ocp_nodes)), len(set(lyso_nodes)), len(set(prostane_nodes)))
print(len(pa_lst), len(pc_lst), len(pe_lst), len(pg_lst), len(ps_lst), len(oap_lst), len(ocp_lst), len(lyso_lst))
print(pa_df.shape, pc_df.shape, pe_df.shape, pg_df.shape, ps_df.shape, oap_df.shape, ocp_df.shape, lyso_df.shape)

edges_origin = []
for key in df_dict.keys():
    for value in df_dict[key]:
        edges_origin.append((key, value))
img = plt.figure(figsize=(20, 20))
ax = img.add_subplot(111)
cir_plt = CircosPlot(all_nodes=all_nodes, radius=12, subplot=ax, fig=img)


# cir_plt.add_edges(edges_origin, edgecolor='grey', alpha=0.1, lw=2)

for node in all_nodes:
    if node in pa_nodes:
        edgecolor = (0.8, 0.0, 1.0, 0.2)  # purple
    elif node in pc_nodes:
        edgecolor = (1.0, 0.4, 0.0, 0.2)  # orange
    elif node in pe_nodes:
        edgecolor = (0.0, 0.7, 0.8, 0.2)  # cyan
    elif node in pg_nodes:
        edgecolor = (0.6, 0.6, 0.0, 0.2)  # yellow
    elif node in ps_nodes:
        edgecolor = (0.4, 0.0, 0.0, 0.2)  # dark red
    else:
        edgecolor = (0.0, 0.0, 0.0, 0.2)  # grey

    edges = []
    if node in df_dict.keys():
        for value in df_dict[node]:
            edges.append((node, value))

        cir_plt.add_edges(edges, edgecolor=edgecolor, lw=2)


print(node_data_dct.keys())
cir_plt.add_nodes_data(all_nodes, nodes_data=node_data_dct)

cir_plt.add_nodes(pa_nodes, nodecolor=(0.8, 0.0, 1.0, 0.3))  # purple
cir_plt.add_nodes(pc_nodes, nodecolor=(1.0, 0.4, 0.0, 0.3))  # orange
cir_plt.add_nodes(pe_nodes, nodecolor=(0.0, 0.7, 0.8, 0.3))  # cyan
cir_plt.add_nodes(pg_nodes, nodecolor=(0.6, 0.6, 0.0, 0.3))  # yellow
cir_plt.add_nodes(ps_nodes, nodecolor=(0.4, 0.0, 0.0, 0.3))  # dark red
cir_plt.add_nodes(lyso_nodes, nodecolor=(0.0, 0.8, 0.6, 0.3))  # deep green
cir_plt.add_nodes(prostane_nodes, nodecolor=(0.0, 0.0, 0.0, 0.3))  # grey
cir_plt.add_nodes(ocp_nodes, nodecolor=(1.0, 0.0, 0.0, 0.3))  # red
cir_plt.add_nodes(oap_nodes, nodecolor=(0.0, 0.0, 1.0, 0.3))  # blue

for node in plot_lst:
    node_dct = plt_dct[node]
    nodecolor = node_dct['nodecolor']
    edgecolor = node_dct['edgecolor']
    nodes = [node]
    edges = []
    for _node in nodes:
        for value in df_dict[_node]:
            edges.append((_node, value))

    cir_plt.add_edges(edges, edgecolor=edgecolor, zorder=10, alpha=0.6, lw=3)
    cir_plt.add_nodes(nodes, nodecolor=nodecolor, zorder=10)

# save as png
img.savefig(r'SampleData\CM_circos_plot_600dpi.png', dpi=600)
# save as svg
img.savefig(r'SampleData\CM_circos_plot_600dpi.svg', dpi=600)

print('!!SAVED!!')
