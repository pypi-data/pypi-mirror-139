#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import h5py
import pandas as pd
import seaborn as sns
from gefpy.bgef_reader_cy import BgefR
from gefpy.utils import gef_is_cell_bin

# def find_cutoff(score_list, p):
#     """
#     calculate
#     :param score_list:
#     :param p: expression data for gene
#     :return: the cutoff of E10 or C50
#     """
#     #pdb.set_trace()
#     curve = score_list
#     mu = np.mean(curve)
#     sd = statistics.stdev(curve)
#     cutoff = stats.norm.ppf(p) * sd + mu
#     pkk = stats.norm.cdf(stats.norm.ppf(p))
#     return cutoff

def save_exp_heat_map(input_gef, output_png, scale=2, dpi=72):
    h5f = h5py.File(input_gef, 'r')
    if 'cellBin' in h5f:
        d_x = h5f['cellBin']['cell']['x']
        d_y = h5f['cellBin']['cell']['y']
        d_cnt = h5f['cellBin']['cell']['expCount']
        h5f.close()
    else:
        h5f.close()
        bgef = BgefR(input_gef, 200, 4)
        exp = bgef.get_reduce_expression()
        d_x = exp[:, 0]
        d_y = exp[:, 1]
        d_cnt = exp[:, 2]

    try:
        cmap = mpl.colors.ListedColormap(['#0C3383', '#0A88BA', '#F2D338', '#F28F38', '#D91E1E'])
        x_range=max(d_x) - min(d_x)
        y_range=max(d_y) - min(d_y)
        #x_num = len(data['x'].drop_duplicates())
        x_num = len(list(set(d_x)))

        plt.figure(figsize=(1*scale,y_range/x_range*scale), facecolor='#262B3D', edgecolor='black') ## 设置图像大小 inch
        ##去掉图像旁边的空白区
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        ##将y的坐标翻转
        plt.gca().xaxis.set_ticks_position('top')
        plt.gca().invert_yaxis()
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
        plt.margins(0,0)
        ##添加标题
        r = scale*72/(x_range/200)
        dot_size = r**2
        plt.scatter(d_x, d_y, c=d_cnt, s=dot_size, cmap=cmap)
        plt.axis('off')
        plt.savefig(output_png,facecolor='#262B3D', dpi=dpi, pad_inches = 0)
        return True
    except Exception as e:
        print(e)
        return False


def cgef_stat(input_cgef, figpath):
    b = 1
    scapath = os.path.join(figpath, "scatter_{0}x{0}_MID_gene_counts.png".format(b if b != 0 else "cell"))
    violinpath = os.path.join(figpath, "violin_{0}x{0}_MID_gene.png".format(b if b != 0 else "cell"))
    statisticPath = os.path.join(figpath, "statistic_{0}x{0}_MID_gene_DNB.png".format(b if b != 0 else "cell"))
    plt.figure(figsize=(5, 5))

    cgef = h5py.File(input_cgef)
    df = pd.DataFrame(cgef['cellBin']['cell']['expCount', 'geneCount', 'dnbCount'])
    df = df.rename(columns={'expCount': 'MID Count', 'geneCount': 'Gene Number', 'dnbCount': 'DNB Number'})
    # sns.scatterplot(x=df['n_counts'], y=df['n_genes'], edgecolor="gray", color="gray")
    plt.scatter(df['MID Count'], df['Gene Number'], color="gray", edgecolors="gray", s=0.8)
    plt.grid()
    plt.xlabel("MID Count")
    plt.ylabel("Gene Number")
    plt.savefig(scapath, format="png", bbox_inches="tight")

    plt.figure(figsize=(10, 6))
    plt.subplot(121)
    sns.violinplot(y=df['MID Count'])
    sns.stripplot(y=df['MID Count'], jitter=0.4, color="black", size=0.8)
    plt.ylabel("")
    plt.title("MID Count")
    plt.subplot(122)
    sns.violinplot(y=df['Gene Number'])
    sns.stripplot(y=df['Gene Number'], jitter=0.4, color="black", size=0.8)
    plt.ylabel("")
    plt.title("Gene Number")
    plt.savefig(violinpath, format="png", bbox_inches="tight")

    g = sns.FacetGrid(pd.melt(df[['MID Count', 'Gene Number', 'DNB Number']]), col='variable', hue='variable',
                      sharex=False, sharey=False, height=8, palette='Set1')
    g = (g.map(sns.distplot, "value", hist=False, rug=True))
    plt.savefig(statisticPath)

if __name__=='__main__':
    #a = [8,9,10,35,78,6,45,23,11,66,33,24,28,54,32, 26]
    #find_cutoff(a, 0.9)
    rc = save_exp_heat_map(
        # "../test_data/FP200000617TL_B6/FP200000617TL_B6.gefpy.bin1.3.gef",
        # "../../test_data/FP200000617TL_B6/FP200000617TL_B6.bgef.h5.gef",
        "../test_data/FP200000617TL_B6/FP200000617TL_B6.gefpy.cgef",
        "../test_data/FP200000617TL_B6/cellbin.png")
    cgef_stat("../test_data/FP200000617TL_B6/FP200000617TL_B6.gefpy.cgef", "../test_data/FP200000617TL_B6/")
    sys.exit(0 if rc else 2)



