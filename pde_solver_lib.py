
"""
Author : Guillaume FOUCAUD
Date : 31/03/2024 [d/m/y]

Standardized docstrings generated using GPT4 (verified by me afterward)
"""

# ================================================================================================================
#   imports
# ================================================================================================================

import numpy as np

# ================================================================================================================
#   Domains definition
# ================================================================================================================

class Interval:
    """
    Represents a real interval between two endpoints: [minimum, maximum].
    
    Attributes:
        min (float|int): The minimum value of the interval.
        max (float|int): The maximum value of the interval.
    """
    
    def __init__(self, minimum, maximum) -> None:
        """
        Initializes a new instance of the Interval class with specified minimum and maximum values.
        
        Parameters:
            minimum (float|int): The minimum value of the interval.
            maximum (float|int): The maximum value of the interval.
            
        Raises:
            ValueError: If `maximum` is less than `minimum`.
        """
        if maximum < minimum:
            raise ValueError("maximum should be greater than or equal to minimum")
        self.min = minimum
        self.max = maximum

    def isIn(self, x) -> bool:
        """
        Determines if a given value falls within the interval.
        
        Parameters:
            x (float|int|array-like): The value to check.
            
        Returns:
            bool: True if `x` is within the interval (inclusive of boundaries); False otherwise.
        """

        x = np.array(x)
        return (self.min <= x) & (x <= self.max)
    
    def getLength(self) -> float:
        """
        Calculates the length of the interval.

        This method computes the difference between the maximum and minimum values of the interval,
        effectively determining its length. This can be useful for understanding the size of the interval
        or for calculations that require the interval's magnitude.

        Returns:
            float: The length of the interval, calculated as the difference between the maximum and minimum values.
        """
        return self.max - self.min


    def __str__(self) -> str:
        """
        Returns a string representation of the interval.
        
        Returns:
            str: The string representation of the interval in the format "[min,max]".
        """
        return f"[{self.min},{self.max}]"
    
class Bounds:
    """
    Represents a 2D boundary defined by two intervals: one for the x-coordinate and one for the t-coordinate.
    Essentially, it defines a rectangular region in a 2D space, described by [a,b]x[c,d], where
    [a,b] is the interval for the x-coordinate, and [c,d] is the interval for the t-coordinate.
    
    Attributes:
        t (Interval): The interval for the t-coordinate.
        x (Interval): The interval for the x-coordinate.
    """
    
    def __init__(self, tInterval, xInterval) -> None:
        """
        Initializes a new instance of the Bounds class with specified intervals for t and x coordinates.
        
        Parameters:
            tInterval (Interval): The interval object for the t-coordinate.
            xInterval (Interval): The interval object for the x-coordinate.
        """
        self.t = tInterval
        self.x = xInterval

    def isIn(self, x, t) -> bool:
        """
        Determines if a given point (t, x) falls within the defined bounds.
        
        Parameters:
            t (float|int|array-like): The t-coordinate of the point to check.
            x (float|int|array-like): The x-coordinate of the point to check.
            
        Returns:
            bool: True if the point (t, x) is within the bounds; False otherwise.
        """

        x = np.array(x)
        return (self.x.isIn(x)) & (self.t.isIn(t))
    

    def __str__(self) -> str:
        """
        Returns a string representation of the Bounds instance, showcasing the intervals for x and t coordinates.
        
        Returns:
            str: The string representation of the bounds in the format "[a,b]x[c,d]".
        """
        return f"{self.t}x{self.x}"
    
# ================================================================================================================
#   Functions
# ================================================================================================================

