# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% setup
__name__=='__main__'

# %%
import os
import openseespywin.opensees as ops
from math import isclose

panel_text="""
L = 48 # in
E = 29000 # ksi
A = 20 # in^2
I = 800 # in^4
P = 10 # kips
"""

# config = {
#     'L': 48, # in
#     'E': 29000, # ksi
#     'A': 20, # in^2
#     'I': 800, # in^4
#     'P': 10 # kips
# }
config={}
exec(panel_text, {}, config)

# %% model setup
ops.wipe()
ops.model('basic','-ndm',2,'-ndf',3)

ops.node(1,0,0); ops.fix(1,1,1,1)
ops.node(2,config['L'],0)

ops.section('Elastic',1,config['E'],config['A'],config['I'])
ops.beamIntegration('Lobatto',1, # tag
    1, # secTag
    3 # N
)

ops.geomTransf('Linear',
    1 # transfTag
)

ops.element('forceBeamColumn',1,
    1,2,
    1, # secTag
    1 # transfTag
)

ops.timeSeries('Constant',1)
ops.pattern('Plain',1,1)
ops.load(2, # nodeTag
    0,config['P'],0 # loadValues
)

ops.analysis('Static')
ops.analyze(1)

# WARNING analysis Static - no Algorithm yet specified,
#  NewtonRaphson default will be used
# WARNING analysis Static - no ConstraintHandler yet specified,
#  PlainHandler default will be used
# WARNING analysis Static - no Numberer specified,
#  RCM default will be used
# WARNING analysis Static - no Integrator specified,
#  StaticIntegrator default will be used
# WARNING analysis Static - no LinearSOE specified,
#  ProfileSPDLinSOE default will be used
# %% reactions

ops.reactions()

# %% test_force

assert isclose(ops.nodeReaction(1,2),-config['P'])

# %% test_moment

assert isclose(ops.nodeReaction(1,3),-config['P']*config['L'])

# %% test_deflection
ops.nodeDisp(2,2)

assert isclose(ops.nodeDisp(2,2),config['P']*config['L']**3/(3*config['E']*config['I']))

# %% test_rotation
ops.nodeDisp(2,3)
assert isclose(ops.nodeDisp(2,3),config['P']*config['L']**2/(2*config['E']*config['I']))

# %% start of recorder generation


import datetime
timestamp= datetime.datetime.now().strftime("%y%m%d_%H%M%S")
if not os.path.exists("tests/recordings"):
    os.makedirs("tests/recordings")

node_out=os.path.join("tests/recordings", "node_" + timestamp + ".out")
eleGlobal_out=os.path.join("tests/recordings", "eleGlobal_" + timestamp + ".out")
eleLocal_out=os.path.join("tests/recordings", "eleLocal_" + timestamp + ".out")

# create a Recorder object for the nodal displacements at node 4
ops.recorder("Node", "-file", "example.out", "-time", "-node", 4, "-dof", 1, 2, "disp")
ops.recorder("Element", "-file", "eleGlobal.out", "-time", "-ele", 1, 2, 3, "forces")
ops.recorder("Element", "-file", "eleLocal.out", "-time", "-ele", 1, 2, 3, "basicForces")
