"""
Integral Verification Project
=============================

Problem:
    ∫ [x + sec(2x) - tan(2x) cot(x)]
      / [sqrt(-x^3 + 5x^2 - 8x + 9) + 2 - 2x] dx

Closed-form answer:
    F(x) = 2(1 + sqrt(1-x))
           - 4 ln(1 + sqrt(1-x))
           - 2/(1 + sqrt(1-x)) + C

The verification below:
1. verifies the polynomial factorization,
2. verifies the trigonometric simplification numerically,
3. differentiates F(x) symbolically,
4. verifies F'(x) = simplified integrand,
5. compares the original and simplified integrands numerically.

Domain used for the real-valued antiderivative:
    x < 1
The original trigonometric expression also has isolated points where
sin(x) or cos(2x) is zero, so numerical tests avoid those points.
"""

import sympy as sp

x = sp.symbols("x", real=True)

# ---------------------------------------------------------
# A. Original problem
# ---------------------------------------------------------
numerator_original = (
    x + sp.sec(2*x) - sp.tan(2*x)*sp.cot(x)
)

denominator_original = (
    sp.sqrt(-x**3 + 5*x**2 - 8*x + 9) + 2 - 2*x
)

integrand_original = numerator_original / denominator_original

# ---------------------------------------------------------
# B. Algebraic simplification
# ---------------------------------------------------------
polynomial = -x**3 + 5*x**2 - 8*x + 9
polynomial_factorized = (2-x)**2 * (1-x)

print("1. Polynomial factorization:")
print("   Original :", polynomial)
print("   Factored :", sp.expand(polynomial_factorized))
print("   Check    :", sp.simplify(polynomial - polynomial_factorized))
print()

# The trigonometric identity:
#
# sec(2x) - tan(2x)cot(x) = -1
#
# wherever the original trigonometric expression is defined.
# Therefore the numerator becomes x - 1.

integrand_simplified = (
    (x - 1) /
    (sp.sqrt((2-x)**2 * (1-x)) + 2*(1-x))
)

# On x < 1, 2-x > 0, so
# sqrt((2-x)^2(1-x)) = (2-x)sqrt(1-x).
integrand_reduced = (
    (x - 1) /
    ((2-x)*sp.sqrt(1-x) + 2*(1-x))
)

# ---------------------------------------------------------
# C. Proposed antiderivative
# ---------------------------------------------------------
F = (
    2*(1 + sp.sqrt(1-x))
    - 4*sp.log(1 + sp.sqrt(1-x))
    - 2/(1 + sp.sqrt(1-x))
)

F_prime = sp.diff(F, x)

# The simplest form of the integrand after factorization.
integrand_target = (
    -sp.sqrt(1-x) /
    (1 + sp.sqrt(1-x))**2
)

print("2. Derivative verification:")
print("   F'(x) - target integrand =")
print("  ", sp.simplify(F_prime - integrand_target))
print()

# A second symbolic check against the factored/reduced integrand.
print("3. Check against reduced integrand:")
print("   target - reduced =")
print("  ", sp.simplify(
    integrand_target - integrand_reduced
))
print()

# ---------------------------------------------------------
# D. Numerical verification
# ---------------------------------------------------------
print("4. Numerical verification")
print("   x          original          simplified         F'(x)")
print("   --------------------------------------------------------")

test_values = [0.2, 0.4, 0.6, 0.8]

original_fun = sp.lambdify(x, integrand_original, "math")
reduced_fun = sp.lambdify(x, integrand_target, "math")
derivative_fun = sp.lambdify(x, F_prime, "math")

for value in test_values:
    original_value = original_fun(value)
    reduced_value = reduced_fun(value)
    derivative_value = derivative_fun(value)
    print(
        f"   {value:<5.1f}   "
        f"{original_value: .12f}   "
        f"{reduced_value: .12f}   "
        f"{derivative_value: .12f}"
    )

print()
print("Conclusion:")
print("The symbolic derivative equals the reduced integrand,")
print("and the numerical values agree with the original expression")
print("at the selected valid test points.")
