"""
Contains the decorator & helper function
to sort passed parameters into
    - positional
    - args
    - kwargs
    - type hints

"""

import copy
import typing
import inspect

def _convert_any():
    """Returns a Union for most common types
    
    A list of all types (not all supported
    though)
        https://www.informit.com/articles/article.aspx?p=453682&seqNum=5

    params:
    -------
    None

    returns:
    --------
    typing.Union
        The union containing all types

    """

    # list of supported types.
    allTypes = (
        type(None), 
        int, float, complex, bool,
        str, list, tuple,
        dict,
        set,
        object
    )

    return allTypes

def sort_parameters(func, loc:dict, decorated=True) -> dict:
    """Function sorts the python parameters

    Python makes a mess out of the function
    calls. As soon as you add the variable
    name to the passed argument (like a=5)
    it moves the variable to kwargs (like arg
    'a' moves to kwargs).
    To enable reliable dtype checking we are
    going to sort the passed parameters so
    each passed element is actually in a dict
    with its parameter name as key and the
    passed value as value.
    
    The only exception is '*args' because
    these elements are just positional (with
    no variable name).

    CAUTION:
    If there is type hinting provided we also
    get these elements.

    params:
    func : function
        The python function to 'clean'.
    loc : dict
        The python locals of the scope.
    decorated : bool
        If True, the function assumes it
        is called by a decorator.

    returns:
    --------
    dict
        Dict with the sorted elements
        for further processing.
            Format: {
                'positional':dict,
                'args':list,
                'kwargs':dict,
                'hinting':dict,
                'defined':list,
                'self':dict
            }
    
    """

    # get full arg spec
    iArgs, iVarargs, iVarkw, iDefaults, iKwonlyargs, iKwonlydefaults, iAnnotations = inspect.getfullargspec(func)

    # is self within the iArgs?
    selfData = {'available':False, 'value':None}
    
    if "self" in iArgs:

        # differenciate between 'decorated' or not
        if decorated:
            """
            CAUTION:
            If the function was decorated, the 'self' parameter
            is within the loc['args'] list.
            Else its a keyword within the loc.

            In the first case, we have to get rid of the
            first element of the loc['args'] list (because
            its the passed 'self'.)
            In the second case, we have to get the 'self'
            value from the locs.
            
            In both cases, we have to delete the 'self'
            element in iArgs.

            """

            # grab self data
            selfData = {'available':True, 'value':loc['args'][0]}

            # modify the loc['args'] list
            loc['args'] = loc['args'][1:]

        else: selfData = {'available':True, 'value':loc['self']}

        # kill self
        iArgs = [element for element in iArgs if element != "self"]

    # get basic positionals
    # locals() show all variables in the local scope
    # getfullargspec gives back the possible arguments for the function
    if decorated: 
        # get basic elements
        positional = {expected:found for found,expected in zip(loc['args'], iArgs)}

        # python moves positional arguments, which get uniquely defined during
        # runtime into 'kwargs'. To get them back, we search within kwargs for
        # the missing ones
        for expected in iArgs:
            if expected in loc['kwargs']: positional.update({expected:loc['kwargs'][expected]})

    else: positional = {expected:loc[expected] for expected in iArgs}

    # create declared, which tells you which parameters the programmer declared
    declared = copy.deepcopy(iArgs)

    # get fallback for trueKwargs, trueArgs & trueAnnotations
    trueKwargs = {}
    trueArgs = []
    trueAnnotations = {}

    # generate the true kwargs if the developer declared **kwargs
    if iVarkw is not None:

        # get true kwargs
        trueKwargs = {key:loc['kwargs'][key] for key in loc['kwargs'] if key not in positional}

        # add 'kwargs' to defined
        declared.append('kwargs')

    # any element in iArgs, which is still left is a trueArgs
    if iVarargs is not None:

        if decorated:
        
            # calculate difference (expressed in idx)
            idx = len(loc['args']) - len(iArgs)

            if idx > 0: trueArgs = copy.deepcopy((loc['args'][-idx:]))

        else: trueArgs = loc['args']

        # add 'args' to defined
        declared.append('args')

    
    # grab defaults and add them to the positionals
    if bool(iDefaults):
        
        # because the defaults are orderd in appearance, and we do not know which 
        # parameter was not passed, we build a map (in reverse)
        defaultMap = {first:second for first, second in zip(reversed(iArgs), reversed(iDefaults))}

        # check each key and add still missing args to positional
        for key in defaultMap:
            if key not in positional: positional.update({key:defaultMap[key]})

    # get annotations (aka python type hinting)
    if bool(iAnnotations):
        for key in iAnnotations:
            
            if key not in ["return", "args", "kwargs", "self"]:
                # differenciate between typing.Union, typing.Any and others
                if typing.get_origin(iAnnotations[key]) == typing.Union: trueAnnotations.update({key:typing.get_args(iAnnotations[key])})
                elif str(iAnnotations[key]) == "typing.Any": trueAnnotations.update({key:_convert_any()})
                else: trueAnnotations.update({key:iAnnotations[key]})

        # add missings as typing.Any
        for key in declared:
            if key not in trueAnnotations and key not in ["args", "kwargs"]: trueAnnotations.update({key:_convert_any()})
    
    complete = {
        'positional':copy.deepcopy(positional),
        'args':copy.deepcopy(trueArgs),
        'kwargs':copy.deepcopy(trueKwargs),
        'hinting':copy.deepcopy(trueAnnotations),
        'declared':declared,
        'self':selfData
        }

    return complete








                            



                

