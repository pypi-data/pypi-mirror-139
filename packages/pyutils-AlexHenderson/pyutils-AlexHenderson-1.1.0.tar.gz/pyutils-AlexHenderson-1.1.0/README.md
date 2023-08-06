# pyutils
Various Python utilities

Requires Python 3.7 or higher.  
Other requirements are listed per utility. 

## Utilities ##

- unit_manager 
- json_pint_encoder
- json_datetime_encoder
- multiple_json_encoders

### pint_utils/unit_manager ###

#### Requirements ####
    pint

#### Details ####

This is a wrapper around the Pint unit management system 
(https://pint.readthedocs.io/en/stable/). Formats a quantity label 
suitable for use on the x-axis of a chart. Units are output in their 
shortform (nm for nanometer). If a unit is not provided, the quantity 
will be treated as dimensionless.

Example for a wavelength of 280 nm:

        >>> from pyutils.pint_utils import unit_manager
        >>> ureg = unit_manager.pint.UnitRegistry()
        >>> output = unit_manager.unit_manager('wavelength', ureg.nanometer, 280)
        >>> output
        {'name': 'wavelength', 'unit': 'nm', 'label': 'wavelength (nm)', 'value': 280, 'quantity': '280 nm'}
        >>> print(output['label'])
        wavelength (nm)
        >>> print(f'peak position = {output["quantity"]}')
        peak position = 280 nm

Example for unitless absorbance:

        >>> from pyutils.pint_utils import unit_manager
        >>> ureg = unit_manager.pint.UnitRegistry()
        >>> output = unit_manager.unit_manager('absorbance')
        >>> output
        {'name': 'absorbance', 'unit': '', 'label': 'absorbance'}
        >>> print(output['label'])
        absorbance

### pint_utils/json_pint_encoder ###
#### Requirements ####
    pint

#### Details ####

JSON can only encode certain variable types as output. 
Variables from the Pint unit management system 
(https://pint.readthedocs.io/en/stable/) are not handled 
automatically. This code converts a Pint unit to a string, 
and passes that to the JSON encoding function.  

Example:
    
    >>> from pint import Quantity, Unit, UnitRegistry
    >>> from pyutils.pint_utils.json_pint_encoder import json_pint_encoder

    >>> ureg = UnitRegistry()
    >>> duration = Quantity(5.6, ureg.sec)

    >>> encoder = json_pint_encoder
    >>> jsonoutput = json.dumps(duration, cls=encoder)
    >>> print(jsonoutput)
    "5.6 second"

### datetimeutils/json_datetime_encoder ###
#### Details ####

JSON can only encode certain variable types as output. 
`datetime` variables are not handled automatically. 
This code converts a `datetime` variable into its `isoformat` string 
([ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)), and 
passes that to the JSON encoding function.  

Example:
    
    >>> import datetime
    >>> import json

    >>> from pyutils.datetime_utils.json_datetime_encoder import json_datetime_encoder

    >>> example = datetime.datetime(2000, 12, 25, 13, 23)

    >>> encoder = json_datetime_encoder
    >>> jsonoutput = json.dumps(example, cls=encoder)
    >>> print(jsonoutput)
    "2000-12-25T13:23:00"

### multiple_json_encoders ###
#### Details ####

JSON can only encode certain variable types as output.
We can supply our own encoder to convert a variable into a format the JSON engine can work with. However, there are 
occasions when we need to manage more than one type of variable. This class takes multiple encoders and dispatches each 
variable to its own encoder, before forwarding the output to the JSON engine. The order the encoders are listed as 
arguments to the multiple_encoders constructor, is the order in which they are evaluated.  

Example: 

    >>> import datetime 
    >>> import json
    
    >>> from pint import Quantity, Unit, UnitRegistry
    
    >>> from pyutils.json_utils.multiple_json_encoders import multiple_json_encoders
    >>> from pyutils.pint_utils.json_pint_encoder import json_pint_encoder
    >>> from pyutils.datetime_utils.json_datetime_encoder import json_datetime_encoder

    >>> christmas_time = datetime.datetime(2000, 12, 25, 13, 23)
    >>> ureg = UnitRegistry()
    >>> duration = Quantity(5.6, ureg.sec)

    >>> encoder = multiple_json_encoders(json_pint_encoder, json_datetime_encoder)

    >>> christmas_time_output = json.dumps(christmas_time, cls=encoder)
    >>> print(christmas_time_output)
    "2000-12-25T13:23:00"

    >>> durationoutput = json.dumps(duration, cls=encoder)
    >>> print(durationoutput)
    "5.6 second"


## Usage rights ##
Copyright (c) 2021-2022 Alex Henderson (alex.henderson@manchester.ac.uk)   
Licensed under the MIT License. See https://opensource.org/licenses/MIT      
SPDX-License-Identifier: MIT   
Version 1.1.0   
See https://github.com/AlexHenderson/pyutils/ for the most recent version  

