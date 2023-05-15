import os

from polaris import TestCase


class StandardPhysics(TestCase):
    """
    The standard physics test case for the "single column" test group creates
    the mesh and initial condition, then performs a short forward run on 4
    cores.

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
        # self.add_step(
        #   InitialState(test_case=self))
