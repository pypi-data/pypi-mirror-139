"""
Contains the decorator to check dtypes of user-
inputs.

"""

# import
import copy
import typing
from tcheasy.sort_parameters import sort_parameters

# region 'helpers' -------------------------------------
def _check_decorator_declaration(to_check:dict, name:str) -> dict:
    """Checks the declared decorator for correctness 
    
    params:
    -------
    to_check : dict
        The dict containing the different
        parameter definitions for the decorated
        function.
    name : str
        The name of the declared parameter 
        types.
            Options: { 'positional', 'kwargs', 'args }
    
    returns:
    --------
    dict
        Contains info about success, error & flag state
    
    """

    # check which algorithmn to apply
    if name == "args": result = _check_arbitrary(to_check)
    else: result = _check_keyworded(to_check, name)

    return result

def _check_keyworded(to_check:dict, name:str) -> dict:
    """Checks the keyworded inputs of the @ decorator

    This function checks the inputs for the
    decorator (@).
    
    Keyworded inputs are the 'positional' and
    'kwargs' (not 'args').
    
    If all assertions are correct, it
    returns a flag to indicate to
    check the specific keyworded parameters
    of the decorated function.

    params:
    -------
    to_check : dict
        The dict containing (only) the 
        different keyworded parameter
        (= positional, **kwargs) 
        definition for the decorated 
        function.
    name : str
        The name of the declared parameter 
        types.
            Options: { 'positional', 'kwargs' }
    
    returns:
    --------
    dict
        Returns info about success, error &
        state of 'check'
    
    """

    # build fallbacks
    result = {
        'success':False,
        'error':"",
        'check':False
    }

    # empty?
    if bool(to_check):

        # dict?
        try: assert(isinstance(to_check, dict))
        except AssertionError as e:
            result.update({'error': "'{name}' needs to be a dict.".format(name = name) })
            return result
        
        # check all definitions
        for k in to_check.keys():
            """
            only the 'type' is mandatory. 

            """

            try: assert(isinstance(k, str))
            except AssertionError as e:
                result.update({'error': "The passed parameter names in '{name}' need to be strings. Not a string: '{k}'.".format(k = str(k), name = name) })
                return result

            try: assert(all(keyphrase in ["type", "default", "restriction"] for keyphrase in to_check[k]))
            except AssertionError as e:
                result.update({'error': "The passed parameter '{k}' in '{name}' contains a keyword which is not one of the following: 'type', 'default', 'restriction'.".format(k = str(k), name = name) })
                return result

            try: assert("type" in to_check[k].keys())
            except AssertionError as e:
                result.update({'error': "Missing 'type' definition in '{name}': '{k}'.".format(k = str(k), name = name) })
                return result

            # is the type correctly formulated?
            try: isinstance(5, to_check[k]['type'])
            except TypeError as e:
                
                # will only be raised by None, because we have
                # to add it as type(None) to work with isinstance()
                result.update({'error': "If you want to specify the 'type' None you have to pass it as type(None). Error in '{name}': '{k}'.".format(k = str(k), name = name) })
                return result

            # restriction correct?
            if "restriction" in to_check[k].keys():
                try: assert(isinstance(to_check[k]['restriction'], str))
                except AssertionError as e:
                    result.update({'error': "'restriction' specified in '{name}': '{k}' is not a str.".format(k = str(k), name = name) })
                    return result

                try: assert(isinstance(to_check[k]['type'], tuple) == False)
                except AssertionError as e:
                    result.update({'error': "If you want to use a 'restriction', then you are not allowed to pass multiple 'type's. Error occured in '{name}': '{k}'.".format(k = str(k), name = name) })
                    return result

            # optional aka default provided?
            if "default" in to_check[k].keys():

                # prepare type error text
                if isinstance(to_check[k]['type'], tuple): typeFormat = " | ".join([str(e.__name__) for e in to_check[k]['type']])
                else: typeFormat = str(to_check[k]['type'].__name__)

                try: assert(isinstance(to_check[k]['default'], to_check[k]['type']))
                except AssertionError as e:
                    result.update({'error': "Provided 'default' specified in '{name}': '{k}' is no '{t}'.".format(k = str(k), t = typeFormat, name = name) })
                    return result

                if "restriction" in to_check[k].keys():
                    value = to_check[k]['default']
                    try: assert(eval(to_check[k]['restriction']))
                    except AssertionError as e:
                        result.update({'error': "'default' specified in '{name}': '{k}' does not meet the 'restriction'.".format(k = str(k), name = name) })
                        return result

        # set flag kwargs to true
        result['check'] = True
    
    # did run through
    result['success'] = True

    return result

