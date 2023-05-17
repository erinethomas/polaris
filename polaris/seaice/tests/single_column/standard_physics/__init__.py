import os

from polaris import TestCase
from polaris.seaice.tests.single_column.standard_physics.forward import Forward
from polaris.validate import compare_variables


class StandardPhysics(TestCase):
    """
    The standard physics test case for the "single column" test group creates
    the mesh and initial condition, then performs a short forward run.

    Attributes
    ----------
    """

    def __init__(self, test_group):
        """
        Create the test case

        Parameters
        ----------
        test_group : polaris.seaice.tests.single_column.SingleColumn
            The test group that this test case belongs to

        """
        name = 'standard_physics'
        super().__init__(test_group=test_group, name=name)
        self.add_step(Forward(test_case=self))

    def validate(self):
        """
        Compare six output variables in the ``forward`` step
        with a baseline if one was provided.
        """
        super().validate()

        variables = ['iceAreaCell', 'iceVolumeCell', 'snowVolumeCell',
                     'surfaceTemperatureCell', 'shortwaveDown', 'longwaveDown']
        compare_variables(test_case=self, variables=variables,
                          filename1='forward/output/output.2001.nc')
