
# ==================================================================================
#						IMPORTS
# ==================================================================================

import numpy as np

# ==================================================================================
#						SCHEMES
# ==================================================================================

# -----------------------------------------------------------
#				Lax-Friedrich
# -----------------------------------------------------------

# Finite Differences
def LF_FD(u, dt, dx, flux):

	dt_dx = dt / dx

	return 0.5 * (u[2:] + u[:-2]) - 0.5 * dt_dx * (flux(u[2:]) - flux(u[:-2]))

# Finite Volumes
def LF_FV(u, dt, dx, flux):

	dt_dx = dt / dx

	fluxes = flux(u[:-1]) + flux(u[1:]) - dt_dx * (u[1:] - u[:-1])
	fluxes = 0.5 * fluxes

	return u[1:-1] - dt_dx * (fluxes[1:] - fluxes[:-1])

# -----------------------------------------------------------
#				Lax-Wendroff
# -----------------------------------------------------------

# Finite Differences
def LW_FD(u, dt, dx, flux):

	fprime = flux.data["prime"]

	dt_dx = dt / dx
	dt_dx2 = dt_dx * dt_dx

	a = fprime((u[2:] + u[:-2]) * 0.5)

	return u[1:-1] - 0.5 * dt_dx * (flux(u[2:]) - flux(u[:-2])) + 0.5 * dt_dx2 * a * (flux(u[2:]) - 2 * flux(u[1:-1]) + flux(u[:-2]))

# Finite Volumes
def LW_FV(u, dt, dx, flux): # todo : à corriger

	fprime = flux.data["prime"]

	dt_dx = dt / dx
	dt_dx2 = dt_dx * dt_dx

	a = fprime((u[1:] + u[:-1]) * 0.5)

	fluxes = flux(u[:-1]) + flux(u[1:]) - dt_dx * a * (flux(u[1:]) - flux(u[:-1]))
	fluxes = 0.5 * fluxes

	return u[1:-1] - 0.5 * dt_dx * (fluxes[1:] - fluxes[:-1]) + 0.5 * dt_dx2 * a[:-1] * (flux(u[2:]) - 2 * flux(u[1:-1]) + flux(u[:-2]))


# ==================================================================================
#						SCHEMES & METHODS
# ==================================================================================

methods = {
	"LaxFriedrich" : {
		"FiniteDifferences" : LF_FD,
		"FiniteVolumes" : LF_FV,
		#"FiniteElements" : LF_FE,
	},
	"LaxWendroff" : {
		"FiniteDifferences" : LW_FD,
		"FiniteVolumes" : LW_FV,
		#"FiniteElements" : LW_FE,
	},
}