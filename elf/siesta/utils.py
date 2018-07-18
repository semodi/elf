"""Utility functions for real-space grid properties
"""
import numpy as np
import struct

def get_data_bin(file_path):
    """ Same as get_data for binary (unformatted) files
    """
    #Warning: Only works for cubic cells!!!
    #TODO: Implement for arb. cells

    bin_file = open(file_path, mode = 'rb')

    unitcell = '<I9dI'
    grid = '<I4iI'

    unitcell = np.array(struct.unpack(unitcell,
        bin_file.read(struct.calcsize(unitcell))))[1:-1].reshape(3,3)

    grid = np.array(struct.unpack(grid,bin_file.read(struct.calcsize(grid))))[1:-1]
    if (grid[0] == grid[1] == grid[2]) and grid[3] == 1:
        a = grid[0]
    else:
        raise Exception('get_data_bin cannot handle non-cubic unitcells or spin')

    block = '<' + 'I{}fI'.format(a)*a*a
    content = np.array(struct.unpack(block,bin_file.read(struct.calcsize(block))))

    rho = content.reshape(a+2, a, a, order = 'F')[1:-1,:,:]
    return rho, unitcell, grid

def get_data(file_path):
    """Import data from RHO file (or similar real-space grid files)
    Data is saved in global variables.

    Structure of RHO file:
    first three lines give the unit cell vectors
    fourth line the grid dimensions
    subsequent lines give density on grid

    Parameters:
    -----------
    file_path: string; path to RHO file from which density is read

    Returns:
    --------
    None

    Other:
    ------
    unitcell: (3,3) np.array; saves the unitcell dimension in euclidean coordinates
    grid: (,3) np.array; number of grid points in each euclidean direction
    rho: (grid[1],grid[2],grid[3]) np.array; density on grid
    """
    rhopath = file_path
    unitcell = np.zeros([3, 3])
    grid = np.zeros([4])

    with open(file_path, 'r') as rhofile:

        # unit cell (in Bohr)
        for i in range(0, 3):
            unitcell[i, :] = rhofile.readline().split()

        grid[:] = rhofile.readline().split()
        grid = grid.astype(int)
        n_el = grid[0] * grid[1] * grid[2] * grid[3]

        # initiatialize density with right shape
        rho = np.zeros(grid)

        for z in range(grid[2]):
            for y in range(grid[1]):
                for x in range(grid[0]):
                    rho[x, y, z, 0] = rhofile.readline()

    # closed shell -> we don't care about spin.
    rho = rho[:, :, :, 0]
    grid = grid[:3]
    return rho, unitcell, grid
