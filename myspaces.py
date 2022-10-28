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

@space
class ObservedParticle:
    pos:CartesianPlane
    prev:CartesianPlane

@block
def particleIntegrator(state: Point[Particle], input: Point[CartesianPlane])-> Point[Particle]:
    #input is acceleration
    #output is the new particle state
    output = deepcopy(state)

    output['pos']['x']  += input['particle']['vel']['x']
    output['pos']['y']  += input['particle']['vel']['y']

    output['vel']['x']  += input['x']
    output['vel']['y']  += input['y']

    return output

@block
def randomPoint(input:Point[EmptySpace])-> Point[CartesianPlane]:
    data = {}
    data['x'] = .005+np.random.randn()/5.0
    data['y'] = .005+np.random.randn()/5.0

    return Point(CartesianPlane, data)

### ---
BlockType = type(particleIntegrator)

@space
class ParticleAgent:
    plant: Particle
    maxspeed: float
    reference: ObservedParticle
    strategy: BlockType

