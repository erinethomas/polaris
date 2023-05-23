(dev-seaice-single-column)=

# single_column

The `single_column` test group
({py:class}`polaris.seaice.tests.single_column.SingleColumn`)
implements test cases that exercise vertical dynamics only. There is currently
one test case that exercises CVMix. Here, we describe the shared framework for
this test group and the CVMix test case.

(dev-seaice-single-column-framework)=

## framework

The shared config options for the `single_column` test group
are described in {ref}`seaice-single-column` in the User's Guide.

Additionally, the test group has a shared `forward.yaml` file with
a few common model config options related to run duration and horizontal
diffusion and cvmix, as well as defining `mesh`, `input`, `restart`, `output`,
`KPP_testing` and `mixedLayerDepthsOutput` streams.

### forward

The class {py:class}`polaris.seaice.tests.single_column.forward.Forward`
defines a step for running MPAS-Seaice from the initial condition produced in
the `initial_state` step. The seaice model is run.

### viz

The class {py:class}`polaris.seaice.tests.single_column.viz.Viz`
produces figures comparing the initial and final profiles of temperature and
salinity.

## standard_physics_test
The {py:class}`polaris.ocean.tests.baroclinic_channel.decomp_test.DecompTest`

## exact_restart_test

