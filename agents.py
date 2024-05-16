from optparse import check_builtin
import random
import mesa
from collections import OrderedDict
from pprint import pprint

NUMBER_OF_CELLS = 25
UNDONE = 0
DONE = 1

class Terrain(mesa.Agent):
    def __init__(self, id, model, terrain_type):
        super().__init__(id, model)
        self.terrain_type = terrain_type

class PalmTree(mesa.Agent):
    def __init__(self, id, model):
        super().__init__(id, model)

#BigRobot is CT 
#initilization of battery, hopper, vision values
class BigRobot(mesa.Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.designated_area = get_designated_area(agent_id= id-2000, num_agents=model.num_cts, grid_height= model.grid.height)
        self.search_next = (0, self.designated_area[0])
        self.vision_range = 3
        self.battery_capacity = 200
        self.battery_level = random.randint(50, self.battery_capacity)
        self.charging = False
        self.hopper_capacity = 2
        self.hopper_current = 0
        self.unloading = False
        self.finished = False
        self.trash_to_collect = None

    def deliberate(self):
    #decisions by priority
        pprint(vars(self))
        if self.finished :
            self.finished = False
            self.search_next = (0, self.designated_area[0])
            return
        
        x, y = self.pos
        if self.charging or self.battery_level < x+y+4 :
            self.move_to_charger_and_charge()
            return

        print(self.hopper_current, ">=", self.hopper_capacity)
        if self.unloading or self.hopper_current >= self.hopper_capacity :
            self.move_to_wastebin_and_unload()
            return
        
        if self.trash_to_collect is not None :
            self.move_towards(self.trash_to_collect)
            self.pick_up_trash()
            return
        
        self.clean()
        
    #search pattern
    def clean(self):
        x, y = self.pos

        #3x3 vision so skip 3 rows
        #movement behaviour of designated areas
        skip_rows = 3
        if self.pos == self.search_next:   
            if ((y - self.designated_area[0]) // skip_rows) % 2 == 0 :
                if x+1 < self.model.grid.width :
                    self.search_next = (x+1, y)
                elif y+skip_rows < self.designated_area[1] :
                    self.search_next = (x,y+skip_rows)  
                else :
                    self.finished = True
            else :
                if x-1 >= 0:
                    self.search_next = (x-1, y)
                elif y+skip_rows < self.designated_area[1] :
                    self.search_next = (x,y+skip_rows)  
                else :
                    self.finished = True

        self.move_towards(self.search_next)

    def move_to_charger_and_charge(self):
        x, y = self.pos
        charger_pos = (0, 0)

        #pass target and guides path automatically
        self.move_towards(charger_pos)

        if self.pos == charger_pos and self.battery_level <= self.battery_capacity:
            self.charging = True
            self.battery_level += 25
            if self.battery_level >= self.battery_capacity:
                self.charging = False
                self.battery_level = self.battery_capacity

    def move_to_wastebin_and_unload(self):
        x, y = self.pos
        wastebin_pos = (self.model.grid.width - 1, 0)

        self.move_towards(wastebin_pos)
        
        if self.pos == wastebin_pos and self.hopper_current > 0:
            self.unloading = True
            self.hopper_current -= 1
            if self.hopper_current <= 0:
                self.unloading = False
                self.hopper_current = 0

    def move_towards(self, target) :
        self.detect_trash()
        
        x, y = self.pos
        target_x, target_y = target

        move_speed = 1

        if x < target_x:
            x += move_speed
        elif x > target_x:
            x -= move_speed
        elif y < target_y:
            y += move_speed
        elif y > target_y:
            y -= move_speed

        self.model.grid.move_agent(self, (x, y))
        self.battery_level -= 1

    def step(self):
        self.deliberate()

    #vision 
    def detect_trash(self):
        x, y = self.pos
        auctioneer = next((a for a in self.model.schedule.agents if isinstance(a, Auctioneer)), None)
        for i in range(-self.vision_range, self.vision_range + 1):
            for j in range(-self.vision_range, self.vision_range + 1):
                new_x, new_y = x + i, y + j
                if 0 <= new_x < self.model.grid.width and 0 <= new_y < self.model.grid.height:
                    cell_contents = self.model.grid.get_cell_list_contents([(new_x, new_y)])
                    trash_at_position = [agent for agent in cell_contents if isinstance(agent, Trash)]
                    if trash_at_position:
                        auctioneer.add_to_queue((new_x, new_y))

    def pick_up_trash(self):
        x, y = self.pos
        trash_at_position = [agent for agent in self.model.grid.get_cell_list_contents([(x, y)]) if isinstance(agent, Trash)]

        if trash_at_position:
            trash_piece = trash_at_position[0]
            self.model.grid.remove_agent(trash_piece)
            self.model.schedule.remove(trash_piece)
            self.hopper_current += 1

        if self.pos == self.trash_to_collect:
            auctioneer = next((a for a in self.model.schedule.agents if isinstance(a, Auctioneer)), None)
            auctioneer.collected(self.trash_to_collect)
            self.trash_to_collect = None

    def calculate_journey_distance(self, waypoints) :
        waypoints.insert(0, self.pos)
        return sum([sum(abs(x - y) for x, y in zip(waypoint1, waypoint2)) for waypoint1, waypoint2 in zip(waypoints[:-1], waypoints[1:])])

    #make sure robots dont die on journey
    def battery_remaining_after_journey(self, waypoints) :
        total_dist = self.calculate_journey_distance(waypoints)
        return self.battery_level - (total_dist-2)

    #bidding on fitness
    def collecting_trash_fitness(self, trash) :
        wastebin_pos = (self.model.grid.width - 1, 0)
        charger_pos = (0, 0)
        waypoints = [trash, wastebin_pos, charger_pos]
        if self.hopper_current == self.hopper_capacity or self.trash_to_collect is not None :
            return -1
        return self.battery_remaining_after_journey(waypoints) * self.calculate_journey_distance([wastebin_pos])

class WasteBin(mesa.Agent):
    def __init__(self, id, model):
        super().__init__(id, model)

class Charge(mesa.Agent):
    def __init__(self, id, model):
        super().__init__(id, model)   

class Auctioneer(mesa.Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.trash_queue = OrderedDict()
        
    def step(self):
        trash_list = [t for t in self.trash_queue.keys() if self.trash_queue[t] == "unassigned"]
        for trash in trash_list :
            robots = [r for r in self.model.schedule.agents if isinstance(r, BigRobot)]
            robots = [r for r in robots if r.trash_to_collect is None]
            robots = [(r, r.collecting_trash_fitness(trash)) for r in robots]
            robots = [r for r in robots if r[1] > 0]
            if len(robots) > 0:
                lowest_battery_robot, _ = min(robots, key=lambda x: x[1])
                lowest_battery_robot.trash_to_collect = trash

                self.trash_queue[trash] = "assigned"

                print("assigned "+str(trash)+" to " + str(lowest_battery_robot))

    
    def add_to_queue(self, trash_coordinate) :
        if (trash_coordinate not in self.trash_queue or self.trash_queue[trash_coordinate] == None) :
            self.trash_queue[trash_coordinate] = "unassigned"

    def collected(self, trash_coordinate) :
        if (trash_coordinate in self.trash_queue) :
            self.trash_queue[trash_coordinate] = None

#this class is used as recyled material for extended operation and plastic bottles before extention
class Trash(mesa.Agent):
    def __init__(self, id, model):
        super().__init__(id, model)

class Hazard(mesa.Agent):
    def __init__(self, id, model):
        super().__init__(id, model)

class BioDegradable(mesa.Agent):
    def __init__(self, id, model):
        super().__init__(id, model)

class SmallRobot(mesa.Agent):
    def __init__(self, id, model):
     
        super().__init__(id, model)
        self.designated_area = get_designated_area(agent_id= id-1000, num_agents=model.num_lcs, grid_height= model.grid.height)
        self.to_clean_next = (0, self.designated_area[0])
        self.hopper_capacity = 100
        self.hopper_current = 0
        self.finished = False
        self.unloading = False

    @property
    def isBusy(self):
        return self.state == BUSY

    def step(self):
        self.deliberate()

    # Robot decision model

    def deliberate(self):
        if self.finished :
            return
        if self.hopper_current >= self.hopper_capacity or self.unloading :
            self.move_to_wastebin_and_unload()
        else :
            self.detect_trash()
            self.clean()

    def detect_trash(self):
        x, y = self.pos
        auctioneer = next((a for a in self.model.schedule.agents if isinstance(a, Auctioneer)), None)
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_x, new_y = x + i, y + j
                if 0 <= new_x < self.model.grid.width and 0 <= new_y < self.model.grid.height:
                    cell_contents = self.model.grid.get_cell_list_contents([(new_x, new_y)])
                    trash_at_position = [agent for agent in cell_contents if isinstance(agent, Trash)]
                    if trash_at_position:
                        auctioneer.add_to_queue((new_x, new_y))

    def move_to_wastebin_and_unload(self):
        x, y = self.pos
        wastebin_pos = (self.model.grid.width - 1, 0)

        self.move_towards(wastebin_pos)

        if self.pos == wastebin_pos and self.hopper_current >= 0:
            self.unloading = True
            self.hopper_current -= 10
            if self.hopper_current <= 0:
                self.unloading = False
                self.hopper_current = 0

    def clean(self):
        x, y = self.pos
        if self.pos == self.to_clean_next:   
            if (y - self.designated_area[0]) % 2 == 0 :
                if x+1 < self.model.grid.width :
                    self.to_clean_next = (x+1, y)
                elif y+1 < self.designated_area[1] :
                    self.to_clean_next = (x,y+1)  
                else :
                    self.finished = True
            else :
                if x-1 >= 0:
                    self.to_clean_next = (x-1, y)
                elif y+1 < self.designated_area[1] :
                    self.to_clean_next = (x,y+1)  
                else :
                    self.finished = True        

        self.move_towards(self.to_clean_next)

    def move_towards(self, target) :
        self.detect_trash()

        x, y = self.pos
        target_x, target_y = target

        # clean current terrain
        if self.hopper_current < self.hopper_capacity :
            for c in self.model.grid.get_cell_list_contents([self.pos]):
                if isinstance(c, Terrain) and c.terrain_type == False:
                    self.hopper_current += 4
                    c.terrain_type = True

        move_speed = 1 if self.hopper_current > self.hopper_capacity/2 else 1

        if y < target_y:
            y += move_speed
        elif y > target_y:
            y -= move_speed
        elif x < target_x:
            x += move_speed
        elif x > target_x:
            x -= move_speed

        self.model.grid.move_agent(self, (x, y))

#translated from mpt.java
def get_designated_area(agent_id, num_agents, grid_height):
    a = grid_height // num_agents  # rows per agent
    rem = grid_height % num_agents  # remaining rows
    left = agent_id * a + min(agent_id, rem)  # is 0 based
    right = left + a + (1 if agent_id < rem else 0)  # right is exclusive
    return left, right
