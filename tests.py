
"""
Author : Guillaume FOUCAUD
Date : 31/03/2024 [d/m/y]


"""

class RiemannProblem:
	"""
	# https://fr.wikipedia.org/wiki/Probl%C3%A8me_de_Riemann
	# https://en.wikipedia.org/wiki/Riemann_solver

	Problème de Riemann : 
	"""
	def __init__(self, ul, ur, x0 = 0):
		self.ul = ul 
		self.ur = ur 
		self.x0 = x0
		self.sigma = None

	def getShockSpeed(self, f):
		"""
		Relations de Hunkine-Hugoniot
		"""
		sigma = (f(self.ur) - f(self.ul)) / (self.ur - self.ul)
		return sigma

	def initSigma(self, f):
		"""
		Initialisation de la valeur de Sigma
		"""
		self.sigma = self.getShockSpeed(f)
		return self

	def indicator(self, x):
		"""
		Condition initiale
		"""
		return (x < self.x0) * self.ul + (x > self.x0) * self.ur

	def isShock(self, fprime):
		"""
		Détection de chocs
		"""
		return (self.ul > self.ur) and ( fprime(self.ul) > self.sigma ) and ( fprime(self.ur) < self.sigma )

	def shockCurve(self, t, t0):
		"""
		Courbe (ligne) du choc
		"""
		return self.sigma * (t - t0) + self.x0

	def solve(self, f, fprime):
		"""
		Calcul de la solution u(t,x)
		Retourne la solution u
		"""
		isShock = self.isShock(fprime)


		# choc
		if isShock:
			def u(t, x):
				ratio = (x - self.x0) / t
				return (ratio < self.sigma) * self.ul + (ratio > self.sigma) * self.ur
			return u

		# détente
		def u(t, x):
			ratio = (x - self.x0) / t
			return (ratio < fprime(self.ul)) * self.ul + 0 + (ratio > fprime(self.ur)) * self.ur
		return u

	def __str__(self):
		return f"RiemannProblem(\n\t(ul, ur) = ({self.ul}, {self.ur}),\n\tx0 = {self.x0},\n\tsigma = {self.sigma}\n)"
	
# ================================================================================================================
#   imports
# ================================================================================================================

import numpy as np

# custom libs
import pde_solver_lib as psl

# ================================================================================================================
#   bounds
# ================================================================================================================

bounds_debug = psl.Bounds(psl.Interval(1, 3), psl.Interval(1, 7))

bounds_small = psl.Bounds(psl.Interval(0, 1), psl.Interval(0, 1))
bounds_medium = psl.Bounds(psl.Interval(0, 1), psl.Interval(-2, 5))
bounds_large = psl.Bounds(psl.Interval(0, 1), psl.Interval(-5, 50))

# ================================================================================================================
#   functions (flux)
# ================================================================================================================



def getLinearFlux(scalar):

    def identity_scalar(x):
        return x * scalar
    
    def constant_scalar(x):
        return np.ones_like(x) * scalar
    
    return psl.Function(func = identity_scalar, name = f"linear{int(scalar)}", data = { "prime" : constant_scalar, "isLinear" : True })

# f(u) = u
flux_identity = getLinearFlux(1.0)
flux_fiveHalfIdentity = getLinearFlux(2.5)

def square_half(x):
    """Returns the square of a number."""
    return x * x * 0.5

# f(u) = u^2/2
flux_square_half = psl.Function(func = square_half, name = "square_half", data = { "prime" : flux_identity, "isLinear" : False, "isQuadratic" : True })

# ================================================================================================================
#   functions (initial)
# ================================================================================================================

initial_ind23 = psl.Function.indicator(psl.Interval(2, 3))

initial_ind01 = psl.Function.indicator(psl.Interval(0, 1))
initial_step10_0 = psl.Function.changingStep(1, 0, 0, data = {
	"canBeRiemannProblem": True,
	"ul": 1,
	"ur": 0,
	"x0": 0
})
initial_sawTooth01 = psl.Function.sawTooth(0, 1)
initial_triangle012 = psl.Function.triangle(0, 1, 2)

def custom_func(x):
    return np.exp( - x * x) * np.sin(x * np.pi)

initial_custom = psl.Function(custom_func, "wavelet")

# ================================================================================================================
#   functions (exact)
# ================================================================================================================
# naming: exact_[initial]_[flux]


def getExactSolution(initial, flux):

    if flux.data.get("isLinear"):

        def exactSolution(t, x):
            scalar = flux(1)
            return initial(x - scalar * t)
        
        return psl.Function(func = exactSolution, name = f"exact_{initial.name}_{flux.name}")
    
    print(initial.data, flux.data)
    if initial.data.get("canBeRiemannProblem") and flux.data.get("isQuadratic"):
		
        
              
        ul = initial.data.get("ul")
        ur = initial.data.get("ur")
        x0 = initial.data.get("x0")

        rp = RiemannProblem(ul, ur, x0).initSigma(flux)
        exactSolution = rp.solve(flux, flux.data.get("prime"))
		
        return psl.Function(func = exactSolution, name = f"exact_{initial.name}_{flux.name}")
		

    return None

