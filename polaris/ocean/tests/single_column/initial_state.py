import xarray as xr
from mpas_tools.io import write_netcdf
from mpas_tools.mesh.conversion import convert, cull
from mpas_tools.planar_hex import make_planar_hex_mesh

from polaris import Step
from polaris.mesh.planar import compute_planar_hex_nx_ny
from polaris.ocean.vertical import init_vertical_coord


class InitialState(Step):
    """
    A step for creating a mesh and initial condition for single column
    test cases
    Attributes
    ----------
    resolution : float
        The resolution of the test case in km
    """
    def __init__(self, test_case, resolution):
        """
        Create the step
        Parameters
        ----------
        test_case : polaris.TestCase
            The test case this step belongs to
        resolution : float
            The resolution of the test case in km
        """
        super().__init__(test_case=test_case, name='initial_state')
        self.resolution = resolution
        for file in ['base_mesh.nc', 'culled_mesh.nc', 'culled_graph.info',
                     'initial_state.nc']:
            self.add_output_file(file)

    def run(self):
        """
        Run this step of the test case
        """
        logger = self.logger
        config = self.config
        section = config['single_column']
        resolution = self.resolution
        lx = section.getfloat('lx')
        ly = section.getfloat('ly')
        nx, ny = compute_planar_hex_nx_ny(lx, ly, resolution)
        dc = 1e3 * resolution
        ds_mesh = make_planar_hex_mesh(nx=nx, ny=ny, dc=dc,
                                       nonperiodic_x=False,
                                       nonperiodic_y=False)
        write_netcdf(ds_mesh, 'base_mesh.nc')
        ds_mesh = cull(ds_mesh, logger=logger)
        ds_mesh = convert(ds_mesh, graphInfoFileName='culled_graph.info',
                          logger=logger)
        write_netcdf(ds_mesh, 'culled_mesh.nc')

        ds = ds_mesh.copy()
        x_cell = ds.xCell
        bottom_depth = config.getfloat('vertical_grid', 'bottom_depth')
        ds['bottomDepth'] = bottom_depth * xr.ones_like(x_cell)
        ds['ssh'] = xr.zeros_like(x_cell)
        init_vertical_coord(config, ds)

        section = config['single_column']
        surface_temperature = section.getfloat(
            'surface_temperature')
        temperature_gradient_mixed_layer = section.getfloat(
            'temperature_gradient_mixed_layer')
        temperature_difference_across_mixed_layer = section.getfloat(
            'temperature_difference_across_mixed_layer')
        temperature_gradient_interior = section.getfloat(
            'temperature_gradient_interior')
        mixed_layer_depth_temperature = section.getfloat(
            'mixed_layer_depth_temperature')
        surface_salinity = section.getfloat(
            'surface_salinity')
        salinity_gradient_mixed_layer = section.getfloat(
            'salinity_gradient_mixed_layer')
        salinity_difference_across_mixed_layer = section.getfloat(
            'salinity_difference_across_mixed_layer')
        salinity_gradient_interior = section.getfloat(
            'salinity_gradient_interior')
        mixed_layer_depth_salinity = section.getfloat(
            'mixed_layer_depth_salinity')
        coriolis_parameter = section.getfloat(
            'coriolis_parameter')

        z_mid = ds.refZMid

        temperature_at_mixed_layer_depth = (
            surface_temperature + temperature_difference_across_mixed_layer)
        temperature_vert = xr.where(
            z_mid > -mixed_layer_depth_temperature,
            surface_temperature + temperature_gradient_mixed_layer * z_mid,
            temperature_at_mixed_layer_depth +
            temperature_gradient_interior *
            (z_mid + mixed_layer_depth_temperature))
        temperature_vert[0] = surface_temperature
        temperature, _ = xr.broadcast(temperature_vert, x_cell)
        temperature = temperature.transpose('nCells', 'nVertLevels')
        temperature = temperature.expand_dims(dim='Time', axis=0)

        salinity_at_mixed_layer_depth = (
            surface_salinity + salinity_difference_across_mixed_layer)
        salinity_vert = xr.where(
            z_mid > -mixed_layer_depth_salinity,
            surface_salinity + salinity_gradient_mixed_layer * z_mid,
            salinity_at_mixed_layer_depth +
            salinity_gradient_interior *
            (z_mid + mixed_layer_depth_salinity))
        salinity_vert[0] = surface_salinity
        salinity, _ = xr.broadcast(salinity_vert, x_cell)
        salinity = salinity.transpose('nCells', 'nVertLevels')
        salinity = salinity.expand_dims(dim='Time', axis=0)

        normal_velocity, _ = xr.broadcast(
            xr.zeros_like(ds.xEdge), ds.refBottomDepth)
        normal_velocity = normal_velocity.transpose('nEdges', 'nVertLevels')
        normal_velocity = normal_velocity.expand_dims(dim='Time', axis=0)

        ds['temperature'] = temperature
        ds['salinity'] = salinity
        ds['normalVelocity'] = normal_velocity
        ds['fCell'] = coriolis_parameter * xr.ones_like(x_cell)
        ds['fEdge'] = coriolis_parameter * xr.ones_like(ds.xEdge)
        ds['fVertex'] = coriolis_parameter * xr.ones_like(ds.xVertex)

        ds.attrs['nx'] = nx
        ds.attrs['ny'] = ny
        ds.attrs['dc'] = dc
        write_netcdf(ds, 'initial_state.nc')
