# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 20:09:37 2021

@author: PURUSHOT

Post process the results on Cu Si pads
"""

import _pickle as cPickle
import matplotlib.pyplot as plt
import numpy as np
import os
from utils_lauenn import Lattice, Symmetry
import LaueTools.findorient as FindO
#from texture import PoleFigure  ### FOR PLOTS 
# from lattice import Lattice, calc_tex_mex_hexa, calc_tex_mex
folder = r"C:\Users\purushot\Desktop\Laue_Zr_HT\model_crg4\ZrO2_1200C_jan2022_1200C_new\results_ZrO2_1200C_2022-02-16_17-46-55"
with open(folder+"//results.pickle", "rb") as input_file:
    best_match, \
    mat_global, rotation_matrix1, strain_matrix, strain_matrixs,\
        col, colx, coly, match_rate, files_treated,\
            lim_x, lim_y, spots_len, iR_pix, fR_pix, material_, \
                material1_, lattice, lattice1, symmetry, symmetry1,\
                    crystal, crystal1 = cPickle.load(input_file)
match_tol = 0
fR_tol = 10000
matnumber = 1
rangemin = -0.5
rangemax = 0.5
bins = 100
rangeval = len(match_rate)
material_id = [material_, material1_]

#%% Compute lattice params from strain
import LaueTools.CrystalParameters as CP
import LaueTools.dict_LaueTools as dictLT
import scipy


constantlength = "a"

a,b,c,alp,bet,gam = [],[],[],[],[],[]
for irot in range(len(rotation_matrix1[0][0])):
    if (match_rate[0][0][irot] < match_tol) or \
        fR_pix[0][0][irot] > fR_tol:
        continue
    
    lattice_parameter_direct_strain = CP.computeLatticeParameters_from_UB(rotation_matrix1[0][0][irot,:,:], 
                                                                          material_, 
                                                                          constantlength, 
                                                                          dictmaterials=dictLT.dict_Materials)
    a.append(lattice_parameter_direct_strain[0])
    b.append(lattice_parameter_direct_strain[1])
    c.append(lattice_parameter_direct_strain[2])
    alp.append(lattice_parameter_direct_strain[3])
    bet.append(lattice_parameter_direct_strain[4])
    gam.append(lattice_parameter_direct_strain[5])


title = "Refined unit cell parameters a"+" "+material_id[0]
fig = plt.figure()
plt.xlabel(r"a", loc='center', fontsize=8)

logdata = np.array(a)
logdata = logdata[~np.isnan(logdata)]
xmin = logdata.min()
xmax = logdata.max()
x1 = np.linspace(xmin, xmax, 1000)
#estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
#pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
# plt.axvline(x=estimated_mu, c="k")
# plt.plot(x1, pdf, 'r')
rangemina, rangemaxa = np.min(logdata)-0.01, np.max(logdata)+0.01
plt.hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemina, rangemaxa))
plt.ylabel('Frequency', fontsize=8)
plt.tick_params(axis='both', which='major', labelsize=8)
plt.tick_params(axis='both', which='minor', labelsize=8)
plt.grid()
plt.savefig(folder+ "//"+title+'.png', format='png', dpi=1000) 
plt.close(fig)

title = "Refined unit cell parameters b"+" "+material_id[0]
fig = plt.figure()
plt.xlabel(r"b", loc='center', fontsize=8)
logdata = np.array(b)
logdata = logdata[~np.isnan(logdata)]
xmin = logdata.min()
xmax = logdata.max()
x1 = np.linspace(xmin, xmax, 1000)
#estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
#pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
# plt.axvline(x=estimated_mu, c="k")
# plt.plot(x1, pdf, 'r')
rangeminb, rangemaxb = np.min(logdata), np.max(logdata)
plt.hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangeminb, rangemaxb))
# axs[0, 1].hist(e22c, bins=bins)
plt.ylabel('Frequency', fontsize=8)
plt.tick_params(axis='both', which='major', labelsize=8)
plt.tick_params(axis='both', which='minor', labelsize=8)
plt.grid()
plt.savefig(folder+ "//"+title+'.png', format='png', dpi=1000) 
plt.close(fig)

title = "Refined unit cell parameters c"+" "+material_id[0]
fig = plt.figure()
plt.xlabel(r"c", loc='center', fontsize=8)
logdata = np.array(c)

logdata = logdata[~np.isnan(logdata)]
xmin = logdata.min()
xmax = logdata.max()
x1 = np.linspace(xmin, xmax, 1000)
#estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
#pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
# plt.axvline(x=estimated_mu, c="k")
# plt.plot(x1, pdf, 'r')
rangeminc, rangemaxc = np.min(logdata), np.max(logdata)
plt.hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangeminc, rangemaxc))
# axs[0, 2].hist(e33c, bins=bins)
plt.ylabel('Frequency', fontsize=8)
plt.tick_params(axis='both', which='major', labelsize=8)
plt.tick_params(axis='both', which='minor', labelsize=8)
plt.grid()
plt.savefig(folder+ "//"+title+'.png', format='png', dpi=1000) 
plt.close(fig)

title = "Refined unit cell parameters alpha"+" "+material_id[0]
fig = plt.figure()
plt.xlabel(r"$\alpha$", loc='center', fontsize=8)
logdata = np.array(alp)
logdata = logdata[~np.isnan(logdata)]
xmin = logdata.min()
xmax = logdata.max()
x1 = np.linspace(xmin, xmax, 1000)
#estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
#pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
# plt.axvline(x=estimated_mu, c="k")
# plt.plot(x1, pdf, 'r')
rangeminal, rangemaxal = np.min(logdata), np.max(logdata)
plt.hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangeminal, rangemaxal))
# axs[1, 0].hist(e12c, bins=bins)
plt.ylabel('Frequency', fontsize=8)
plt.tick_params(axis='both', which='major', labelsize=8)
plt.tick_params(axis='both', which='minor', labelsize=8)
plt.grid()
plt.savefig(folder+ "//"+title+'.png', format='png', dpi=1000) 
plt.close(fig)

title = "Refined unit cell parameters beta"+" "+material_id[0]
fig = plt.figure()
plt.xlabel(r"$\beta$", loc='center', fontsize=8)
logdata = np.array(bet)
logdata = logdata[~np.isnan(logdata)]
xmin = logdata.min()
xmax = logdata.max()
x1 = np.linspace(xmin, xmax, 1000)
#estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
#pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
# plt.axvline(x=estimated_mu, c="k")
# plt.plot(x1, pdf, 'r')
rangeminbe, rangemaxbe = np.min(logdata), np.max(logdata)
plt.hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangeminbe, rangemaxbe))
# axs[1, 1].hist(e13c, bins=bins)
plt.ylabel('Frequency', fontsize=8)
plt.tick_params(axis='both', which='major', labelsize=8)
plt.tick_params(axis='both', which='minor', labelsize=8)
plt.grid()
plt.savefig(folder+ "//"+title+'.png', format='png', dpi=1000) 
plt.close(fig)

title = "Refined unit cell parameters gamma"+" "+material_id[0]
fig = plt.figure()
plt.xlabel(r"$\gamma$", loc='center', fontsize=8)
logdata = np.array(gam)
logdata = logdata[~np.isnan(logdata)]
xmin = logdata.min()
xmax = logdata.max()
x1 = np.linspace(xmin, xmax, 1000)
#estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
#pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
# plt.axvline(x=estimated_mu, c="k")
# plt.plot(x1, pdf, 'r')
rangeminga, rangemaxga = np.min(logdata), np.max(logdata)
plt.hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangeminga, rangemaxga))
# axs[1, 2].hist(e23c, bins=bins)
plt.ylabel('Frequency', fontsize=8)
plt.tick_params(axis='both', which='major', labelsize=8)
plt.tick_params(axis='both', which='minor', labelsize=8)
plt.grid()
# plt.tight_layout()
plt.savefig(folder+ "//"+title+'.png', format='png', dpi=1000) 
plt.close(fig)


from mpl_toolkits.axes_grid1 import make_axes_locatable
mu_sd = []
matid=0

fig = plt.figure(figsize=(11.69,8.27), dpi=100)
bottom, top = 0.1, 0.9
left, right = 0.1, 0.8
fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right, hspace=0.15, wspace=0.25)

try:
    vmin, vmax = mu_sd[matid*6]
except:
    vmin = rangemina
    vmax = rangemaxa
axs = fig.subplots(2, 3)
axs[0, 0].set_title(r"$a$", loc='center', fontsize=8)
strain_matrix_plot = np.array(a)
im=axs[0, 0].imshow(strain_matrix_plot.reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
axs[0, 0].set_xticks([])
axs[0, 0].set_yticks([])
divider = make_axes_locatable(axs[0,0])
cax = divider.append_axes('right', size='5%', pad=0.05)
cbar = fig.colorbar(im, cax=cax, orientation='vertical')
cbar.ax.tick_params(labelsize=8) 

try:
    vmin, vmax = mu_sd[matid*6+1]
except:
    vmin = rangeminb
    vmax = rangemaxb
axs[0, 1].set_title(r"$b$", loc='center', fontsize=8)
strain_matrix_plot = np.array(b)
im=axs[0, 1].imshow(strain_matrix_plot.reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
divider = make_axes_locatable(axs[0,1])
cax = divider.append_axes('right', size='5%', pad=0.05)
cbar = fig.colorbar(im, cax=cax, orientation='vertical')
cbar.ax.tick_params(labelsize=8) 

try:
    vmin, vmax = mu_sd[matid*6+2]
except:
    vmin = rangeminc
    vmax = rangemaxc
axs[0, 2].set_title(r"$c$", loc='center', fontsize=8)
strain_matrix_plot = np.array(c)
im=axs[0, 2].imshow(strain_matrix_plot.reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
divider = make_axes_locatable(axs[0,2])
cax = divider.append_axes('right', size='5%', pad=0.05)
cbar = fig.colorbar(im, cax=cax, orientation='vertical')
cbar.ax.tick_params(labelsize=8) 

try:
    vmin, vmax = mu_sd[matid*6+3]
except:
    vmin = rangeminal
    vmax = rangemaxal
axs[1, 0].set_title(r"$\alpha$", loc='center', fontsize=8)
strain_matrix_plot = np.array(alp)
im=axs[1, 0].imshow(strain_matrix_plot.reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
axs[1, 0].set_xticks([])
axs[1, 0].set_yticks([])
divider = make_axes_locatable(axs[1,0])
cax = divider.append_axes('right', size='5%', pad=0.05)
cbar = fig.colorbar(im, cax=cax, orientation='vertical')
cbar.ax.tick_params(labelsize=8) 

try:
    vmin, vmax = mu_sd[matid*6+4]
except:
    vmin = rangeminbe
    vmax = rangemaxbe
axs[1, 1].set_title(r"$\beta$", loc='center', fontsize=8)
strain_matrix_plot = np.array(bet)
im=axs[1, 1].imshow(strain_matrix_plot.reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
axs[1, 1].set_xticks([])
divider = make_axes_locatable(axs[1,1])
cax = divider.append_axes('right', size='5%', pad=0.05)
cbar = fig.colorbar(im, cax=cax, orientation='vertical')
cbar.ax.tick_params(labelsize=8) 

try:
    vmin, vmax = mu_sd[matid*6+5]
except:
    vmin = rangeminga
    vmax = rangemaxga
axs[1, 2].set_title(r"$\gamma$", loc='center', fontsize=8)
strain_matrix_plot = np.array(gam)
im = axs[1, 2].imshow(strain_matrix_plot.reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
axs[1, 2].set_xticks([]) 
divider = make_axes_locatable(axs[1,2])
cax = divider.append_axes('right', size='5%', pad=0.05)
cbar = fig.colorbar(im, cax=cax, orientation='vertical')
cbar.formatter.set_useOffset(False)
cbar.ax.tick_params(labelsize=8) 

for ax in axs.flat:
    ax.label_outer()
plt.savefig(folder+ "//"+'figure_unticell.png', bbox_inches='tight',format='png', dpi=1000) 
plt.close(fig)
#%% Plot histograms
# from scipy.stats import norms
import scipy
mu_sd = []
material_id = [material_, material1_]
for matid in range(matnumber):
    count = 0
    for index in range(rangeval):
        # if index != 0:
        #     continue
        ### index for nans
        nan_index11 = np.where(match_rate[index][0] < match_tol)[0]
        nan_index1 = np.where(fR_pix[index][0] > fR_tol)[0]
        mat_id_index = np.where(mat_global[index][0] != matid+1)[0]
        nan_index = np.hstack((mat_id_index,nan_index1,nan_index11))
        nan_index = np.unique(nan_index)
        
        if count == 0:
            spots_len_plot = np.copy(spots_len[index][0])
            mr_plot = np.copy(match_rate[index][0])
            iR_pix_plot = np.copy(iR_pix[index][0])
            fR_pix_plot = np.copy(fR_pix[index][0])
            strain_matrix_plot = np.copy(strain_matrix[index][0])
            e11c = np.copy(strain_matrix_plot[:,0,0])#.reshape((lim_x, lim_y))
            e22c = np.copy(strain_matrix_plot[:,1,1])#.reshape((lim_x, lim_y))
            e33c = np.copy(strain_matrix_plot[:,2,2])#.reshape((lim_x, lim_y))
            e12c = np.copy(strain_matrix_plot[:,0,1])#.reshape((lim_x, lim_y))
            e13c = np.copy(strain_matrix_plot[:,0,2])#.reshape((lim_x, lim_y))
            e23c = np.copy(strain_matrix_plot[:,1,2])#.reshape((lim_x, lim_y))
            strain_matrixs_plot = np.copy(strain_matrixs[index][0])
            e11s = np.copy(strain_matrixs_plot[:,0,0])#.reshape((lim_x, lim_y))
            e22s = np.copy(strain_matrixs_plot[:,1,1])#.reshape((lim_x, lim_y))
            e33s = np.copy(strain_matrixs_plot[:,2,2])#.reshape((lim_x, lim_y))
            e12s = np.copy(strain_matrixs_plot[:,0,1])#.reshape((lim_x, lim_y))
            e13s = np.copy(strain_matrixs_plot[:,0,2])#.reshape((lim_x, lim_y))
            e23s = np.copy(strain_matrixs_plot[:,1,2])#.reshape((lim_x, lim_y))
            spots_len_plot[nan_index] = np.nan 
            mr_plot[nan_index] = np.nan 
            iR_pix_plot[nan_index] = np.nan 
            fR_pix_plot[nan_index] = np.nan 
            e11c[nan_index] = np.nan 
            e22c[nan_index] = np.nan 
            e33c[nan_index] = np.nan 
            e12c[nan_index] = np.nan 
            e13c[nan_index] = np.nan 
            e23c[nan_index] = np.nan 
            e11s[nan_index] = np.nan 
            e22s[nan_index] = np.nan 
            e33s[nan_index] = np.nan 
            e12s[nan_index] = np.nan 
            e13s[nan_index] = np.nan 
            e23s[nan_index] = np.nan 
            count = 1
            
        else:
            temp = np.copy(spots_len[index][0])
            temp[nan_index] = np.nan
            spots_len_plot = np.vstack((spots_len_plot,temp))
            
            temp = np.copy(match_rate[index][0])
            temp[nan_index] = np.nan
            mr_plot = np.vstack((mr_plot,temp))
            
            temp = np.copy(iR_pix[index][0])
            temp[nan_index] = np.nan
            iR_pix_plot = np.vstack((iR_pix_plot,temp))
    
            temp = np.copy(fR_pix[index][0])
            temp[nan_index] = np.nan
            fR_pix_plot = np.vstack((fR_pix_plot,temp))
            
            strain_matrix_plot = np.copy(strain_matrix[index][0])
            temp = np.copy(strain_matrix_plot[:,0,0])
            temp[nan_index] = np.nan
            e11c = np.vstack((e11c,temp))
            temp = np.copy(strain_matrix_plot[:,1,1])
            temp[nan_index] = np.nan
            e22c = np.vstack((e22c,temp))
            temp = np.copy(strain_matrix_plot[:,2,2])
            temp[nan_index] = np.nan
            e33c = np.vstack((e33c,temp))
            temp = np.copy(strain_matrix_plot[:,0,1])
            temp[nan_index] = np.nan
            e12c = np.vstack((e12c,temp))
            temp = np.copy(strain_matrix_plot[:,0,2])
            temp[nan_index] = np.nan
            e13c = np.vstack((e13c,temp))
            temp = np.copy(strain_matrix_plot[:,1,2])
            temp[nan_index] = np.nan
            e23c = np.vstack((e23c,temp))
            ##
            strain_matrixs_plot = np.copy(strain_matrixs[index][0])
            temp = np.copy(strain_matrixs_plot[:,0,0])
            temp[nan_index] = np.nan
            e11s = np.vstack((e11s,temp))
            temp = np.copy(strain_matrixs_plot[:,1,1])
            temp[nan_index] = np.nan
            e22s = np.vstack((e22s,temp))
            temp = np.copy(strain_matrixs_plot[:,2,2])
            temp[nan_index] = np.nan
            e33s = np.vstack((e33s,temp))
            temp = np.copy(strain_matrixs_plot[:,0,1])
            temp[nan_index] = np.nan
            e12s = np.vstack((e12s,temp))
            temp = np.copy(strain_matrixs_plot[:,0,2])
            temp[nan_index] = np.nan
            e13s = np.vstack((e13s,temp))
            temp = np.copy(strain_matrixs_plot[:,1,2])
            temp[nan_index] = np.nan
            e23s = np.vstack((e23s,temp))
    
    spots_len_plot = spots_len_plot.flatten()
    mr_plot = mr_plot.flatten()
    iR_pix_plot = iR_pix_plot.flatten()
    fR_pix_plot = fR_pix_plot.flatten() 
    e11c = e11c.flatten()
    e22c = e22c.flatten()
    e33c = e33c.flatten()
    e12c = e12c.flatten()
    e13c = e13c.flatten()
    e23c = e23c.flatten()
    e11s = e11s.flatten()
    e22s = e22s.flatten()
    e33s = e33s.flatten()
    e12s = e12s.flatten()
    e13s = e13s.flatten()
    e23s = e23s.flatten()
    
    spots_len_plot = spots_len_plot[~np.isnan(spots_len_plot)]
    mr_plot = mr_plot[~np.isnan(mr_plot)]
    iR_pix_plot = iR_pix_plot[~np.isnan(iR_pix_plot)]
    fR_pix_plot = fR_pix_plot[~np.isnan(fR_pix_plot)]
    e11c = e11c[~np.isnan(e11c)]
    e22c = e22c[~np.isnan(e22c)]
    e33c = e33c[~np.isnan(e33c)]
    e12c = e12c[~np.isnan(e12c)]
    e13c = e13c[~np.isnan(e13c)]
    e23c = e23c[~np.isnan(e23c)]
    e11s = e11s[~np.isnan(e11s)]
    e22s = e22s[~np.isnan(e22s)]
    e33s = e33s[~np.isnan(e33s)]
    e12s = e12s[~np.isnan(e12s)]
    e13s = e13s[~np.isnan(e13s)]
    e23s = e23s[~np.isnan(e23s)]
    
    try:
        title = "Number of spots and matching rate"
        fig = plt.figure()
        axs = fig.subplots(1, 2)
        axs[0].set_title("Number of spots", loc='center', fontsize=8)
        axs[0].hist(spots_len_plot, bins=bins)
        axs[0].set_ylabel('Frequency', fontsize=8)
        axs[0].tick_params(axis='both', which='major', labelsize=8)
        axs[0].tick_params(axis='both', which='minor', labelsize=8)
        axs[1].set_title("matching rate", loc='center', fontsize=8)
        axs[1].hist(mr_plot, bins=bins)
        axs[1].set_ylabel('Frequency', fontsize=8)
        axs[1].tick_params(axis='both', which='major', labelsize=8)
        axs[1].tick_params(axis='both', which='minor', labelsize=8)
        plt.tight_layout()
        plt.savefig(folder+ "//"+title+"_"+material_id[matid]+'.png', format='png', dpi=1000) 
        plt.close(fig)
    except:
        pass

    # try:
    #     title = "strain Crystal reference11"+" "+material_id[matid]
    #     fig = plt.figure()
    #     plt.xlabel(r"$\epsilon_{11}$ (%)", loc='center', fontsize=8)
    #     logdata = e11c #np.log(e11c)
    #     xmin = logdata.min()
    #     xmax = logdata.max()
    #     x1 = np.linspace(xmin, xmax, 1000)
    #     estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
    #     pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
    #     # plt.axvline(x=estimated_mu, c="k")
    #     # plt.plot(x1, pdf, 'r')
    #     plt.hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
    #     plt.ylabel('Frequency', fontsize=8)
    #     plt.tick_params(axis='both', which='major', labelsize=8)
    #     plt.tick_params(axis='both', which='minor', labelsize=8)
    #     # ax.set_xlim(xmin=-10, xmax=10)
    #     plt.grid()
    #     plt.savefig(title+'.png', format='png', dpi=1000) 
    #     plt.close(fig)
        
    #     title = "strain Crystal reference22"+" "+material_id[matid]
    #     fig = plt.figure()
    #     plt.xlabel(r"$\epsilon_{22}$ (%)", loc='center', fontsize=8)
    #     logdata = e22c #np.log(e22c)
    #     xmin = logdata.min()
    #     xmax = logdata.max()
    #     x1 = np.linspace(xmin, xmax, 1000)
    #     estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
    #     pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
    #     # plt.axvline(x=estimated_mu, c="k")
    #     # plt.plot(x1, pdf, 'r')
    #     plt.hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
    #     # axs[0, 1].hist(e22c, bins=bins)
    #     plt.ylabel('Frequency', fontsize=8)
    #     plt.tick_params(axis='both', which='major', labelsize=8)
    #     plt.tick_params(axis='both', which='minor', labelsize=8)
    #     plt.grid()
    #     plt.savefig(title+'.png', format='png', dpi=1000) 
    #     plt.close(fig)
        
    #     title = "strain Crystal reference33"+" "+material_id[matid]
    #     fig = plt.figure()
    #     plt.xlabel(r"$\epsilon_{33}$ (%)", loc='center', fontsize=8)
    #     logdata = e33c #np.log(e33c)
    #     xmin = logdata.min()
    #     xmax = logdata.max()
    #     x1 = np.linspace(xmin, xmax, 1000)
    #     estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
    #     pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
    #     # plt.axvline(x=estimated_mu, c="k")
    #     # plt.plot(x1, pdf, 'r')
    #     plt.hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
    #     # axs[0, 2].hist(e33c, bins=bins)
    #     plt.ylabel('Frequency', fontsize=8)
    #     plt.tick_params(axis='both', which='major', labelsize=8)
    #     plt.tick_params(axis='both', which='minor', labelsize=8)
    #     plt.grid()
    #     plt.savefig(title+'.png', format='png', dpi=1000) 
    #     plt.close(fig)
        
    #     title = "strain Crystal reference12"+" "+material_id[matid]
    #     fig = plt.figure()
    #     plt.xlabel(r"$\epsilon_{12}$ (%)", loc='center', fontsize=8)
    #     logdata = e12c #np.log(e12c)
    #     xmin = logdata.min()
    #     xmax = logdata.max()
    #     x1 = np.linspace(xmin, xmax, 1000)
    #     estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
    #     pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
    #     # plt.axvline(x=estimated_mu, c="k")
    #     # plt.plot(x1, pdf, 'r')
    #     plt.hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
    #     # axs[1, 0].hist(e12c, bins=bins)
    #     plt.ylabel('Frequency', fontsize=8)
    #     plt.tick_params(axis='both', which='major', labelsize=8)
    #     plt.tick_params(axis='both', which='minor', labelsize=8)
    #     plt.grid()
    #     plt.savefig(title+'.png', format='png', dpi=1000) 
    #     plt.close(fig)
        
    #     title = "strain Crystal reference13"+" "+material_id[matid]
    #     fig = plt.figure()
    #     plt.xlabel(r"$\epsilon_{13}$ (%)", loc='center', fontsize=8)
    #     logdata = e13c #np.log(e13c)
    #     xmin = logdata.min()
    #     xmax = logdata.max()
    #     x1 = np.linspace(xmin, xmax, 1000)
    #     estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
    #     pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
    #     # plt.axvline(x=estimated_mu, c="k")
    #     # plt.plot(x1, pdf, 'r')
    #     plt.hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
    #     # axs[1, 1].hist(e13c, bins=bins)
    #     plt.ylabel('Frequency', fontsize=8)
    #     plt.tick_params(axis='both', which='major', labelsize=8)
    #     plt.tick_params(axis='both', which='minor', labelsize=8)
    #     plt.grid()
    #     plt.savefig(title+'.png', format='png', dpi=1000) 
    #     plt.close(fig)
        
    #     title = "strain Crystal reference23"+" "+material_id[matid]
    #     fig = plt.figure()
    #     plt.xlabel(r"$\epsilon_{23}$ (%)", loc='center', fontsize=8)
    #     logdata = e23c #np.log(e23c)
    #     xmin = logdata.min()
    #     xmax = logdata.max()
    #     x1 = np.linspace(xmin, xmax, 1000)
    #     estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
    #     pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
    #     # plt.axvline(x=estimated_mu, c="k")
    #     # plt.plot(x1, pdf, 'r')
    #     plt.hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
    #     # axs[1, 2].hist(e23c, bins=bins)
    #     plt.ylabel('Frequency', fontsize=8)
    #     plt.tick_params(axis='both', which='major', labelsize=8)
    #     plt.tick_params(axis='both', which='minor', labelsize=8)
    #     plt.grid()
    #     # plt.tight_layout()
    #     plt.savefig(title+'.png', format='png', dpi=1000) 
    #     plt.close(fig)
    # except:
    #     pass

#%% Plot histograms
import scipy
mu_sd = []
material_id = [material_, material1_]
for matid in range(matnumber):
    count = 0
    for index in range(rangeval):
        # if index != 0:
        #     continue
        ### index for nans
        nan_index11 = np.where(match_rate[index][0] < match_tol)[0]
        nan_index1 = np.where(fR_pix[index][0] > fR_tol)[0]
        mat_id_index = np.where(mat_global[index][0] != matid+1)[0]
        nan_index = np.hstack((mat_id_index,nan_index1,nan_index11))
        nan_index = np.unique(nan_index)
        
        if count == 0:
            spots_len_plot = np.copy(spots_len[index][0])
            mr_plot = np.copy(match_rate[index][0])
            iR_pix_plot = np.copy(iR_pix[index][0])
            fR_pix_plot = np.copy(fR_pix[index][0])
            strain_matrix_plot = np.copy(strain_matrix[index][0])
            e11c = np.copy(strain_matrix_plot[:,0,0])#.reshape((lim_x, lim_y))
            e22c = np.copy(strain_matrix_plot[:,1,1])#.reshape((lim_x, lim_y))
            e33c = np.copy(strain_matrix_plot[:,2,2])#.reshape((lim_x, lim_y))
            e12c = np.copy(strain_matrix_plot[:,0,1])#.reshape((lim_x, lim_y))
            e13c = np.copy(strain_matrix_plot[:,0,2])#.reshape((lim_x, lim_y))
            e23c = np.copy(strain_matrix_plot[:,1,2])#.reshape((lim_x, lim_y))
            strain_matrixs_plot = np.copy(strain_matrixs[index][0])
            e11s = np.copy(strain_matrixs_plot[:,0,0])#.reshape((lim_x, lim_y))
            e22s = np.copy(strain_matrixs_plot[:,1,1])#.reshape((lim_x, lim_y))
            e33s = np.copy(strain_matrixs_plot[:,2,2])#.reshape((lim_x, lim_y))
            e12s = np.copy(strain_matrixs_plot[:,0,1])#.reshape((lim_x, lim_y))
            e13s = np.copy(strain_matrixs_plot[:,0,2])#.reshape((lim_x, lim_y))
            e23s = np.copy(strain_matrixs_plot[:,1,2])#.reshape((lim_x, lim_y))
            spots_len_plot[nan_index] = np.nan 
            mr_plot[nan_index] = np.nan 
            iR_pix_plot[nan_index] = np.nan 
            fR_pix_plot[nan_index] = np.nan 
            e11c[nan_index] = np.nan 
            e22c[nan_index] = np.nan 
            e33c[nan_index] = np.nan 
            e12c[nan_index] = np.nan 
            e13c[nan_index] = np.nan 
            e23c[nan_index] = np.nan 
            e11s[nan_index] = np.nan 
            e22s[nan_index] = np.nan 
            e33s[nan_index] = np.nan 
            e12s[nan_index] = np.nan 
            e13s[nan_index] = np.nan 
            e23s[nan_index] = np.nan 
            count = 1
            
        else:
            temp = np.copy(spots_len[index][0])
            temp[nan_index] = np.nan
            spots_len_plot = np.vstack((spots_len_plot,temp))
            
            temp = np.copy(match_rate[index][0])
            temp[nan_index] = np.nan
            mr_plot = np.vstack((mr_plot,temp))
            
            temp = np.copy(iR_pix[index][0])
            temp[nan_index] = np.nan
            iR_pix_plot = np.vstack((iR_pix_plot,temp))
    
            temp = np.copy(fR_pix[index][0])
            temp[nan_index] = np.nan
            fR_pix_plot = np.vstack((fR_pix_plot,temp))
            
            strain_matrix_plot = np.copy(strain_matrix[index][0])
            temp = np.copy(strain_matrix_plot[:,0,0])
            temp[nan_index] = np.nan
            e11c = np.vstack((e11c,temp))
            temp = np.copy(strain_matrix_plot[:,1,1])
            temp[nan_index] = np.nan
            e22c = np.vstack((e22c,temp))
            temp = np.copy(strain_matrix_plot[:,2,2])
            temp[nan_index] = np.nan
            e33c = np.vstack((e33c,temp))
            temp = np.copy(strain_matrix_plot[:,0,1])
            temp[nan_index] = np.nan
            e12c = np.vstack((e12c,temp))
            temp = np.copy(strain_matrix_plot[:,0,2])
            temp[nan_index] = np.nan
            e13c = np.vstack((e13c,temp))
            temp = np.copy(strain_matrix_plot[:,1,2])
            temp[nan_index] = np.nan
            e23c = np.vstack((e23c,temp))
            ##
            strain_matrixs_plot = np.copy(strain_matrixs[index][0])
            temp = np.copy(strain_matrixs_plot[:,0,0])
            temp[nan_index] = np.nan
            e11s = np.vstack((e11s,temp))
            temp = np.copy(strain_matrixs_plot[:,1,1])
            temp[nan_index] = np.nan
            e22s = np.vstack((e22s,temp))
            temp = np.copy(strain_matrixs_plot[:,2,2])
            temp[nan_index] = np.nan
            e33s = np.vstack((e33s,temp))
            temp = np.copy(strain_matrixs_plot[:,0,1])
            temp[nan_index] = np.nan
            e12s = np.vstack((e12s,temp))
            temp = np.copy(strain_matrixs_plot[:,0,2])
            temp[nan_index] = np.nan
            e13s = np.vstack((e13s,temp))
            temp = np.copy(strain_matrixs_plot[:,1,2])
            temp[nan_index] = np.nan
            e23s = np.vstack((e23s,temp))
    
    spots_len_plot = spots_len_plot.flatten()
    mr_plot = mr_plot.flatten()
    iR_pix_plot = iR_pix_plot.flatten()
    fR_pix_plot = fR_pix_plot.flatten() 
    e11c = e11c.flatten()
    e22c = e22c.flatten()
    e33c = e33c.flatten()
    e12c = e12c.flatten()
    e13c = e13c.flatten()
    e23c = e23c.flatten()
    e11s = e11s.flatten()
    e22s = e22s.flatten()
    e33s = e33s.flatten()
    e12s = e12s.flatten()
    e13s = e13s.flatten()
    e23s = e23s.flatten()
    
    spots_len_plot = spots_len_plot[~np.isnan(spots_len_plot)]
    mr_plot = mr_plot[~np.isnan(mr_plot)]
    iR_pix_plot = iR_pix_plot[~np.isnan(iR_pix_plot)]
    fR_pix_plot = fR_pix_plot[~np.isnan(fR_pix_plot)]
    e11c = e11c[~np.isnan(e11c)]
    e22c = e22c[~np.isnan(e22c)]
    e33c = e33c[~np.isnan(e33c)]
    e12c = e12c[~np.isnan(e12c)]
    e13c = e13c[~np.isnan(e13c)]
    e23c = e23c[~np.isnan(e23c)]
    e11s = e11s[~np.isnan(e11s)]
    e22s = e22s[~np.isnan(e22s)]
    e33s = e33s[~np.isnan(e33s)]
    e12s = e12s[~np.isnan(e12s)]
    e13s = e13s[~np.isnan(e13s)]
    e23s = e23s[~np.isnan(e23s)]
    
    try:
        title = "Number of spots and matching rate"
        fig = plt.figure()
        axs = fig.subplots(1, 2)
        axs[0].set_title("Number of spots", loc='center', fontsize=8)
        axs[0].hist(spots_len_plot, bins=bins)
        axs[0].set_ylabel('Frequency', fontsize=8)
        axs[0].tick_params(axis='both', which='major', labelsize=8)
        axs[0].tick_params(axis='both', which='minor', labelsize=8)
        axs[1].set_title("matching rate", loc='center', fontsize=8)
        axs[1].hist(mr_plot, bins=bins)
        axs[1].set_ylabel('Frequency', fontsize=8)
        axs[1].tick_params(axis='both', which='major', labelsize=8)
        axs[1].tick_params(axis='both', which='minor', labelsize=8)
        plt.tight_layout()
        plt.savefig(folder+ "//"+title+"_"+material_id[matid]+'.png', format='png', dpi=1000) 
        plt.close(fig)
    except:
        pass

    try:
        title = "strain Crystal reference"+" "+material_id[matid]
        fig = plt.figure()
        fig.suptitle(title, fontsize=10)
        axs = fig.subplots(2, 3)
        axs[0, 0].set_title(r"$\epsilon_{11}$ (%)", loc='center', fontsize=8)
        logdata = e11c #np.log(e11c)
        xmin = logdata.min()
        xmax = logdata.max()
        x1 = np.linspace(xmin, xmax, 1000)
        estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
        pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
        axs[0, 0].axvline(x=estimated_mu, c="k")
        # axs[0, 0].plot(x1, pdf, 'r')
        axs[0, 0].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
        axs[0, 0].set_ylabel('Frequency', fontsize=8)
        axs[0, 0].tick_params(axis='both', which='major', labelsize=8)
        axs[0, 0].tick_params(axis='both', which='minor', labelsize=8)
        mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
        
        axs[0, 1].set_title(r"$\epsilon_{22}$ (%)", loc='center', fontsize=8)
        logdata = e22c #np.log(e22c)
        xmin = logdata.min()
        xmax = logdata.max()
        x1 = np.linspace(xmin, xmax, 1000)
        estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
        pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
        axs[0, 1].axvline(x=estimated_mu, c="k")
        # axs[0, 1].plot(x1, pdf, 'r')
        axs[0, 1].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
        # axs[0, 1].hist(e22c, bins=bins)
        axs[0, 1].set_ylabel('Frequency', fontsize=8)
        axs[0, 1].tick_params(axis='both', which='major', labelsize=8)
        axs[0, 1].tick_params(axis='both', which='minor', labelsize=8)
        mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
        
        axs[0, 2].set_title(r"$\epsilon_{33}$ (%)", loc='center', fontsize=8)
        logdata = e33c #np.log(e33c)
        xmin = logdata.min()
        xmax = logdata.max()
        x1 = np.linspace(xmin, xmax, 1000)
        estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
        pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
        axs[0, 2].axvline(x=estimated_mu, c="k")
        # axs[0, 2].plot(x1, pdf, 'r')
        axs[0, 2].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
        # axs[0, 2].hist(e33c, bins=bins)
        axs[0, 2].set_ylabel('Frequency', fontsize=8)
        axs[0, 2].tick_params(axis='both', which='major', labelsize=8)
        axs[0, 2].tick_params(axis='both', which='minor', labelsize=8)
        mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
        
        axs[1, 0].set_title(r"$\epsilon_{12}$ (%)", loc='center', fontsize=8)
        logdata = e12c#np.log(e12c)
        xmin = logdata.min()
        xmax = logdata.max()
        x1 = np.linspace(xmin, xmax, 1000)
        estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
        pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
        axs[1, 0].axvline(x=estimated_mu, c="k")
        # axs[1, 0].plot(x1, pdf, 'r')
        axs[1, 0].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
        # axs[1, 0].hist(e12c, bins=bins)
        axs[1, 0].set_ylabel('Frequency', fontsize=8)
        axs[1, 0].tick_params(axis='both', which='major', labelsize=8)
        axs[1, 0].tick_params(axis='both', which='minor', labelsize=8)
        mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
        
        axs[1, 1].set_title(r"$\epsilon_{13}$ (%)", loc='center', fontsize=8)
        logdata = e13c#np.log(e13c)
        xmin = logdata.min()
        xmax = logdata.max()
        x1 = np.linspace(xmin, xmax, 1000)
        estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
        pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
        axs[1, 1].axvline(x=estimated_mu, c="k")
        # axs[1, 1].plot(x1, pdf, 'r')
        axs[1, 1].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
        # axs[1, 1].hist(e13c, bins=bins)
        axs[1, 1].set_ylabel('Frequency', fontsize=8)
        axs[1, 1].tick_params(axis='both', which='major', labelsize=8)
        axs[1, 1].tick_params(axis='both', which='minor', labelsize=8)
        mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
        
        axs[1, 2].set_title(r"$\epsilon_{23}$ (%)", loc='center', fontsize=8)
        logdata = e23c#np.log(e23c)
        xmin = logdata.min()
        xmax = logdata.max()
        x1 = np.linspace(xmin, xmax, 1000)
        estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
        pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
        axs[1, 2].axvline(x=estimated_mu, c="k")
        # axs[1, 2].plot(x1, pdf, 'r')
        axs[1, 2].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
        # axs[1, 2].hist(e23c, bins=bins)
        axs[1, 2].set_ylabel('Frequency', fontsize=8)
        axs[1, 2].tick_params(axis='both', which='major', labelsize=8)
        axs[1, 2].tick_params(axis='both', which='minor', labelsize=8)
        
        mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
        
        plt.tight_layout()
        plt.savefig(folder+ "//"+title+'.png', format='png', dpi=1000) 
        plt.close(fig)
    except:
        pass
    
    try:
        title = "strain Sample reference"+" "+material_id[matid]
        fig = plt.figure()
        fig.suptitle(title, fontsize=10)
        axs = fig.subplots(2, 3)
        axs[0, 0].set_title(r"$\epsilon_{11}$ (%)", loc='center', fontsize=8)
        logdata = e11s #np.log(e11c)
        xmin = logdata.min()
        xmax = logdata.max()
        x1 = np.linspace(xmin, xmax, 1000)
        estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
        pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
        axs[0, 0].axvline(x=estimated_mu, c="k")
        print("E11 = ",estimated_mu, estimated_sigma)
        # axs[0, 0].plot(x1, pdf, 'r')
        axs[0, 0].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
        # axs[0, 0].hist(e11s, bins=bins)
        axs[0, 0].set_ylabel('Frequency', fontsize=8)
        axs[0, 0].tick_params(axis='both', which='major', labelsize=8)
        axs[0, 0].tick_params(axis='both', which='minor', labelsize=8)
        
        # mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
        
        axs[0, 1].set_title(r"$\epsilon_{22}$ (%)", loc='center', fontsize=8)
        logdata = e22s #np.log(e22c)
        xmin = logdata.min()
        xmax = logdata.max()
        x1 = np.linspace(xmin, xmax, 1000)
        estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
        pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
        axs[0, 1].axvline(x=estimated_mu, c="k")
        print("E22 = ",estimated_mu, estimated_sigma)
        # axs[0, 1].plot(x1, pdf, 'r')
        axs[0, 1].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
        # axs[0, 1].hist(e22s, bins=bins)
        axs[0, 1].set_ylabel('Frequency', fontsize=8)
        axs[0, 1].tick_params(axis='both', which='major', labelsize=8)
        axs[0, 1].tick_params(axis='both', which='minor', labelsize=8)
        
        # mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
        
        axs[0, 2].set_title(r"$\epsilon_{33}$ (%)", loc='center', fontsize=8)
        logdata = e33s #np.log(e33c)
        xmin = logdata.min()
        xmax = logdata.max()
        x1 = np.linspace(xmin, xmax, 1000)
        estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
        pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
        axs[0, 2].axvline(x=estimated_mu, c="k")
        print("E33 = ",estimated_mu, estimated_sigma)
        # axs[0, 2].plot(x1, pdf, 'r')
        axs[0, 2].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
        # axs[0, 2].hist(e33s, bins=bins)
        axs[0, 2].set_ylabel('Frequency', fontsize=8)
        axs[0, 2].tick_params(axis='both', which='major', labelsize=8)
        axs[0, 2].tick_params(axis='both', which='minor', labelsize=8)
        
        # mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
        
        axs[1, 0].set_title(r"$\epsilon_{12}$ (%)", loc='center', fontsize=8)
        logdata = e12s#np.log(e12c)
        xmin = logdata.min()
        xmax = logdata.max()
        x1 = np.linspace(xmin, xmax, 1000)
        estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
        pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
        axs[1, 0].axvline(x=estimated_mu, c="k")
        print("E12 = ",estimated_mu, estimated_sigma)
        # axs[1, 0].plot(x1, pdf, 'r')
        axs[1, 0].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
        # axs[1, 0].hist(e12s, bins=bins)
        axs[1, 0].set_ylabel('Frequency', fontsize=8)
        axs[1, 0].tick_params(axis='both', which='major', labelsize=8)
        axs[1, 0].tick_params(axis='both', which='minor', labelsize=8)
        
        # mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
        
        axs[1, 1].set_title(r"$\epsilon_{13}$ (%)", loc='center', fontsize=8)
        logdata = e13s#np.log(e13c)
        xmin = logdata.min()
        xmax = logdata.max()
        x1 = np.linspace(xmin, xmax, 1000)
        estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
        pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
        axs[1, 1].axvline(x=estimated_mu, c="k")
        print("E13 = ",estimated_mu, estimated_sigma)
        # axs[1, 1].plot(x1, pdf, 'r')
        axs[1, 1].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
        # axs[1, 1].hist(e13s, bins=bins)
        axs[1, 1].set_ylabel('Frequency', fontsize=8)
        axs[1, 1].tick_params(axis='both', which='major', labelsize=8)
        axs[1, 1].tick_params(axis='both', which='minor', labelsize=8)
        
        # mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
        
        axs[1, 2].set_title(r"$\epsilon_{23}$ (%)", loc='center', fontsize=8)
        logdata = e23s#np.log(e23c)
        xmin = logdata.min()
        xmax = logdata.max()
        x1 = np.linspace(xmin, xmax, 1000)
        estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
        pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
        axs[1, 2].axvline(x=estimated_mu, c="k")
        print("E23 = ",estimated_mu, estimated_sigma)
        # axs[1, 2].plot(x1, pdf, 'r')
        axs[1, 2].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
        # axs[1, 2].hist(e23s, bins=bins)
        axs[1, 2].set_ylabel('Frequency', fontsize=8)
        axs[1, 2].tick_params(axis='both', which='major', labelsize=8)
        axs[1, 2].tick_params(axis='both', which='minor', labelsize=8)
        
        # mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
        
        plt.tight_layout()
        plt.savefig(folder+ "//"+title+'.png', format='png', dpi=1000) 
        plt.close(fig)  
    except:
        pass
#%%    Plot strain data    
from mpl_toolkits.axes_grid1 import make_axes_locatable
mu_sd = []
for matid in range(matnumber):
    for index in range(rangeval):
        nan_index11 = np.where(match_rate[index][0] < match_tol)[0]
        nan_index1 = np.where(fR_pix[index][0] > fR_tol)[0]
        mat_id_index = np.where(mat_global[index][0] != matid+1)[0]
        nan_index = np.hstack((mat_id_index,nan_index1,nan_index11))
        nan_index = np.unique(nan_index)
    
        strain_matrix_plot = np.copy(strain_matrix[index][0])
        strain_matrix_plot[nan_index,:,:] = np.nan             
    
        fig = plt.figure(figsize=(11.69,8.27), dpi=100)
        bottom, top = 0.1, 0.9
        left, right = 0.1, 0.8
        fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right, hspace=0.15, wspace=0.25)
        
        try:
            vmin, vmax = mu_sd[matid*6]
        except:
            vmin = rangemin
            vmax = rangemax
        max_vm = np.max((np.abs(vmax),np.abs(vmin)))
        vmin = -max_vm
        vmax = max_vm
        axs = fig.subplots(2, 3)
        axs[0, 0].set_title(r"$\epsilon_{11}$ (%)", loc='center', fontsize=8)
        im=axs[0, 0].imshow(strain_matrix_plot[:,0,0].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
        axs[0, 0].set_xticks([])
        axs[0, 0].set_yticks([])
        divider = make_axes_locatable(axs[0,0])
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = fig.colorbar(im, cax=cax, orientation='vertical')
        cbar.ax.tick_params(labelsize=8) 
        
        try:
            vmin, vmax = mu_sd[matid*6+1]
        except:
            vmin = rangemin
            vmax = rangemax
        max_vm = np.max((np.abs(vmax),np.abs(vmin)))
        vmin = -max_vm
        vmax = max_vm
        axs[0, 1].set_title(r"$\epsilon_{22}$ (%)", loc='center', fontsize=8)
        im=axs[0, 1].imshow(strain_matrix_plot[:,1,1].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
        divider = make_axes_locatable(axs[0,1])
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = fig.colorbar(im, cax=cax, orientation='vertical')
        cbar.ax.tick_params(labelsize=8) 
        
        try:
            vmin, vmax = mu_sd[matid*6+2]
        except:
            vmin = rangemin
            vmax = rangemax
        max_vm = np.max((np.abs(vmax),np.abs(vmin)))
        vmin = -max_vm
        vmax = max_vm
        axs[0, 2].set_title(r"$\epsilon_{33}$ (%)", loc='center', fontsize=8)
        im=axs[0, 2].imshow(strain_matrix_plot[:,2,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
        divider = make_axes_locatable(axs[0,2])
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = fig.colorbar(im, cax=cax, orientation='vertical')
        cbar.ax.tick_params(labelsize=8) 
        
        try:
            vmin, vmax = mu_sd[matid*6+3]
        except:
            vmin = rangemin
            vmax = rangemax
        max_vm = np.max((np.abs(vmax),np.abs(vmin)))
        vmin = -max_vm
        vmax = max_vm
        axs[1, 0].set_title(r"$\epsilon_{12}$ (%)", loc='center', fontsize=8)
        im=axs[1, 0].imshow(strain_matrix_plot[:,0,1].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
        axs[1, 0].set_xticks([])
        axs[1, 0].set_yticks([])
        divider = make_axes_locatable(axs[1,0])
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = fig.colorbar(im, cax=cax, orientation='vertical')
        cbar.ax.tick_params(labelsize=8) 
        
        try:
            vmin, vmax = mu_sd[matid*6+4]
        except:
            vmin = rangemin
            vmax = rangemax
        max_vm = np.max((np.abs(vmax),np.abs(vmin)))
        vmin = -max_vm
        vmax = max_vm
        axs[1, 1].set_title(r"$\epsilon_{13}$ (%)", loc='center', fontsize=8)
        im=axs[1, 1].imshow(strain_matrix_plot[:,0,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
        axs[1, 1].set_xticks([])
        divider = make_axes_locatable(axs[1,1])
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = fig.colorbar(im, cax=cax, orientation='vertical')
        cbar.ax.tick_params(labelsize=8) 
        
        try:
            vmin, vmax = mu_sd[matid*6+5]
        except:
            vmin = rangemin
            vmax = rangemax
        max_vm = np.max((np.abs(vmax),np.abs(vmin)))
        vmin = -max_vm
        vmax = max_vm
        axs[1, 2].set_title(r"$\epsilon_{23}$ (%)", loc='center', fontsize=8)
        im = axs[1, 2].imshow(strain_matrix_plot[:,1,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
        axs[1, 2].set_xticks([]) 
        divider = make_axes_locatable(axs[1,2])
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = fig.colorbar(im, cax=cax, orientation='vertical')
        cbar.ax.tick_params(labelsize=8) 

        for ax in axs.flat:
            ax.label_outer()
        plt.savefig(folder+ "//"+'figure_strainCRYSTAL_UB_'+str(matid)+"_"+str(index)+'.png', bbox_inches='tight',format='png', dpi=1000) 
        plt.close(fig)
        
for matid in range(matnumber):
    for index in range(rangeval):
        nan_index11 = np.where(match_rate[index][0] < match_tol)[0]
        nan_index1 = np.where(fR_pix[index][0] > fR_tol)[0]
        mat_id_index = np.where(mat_global[index][0] != matid+1)[0]
        nan_index = np.hstack((mat_id_index,nan_index1,nan_index11))
        nan_index = np.unique(nan_index)
    
        strain_matrix_plot = np.copy(strain_matrixs[index][0])
        strain_matrix_plot[nan_index,:,:] = np.nan             
    
        fig = plt.figure(figsize=(11.69,8.27), dpi=100)
        bottom, top = 0.1, 0.9
        left, right = 0.1, 0.8
        fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right, hspace=0.15, wspace=0.25)
        
        try:
            vmin, vmax = mu_sd[matid*6]
        except:
            vmin = rangemin
            vmax = rangemax
        max_vm = np.max((np.abs(vmax),np.abs(vmin)))
        vmin = -max_vm
        vmax = max_vm
        axs = fig.subplots(2, 3)
        axs[0, 0].set_title(r"$\epsilon_{11}$ (%)", loc='center', fontsize=8)
        im=axs[0, 0].imshow(strain_matrix_plot[:,0,0].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
        axs[0, 0].set_xticks([])
        axs[0, 0].set_yticks([])
        divider = make_axes_locatable(axs[0,0])
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = fig.colorbar(im, cax=cax, orientation='vertical')
        cbar.ax.tick_params(labelsize=8) 
        
        try:
            vmin, vmax = mu_sd[matid*6+1]
        except:
            vmin = rangemin
            vmax = rangemax
        max_vm = np.max((np.abs(vmax),np.abs(vmin)))
        vmin = -max_vm
        vmax = max_vm
        axs[0, 1].set_title(r"$\epsilon_{22}$ (%)", loc='center', fontsize=8)
        im=axs[0, 1].imshow(strain_matrix_plot[:,1,1].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
        divider = make_axes_locatable(axs[0,1])
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = fig.colorbar(im, cax=cax, orientation='vertical')
        cbar.ax.tick_params(labelsize=8) 
        
        try:
            vmin, vmax = mu_sd[matid*6+2]
        except:
            vmin = rangemin
            vmax = rangemax
        max_vm = np.max((np.abs(vmax),np.abs(vmin)))
        vmin = -max_vm
        vmax = max_vm
        axs[0, 2].set_title(r"$\epsilon_{33}$ (%)", loc='center', fontsize=8)
        im=axs[0, 2].imshow(strain_matrix_plot[:,2,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
        divider = make_axes_locatable(axs[0,2])
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = fig.colorbar(im, cax=cax, orientation='vertical')
        cbar.ax.tick_params(labelsize=8) 
        
        try:
            vmin, vmax = mu_sd[matid*6+3]
        except:
            vmin = rangemin
            vmax = rangemax
        max_vm = np.max((np.abs(vmax),np.abs(vmin)))
        vmin = -max_vm
        vmax = max_vm
        axs[1, 0].set_title(r"$\epsilon_{12}$ (%)", loc='center', fontsize=8)
        im=axs[1, 0].imshow(strain_matrix_plot[:,0,1].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
        axs[1, 0].set_xticks([])
        axs[1, 0].set_yticks([])
        divider = make_axes_locatable(axs[1,0])
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = fig.colorbar(im, cax=cax, orientation='vertical')
        cbar.ax.tick_params(labelsize=8) 
        
        try:
            vmin, vmax = mu_sd[matid*6+4]
        except:
            vmin = rangemin
            vmax = rangemax
        max_vm = np.max((np.abs(vmax),np.abs(vmin)))
        vmin = -max_vm
        vmax = max_vm
        axs[1, 1].set_title(r"$\epsilon_{13}$ (%)", loc='center', fontsize=8)
        im=axs[1, 1].imshow(strain_matrix_plot[:,0,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
        axs[1, 1].set_xticks([])
        divider = make_axes_locatable(axs[1,1])
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = fig.colorbar(im, cax=cax, orientation='vertical')
        cbar.ax.tick_params(labelsize=8) 
        
        try:
            vmin, vmax = mu_sd[matid*6+5]
        except:
            vmin = rangemin
            vmax = rangemax
        max_vm = np.max((np.abs(vmax),np.abs(vmin)))
        vmin = -max_vm
        vmax = max_vm
        axs[1, 2].set_title(r"$\epsilon_{23}$ (%)", loc='center', fontsize=8)
        im = axs[1, 2].imshow(strain_matrix_plot[:,1,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
        axs[1, 2].set_xticks([]) 
        divider = make_axes_locatable(axs[1,2])
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = fig.colorbar(im, cax=cax, orientation='vertical')
        cbar.ax.tick_params(labelsize=8) 

        for ax in axs.flat:
            ax.label_outer()
        plt.savefig(folder+ "//"+'figure_strainSAMPLE_UB_'+str(matid)+"_"+str(index)+'.png', bbox_inches='tight',format='png', dpi=1000) 
        plt.close(fig)
#%%
# import imageio ## IMAGE READING LIBRARY

# for matid in range(matnumber):
#     if matid ==0:
#         index = 0
#     if matid ==1:
#         index = 1
#     nan_index11 = np.where(match_rate[index][0] < match_tol)[0]
#     nan_index1 = np.where(fR_pix[index][0] > fR_tol)[0]
#     mat_id_index = np.where(mat_global[index][0] != matid+1)[0]
#     nan_index = np.hstack((mat_id_index,nan_index1,nan_index11))
#     nan_index = np.unique(nan_index)

#     col_plot = np.copy(col[index][0])
#     col_plot[nan_index,:] = 0,0,0
#     col_plot = col_plot.reshape((lim_x, lim_y, 3))

#     image = []
#     image1 = np.zeros((col_plot.shape[0],col_plot.shape[1],3))
#     count = 0
#     for g_id in range(col_plot.shape[0]):
#         for g_id1 in range(col_plot.shape[1]):   
#             image1[g_id,g_id1,:] = col_plot[g_id,g_id1,:]
#             image.append(np.copy(image1))
#             count += 1
    
#     gif_file = str(matid)+"_"+str(index)+".gif"    
#     imageio.mimsave(gif_file, image, loop=1, fps=1) #duration=0.001, 
#%%
# import os
# for matid in range(matnumber):
#     # if matid!=1:
#     #     continue
#     if matid ==0:
#         index = 1
#     # if matid ==1:
#     #     index = 2#1
        
#     nan_index11 = np.where(match_rate[index][0] < match_tol)[0]
#     nan_index1 = np.where(fR_pix[index][0] > fR_tol)[0]
#     mat_id_index = np.where(mat_global[index][0] != matid+1)[0]
#     nan_index = np.hstack((mat_id_index,nan_index1,nan_index11))
#     nan_index = np.unique(nan_index)

#     col_plot = np.copy(col[index][0])
#     col_plot[nan_index,:] = 0,0,0
#     col_plot = col_plot.reshape((lim_x, lim_y, 3))
    
#     save_directory_ = r"C:\Users\purushot\Desktop\pattern_matching\experimental\GUIv0\latest_version\latest_files\gif_image_"+str(matid)+"_"+str(index)
#     if not os.path.exists(save_directory_):
#         os.makedirs(save_directory_)
    
#     image1 = np.zeros((col_plot.shape[0],col_plot.shape[1],3))
#     count = 0
#     for g_id in range(col_plot.shape[0]):
#         for g_id1 in range(col_plot.shape[1]):
#             img_file = save_directory_ + "\\"+str(count)+".png"    
#             image1[g_id,g_id1,:] = col_plot[g_id,g_id1,:]
#             fig = plt.figure(frameon=False)
#             # fig.set_size_inches(col_plot.shape[0],col_plot.shape[1])
#             ax = fig.subplots() #plt.Axes(fig)
#             ax.set_axis_off()
#             fig.add_axes(ax)
#             ax.imshow(image1, aspect='auto')
#             fig.savefig(img_file)
#             plt.close(fig)
#             count += 1
#%%
# import os
# # from PIL import Image
# import matplotlib.pyplot as plt
# import numpy as np
# # im = Image.open(r'C:\Users\purushot\Desktop\pattern_matching\latest_files\image2.tif')
# # im.show()
# # imarray = np.array(im)

# col_plot = np.zeros((61,61,3))
# upper_red = np.array([120,60,90])
        
# save_directory_ = r"C:\Users\purushot\Desktop\pattern_matching\latest_files\gif_image"
# if not os.path.exists(save_directory_):
#     os.makedirs(save_directory_)

# count = 0
# for g_id in range(col_plot.shape[0]):
#     for g_id1 in range(col_plot.shape[1]):
#         img_file = save_directory_ + "\\"+str(count)+".png" 
        
#         # image1 = np.zeros((col_plot.shape[0],col_plot.shape[1],3))      
#         # image1[g_id,g_id1,:] = upper_red
        
#         image1 = np.zeros((col_plot.shape[0],col_plot.shape[1]))      
#         image1[g_id,g_id1] = 1
        
#         fig = plt.figure(frameon=False)
#         # fig.set_size_inches(col_plot.shape[0],col_plot.shape[1])
#         ax = fig.subplots() #plt.Axes(fig)
#         ax.set_axis_off()
#         fig.add_axes(ax)
#         ax.imshow(image1, aspect='auto',cmap='jet')
#         fig.savefig(img_file)
#         plt.close(fig)
#         count += 1