def _check_arbitrary(to_check:dict) -> dict:
    """Checks the arbitrary inputs of the @ decorator

    This function checks the inputs for the
    decorator (@).

    Arbitrary parameters are *args.

    If all assertions are correct, it
    returns a flag to indicate to
    check the specific arbitrary parameters
    of the decorated function.

    CAUTION:
    Arbitrary parameters are order sensitive!

    params:
    -------
    to_check : list
        The list containing (only) the
        different arbitrary parameters
        (= *args) for the decorated function.
    
    returns:
    --------
    dict
        Returns info about success, error &
        state of 'check'
    
    """

    # set fallbacks
    result = {
        'success':False,
        'error':"",
        'check':False
    }

    # empty?
    if bool(to_check):

        # list?
        try: assert(isinstance(to_check, list))
        except AssertionError as e:
            result.update({'error': "'args' needs to be a list." })
            return result

        # check each element
        for i, element in enumerate(to_check):

            # dict?
            try: assert(isinstance(element, dict))
            except AssertionError as e:
                result.update({'error': "Each element of 'args' needs to be a dict." })
                return result

            # check if all provided keywords are allowed
            try: assert(all([key in ['type', 'default', 'restriction'] for key in element.keys()]))
            except AssertionError as e:
                result.update({'error': "'args' at position '{i}' has a keyword, which is not one of the following: 'type', 'default', 'restriction'.".format(i = str(i)) })
                return result

            # 'type' in keys?
            try: assert("type" in element.keys())
            except AssertionError as e:
                result.update({'error': "'type' missing in element '{i}' of 'args'.".format(i = str(i)) })
                return result

            # check if None was correctly specified in 'type'
            # is the type correctly formulated?
            try: isinstance(5, element['type'])
            except TypeError as e:
                
                # will only be raised by None, because we have
                # to add it as type(None) to work with isinstance()
                result.update({'error': "If you want to specify the 'type' None you have to pass it as type(None). Error in 'args' at position: '{i}'.".format(i = str(i)) })
                return result

            if "restriction" in element.keys():
                try: assert(isinstance(element['restriction'], str))
                except AssertionError as e:
                    result.update({'error': "'restriction' in element '{i}' of 'args' is not a str.".format(i = str(i)) })
                    return result

                try: assert(isinstance(element['type'], tuple) == False) 
                except AssertionError as e:
                    result.update({'error': "If you want to use a 'restriction', then you are not allowed to pass multiple 'type's. Error occured at 'args': '{i}'.".format(i = str(i)) })
                    return result

            # default given?
            if "default" in element.keys():

                # prepare type error text
                if isinstance(element['type'], tuple): typeFormat = " | ".join([str(e.__name__) for e in element['type']])
                else: typeFormat = str(element['type'].__name__)

                try: assert(isinstance(element['default'], element['type']))
                except AssertionError as e:
                    result.update({'error': "Provided 'default' in element '{i}' of 'args' is not a(n) '{t}'.".format(i = str(i), t = typeFormat) })
                    return result

                if "restriction" in element.keys():
                    value = element['default']
                    try: assert(eval(element['restriction']))
                    except AssertionError as e:
                        result.update({'error': "The 'default' specified in element '{i}' does not meet the 'restriction'.".format(i = str(i)) })
                        return result


        # set flag to true
        result['check'] = True

    # did run throug?
    result['success'] = True

    return result

def _parse_hints(hints:dict) -> dict:
    """Parses the python type hints
    
    Parses the type hints into the correct
    format to use it as 'positional'
    parameters.
    
    params:
    -------
    hints : dict
        The hints for positional parameter.
            Format: {'param-name':type, ...}
    
    returns:
    -------
    dict
        Contains the positional definition
        according to the 'to_check' structure.

    """

    parsedHints = {}

    # for each parameter
    for key in hints:

        # create shortcut
        tmp = hints[key]
        
        # check if its a typing.Union
        if typing.get_origin(tmp) == typing.Union: parsedHints.update({key:{'type': typing.get_args(tmp)}})
        else: parsedHints.update({key:{'type':copy.deepcopy(tmp)}})

    return parsedHints

