import numpy as np
from gdal import Open
import matplotlib.pyplot as plt

# Define a function to allocate land uses
def allocate_land_uses(land_demand, demand_units, allocation):
    # Define the demand for each land use
    demand_units = np.array([3102, 3103, 3106, 3107, 3108])
    Agriculture_demand_all = np.array([12, 40, 32, 31, 10])
    Urban_demand_all = np.array([8, 0, 0, 32, 0])
    Industry_demand_all = np.array([0, 12, 19, 20, 5])

    # Calculate the demand for each land use in each year
    Agriculture_demand = np.zeros(np.shape(Agriculture))
    Urban_demand = np.zeros(np.shape(Urban))
    Industry_demand = np.zeros(np.shape(Industry))

    for i in range(len(demand_units)):
        # in odd years allocation is more than even years
        if i % 2 == 1:
            Agriculture_demand.append(np.floor((Agriculture_demand_all) / 4))
            Urban_demand.append(np.floor((Urban_demand_all) / 4))
            Industry_demand.append(np.floor((Industry_demand_all) / 4))
        else:
            Agriculture_demand.append(np.floor((Agriculture_demand_all) / 5))
            Urban_demand.append(np.floor((Urban_demand_all) / 5))
            Industry_demand.append(np.floor((Industry_demand_all) / 5))

    # Allocate land uses for each year
    count = np.zeros(len(demand_units))
    for j in range(5):
        # Allocate urban land use
        count = count * 0
        while True:
            row = np.where(Urban == np.max(np.max(Urban)))[0][0]
            column = np.where(Urban == np.max(np.max(Urban)))[1][0]
            if count[0] == Urban_demand[j][0] and count[1] == Urban_demand[j][1] and count[2] == Urban_demand[j][2] and count[3] == Urban_demand[j][3] and count[4] == Urban_demand[j][4]:
                break
            else:
                for i in range(len(demand_units)):
                    if land_demand[row, column] == demand_units[i]:
                        if count[i] < Urban_demand[j][i]:
                            allocation[row, column] = 1
                            count[i] += 1
                            Agriculture[row, column] = 0
                            Industry[row, column] = 0

                Urban[row, column] = 0

        # Allocate industry land use
        count = count * 0
        while True:
            row = np.where(Industry == np.max(np.max(Industry)))[0][0]
            column = np.where(Industry == np.max(np.max(Industry)))[1][0]
            if count[0] == Industry_demand[j][0] and count[1] == Industry_demand[j][1] and count[2] == Industry_demand[j][2] and count[3] == Industry_demand[j][3] and count[4] == Industry_demand[j][4]:
                break
            else:
                for i in range(len(demand_units)):
                    if land_demand[row, column] == demand_units[i]:
                        if count[i] < Industry_demand[j][i]:
                            allocation[row, column] = 2
                            count[i] += 1
                            Agriculture[row, column] = 0
                            Urban[row, column] = 0

            Industry[row, column] = 0

        # Allocate agriculture land use
        count = count * 0
        while True:
            row = np.where(Agriculture == np.max(np.max(Agriculture)))[0][0]
            column = np.where(Agriculture == np.max(np.max(Agriculture)))[1][0]

            if count[0] == Agriculture_demand[j][0] and count[1] == Agriculture_demand[j][1] and count[2] == Agriculture_demand[j][2] and count[3] == Agriculture_demand[j][3] and count[4] == Agriculture_demand[j][4]:
                break
            else:
                for i in range(len(demand_units)):
                    if land_demand[row, column] == demand_units[i]:
                        if count[i] < Agriculture_demand[j][i]:
                            allocation[row, column] = 4
                            count[i] += 1
                            Urban[row, column] = 0
                            Industry[row, column] = 0

            Agriculture[row, column] = 0

        # Plot the allocation for each year
        plt.pyplot.imshow(allocation , cmap="jet")
        plt.pyplot.title("Allocations in year of " + str(j + 1) + " to all land uses"), fontsize=25)
        plt.pyplot.colorbar()
        plt.pyplot.show()
        np.save("Allocation" + str(j + 1), allocation)

# Read data
Land_demand_unit = Open(r"data/Land_demand_unit.tif")
Agriculture_map = Open(r"data/Agriculture_potential.tif")
Urban_map = Open(r"data/URban_potential.tif")
Industry_map = Open(r"data/Industry_Potential.tif")

# Read data as array
landDemand = np.array(Land_demand_unit.ReadAsArray(), dtype=int)
Agriculture = np.array(Agriculture_map.ReadAsArray(), dtype=float)
Urban = np.array(Urban_map.ReadAsArray(), dtype=float)
Industry = np.array(Industry_map.ReadAsArray(), dtype=float)

# Convert land demand codes to demand units
shape = landDemand.shape
for i in range(shape[0]):
    for j in range(shape[1]):
        if landDemand[i, j] == 1:
            landDemand[i, j] = 3107
        elif landDemand[i, j] == 2:
            landDemand[i, j] = 3103
        elif landDemand[i, j] == 3:
            landDemand[i, j] = 3108
        elif landDemand[i, j] == 4:
            landDemand[i, j] = 3106
        elif landDemand[i, j] == 5:
            landDemand[i, j] = 3102

# Allocate land uses for each year
allocation = np.zeros(np.shape(Agriculture))
demand_units = np.array([3102, 3103, 3106, 3107, 3108])
allocate_land_uses(landDemand, demand_units, allocation)
