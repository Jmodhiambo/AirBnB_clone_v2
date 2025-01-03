def create_instance(args, classes):
    """
    Creates an instance of a class based on the provided arguments.
    Args:
        args (str): Command-line input  with the class name and parameters.
        classes (dict): Dictionary of valid class names and their constructors.
    Returns:
        str: The ID of the created instance.
    """
    arguments = args.split()  # Splitting the arguments
    class_name = arguments[0]  # Extracting the class name

    # Create an instance of the class
    instance = classes[class_name]()

    # Process parameters
    for param in arguments[1:]:
        if "=" not in param:
            continue  # Skip invalid parameters

        key, value = param.split("=", 1)

        # Process value
        if value.startswith('"') and value.endswith('"'):
            # Remove quotes and replace underscores with spaces
            value = value[1:-1].replace('_', ' ')
            value = value.replace('\\"', '"')
        elif '.' in value:
            try:
                value = float(value)
            except ValueError:
                continue  # Skip invalid float
        else:
            try:
                value = int(value)
            except ValueError:
                continue  # Skip invalid integer

        # Set the attribute on the instance
        setattr(instance, key, value)

    # Save the instance and return its ID
    instance.save()
    return instance.id