def _check_types(to_check:typing.Union[dict, list], parameters:typing.Union[dict, list], name:str) -> dict:
    """Checks the passed parameters for the decorated function

    Applies the correct algorithmn for the checks and
    returns information about the correctness, errors
    & modifications.

    params:
    -------
    to_check : dict, list
        Instructions to check against (only
        the relevant!).
    parameters : dict, list
        Contains the parameters to check (only
        the relevant from the decorated function).
    name : str
        Type of paramter group to check.
            Options: { 'positional', 'args', 'kwargs' }
    
    returns:
    --------
    dict
        Dict containing the information (see above)

    """

    # check which algorithmn to apply
    if name == "args": result = _check_decorated_arbitrary(to_check, parameters)
    else: result = _check_decorated_keyworded(to_check, parameters)

    return result

def _check_decorated_arbitrary(to_check:list, parameters:list) ->dict:
    """ Checks and modifies arbitrary parameters

    Checks and modifies the arbitrary parameters
    (for 'args') of the decorated
    function.

    NOTE:
    Used error codes
    ----------------------------------------------

        [A.0]: not expected param
        [A.1]: missing param
        [A.2]: wrong type
        [A.3]: restriction not met

    ----------------------------------------------
    
    params:
    -------
    to_check : list
        The instructions to check against (only
        relevant ones).
    parameters : list
        The parameters (arbitrary) to check (only
        relevant ones).
    
    returns:
    --------
    dict
        Contains info about success,
        error msg & modified parameters.
            Format: {
                'succes':bool,
                'error':str,
                'mod':list
                }

    """

    # create result dict
    result = {
        'success':False,
        'error':"",
        'mod':[]
    }

    # check if there are more parameters than
    # definitions
    if len(to_check) < len(parameters):
        
        # build error msg
        msg = "[A.0]: The are more arbitrary parameters than expected (found '{a}', expected '{e}').".format(a = str(len(parameters)), e = str(len(to_check)))
        result.update({'error':msg})

        return result

    # iterate through each positional argument
    for i in range(len(to_check)):
        """
        CAUTION:
        you do not have to use '.keys()'
        to iterate through a dict, but in this
        case we have a mixed type (list & dict).
        To be as distinct as possible we use
        .key() to indicate iteration through
        dictionaries.
        
        """
        
        # was the position provided?
        try: parameters[i]
        except Exception as e:

            # [A.1]: is a default value given?
            if "default" in to_check[i].keys():

                # add default
                result['mod'].append(to_check[i]['default'])

                continue

            # else return the error msg
            else: 

                # create msg
                msg = "[A.1]: The '*args' parameter at position '{i}' is missing.".format(i = str(i))

                result.update({'error':msg})

                return result

        # [A.2]: correct type?
        try: assert(isinstance(parameters[i], to_check[i]['type']))
        except AssertionError as e:
            
            # check if it is a filled tuple (--> Union)
            if isinstance(to_check[i]['type'], tuple): typeFormat = " | ".join([str(e.__name__) for e in to_check[i]['type']])
            else: typeFormat = str(to_check[i]['type'].__name__)

            # create msg
            msg = "[A.2]: The '*args' parameter at position '{i}' needs to be a(n) {t}.".format(i = str(i), t = typeFormat)

            result.update({'error':msg})

            return result

        # passed restriction?
        if "restriction" in to_check[i].keys():

            # [A.3]: check if it meets the restriction
            try:
                value = parameters[i]
                assert(eval(to_check[i]['restriction']))

            except AssertionError as e:

                # create msg
                msg = "[A.3]: The '*args' parameter at position '{i}' does not meet the restriction '{r}'. Value is currently '{v}'.".format(i = str(i), r = to_check[i]['restriction'], v = str(parameters[i]))
    
                result.update({'error':msg})

                return result

        # all passed? --> add to new
        result['mod'].append(parameters[i])

    # did all work? 
    result['success'] = True

    return result