class Function:
    """
    Represents a mathematical or computational function. This class allows the encapsulation of a function alongside
    its metadata such as its name and any additional data related to the function.
    
    Attributes:
        func (callable): The function to be encapsulated. This should be a callable that accepts at least one argument.
        name (str): The name of the function, used for identification purposes.
        data (dict, optional): A dictionary of additional data related to the function. Defaults to an empty dict.
    """
    
    def __init__(self, func, name, data = None) -> None:
        """
        Initializes a new instance of the Function class.
        
        Parameters:
            func (callable): The actual function to encapsulate.
            name (str): The name of the function.
            data (dict, optional): Any additional data as a dictionary. Defaults to None.
        """
        if data is None:
            data = {}
        self.func = func
        self.name = name
        self.data = data

    def __call__(self, *args, **kwargs):
        """
        Allows the instance to be called as a function. This method directly passes all arguments to the encapsulated
        function and returns its result.
        
        Returns:
            The result of the encapsulated function.
        """
        return self.func(*args, **kwargs)

    def __str__(self) -> str:
        """
        Returns a string representation of the Function instance, primarily showing the function's name.
        
        Returns:
            str: The string representation of the function in the format "Function:<name>(.)".
        """
        return f"Function:{self.name}(.)"

    def help(self) -> str:
        """
        Provides a help string for the encapsulated function, attempting to retrieve its docstring if available.
        
        Returns:
            str: The docstring of the encapsulated function, or a message indicating it's unavailable.
        """
        if self.func.__doc__:
            return self.func.__doc__
        else:
            return f"No documentation available for Function:{self.name}"

    def addData(self, key, value) -> None:
        """
        Adds or updates a key-value pair in the function's additional data dictionary.
        
        Parameters:
            key (str): The key under which to store the value.
            value: The value to be stored.
        """
        self.data[key] = value

    def getData(self, key, default = None):
        """
        Retrieves a value from the function's additional data dictionary based on a given key.
        
        Parameters:
            key (str): The key corresponding to the value to be retrieved.
            default (optional): The default value to return if the key is not found. Defaults to None.
            
        Returns:
            The value associated with the key if it exists, else `default`.
        """
        return self.data.get(key, default)
    

    @classmethod
    def indicator(cls, interval, name = "indicator", data = None):
        """
        Creates an indicator function for a given interval.

        Parameters:
            interval (Interval): An Interval representing the interval [min, max].
            name (str, optional): The name of the function. Defaults to "indicator".
            data (dict, optional): Additional data related to the function. Defaults to None.

        Returns:
            Function: An instance of Function that acts as an indicator function for the given interval.
        """
        def indicator_func(x):
            return interval.isIn(x).astype(float)

        return cls(indicator_func, name, data)
    
    # ascending step
    # descending step
    @classmethod
    def changingStep(cls, ul, ur, x0, name = "changingStep", data = None):
        """
        Creates a step function that changes from 'ul' to 'ur' at 'x0'.

        Parameters:
            ul (float|int): The value of the function to the left of 'x0'.
            ur (float|int): The value of the function to the right of 'x0'.
            x0 (float|int): The point at which the function changes value.
            name (str, optional): The name of the function. Defaults to "changingStep".
            data (dict, optional): Additional data related to the function. Defaults to None.

        Returns:
            Function: An instance of Function that acts as a changing step function.
        """
        def step_func(x):
            return np.where(x < x0, ul, ur)
        
        return cls(step_func, name, data)

    
    @classmethod
    def sawTooth(cls, start, end, name = "sawTooth", data = None):
        """
        Creates a sawtooth function that rises from 0 at 'start' to 1 at 'end', then drops back to 0.

        Parameters:
            start (float|int): The starting point of the sawtooth.
            end (float|int): The ending point of the sawtooth.
            name (str, optional): The name of the function. Defaults to "sawTooth".
            data (dict, optional): Additional data related to the function. Defaults to None.

        Returns:
            Function: An instance of Function that acts as a sawtooth wave function.
        """
        def sawtooth_func(x):
            return np.where((x >= start) & (x <= end), (x - start) / (end - start), 0)
        
        return cls(sawtooth_func, name, data)

    
    @classmethod
    def triangle(cls, start, middle, end, name="triangle", data=None):
        """
        Creates a triangular function that rises from 0 at 'start' to 1 at 'middle', then falls back to 0 by 'end'.

        Parameters:
            start (float|int): The starting point of the triangle.
            middle (float|int): The peak point of the triangle where the value is 1.
            end (float|int): The ending point of the triangle.
            name (str, optional): The name of the function. Defaults to "triangle".
            data (dict, optional): Additional data related to the function. Defaults to None.

        Returns:
            Function: An instance of Function that acts as a triangular wave function.
        """
        def triangle_func(x):
            return np.where((x >= start) & (x <= middle), (x - start) / (middle - start),
                    np.where((x > middle) & (x <= end), (end - x) / (end - middle), 0))
        
        return cls(triangle_func, name, data)



# ================================================================================================================
#   Equations and Models
# ================================================================================================================
    
