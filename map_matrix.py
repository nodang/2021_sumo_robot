import math
import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize,linewidth=np.inf)

me = 1
you = 2
blue = 3
red = 4

map_max = 48
blue_size_ = blue_size = 14
red_size_ = red_size = 14
# start 0

map_sumo = np.zeros((map_max,map_max))     #2.4m -> divide to 48, 50mm -> index(1)

#==========================================================================#        #blue area set
map_sumo[0,:blue_size_] = map_sumo[0,map_max-blue_size_:] = blue
map_sumo[1,:blue_size_] = map_sumo[1,map_max-blue_size_:] = blue
map_sumo[2,:blue_size_] = map_sumo[2,map_max-blue_size_:] = blue
map_sumo[3,:blue_size_] = map_sumo[3,map_max-blue_size_:] = blue
map_sumo[4,:blue_size_] = map_sumo[4,map_max-blue_size_:] = blue

blue_size_ = blue_size-1
map_sumo[5,:blue_size_] = map_sumo[5,map_max-blue_size_:] = blue
map_sumo[6,:blue_size_] = map_sumo[6,map_max-blue_size_:] = blue
map_sumo[7,:blue_size_] = map_sumo[7,map_max-blue_size_:] = blue

blue_size_ = blue_size-2
map_sumo[8,:blue_size_] = map_sumo[8,map_max-blue_size_:] = blue
map_sumo[9,:blue_size_] = map_sumo[9,map_max-blue_size_:] = blue

blue_size_ = blue_size-3
map_sumo[10,:blue_size_] = map_sumo[10,map_max-blue_size_:] = blue

blue_size_ = blue_size-4
map_sumo[11,:blue_size_] = map_sumo[11,map_max-blue_size_:] = blue

blue_size_ = blue_size-6
map_sumo[12,:blue_size_] = map_sumo[12,map_max-blue_size_:] = blue

blue_size_ = blue_size-9
map_sumo[13,:blue_size_] = map_sumo[13,map_max-blue_size_:] = blue

map_sumo[34,:blue_size_] = map_sumo[34,map_max-blue_size_:] = blue

blue_size_ = blue_size-6
map_sumo[35,:blue_size_] = map_sumo[35,map_max-blue_size_:] = blue

blue_size_ = blue_size-4
map_sumo[36,:blue_size_] = map_sumo[36,map_max-blue_size_:] = blue

blue_size_ = blue_size-3
map_sumo[37,:blue_size_] = map_sumo[37,map_max-blue_size_:] = blue

blue_size_ = blue_size-2
map_sumo[38,:blue_size_] = map_sumo[38,map_max-blue_size_:] = blue
map_sumo[39,:blue_size_] = map_sumo[39,map_max-blue_size_:] = blue

blue_size_ = blue_size-1
map_sumo[40,:blue_size_] = map_sumo[40,map_max-blue_size_:] = blue
map_sumo[41,:blue_size_] = map_sumo[41,map_max-blue_size_:] = blue
map_sumo[42,:blue_size_] = map_sumo[42,map_max-blue_size_:] = blue

blue_size_ = blue_size
map_sumo[43,:blue_size_] = map_sumo[43,map_max-blue_size_:] = blue
map_sumo[44,:blue_size_] = map_sumo[44,map_max-blue_size_:] = blue
map_sumo[45,:blue_size_] = map_sumo[45,map_max-blue_size_:] = blue
map_sumo[46,:blue_size_] = map_sumo[46,map_max-blue_size_:] = blue
map_sumo[47,:blue_size_] = map_sumo[47,map_max-blue_size_:] = blue
#=================================================================================#
red_size_ = red_size-1
pos = 22
red_l = 4  #start 4 -> end 14
map_sumo[17,pos:pos+red_l] = map_sumo[17+red_size_,pos:pos+red_l] = red
red_size_ = red_size-2
pos = pos-2
red_l = 4+4
map_sumo[18,pos:pos+red_l] = map_sumo[17+red_size_,pos:pos+red_l] = red
red_size_ = red_size-3
pos = pos-1
red_l = 4+4+2
map_sumo[19,pos:pos+red_l] = map_sumo[17+red_size_,pos:pos+red_l] = red
red_size_ = red_size-4
pos = pos-1
red_l = 4+4+2+2
map_sumo[20,pos:pos+red_l] = map_sumo[17+red_size_,pos:pos+red_l] = red
red_size_ = red_size-5
pos = pos
red_l = 4+4+2+2
map_sumo[21,pos:pos+red_l] = map_sumo[17+red_size_,pos:pos+red_l] = red
red_size_ = red_size-6
pos = pos-1
red_l = 4+4+2+2+2
map_sumo[22,pos:pos+red_l] = map_sumo[17+red_size_,pos:pos+red_l] = red
red_size_ = red_size-7
pos = pos
red_l = 4+4+2+2+2
map_sumo[23,pos:pos+red_l] = map_sumo[17+red_size_,pos:pos+red_l] = red
#=================================================================================#
#print(map_sumo)