def _check_decorated_keyworded(to_check:dict, parameters:dict) ->dict:
    """ Checks and modifies keyworded parameters

    Checks and modifies the keyworded parameters
    (for 'positional' & 'kwargs') of the decorated
    function.

    NOTE:
    Used error codes
    ----------------------------------------------

        [K.0]: not expected param
        [K.1]: missing param
        [K.2]: wrong type
        [K.3]: restriction not met
        [K.4]: unexpected error

    ----------------------------------------------
    
    params:
    -------
    to_check : dict
        The instructions to check against (only
        relevant ones).
    parameters : dict
        The parameters (keyworded) to check (only
        relevant ones).
    
    returns:
    --------
    dict
        Contains info about success,
        error msg & modified parameters.
            Format: {
                'succes':bool,
                'error':str,
                'mod':dict
                }

    """

    # create result dict
    result = {
        'success':False,
        'error':"",
        'mod':{}
    }

    #region 'checks' -----------------------------------

    # [K.0] check if all passed func keyworded params are expected
    for param in parameters:
        try: assert(param in to_check)
        except AssertionError as e: 
            
            # update error
            msg = "[K.0]: Your passed parameter '{p}' was not expected.".format(p = str(param))
            result.update({'error':msg})

            return result

    # check all types
    for param in to_check:

        # grab element for shortcut
        declaration = to_check[param]

        # check if defined
        if param not in parameters:

            # [K.1] was it mandatory aka no default provided?
            if "default" not in declaration:
                
                # update error
                msg = "[K.1]: The parameter '{p}' is missing.".format(p = str(param))
                result.update({'error':msg})

                return result

            # else update to default --> keyword:value 
            else: result['mod'].update({param:declaration['default']})

            # continue with next
            continue

        # [K.2] check type
        try: assert(isinstance(parameters[param], declaration['type']))
        except AssertionError as e:
            
            # check if it is a filled tuple (--> Union)
            if isinstance(declaration['type'], tuple): typeFormat = " | ".join([str(e.__name__) for e in declaration['type']])
            else: typeFormat = str(declaration['type'].__name__)

            # update error
            msg = "[K.2]: The parameter '{p}' needs to be a(n) {t}.".format(p = str(param), t = typeFormat)
            result.update({'error':msg})

            return result

        # [L.3] & [K.4] check restriction
        if "restriction" in declaration:
            
            try:
                value = parameters[param]
                assert(eval(declaration['restriction']))
            except AssertionError as e:

                # update error
                msg = "[K.3]: The parameter '{p}' does not meet the restriction '{r}'. Value is currently '{v}'.".format(p = str(param), r = declaration['restriction'], v = str(parameters[param]))
                result.update({'error':msg})

                return result

            except Exception as e:

                # update unexpected error
                msg = "[K.4]: There occured an unexpected error. The error is '{e}:{et}'.".format(e = str(type(e).__name__), et = str(e))
                result.update({'error':msg})

                return result
        
        # all correct? --> add original to new kwargs
        result['mod'].update({param:parameters[param]})

    # did all work?
    result['success'] = True

    return result

    #endregion

#endregion

