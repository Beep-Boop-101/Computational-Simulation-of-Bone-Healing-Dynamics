def compute_strain_tensors(u_grid, L=1.0):
    """
    Input: u_grid (displacements from FEA).
    Output: 10x10x10x3x3 array of symmetric strain tensors.
    """
    strains = np.zeros((10, 10, 10, 3, 3))
    for i in range(10):
        for j in range(10):
            for k in range(10):
                # Normal strains
                exx = (u_grid[i+1,j,k,0] - u_grid[i,j,k,0]) / L
                eyy = (u_grid[i,j+1,k,1] - u_grid[i,j,k,1]) / L
                ezz = (u_grid[i,j,k+1,2] - u_grid[i,j,k,2]) / L
                
                # Tensor Shear strains (Engineering shear / 2)
                exy = 0.5 * ((u_grid[i,j+1,k,0] - u_grid[i,j,k,0])/L + (u_grid[i+1,j,k,1] - u_grid[i,j,k,1])/L)
                eyz = 0.5 * ((u_grid[i,j,k+1,1] - u_grid[i,j,k,1])/L + (u_grid[i,j+1,k,2] - u_grid[i,j,k,2])/L)
                exz = 0.5 * ((u_grid[i+1,j,k,2] - u_grid[i,j,k,2])/L + (u_grid[i,j,k+1,0] - u_grid[i,j,k,0])/L)

                strains[i,j,k] = [[exx, exy, exz], [exy, eyy, eyz], [exz, eyz, ezz]]
    return strains


from scipy.ndimage import laplace

def update_cell_diffusion(bone_data, D=0.1, dt=1.0):
    """
    Input: bone_data array (10x10x10x4) where index 1 is cell density n.
    Output: Updated bone_data with new cell positions.
    """
    n = bone_data[:, :, :, 1]
    
    # Calculate change using the Laplacian (diffusion)
    dn_dt = D * laplace(n)
    
    # Update and clip to ensure n stays between 0 and 1
    bone_data[:, :, :, 1] = np.clip(n + dn_dt * dt, 0, 1)
    
    return bone_data
