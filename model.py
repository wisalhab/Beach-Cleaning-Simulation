from pydoc import doc
import mesa
import random
import numpy as np
from random import randint
from agents import SmallRobot
from agents import BigRobot
from agents import PalmTree
from agents import Trash
from agents import WasteBin
from agents import UNDONE
from agents import NUMBER_OF_CELLS 
from agents import Terrain
from agents import Charge
from agents import BioDegradable
from agents import Hazard 
from agents import Auctioneer

class Warehouse(mesa.Model):
    """ Model representing an automated warehouse""" #using warehouse lab as base 
    def __init__(self, n_lcs, n_hazard, n_cts, n_trash, width=50, height=50):
        
        self.num_lcs = n_lcs
        self.num_cts = n_cts
        self.num_trash = n_trash
        self.num_hazard = n_hazard
        self.num_palm_trees = random.choice([3,4,5,6])  # allows random selection with each reset
        self.grid = mesa.space.MultiGrid(width, height, False)
        self.grid.trash_bid_queue = []
        self.schedule = mesa.time.RandomActivation(self)
        self.width = width
        self.height = height
       
        num_agents = 0
        self.running = True
        for x in range(NUMBER_OF_CELLS):
            for y in range(NUMBER_OF_CELLS): 
                k = random.random()
                type = False
                #20% of map is clean at start
                if k < 0.2:
                    type = True
                a = Terrain((num_agents), self, type)
                self.schedule.add(a)
                self.grid.place_agent(a, (x, y))
                num_agents += 1 
        
        middle_x = width // 2
        middle_y = height // 2


        for i in range(n_lcs):
            #middle spawn for LC
            start_x = middle_x + i
            start_y = middle_y

            robot = SmallRobot(i + 1000, self)  #diff id for robots
            self.schedule.add(robot)
            self.grid.place_agent(robot, (start_x, start_y))

            #CT are placed randomly
        for j in range(n_cts): 
            bot_x = random.randrange(width)
            bot_y = random.randrange(height)

            big_robot = BigRobot(j + 2000, self)  
            self.schedule.add(big_robot)
            self.grid.place_agent(big_robot, (bot_x, bot_y)) 

            #plastic trash random placed
        for z in range(n_trash): 
            bot_x = random.randrange(width)
            bot_y = random.randrange(height)

            trash = Trash(z + 4000, self)  
            self.schedule.add(trash)
            self.grid.place_agent(trash, (bot_x, bot_y)) 

            #hazardous waste is randomly placed
        for z in range(n_hazard): 
            bot_x = random.randrange(width)
            bot_y = random.randrange(height)

            hazard = Hazard(z + 6000, self)  
            self.schedule.add(hazard)
            self.grid.place_agent(hazard, (bot_x, bot_y))


            #trees randomly placed in range of 3-6
        for _ in range(self.num_palm_trees):
            tree_x = random.randrange(width)
            tree_y = random.randrange(height)

            palm_tree = PalmTree(num_agents, self)  
            self.schedule.add(palm_tree)
            self.grid.place_agent(palm_tree, (tree_x, tree_y)) 
            num_agents += 1

        #single agents with designated location
        waste_bin = WasteBin(5000, self)
        self.schedule.add(waste_bin)
        self.grid.place_agent(waste_bin, (width - 1, 0)) 
        num_agents += 1
        

        charge = Charge(5001, self)
        self.schedule.add(charge)
        self.grid.place_agent(charge, (0, 0)) 
        num_agents += 1

        #auctioneer wont be placed on model however decides for queue
        auctioneer = Auctioneer (6007, self)
        self.schedule.add(auctioneer)
        num_agents += 1


    def step(self):
        if random.randint(0, 25) == 0 :
            trash_x = random.randrange(self.width)
            trash_y = random.randrange(self.height)

            self.num_trash += 1

            trash = Trash(self.num_trash + 4000, self)  
            self.schedule.add(trash)
            self.grid.place_agent(trash, (trash_x, trash_y)) 
        
        self.schedule.step()
        
    
        '''for agent in self.schedule.agents:
            if isinstance(agent, BigRobot):
                agent.step()'''
