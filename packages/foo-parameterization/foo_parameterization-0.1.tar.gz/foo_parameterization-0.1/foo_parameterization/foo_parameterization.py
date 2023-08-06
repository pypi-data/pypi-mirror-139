"""Calculate the Foo et al. parameterization for atmospheric sea-spray
physics

Currently this module simply calculates the volume of a sphere from a
user-supplied radius.

Authors
-------
    - Matthew Bourque

Use
---

    This module can be executed via the command line as such:

        python foo_parameterization.py -r <radius>

    where <radius> is the radius of a sphere from which to calculate
    the volume.

    The user may also perform the calculate from within a python
    environment, e.g.:

        from foo_parameterization import foo_parameterization
        foo = foo_parameterization.FooParameterization()
        result = foo.calculate(1.0)

    This module may be imported by other modules/packages as such:

        import foo_parameterization

Notes
-----

    There are some potential improvements that could be made to this
    code, namely:
        - User-supplied parameters could be stored and read in via a
          file (e.g. a JSON file).  This could be handy if there are
          to be many parameters used in future calculations.  It could
          also help the user save parameters used in previous runs of
          the code.
        - The code could make use of inheritance if the Foo et al.
          parameterization is only one of several parameterizations
          that could be used for atmospheric sea-spray physics modeling
        - Currently the code simple prints the results of the
          calculation to the screen, but it would be more useful to
          store and/or plot the results perhaps.
"""

import argparse
import math


class FooParameterization:
    """The main class for calculating the Foo parameterization"""

    def calculate(self, radius, *args, **kwargs):
        """Calculate the foo parameterization.

        If the calculation is to involve more parameters someday, they
        could be accessed through args and/or kwargs.

        Parameters
        ----------
        radius : float
            The radius of the sphere

        Returns
        -------
        volume : float
            The volume of the sphere
        """

        volume = (4/3) * math.pi * radius**3

        return volume


def parse_args():
    """Parse command line arguments

    Returns
    -------
    args: argparse.Namespace object
        The parsed arguments
    """

    # Help description for arguments
    radius_help = 'The radius [float]'

    # Parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--radius', dest='radius', action='store', type=float, required=True, help=radius_help)
    args = parser.parse_args()

    return args


def test_args(args):
    """Tests the command line arguments to make sure they are valid

    Parameters
    ----------
    args: argparse.Namespace object
        The command line arguments
    """

    # Ensure that the radius is not a negative number
    assert args.radius >= 0, f'The given radius ({args.radius}) is a negative number'


if __name__ == '__main__':

    # Parse the arguments and make sure they are valid
    args = parse_args()
    test_args(args)

    # Perform calcuation
    foo = FooParameterization()
    result = foo.calculate(args.radius)

    # Print the results
    print(f'Result: {result}')
