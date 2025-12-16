import itertools


class CombinationGenerator:
    """
    Generates string combinations from registered variables in a nested-loop fashion.

    The order of combinations follows the order of variable registration.
    For example, if you register 'A' then 'B', it will iterate through
    all 'B' values for the first 'A' value, then all 'B' values for
    the second 'A' value, and so on.
    """

    def __init__(self):
        # In Python 3.7+, dicts preserve insertion order, which is
        # crucial for maintaining the 'A' then 'B' then 'C' logic.
        self.variables = {}
        self.iterator = None

    def register(self, var_name, values):
        """
        Registers a variable name and its list of possible string values.

        Args:
            var_name (str): The name of the variable (e.g., "A").
            values (list[str]): A non-empty list of string values for this variable.
        """
        if not values or not isinstance(values, (list, tuple)):
            raise ValueError(f"Values for '{var_name}' must be a non-empty list or tuple.")

        if self.iterator:
            print(f"Warning: Registering '{var_name}' after iteration started. "
                  "Call reset() to use new variables.")
            # Or, we could just reset automatically:
            # self.reset()

        self.variables[var_name] = values
        # Invalidate the old iterator if a new variable is registered
        self.iterator = None

    def _initialize_iterator(self):
        """Internal helper to set up the itertools.product iterator."""
        if not self.variables:
            print("Warning: No variables registered.")
            self.iterator = iter([])  # Empty iterator
        else:
            # Get all the value lists in the order they were registered
            value_lists = self.variables.values()

            # itertools.product creates the Cartesian product (the nested loop)
            # The '*' (splat) operator unpacks the list of lists
            # into separate arguments for the product function.
            self.iterator = itertools.product(*value_lists)

    def getNext(self):
        """
        Returns the next combination string, or None if all
        combinations have been generated.

        The string is formatted as '<val_A>_<val_B>_...'.
        """
        # Initialize the iterator on the first call
        if self.iterator is None:
            self._initialize_iterator()

        try:
            # Get the next tuple, e.g., ('a1', 'b1', 'c2')
            combination_tuple = next(self.iterator)

            # Join the tuple elements with an underscore
            return "_".join(combination_tuple)
        except StopIteration:
            # We've reached the end
            return None

    def reset(self):
        """Resets the generator to start from the beginning."""
        self.iterator = None
        print("Iterator reset. Call getNext() to start from the beginning.")