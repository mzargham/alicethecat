import os
from copy import deepcopy
import numpy as np

os.chdir("/Users/zargham/Documents/GitHub/cadcad-ri")
from cadcad.spaces import space, EmptySpace #, Bit, Real
from cadcad.dynamics import block
from cadcad.points import Point
#from cadcad.systems import Experiment

@space
class CartesianPlane:
    x:float
    y:float

@space
class Particle:
    pos:CartesianPlane
    vel:CartesianPlane

@block
def particleIntegrator(state: Point[Particle], input: Point[CartesianPlane])-> Point[Particle]:
    #input is acceleration
    #output is the new particle state
    output = deepcopy(state)

    output['pos']['x']  += state['particle']['vel']['x']
    output['pos']['y']  += state['particle']['vel']['y']

    output['vel']['x']  += input['x']
    output['vel']['y']  += input['y']

    return output

@block
def randomPoint(input:Point[EmptySpace])-> Point[CartesianPlane]:
    data = {}
    data['x'] = .005+np.random.randn()/5.0
    data['y'] = .005+np.random.randn()/5.0

    return Point(CartesianPlane, data)

@block
def observePosition(input:Point[Particle])-> Point[CartesianPlane]:
    pos = input.data['pos']
    return Point(CartesianPlane, pos)

@block
def chase(state: Point[Particle], ref: Point[CartesianPlane]) -> Point[CartesianPlane]:

    acc = {}
    acc['x'] = ref.data['x']-state.data['pos']['x']
    acc['y'] = ref.data['y']-state.data['pos']['y']

    return Point(CartesianPlane, acc)

@space
class WorldState:
    cat: Particle
    laser:Particle

# this block contains my wiring
# in the future wiring DSL should allow this to be done with piping logic
@block
def worldDynamics(state: Point[WorldState])->Point[WorldState]:

    #split into subspaces
    cat = deepcopy(state['cat'])
    laser = deepcopy(state['laser'])

    #move the laser pointer
    emptyPoint = Point(EmptySpace, {})
    laserAcc = randomPoint(emptyPoint)
    laser = particleIntegrator(laser, laserAcc)

    #chase the laser pointer
    observedLaser = observePosition(laser)
    catAcc = chase(cat, observedLaser)
    cat = particleIntegrator(cat, catAcc)

    data = {'cat':cat.data, 'laser':laser.data }
    
    return Point(WorldState, data)
