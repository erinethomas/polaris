(seaice-single-column)=

# single_column
The `single_column` test group includes any sea ice tests 
using only column physics.

## standard_physics

### description

The test runs a single column in the Arctic with coordinates 71.35N, 156.5W.
A one year simulation is run /......

```{image} images/single_cell.png
:align: center
:width: 500 px
```

### mesh

Specify whether the mesh is global or planar and the resolution(s) tested. If
planar, specify the mesh size. If global, specify whether the mesh is
icosohedral or quasi-uniform. Specify any relevant options in the config file
pertaining to setting up the mesh.


### initial conditions

The initial conditions should be specified for all variables requiring
initial conditions (see {ref}`dev-seaice-model`).

### forcing

If applicable, specify the forcing applied at each time step of the simulation
(in MPAS-Seaice, these are the variables contained in the `forcing` stream).
If not applicable, keep this section with the notation N/A.

### time step and run duration

The time step for forward integration should be specified here for the test
case's resolution. The run duration should also be specified.

### config options

Here, include the config section(s) that is specific to this test case. E.g.,

```cfg
# replace this section with ice variables.

# options for cosine bell convergence test case
[cosine_bell]

# time step per resolution (s/km), since dt is proportional to resolution
dt_per_km = 30

# the constant temperature of the domain
temperature = 15.0

# the constant salinity of the domain
salinity = 35.0
...


# options for visualization for the cosine bell convergence test case
[cosine_bell_viz]

# visualization latitude and longitude resolution
dlon = 0.5
dlat = 0.5

# remapping method ('bilinear', 'neareststod', 'conserve')
remap_method = conserve
```

Include here any further description of each of the config options.

### cores

Specify whether the number of cores is determined by `goal_cells_per_core` and
`max_cells_per_core` in the `seaice` section of the config file or whether the
default and minimum number of cores is given in arguments to the forward step,
and what those defaults are.