# debug
exact_ind23_identity = getExactSolution(initial_ind23, flux_identity)
exact_custom_identity = getExactSolution(initial_custom, flux_identity)

# linear, f(u) = u
exact_ind01_identity = getExactSolution(initial_ind01, flux_identity)
exact_step10_0_identity = getExactSolution(initial_step10_0, flux_identity)
exact_sawTooth01_identity = getExactSolution(initial_sawTooth01, flux_identity)
exact_triangle012_identity = getExactSolution(initial_triangle012, flux_identity)

# linear, f(u) = 5u/2
exact_ind01_fiveHalfIdentity = getExactSolution(initial_ind01, flux_fiveHalfIdentity)
exact_step10_0_fiveHalfIdentity = getExactSolution(initial_step10_0, flux_fiveHalfIdentity)
exact_sawTooth01_fiveHalfIdentity = getExactSolution(initial_sawTooth01, flux_fiveHalfIdentity)
exact_triangle012_fiveHalfIdentity = getExactSolution(initial_triangle012, flux_fiveHalfIdentity)

# quadratic, f(u) = u^2/2
exact_step10_0_square_half = getExactSolution(initial_step10_0, flux_square_half)

# ================================================================================================================
#   equations
# ================================================================================================================

# debug
he_debug = psl.HyperbolicEquation(
    bounds = bounds_debug,
    flux = flux_identity,
    initial = initial_ind23,
).setExact(exact_ind23_identity)

he_debug2 = psl.HyperbolicEquation(
    bounds = bounds_medium,
    flux = flux_identity,
    initial = initial_custom,
).setExact(exact_custom_identity)

# linear: scalar = 1 --------------------------------------------------
he_linear_ind01 = psl.HyperbolicEquation(
    bounds = bounds_medium,
    flux = flux_identity,
    initial = initial_ind01,
).setExact(exact_ind01_identity)

he_linear_step10_0 = psl.HyperbolicEquation(
    bounds = bounds_medium,
    flux = flux_identity,
    initial = initial_step10_0,
).setExact(exact_step10_0_identity)

he_linear_sawTooth01 = psl.HyperbolicEquation(
    bounds = bounds_medium,
    flux = flux_identity,
    initial = initial_sawTooth01,
).setExact(exact_sawTooth01_identity)

he_linear_triangle012 = psl.HyperbolicEquation(
    bounds = bounds_medium,
    flux = flux_identity,
    initial = initial_triangle012,
).setExact(exact_triangle012_identity)

# linear: scalar = 2.5 --------------------------------------------------
he_linear5_2_ind01 = psl.HyperbolicEquation(
    bounds = bounds_medium,
    flux = flux_fiveHalfIdentity,
    initial = initial_ind01,
).setExact(exact_ind01_fiveHalfIdentity)

he_linear5_2_step10_0 = psl.HyperbolicEquation(
    bounds = bounds_medium,
    flux = flux_fiveHalfIdentity,
    initial = initial_step10_0,
).setExact(exact_step10_0_fiveHalfIdentity)

he_linear5_2_sawTooth01 = psl.HyperbolicEquation(
    bounds = bounds_medium,
    flux = flux_fiveHalfIdentity,
    initial = initial_sawTooth01,
).setExact(exact_sawTooth01_fiveHalfIdentity)

he_linear5_2_triangle012 = psl.HyperbolicEquation(
    bounds = bounds_medium,
    flux = flux_fiveHalfIdentity,
    initial = initial_triangle012,
).setExact(exact_triangle012_fiveHalfIdentity)

# non-linear: quadratic --------------------------------------------------

he_quadratic_ind01 = psl.HyperbolicEquation(
    bounds = bounds_medium,
    flux = flux_square_half,
    initial = initial_ind01,
)

he_quadratic_step10_0 = psl.HyperbolicEquation(
    bounds = bounds_medium,
    flux = flux_square_half,
    initial = initial_step10_0,
).setExact(exact_step10_0_square_half)

he_quadratic_sawTooth01 = psl.HyperbolicEquation(
    bounds = bounds_medium,
    flux = flux_square_half,
    initial = initial_sawTooth01,
)

he_quadratic_triangle012 = psl.HyperbolicEquation(
    bounds = bounds_medium,
    flux = flux_square_half,
    initial = initial_triangle012,
)


# ================================================================================================================
#   exports
# ================================================================================================================

TEST_CASES = {
    # debug
    "debug" : he_debug,
    "debug2" : he_debug2,
    # linear: 1
    "linear_ind01" : he_linear_ind01,
    "linear_step10_0" : he_linear_step10_0,
    "linear_sawTooth01" : he_linear_sawTooth01,
    "linear_triangle012" : he_linear_triangle012,
    # linear: 5/2
    "linear5_2_ind01" : he_linear5_2_ind01,
    "linear5_2_step10_0" : he_linear5_2_step10_0,
    "linear5_2_sawTooth01" : he_linear5_2_sawTooth01,
    "linear5_2_triangle012" : he_linear5_2_triangle012,
    #
    "quadratic_ind01" : he_quadratic_ind01,
    "quadratic_step10_0" : he_quadratic_step10_0,
    "quadratic_sawTooth01" : he_quadratic_sawTooth01,
    "quadratic_triangle012" : he_quadratic_triangle012,
}