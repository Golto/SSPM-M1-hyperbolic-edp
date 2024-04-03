# Author:
Golto

# Date: [dd/mm/yyyy]
Creation: 31/03/2024
Published: 01/04/2024
Latest commit: 03/04/2024

# Context:
We have the hyperbolic equation $\partial_t u + \partial_t f(u) = 0$ which we are trying to solve using numerical methods given that $f$ is the flux function and $u_0$ an initial condition.
This code works exclusively for a 1-dimensional equation for now.

### Available methods:
- Lax-Friedrich: finite differences
- Lax-Friedrich: finite volumes
- Lax-Wendroff: finite differences
- Lax-Wendroff: finite volumes

