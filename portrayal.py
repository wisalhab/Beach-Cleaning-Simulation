from agents import SmallRobot
from agents import BigRobot
from agents import Terrain
from agents import Trash
from agents import PalmTree
from agents import WasteBin
from agents import Charge
from agents import BioDegradable
from agents import Hazard

def warehouse_portrayal(agent):  
   if isinstance(agent,SmallRobot):
        return small_robot_portrayal(agent)
   elif isinstance(agent,BigRobot):
        return big_robot_portrayal(agent)
   elif isinstance(agent,Terrain):
        return terrain_portrayal(agent)
   elif isinstance (agent,PalmTree ):
        return tree_portrayal(agent)
   elif isinstance (agent, Trash):
        return trash_portrayal(agent)
   elif isinstance (agent, WasteBin): 
        return waste_bin_portrayal(agent)
   elif isinstance (agent, Charge):
        return charge_portrayal(agent)

def tree_portrayal(PalmTree):

    if PalmTree is None:
        raise AssertionError
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0, 
        "Color": "green",
    } 

def terrain_portrayal(terrain):
    
    if terrain is None:
        raise AssertionError
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "Color": "cornsilk" if terrain.terrain_type==True else "darkgoldenrod"  
    }

def waste_bin_portrayal(WasteBin):

    if WasteBin is None:
        raise AssertionError
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0, 
        "Color": "skyblue",
    } 

def charge_portrayal(WasteBin):

    if WasteBin is None:
        raise AssertionError
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0, 
        "Color": "purple",
    }     



def small_robot_portrayal(robot):
    if robot is None:
        raise AssertionError
    return {
        "Shape": "circle",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 1,
        #"x": robot.x,
        #"y": robot.y,
        "scale": 2,
        #"heading_x": -1 if robot.isBusy else 1,
        #"heading_y":0,
        "r":0.4,
        "Color": "grey",
    }

def big_robot_portrayal(robot):
    if robot is None:
        raise AssertionError
    return {
        "Shape": "circle",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 1,
        #"x": robot.x,
        #"y": robot.y,
        "scale": 2,
        #"heading_x": -1 if robot.isBusy else 1,
        #"heading_y":0,
        "r":0.8,
        "Color": "black",
    }

def trash_portrayal(trash):
    if trash is None:
        raise AssertionError
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 1,
        #"x": robot.x,
        #"y": robot.y,
        #"heading_x": -1 if robot.isBusy else 1,
        #"heading_y":0,
        "r":0.8,
        "Color": "navy",
    }

def Hazard_portrayal(hazard):
    if hazard is None:
        raise AssertionError
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 1,
        "r":0.8,
        "Color": "lime",
    }

def Bio_Degradable_portrayal(BioDegradable):
    if trash is None: #TODO fix
        raise AssertionError
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 1,
        "r":0.5,
        "Color": "cyan",
    }

#TODO add portrayal of different bins
