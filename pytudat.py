#!/usr/bin/env python3
import json
from types import SimpleNamespace
class Empty(SimpleNamespace):
    def __getattr__(self, name):
        setattr(self, name, Empty())
        return getattr(self, name)
class OrbitalElements:
    def __init__(self, semiMajorAxis:float, eccentricity:float, inclination:float, argumentOfPeriapsis:float, longitudeOfAscendingNode:float, trueAnomaly:float):
        self.type = "keplerian"
        self.semiMajorAxis=semiMajorAxis
        self.eccentricity=eccentricity
        self.inclination=inclination
        self.argumentOfPeriapsis=argumentOfPeriapsis
        self.longitudeOfAscendingNode=longitudeOfAscendingNode
        self.trueAnomaly=trueAnomaly

class tudatConfig(Empty):
    def __init__(self, sateliteName: str, finalEpoch : int, intialPosition: OrbitalElements):
        self.initialEpoch = 0
        self.finalEpoch = finalEpoch

        self.globalFrameOrientation = "J2000"

        self.spice.useStandardKernels = True
        self.spice.preloadEphemeris = False

        self.bodies.Earth.useDefaultSettings = True
        getattr(self.bodies, sateliteName).initialState  = intialPosition

        self.propagators = [] 
        self.propagators.append(Empty(integratedStateType = "translational",
                                      centralBodies = ["Earth"],
                                      bodiesToPropagate = [sateliteName]))
        getattr(self.propagators[0].accelerations, sateliteName).Earth = [Empty(type="pointMassGravity")]
        self.integrator.type = "rungeKutta4"
        self.integrator.stepSize = 10

        self.export =[Empty(file = "@path(stateHistory.txt)", variables = [ Empty(type="state") ])]

        self.options.fullSettingsFile = "@path(fullSettings.json)"

a = tudatConfig("Asterix", 86400, OrbitalElements(7.5E6,0.1,1.4888,4.1137,0.4084,2.4412))
b = json.dumps(a, indent=2, default=lambda o: o.__dict__)
print(b)

