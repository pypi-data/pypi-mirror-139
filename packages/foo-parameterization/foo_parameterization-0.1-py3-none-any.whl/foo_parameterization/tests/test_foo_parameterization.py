from foo_parameterization.foo_parameterization import FooParameterization

def test_calculate():
    """Test the ``calculate()`` method of the ``FooParameterization``
    class
    """

    foo = FooParameterization()
    result = foo.calculate(1.0)
    assert(round(result, 3)) == 4.189
