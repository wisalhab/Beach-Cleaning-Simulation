import mesa
from model import Warehouse
from portrayal import warehouse_portrayal
from agents import NUMBER_OF_CELLS

SIZE_OF_CANVAS_IN_PIXELS_X = 500
SIZE_OF_CANVAS_IN_PIXELS_Y = 500

simulation_params = {
    "height": NUMBER_OF_CELLS, 
    "width": NUMBER_OF_CELLS,
    "n_lcs": mesa.visualization.Slider(
        'Number of LCs',
        2, #default
        1, #min
        10, #max
        1, #step
        "Choose how many Lightweight Cleaning to include in the simulation"
    ),
    "n_cts": mesa.visualization.Slider(
        'Number of CTs',
        2, #default
        1, #min
        3, #max
        1, #step
        "Choose how many Cleaning Tank Robots to include in the simulation"
    ),
    "n_trash": mesa.visualization.Slider(
        'number of big trash pieces',
        1, #default
        7, #min
        15, #max
        1, #step
        "choose how much trash to include in the simulation"
    ),
    "n_hazard": mesa.visualization.Slider(
        'number of hazardous waste',
        2, #default
        2, #min
        7, #max
        1, #step
        "choose how much hazardous waste to include in the simulation"
    ),
    }
grid = mesa.visualization.CanvasGrid(warehouse_portrayal, NUMBER_OF_CELLS, NUMBER_OF_CELLS, SIZE_OF_CANVAS_IN_PIXELS_X, SIZE_OF_CANVAS_IN_PIXELS_Y)


server = mesa.visualization.ModularServer(
    Warehouse, [grid], "Beach Cleaning Simulation", simulation_params
)
