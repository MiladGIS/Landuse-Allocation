import numpy as np
import matplotlib as plt

# Reading the image
lu1 = plt.image.imread(r"data/Land_use.tif")

# Creating a copy of the image
lu = lu1.copy()

# Mapping the values
# Create a dictionary to map the values to the desired numbers
mapping = {51: 1, 34: 2, 17: 3, 255: 0, 68: 4}

# Use the dictionary and NumPy's vectorized operations to map the values
for value, number in mapping.items():
    lu[lu1 == value] = number

# Number of land use
nlu = 3
# Number of rings
dist = 8
# Empty matrices to put the accumulation of each ring of effects in corresponding entry
Flk = np.zeros((dist, nlu, nlu))
# Count all cells and each land use
Numbers = [np.count_nonzero(lu == i) for i in range(1, nlu + 1)]
N = np.count_nonzero(lu)

# Iterate over each land use to calculate the enrichment factor
for l in range(1, nlu + 1):
    # Iterate over each cell in the land use matrix
    for i in range(dist, shape[0]):
        for j in range(dist, shape[1]):
            if lu[i, j] == l:
                # Iterate over each ring
                for k in range(1, dist + 1):
                    # Initialize the variable to iterate and sum
                    nkdi = 0
                    # Define a ring with the appropriate distance from the center cell
                    newlu = lu[i - k:i + k + 1, j - k:j + k + 1].copy()
                    # Disregard the inside of the defined ring
                    newlu[1:2 * k, 1:2 * k] = 0
                    # Iterate over each secondary land use
                    for ll in range(1, nlu + 1):
                        Nk = Numbers[ll - 1]
                        # Count the number of changed land use cells in the defined ring
                        nkdi = np.count_nonzero(newlu == ll)
                        # Calculate the Enrichment factor if the count is greater than 0
                        if nkdi > 0:
                            fNew = float((nkdi / (8 * k)) / (Nk / N))
                            # Accumulate the enrichment factor for each ring and put it in the corresponding entry
                            Flk[k-1, l-1, ll-1] += fNew

# Define names and appropriate colors for each land use
Names = ["Urban", "Industrial", "Agricultural"]
Colors = ['b', 'r', 'g']

# Define the number of land uses, number of rings, and the Flk array
nlu = len(Names)
dist = 10  # Example value, replace with actual number of rings
Flk = np.random.rand(dist, nlu, nlu)  # Example random data, replace with actual Flk array

# Use nested for loops to calculate the average and logarithm of each ring and the effect of the first land use to the second one
for o in range(nlu):
    for p in range(nlu):
        for r in range(dist):
            if Flk[r, o, p] != 0:
                # Calculate the logarithm of the Flk value
                Flk[r, o, p] = np.log10(Flk[r, o, p] / (Numbers[p]))  # Check and define Numbers array

        # Plot the outcomes
        plt.plot(range(1, dist + 1), Flk[::-1, o, p], color=Colors[p], linewidth=5)
        plt.title("Effect of " + Names[o] + " to " + Names[p], fontsize=25)
        plt.xlabel("Rings", fontsize=20)
        plt.ylabel("W", fontsize=20)
        plt.xticks(range(1, dist + 1), fontsize=15)
        plt.yticks(fontsize=15)
        plt.show()



# Create a mask array containing the indices of the neighbors relative to the current cell
mask = np.arange(-8, 9).reshape((1, -1))

# Initialize the neighborhood matrices
neighborhood_U = np.zeros((shape[0], shape[1]))
neighborhood_I = np.zeros((shape[0], shape[1]))
neighborhood_A = np.zeros((shape[0], shape[1]))

# Loop over the neighbors
for i in range(-1, 2):
    for j in range(-1, 2):
        # Skip the current cell
        if i == 0 and j == 0:
            continue
        
        # Create a neighborhood mask using array slicing and broadcasting
        neighborhood = lu[max(0, i):shape[0]+min(0, i), max(0, j):shape[1]+min(0, j)]
        
        # Create masks for each neighborhood matrix (U, I, and A)
        mask_U = (neighborhood == 1) * Flk[:, :, 0]
        mask_I = (neighborhood == 2) * Flk[:, :, 1]
        mask_A = (neighborhood == 3) * Flk[:, :, 2]
        
        # Sum the masks along the appropriate axes
        neighborhood_U += np.sum(mask_U[:, -j:shape[1]-j], axis=(0, 1)) + np.sum(mask_U[-i:, :], axis=(0, 1))
        neighborhood_I += np.sum(mask_I[:, -j:shape[1]-j], axis=(0, 1)) + np.sum(mask_I[-i:, :], axis=(0, 1))
        neighborhood_A += np.sum(mask_A[:, -j:shape[1]-j], axis=(0, 1)) + np.sum(mask_A[-i:, :], axis=(0, 1))
                        

# Define a function for neighborhood normalization
def normalize_neighborhood(neighborhood, neighborhood_type):
    # Calculate the parameters for normalization
    a = (np.max(neighborhood) - np.min(neighborhood)) / 0.8
    b = (a / 10) - np.min(neighborhood)
    
    # Perform the normalization
    normalized_neighborhood = np.minimum(np.maximum(0, ((neighborhood + b) / a)), 1)
    
    # Show the normalized neighborhood map
    plt.imshow(normalized_neighborhood, cmap="jet")
    plt.colorbar()
    plt.title(f"Normalized neighborhood map of {neighborhood_type}")
    plt.show()
    
    # Save the normalized array to a file
    np.save(f"N_neighborhood_{neighborhood_type}", normalized_neighborhood)

# Perform normalization for each type of neighborhood
normalize_neighborhood(neighborhood_U, "U")
normalize_neighborhood(neighborhood_I, "I")
normalize_neighborhood(neighborhood_A, "A")
