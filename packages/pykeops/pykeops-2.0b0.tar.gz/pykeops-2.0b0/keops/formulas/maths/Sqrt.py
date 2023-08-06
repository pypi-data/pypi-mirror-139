from keops.formulas.VectorizedScalarOp import VectorizedScalarOp
from keops.formulas.maths.IntInv import IntInv
from keops.formulas.maths.Rsqrt import Rsqrt
from keops.utils.math_functions import keops_sqrt


##########################
######    Sqrt       #####
##########################


class Sqrt(VectorizedScalarOp):
    """the square root vectorized operation"""

    string_id = "Sqrt"

    ScalarOpFun = keops_sqrt

    @staticmethod
    def Derivative(f):
        return IntInv(2) * Rsqrt(f)

    # parameters for testing the operation (optional)
    test_ranges = [(0, 2)]  # range of argument
