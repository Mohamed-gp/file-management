def print_module_name():
    """
    This function prints the name of the current module.
    """
    print(__name__)  # Prints the name of the module where this function is defined

print_module_name()  # Prints the name of the module where this function is defined
print(__name__)  # Prints '__main__' since it is the name of the module being executed directly
