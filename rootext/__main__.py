import uproot
import plotext as plx
import numpy as np
import awkward as ak
import sys
import argparse


file_path = "./"
# save_path = "Pythia_PLOTS/"
file_name = "pythia_ACU_fwdtree.root"

def plot_branch_plx(file_path, file_name, tree_name, branch_name, bin_count = 50):
    with uproot.open(file_path + file_name) as file:
        tree = file[tree_name]

        branch = tree[branch_name]
        #Uproot extraxts every run data separately into an array
        # ak_branch = tree.arrays([branch_name], library="np")[branch_name]
        ak_branch = branch.array( library="ak" ) 
        # print (ak_branch)
        data = ak.flatten(ak_branch, axis=None)
        # data = ak.ravel( ak_branch )
        # print(ak.flatten(data, axis=None) )
    
        min_val = ak.min(data)
        max_val = ak.max(data)
    
        bin_list = np.linspace(min_val, max_val, bin_count)
        out_list = np.linspace(min_val, max_val, int(bin_count / 2))
        out_list = np.around(out_list, 2)

        data = ak.to_numpy( data )
        print (data)
        print (data.shape)

        collected_data, bin_edges = np.histogram(data, bins = bin_list)
        delta = (bin_list[1] - bin_list[0]) * 0.7

        plx.clf()

        # plx.hist(data, bin_count, label = "hist")
        plx.bar( bin_list, collected_data, width = delta )
        plx.xticks(out_list)

        plx.title(tree_name + " "+ branch_name)
        plx.show()
    

if __name__ == "__main__":
    # print(sys.argv)
    
    if (len(sys.argv) == 4):
        _, file_name, tree_name, branch_name = sys.argv
        branch = plot_branch_plx(file_path, file_name, tree_name, branch_name)
    elif (len(sys.argv) == 3):
        _, file_name, tree_name = sys.argv
        
        # list branches
        with uproot.open(file_path + file_name) as file:
            tree = file[tree_name]
            print( "\n".join(tree.keys()) )
    else:
        print("Enter three arguments: File Name, Tree Name, Branch Name \n")
        
        