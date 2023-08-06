from keops.formulas.VectorizedScalarOp import VectorizedScalarOp
from keops.formulas.maths.Rsqrt import Rsqrt
from keops.utils.math_functions import keops_acos


class Acos(VectorizedScalarOp):
    """the arc-cosine vectorized operation"""

    string_id = "Acos"

    ScalarOpFun = keops_acos

    @staticmethod
    def Derivative(f):
        return -Rsqrt(1 - f**2)

    # parameters for testing the operation (optional)
    test_ranges = [(-1, 1)]  # range of argument