class HyperbolicEquation:
    """
    Represents a hyperbolic partial differential equation (PDE) of the form:
    du/dt + df(u)/dx = 0, for all (t,x) in a specified bounds, with an initial condition u(t0, x) = u0(x).
    
    This class is designed to encapsulate the components necessary to define and work with such an equation,
    including the spatial and temporal bounds, the flux function 'f', and the initial condition 'u0'.
    
    The PDE is defined over a domain with u: (R+, R) --> R and the flux function f: R --> R, allowing for the
    representation and manipulation of equations with real-valued solutions and inputs.

    Attributes:
        bounds (Bounds): The temporal and spatial bounds for the equation, specifying the domain as a product of two intervals.
        flux (Function): The flux function 'f' in the equation, encapsulated as a Function instance. This function should take a single real argument and return a real value.
        initial (Function): The initial condition 'u0', provided as a Function instance. This function represents the initial state of the system at time t0 over the spatial domain and should accept a single real argument (spatial coordinate) and return a real value.
    """
    
    def __init__(self, bounds, flux, initial) -> None:
        """
        Initializes a new instance of the HyperbolicEquation class with specified bounds, flux function, and initial condition.
        
        Parameters:
            bounds (Bounds): An instance of the Bounds class defining the spatial and temporal boundaries of the equation.
            flux (Function): An instance of the Function class representing the flux function 'f' in the PDE.
            initial (Function): An instance of the Function class representing the initial condition 'u0(x)' of the equation.
        """
        self.bounds = bounds
        self.flux = flux
        self.initial = initial
        self.exact = None

    def setExact(self, exact):
        """
        Assigns an exact solution to the hyperbolic partial differential equation, if known.

        This method allows for the specification of an analytical or exact solution to the hyperbolic PDE represented
        by the instance of HyperbolicEquation. Setting an exact solution is optional but can be useful for comparison
        with numerical solutions, for validation, or for educational purposes. The exact solution should be provided
        as an instance of the Function class, encapsulating the solution's functional form.

        Parameters:
            exact (Function): An instance of the Function class representing the exact solution of the PDE.
            
        Returns:
            self: Returns the instance itself to allow for method chaining.
        """
        self.exact = exact
        return self


    def __str__(self) -> str:
        """
        Returns a string representation of the HyperbolicEquation instance, summarizing the PDE, its flux function, and initial condition.

        This representation includes the general form of the hyperbolic partial differential equation (PDE), 
        du/dt + df(u)/dx = 0, alongside the specific flux function 'f' and the initial condition 'u0(x)' as provided 
        upon instantiation. The bounds within which the equation is defined are also included, offering a concise overview 
        of the equation's definition domain and its key components.

        Returns:
            str: A string summarizing the hyperbolic PDE, its flux function, spatial and temporal bounds, and initial condition.
        """
        return f"HyperbolicEquation:\n\tdu/dt + df(u)/dx = 0, where f = {self.flux}, (t,x) in {self.bounds}\n\tu(t0, x) = u0(x), where u0 = {self.initial}"
    


class Model:
    """
    Represents a computational model for numerical simulations, which relies on discretizing the spatial and temporal domains.

    This class is designed to manage the meshing parameters for numerical simulations, including the number of spatial steps (`nx`), 
    the number of time steps (`nt`), and the Courant-Friedrichs-Lewy (CFL) condition number which is crucial for the stability of the simulation.

    Attributes:
        nt (int): The number of time steps in the simulation.
        nx (int): The number of spatial steps in the simulation.
        cfl (float): The Courant-Friedrichs-Lewy condition number for the simulation.
    """

    def __init__(self, nx, nt, cfl) -> None:
        """
        Initializes a new Model instance with specified mesh parameters.

        Parameters:
            nx (int): The number of spatial steps.
            nt (int): The number of time steps.
            cfl (float): The CFL condition number.
        """
        self.nt = nt
        self.nx = nx
        self.cfl = cfl

    def setSpaceStep(self, nx):
        """
        Sets the number of spatial steps in the simulation.

        Parameters:
            nx (int): The new number of spatial steps.

        Returns:
            self: Enables method chaining.
        """
        self.nx = nx
        return self
    
    def setTimeStep(self, nt):
        """
        Sets the number of time steps in the simulation.

        Parameters:
            nt (int): The new number of time steps.

        Returns:
            self: Enables method chaining.
        """
        self.nt = nt
        return self
    
    def setCFL(self, cfl):
        """
        Sets the Courant-Friedrichs-Lewy condition number for the simulation.

        Parameters:
            cfl (float): The new CFL condition number.

        Returns:
            self: Enables method chaining.
        """
        self.cfl = cfl
        return self
    
    def multiplySpaceStep(self, scalar):
        """
        Multiplies the current number of spatial steps by a scalar value. This can be used to refine or coarsen the spatial mesh.

        Parameters:
            scalar (float): The factor by which to multiply the current number of spatial steps.

        Returns:
            self: Enables method chaining.
        """
        self.nx *= scalar
        return self
