#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt

def floatcustom(s: str):
    '''Function to cast string to float with exception for unseparated coordinate values
    i.e. '-153.534-108.134' returns [-153.534, -108.134]
    
    Parameters:
    -----------
    s : str
        string that should have been parsed properly but PDB didn't account for '-'
    '''
    try:
         return float(s)
    except:
        indices = []
        floats_ = []
        for index, char in enumerate(s): 
            if char == '-':
                indices.append(index)
        if len(indices) > 1 and ' ' not in s:
            for n, i in enumerate(indices):
                if n >= 1:
                    floats_.append(float(s[indices[n-1]:indices[n]]))
            floats_.append(float(s[indices[-1]:]))
        return floats_

def checkflattened(l: list):
    '''Specific function for handling output from customfloat() - ensures list is flattened if it contains
        a sublist and removes last element from different column
    '''
    flattened_ = []
    contains_sublist = False
    for i in l:
        if isinstance(i, list):
            contains_sublist = True
            for j in i:
                flattened_.append(j)
        else:
            flattened_.append(i)
    if contains_sublist:
        del flattened_[-1]
    return flattened_

def pdbParser(pdbtext: str) -> dict:
    '''Returns two dictionaries associated with basic info for the PDB and the PDB atom information
    
    Parameters
    ----------
    pdbtext : str
        The full text of a PDB provided as a string

    '''
    info_ = {
            'HEADER' : None,
            'TITLE' : None, # Will hold lists to be subsequently parsed
            'SOURCE' : [],
            'REMARKS' : [],
            }
    protein_ = {'ATOM' : [], 'HETATM' : []} # Will hold lists to be subsequently parsed
    listofstrings = pdbtext.split('\n')
    listofstrings = [' '.join(substring.split()) for substring in listofstrings] # make only space separated
    for substring in listofstrings:
        split = substring.split(' ')
        if split[0] in tuple(info_.keys()):
            if split[0] == 'HEADER' or split[0] == 'TITLE':
                info_[split[0]] = split[1:]
            else:
                info_[split[0]].append(split[1:])
        elif split[0] in protein_.keys():
            xyz = checkflattened([floatcustom(i) for i in split[6:9]])
            if len(xyz) != 3:
                print('Coordinates not the appropriate length (3) - returning None.')
                return None
            p_ = {
                'serial' : split[1],
                'name' : split[2],
                'resname' : split[3],
                'chain' : split[4],
                'resid' : split[5],
                'xyz' : checkflattened([floatcustom(i) for i in split[6:9]])
                 }
            protein_[split[0]].append(p_)
    return info_, protein_

def addDictKeys(dtarget, add):
    '''Function to add to a dictionary by key-value pair
    
    Parameters:
    -----------
    dtarget : target dictionary to add to
    add : the dictionary we are adding
    '''
    for addkey in tuple(add.keys()):
        if addkey in dtarget.keys():
            dtarget[addkey] += add[addkey]
        else:
            dtarget.update({'{}'.format(addkey) : add[addkey]})

def getSolventExposed(protein, threshold=5):
    '''Returns a dictionary containing residue names and the number of atoms on the outer portion of the protein
    
    Parameters
    ----------
    protein : dict
        dictionary containing protein PDB information produced by pdbParser()
        
    threshold (optional): float (default: 5)
        the top percent of residues which qualify as the most exposed
        
    '''
    c = np.stack(np.asarray([np.asarray(atom['xyz']) for atom in protein['ATOM']]), axis=0)
    resname_list = np.asarray([atom['resname'] for atom in protein['ATOM']])
    center = (np.average(np.asarray(c)[:, 0]), np.average(np.asarray(c)[:, 1]), np.average(np.asarray(c)[:, 2]))
    distance = lambda c_tuple : np.sqrt((c_tuple[0]-center[0])**2 + (c_tuple[1]-center[1])**2 + (c_tuple[2]-center[2])**2)
    distances = np.asarray([distance(coord) for n, coord in enumerate(c)])
    indices = np.argsort(distances)[::-1] # sort from highest to lowest distance - return the indices
    resname_sorted = resname_list[indices]
    distances_sorted = distances[indices]
    percent = 0
    top_residues = []
    for r in resname_sorted:
        percent += 1/len(resname_sorted) * 100
        top_residues.append(r)
        if percent >= threshold:
            break
    d_ = {i:top_residues.count(i) for i in top_residues} # Unique resnames : # of atoms
    return d_

def getData(key: str, index=None, plot=False) -> dict:
    '''Returns dictionary containing a sum of the top x% solvent exposed residues by atom count

    Parameters
    ----------
    key : str
        The category supplied for PDB searches

    index (optional): int or None (default: None)
        The index of a single PDBs to extract data from

    plot (optional): bool (default: False)
        Boolean to decide whether to plot the protein or not (Note: index must be an int)

    Raises
    ------
    ValueError
        Raised if the provided key cannot be converted to a string.
        Raised if 'index' keyword argument is not an integer.
    '''
    dataDict = {}
    try:
        key = str(key)
    except:
        raise ValueError('Key must be able to be cast as a string literal.')
    if plot == True:
        fig = plt.figure()
        ax = plt.axes(projection='3d')
    #pdb_entries = Query(key).search() <-- replacing this
    pdb_entries = os.listdir(key) # <---
    if index != None and isinstance(index, int):
        file =  os.getcwd() + '/' + key + '/' + pdb_entries[index]
        pdb = ''.join(open(file, 'r').read())
        if pdbParser(pdb) == None:
            raise TypeError('pdbParser returned None for the indexed PDB -- try another PDB index.')
        info, protein = pdbParser(pdb)
        coords = [atom['xyz'] for atom in protein['ATOM']]
        if plot == True:
            c = np.asarray(coords)
            ax.plot(c[:, 0], c[:, 1], c[:, 2], lw=0.5)
        plt.show()
        exposedDict = getSolventExposed(protein)
        addDictKeys(dataDict, exposedDict)
    elif index == None:
        for n, i in enumerate(pdb_entries):
            file = os.getcwd() + '/' + key + '/' + i
            #pdb = get_pdb_file(file) <-- replacing this since we no longer have to "get" the PDB
            pdb = ''.join(open(file, 'r').read()) #<--
            if pdbParser(pdb) == None:
                continue # skip iteration if pdbParser() decides to skip the PDB by returning 'None'
            info, protein = pdbParser(pdb)
            exposedDict = getSolventExposed(protein)
            addDictKeys(dataDict, exposedDict)
    else:
        raise ValueError('index keyword must be an integer.')
    return dataDict
