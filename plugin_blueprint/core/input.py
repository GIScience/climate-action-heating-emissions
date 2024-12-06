from pydantic import BaseModel


class ComputeInput(BaseModel):
    # This class defines all the input parameters of your plugin.
    # It uses pydantic to announce the parameters and validate them from the user realm (i.e. the front-end).
    # These parameters will later be available in the computation method.
    # Make sure you document them well using pydantic Fields.
    # The title, description and example parameters as well as marking them as optional (if applicable) are required!
    # If you mark a field as optional, be sure to set the default value as well.
    # Additional constraints can be set.
    pass
