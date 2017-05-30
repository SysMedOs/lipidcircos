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
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from matplotlib.path import Path
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import PatchCollection
from matplotlib.patches import Ellipse


class CircosPlot(object):
    def __init__(self, all_nodes, radius, subplot=None, fig=None):
        self.all_nodes = all_nodes  # list of all_nodes

        self.radius = radius

        if subplot is None or fig is None:
            self.fig = plt.figure(figsize=(8, 8))
            self.ax = self.fig.add_subplot(111)
        else:
            self.ax = subplot
            self.fig = fig
        self.node_radius = self.radius*0.01
        self.ax.set_xlim(-radius*1.2, radius*1.2)
        self.ax.set_ylim(-radius*1.2, radius*1.2)
        self.ax.xaxis.set_visible(False)
        self.ax.yaxis.set_visible(False)
        for k in self.ax.spines.keys():
            self.ax.spines[k].set_visible(False)

    def add_nodes(self, nodes, nodecolor=None, zorder=None):
        """
        Draws all_nodes onto the canvas with colours.
        """
        r = self.radius
        node_radius = r * 0.019
        node_r = node_radius
        nodes_and_colors = zip(nodes, [nodecolor] * len(nodes))

        # Draw the all_nodes to screen.
        for node, color in nodes_and_colors:
            try:
                theta = self.node_theta(self.all_nodes, node)
                x, y = get_cartesian(r, theta)
                node_patch = patches.Ellipse((x, y), node_r, node_r, lw=0, facecolor=nodecolor)
                if zorder is not None:
                    node_patch.set_zorder(zorder)
                self.ax.add_patch(node_patch)
            except ValueError:
                print('PL origin not quantified')

    def add_nodes_data(self, nodes, nodes_data=None, zorder=None):
        """
        Draws all_nodes onto the canvas with colours.
        """
        r = self.radius
        node_radius = r * 0.019
        node_r = node_radius
        # nodes_and_colors = zip(nodes, [nodecolor] * len(nodes))

        cdict1 = {'red': ((0.0, 0.0, 0.0),
                          (0.5, 0.0, 0.1),
                          (1.0, 1.0, 1.0)),
                  'green': ((0.0, 0.0, 0.0),
                            (1.0, 0.0, 0.0)),
                  'blue': ((0.0, 0.0, 1.0),
                           (0.5, 0.1, 0.0),
                           (1.0, 0.0, 0.0))
                  }

        blue_red1 = LinearSegmentedColormap('BlueRed1', cdict1)
        patche_lst = []
        data_color_lst = []
        # Draw the all_nodes to screen.
        for node in nodes:
            try:
                theta = self.node_theta(self.all_nodes, node)
                if node in nodes_data.keys():
                    node_data = nodes_data[node]
                    for idx in range(0, len(node_data)):
                        data_r = r * (1.01 + 0.0225 * (idx + 1))
                        x, y = get_cartesian(data_r, theta)
                        # node_patch = patches.Ellipse((x, y), node_r, node_r, lw=0)
                        patche_lst += [Ellipse((x, y), node_r, node_r, lw=0)]
                        data_value = node_data[idx]
                        if data_value >= 1:
                            data_value = 1
                        elif data_value <= -1:
                            data_value = -1
                        data_color_lst.append(data_value)
            except ValueError:
                print('PL origin not quantified')

        p = PatchCollection(patche_lst, alpha=0.7)
        # blue to red
        # p = PatchCollection(patche_lst, cmap=blue_red1, alpha=0.7)
        p.set_array(np.array(data_color_lst))
        self.ax.add_collection(p)

        # plot color scale bar
        # self.fig.colorbar(p, ax=self.ax, orientation="horizontal", alpha=0.7)

    @staticmethod
    def node_theta(nodes, node):
        """
        Maps node to Angle.
        """
        i = nodes.index(node)
        theta = i*2*np.pi/len(nodes)

        return theta

    def add_edges(self, edges, edgecolor=None, zorder=None, alpha=0.2, lw=1):
        """
        Draws edges to screen.
        """

        for start, end in edges:
            try:
                start_theta = self.node_theta(self.all_nodes, start)
                end_theta = self.node_theta(self.all_nodes, end)
                verts = [get_cartesian(self.radius, start_theta),
                         (0, 0),
                         get_cartesian(self.radius, end_theta)]
                codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
                path = Path(verts, codes)
                edge_patch = patches.PathPatch(path, lw=lw, facecolor='none', edgecolor=edgecolor, alpha=alpha)
                if zorder is not None:
                    edge_patch.set_zorder(zorder)
                self.ax.add_patch(edge_patch)
            except ValueError:
                print('PL origin not quantified')


def get_cartesian(r, theta):
    x = r*np.sin(theta)
    y = r*np.cos(theta)

    return x, y
