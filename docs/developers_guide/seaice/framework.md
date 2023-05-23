(dev-seaice-framework)=

# Seaice framework

The `seaice` component contains an ever expanding set of shared framework code.

(dev-seaice-model)=

## Model

### Running an E3SM component

Steps that run either MPAS-Seaice should descend from the
{py:class}`polaris.seaice.model.SeaiceModelStep` class.  This class descends
from {py:class}`polaris.ModelStep`, so there is a lot of relevant
discussion in {ref}`dev-model`.


#### Setting MPI resources

The target and minimum number of MPI tasks (`ntasks` and `min_tasks`, 
respectively) are set automatically if `ntasks` and `min_tasks` have not
already been set explicitly.  In such cases, a subclass of `SeaiceModelStep`
must override the
{py:meth}`polaris.seaice.model.SeaiceModelStep.compute_cell_count()` method
to compute the number of cells in the mesh.  Since it is typically not possible
to read the cell count from a file during setup, this method may need to have
a heuristic way of approximating the number of cells during setup (i.e. when
the `at_setup` parameter is `True`.  Then, it can return the exact number of 
cells at runtime (i.e. `at_setup == False`).

The algorithm for determining the resources is:

```python
# ideally, about 200 cells per core
self.ntasks = max(1, round(cell_count / goal_cells_per_core + 0.5))
# In a pinch, about 2000 cells per core
self.min_tasks = max(1, round(cell_count / max_cells_per_core + 0.5))
```

The config options `goal_cells_per_core` and `max_cells_per_core` in the
`[seaice]` seciton can be used to control how resources scale with the size of 
the planar mesh.  By default,  the number of MPI tasks tries to apportion 200 
cells to each core, but it will allow as many as 2000. 

(dev-seaice-framework-config)=

## Model config options and streams

The module `polaris.seaice.config` contains yaml files for setting model
config options and configuring streams.  These include things like setting
output to double precision, adjusting sea surface height in ice-shelf cavities, 
and outputting variables related to frazil ice and land-ice fluxes.

(dev-seaice-framework-vertical)=

## Vertical coordinate

The `polaris.seaice.vertical` module provides support for computing general
vertical coordinates for MPAS-Seaice test cases.

The `polaris.seaice.vertical.grid_1d` module provides 1D vertical
coordinates.  To create 1D vertical grids, test cases should call
{py:func}`polaris.seaice.vertical.grid_1d.generate_1d_grid()` with the desired
config options set in the `vertical_grid` section (as described in
the User's Guide under {ref}`seaice-vertical`).

The z-level and z-star coordinates are also controlled by config options from
this section of the config file. The function
{py:func}`polaris.seaice.vertical.init_vertical_coord()` can be used to compute
`minLevelCell`, `maxLevelCell`, `cellMask`, `layerThickness`, `zMid`,
and `restingThickness` variables for {ref}`seaice-z-level` and
{ref}`seaice-z-star` coordinates using the `ssh` and `bottomDepth` as well
as config options from `vertical_grid`.

(dev-seaice-rpe)=

## reference (resting) potential energy (RPE)

The module {py:mod}`polaris.seaice.rpe` is used to compute the reference (or 
resting) potential energy for an entire model domain.  The RPE as given in
[Petersen et al. 2015](https://doi.org/10.1016/j.ocemod.2014.12.004) is:

$$
RPE = g \int_\Omega z \rho^*\left(z\right) dV
$$

where $\Omega$ is the domain and $\rho^*\left(z\right)$ is the sorted
density, which is horizontally constant and increases with depth.

The {py:func}`polaris.seaice.rpe.compute_rpe()` is used to compute the RPE as
a function of time in a series of one or more output files.  The RPE is stored
in `rpe.csv` and also returned as a numpy array for plotting and analysis.