# create decorator
def tcheasy(to_check:dict = {}, debug:bool = False) -> typing.Any:
    """Type checks user input

    This function checks all passed types by
    utilizing either a 'to_check' dict
    or the python type hintings.

    NOTE:
    Prior checking, the algorithmn sorts all
    passed parameters into their correct 
    parameter type.

    There are three different python parameter
    types considered (also used for the 'to_check'
    definition; see below).
        positional: default, keyword, positional
            These parameters are your defined 
            parameters.
                Example: def example(a, b = 2)
        args: arbitrary positional
            These parameters are basically *args.
        kwargs: arbitrary keyword
            These parameters are basically
            **kwargs.
    
    The format of 'to_check' is
    ------------------------------------------

        {
            'positional':{
                'parameter-name':{
                    'type':type,
                    'restriction':str,
                    'default':default
                }
            }
            'args':[
                {
                    'type':type,
                    'default':default,
                    'restriction':str
                },
                {...}, 
                ...
                ],
            'kwargs':{
                'parameter-name':{
                    'type':type,
                    'restriction':str,
                    'default':default
                }
            }
        }

    ------------------------------------------

    If you define one parameter type block, 
    the algorithmn assumes that your declared
    variables are all available during runtime.
    (This means, you have to either provide 
    a complete declaration or skip the 'block'.)

    In most usecases you will specify only the
    'positional' parameters (either by using
    'to_check' or the type hints).

    If a parameter is not met by your decorator
    definitions, it returns an error.
    Possible errors are
    ------------------------------------------

        [CODE]: [CONTENT - OVERVIEW]
        ----------------------------
        [A.0]: *args: not expected param
        [A.1]: *args: missing param
        [A.2]: *args: wrong type
        [A.3]: *args: restriction not met
        [K.0]: keyworded: not expected param
        [K.1]: keyworded: missing param
        [K.2]: keyworded: wrong type
        [K.3]: keyworded: restriction not met
        [K.4]: keyworded: unexpected error

    ------------------------------------------

    If all checks are passed, the decorated
    function runs as you created it.

    CAUTION:
    Keep in mind, that the 'args' have to be
    provided in order of appearance.

    params:
    -------
    to_check : dict
        A dictionary containing the 
        parameter declarations.
            Format: see above.
    debug : bool, optional
        If True, the decorator prints
        debug statements.
        (default is False)


    returns:
    --------
    dict | function return
        If an assertion failed, the decorator
        returns a dict with the information
        about the failure.
        If all assertions passed, the decorator
        will return your function result.
            Format:
                dict: {
                    'success':bool,
                    'error':str
                }

    """

    # make a copy of to_check
    toCheck = copy.deepcopy(to_check)

    #region 'decorator asserts' --------------
    # add flags for which part to check
    flags = {
        'positional':False,
        'args':False,
        'kwargs':False
    }

    # add flag for to raise error & msg
    # decorators somehow suppress exceptions from other
    # functions...
    raiseException = False
    error = ""

    # toCheck a dict?
    try: assert(isinstance(toCheck, dict))
    except AssertionError as e: 
        raiseException = True
        error = "'to_check' needs to be a dict."

    # assert any?
    if bool(toCheck):

        # check if the keywords are only the allowed ones
        try: assert(all([key in ["positional", "args", "kwargs"] for key in toCheck.keys()]))
        except AssertionError as e:
            raiseException = True
            error = "'to_check' allows only the keys 'positional', 'args' & 'kwargs'."
        
        # for each parameter
        for flag in flags:
            
            # should we assert?
            try:
                if bool(toCheck[flag]): 
                    result = _check_decorator_declaration(toCheck[flag], flag)
                    
                    # success?
                    if result['success']: flags.update({flag:result['check']})
                    else:
                        raiseException = True
                        error = result['error']

                        break

            except Exception as e: pass


    # raise globally the exception
    if raiseException: raise AssertionError(error)

    #endregion


    def decorator(func):
        """ Gets the decorated function """

        def wrapper(*args, **kwargs):
            """ Inner scope """
            
            # get locals
            loc = locals()

            #region 'sort parameters' -------
            # sort variables
            sortedParams = sort_parameters(func, loc, decorated=True)

            if debug: print("SORTED: ", sortedParams)

            # are any variables declared (in the decorated function)?
            if not bool(sortedParams['declared']): return func(*args, **kwargs)

            # if flag 'positional' is false, check
            # whether we can utilize type hints or not.
            if not flags['positional']:
                if bool(sortedParams['hinting']): 
                    
                    # update the positional checks
                    toCheck.update({'positional':_parse_hints(sortedParams["hinting"])})

                    # update the flag
                    flags.update({'positional':True})    

            # safety checks --> are 'args' & kwargs' declared?
            for flag in ['args', 'kwargs']:
                if flags[flag]:
                    if flag not in sortedParams['declared']: 
                        
                        # kill the check, because the developer added
                        # something not available
                        flags[flag] = False

            #endregion

            if debug: print("FLAGS: ", flags)

            # check if we should run the checks --> if not, just return function
            if all([flags[flag] == False for flag in flags]): return func(*args, **kwargs)

            #region 'check & mod variables' --
            for flag in flags:

                # check?
                if flags[flag]:

                    # run checks
                    result = _check_types(toCheck[flag], sortedParams[flag], flag)

                    # success? --> update sortedParams
                    if result['success']: sortedParams.update({flag:result['mod']})
                    
                    # else return error code
                    else: return {'success':False, 'error':result['error']}

            #endregion

            if debug: print("MOD:", sortedParams)

            # if checks did pass:
            # build args and kwargs for passing purpose. 
            # CAUTION: bring 'positional' in the correct order first
            # (by using declared!)
            modArgs = tuple([sortedParams['positional'][key] for key in sortedParams['declared'] if key not in ['args', 'kwargs']] + list(sortedParams['args']))
            modKwargs = sortedParams['kwargs']

            # CAUTION2: add 'self' if the function is a class method
            if sortedParams['self']['available']: modArgs = (sortedParams['self']['value'], *modArgs)

            if debug: print("MOD ARGS:", modArgs)
            if debug: print("MOD KWARGS:", modKwargs)

            return func(*modArgs, **modKwargs)

        return wrapper

    return decorator
