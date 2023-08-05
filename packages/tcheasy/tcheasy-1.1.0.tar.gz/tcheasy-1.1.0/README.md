<img src="https://user-images.githubusercontent.com/52833906/149335767-4caee5aa-7362-4f52-ab90-0772a9fc1507.png" alt="It's Mr. Tcheasy!" style="width:90%;">
<p style="color:gray"><em><a href='https://de.freepik.com/vektoren/design'>Checkout - freepik - </a> the photographer of Mr. Tcheasy & Sorpa!</em></p>

<br>
<br>
<br>


# tcheasy

**tcheasy** is a python decorator that makes type checking (at runtime) easy! <br>
Just import the decorator and start **to check your function inputs** from the get-go. <br>
You want to define **input restrictions** as well? Then your are in the right place! <br>

<p style="color:gray"> <em> Python >= 3.8 needed. Tested ver. { 3.8.5, 3.9.9 } </em> <p>

<br>
<br>

## <a name="top"></a> CONTENT
1. [why?](#whats-it)
2. [how?](#how)
4. [install?](#install)
4. [where is Sorpa?](#sorpa)
5. [examples?](#examples)
 

<br>

# <a name='whats-it'></a> WHY? <sub><sub>[Back to top](#top)</sub></sub> 

For one of my projects I needed a way to check user inputs at runtime. <br>
There were already packages that do type-checking, but they only use the - relatively simplistic - python type hints. <br>
The problem, however, was that I needed not only type checking but also the option to restrict some parameter inputs. <br>

<br>

Enter **tcheasy**! <br>

<br>

Out of the need to have a tool for other projects, this python decorator was born. <br>
This little kritter is able to use a predefined `dict` or the `python type hinting`. Please refere to the [how?](#how) & [example?](examples) section for more infos about the usage. <br>

<br>

**tcheasy** ships also with his neat little friend **sorpa**: <br>
The function `sorpa()` is able to extract and sort your passed function parameters at runtime.<br>

<br>

If you are sololy looking for a type checking tool (and some handy utility-tools) you should also check out:
- [beartype](https://github.com/beartype/beartype)
- [typeguard](https://typeguard.readthedocs.io/en/latest/)
- [mypy](http://mypy-lang.org/)

<br>

Else feel free to use and modify **tcheasy** as you please.

<br>

# <a name='how'></a>  HOW? <sub><sub>[Back to top](#top)</sub></sub> 

Just import the package 

<br>

```python
from tcheasy import tcheasy
```

<br>

and add the decorator `@tcheasy()` to your to-be-checked function. <br>
If you are already using `python type hinting` **tcheasy** is ready out of the box. <br>

In the current version, the following types (hints) are supported:
- **NoneType(s)**: None
- **number types**: int, float, complex, bool
- **sequence types**: str, list, tuple
- **mapping types**: dict
- **set types**: sets
- **callable types**: object
- **`typing`-module types**: typing.Any, typing.Union

<br>

But the true might comes from using *declarative dicts*. <br>
By passing a dict to `@tcheasy()` you can specify the parameter types, add rudimentary input restrictions & default values. <br>
The structure of these dictionaries (and their used keywords) is always the same (`type`, `restriction` (optional) & `default` (optional)):

<br>

```python
# define the dict!

to_check = {
    'positional':{
        'parameter-name':{
            'type': type,
            'restriction': "(optional) in the form: value condition",
            'default': "(optional) default value"
        },
        'next-parameter-name':{
            ...
        },
        ...
    },
    'args':[ {'type':type, 'restriction':str, 'default': "value" }, {...}, ...],
    'kwargs': {
        'parameter-name':{...},
        ...
    }
}

```

<br>

As you can see, you have the complete control over potential `*args` and `**kwargs`.
The definition structure of 'kwargs' is also the same as for the `positional`s. <br>
Keep in mind that you do not have to define `restriction` and/or `default`. These two keywords are completely optional.

<br>

After you have defined the `dict` you can pass it to `@tcheasy()` and it will start to monitor the function at runtime (e.g. if your `dict` is called **to_check**, then you pass it like this: `@tcheasy(to_check)`).

<br>

> *Note:* <br>
> *The separation of `positional`, `args` & `kwargs` is derived of the python parameter types. There are 5 distinct types, which can be boiled down to basically 3 'blocks':*
> - *positional:*
>   - *keyword parameters (your typical `def test(a)`, while the call was `test(a='some-value')`)*
>   - *(positional) parameters (again your typical `def test(a)` but this time calling just `test('some-value')`)*
> - *\*args:*
>   - *arbitrary positional arguments (`def test(a, *args)`, while calling `test('value-a', 'value-args')`)*
> - *\**kwargs:*
>   - *arbitrary keyword arguments (`def test(a, **kwargs)`, while calling `test('value-a', add_kwargs="some-value"`))*

<br>

The structure of the `default` keyword is  - as mentioned - always the same. For example consider the following:

<br>

```python

...
    'parameter-name': {
        'type': int,
        'restriction':"value > 1"
    },
...

```

<br>

In this example, the passed `int` parameter gets evaluated and has to be be greater than one.
The word `value` is the placeholder for your function parameter. <br>
To give you another example, you can use `"value in ['yes', 'no', 'maybe']"` to evaluate if the passed string parameter is one of the elements in the list. <br>
With this technique you are able to do some pretty awsome stuff! <br>

<br>

If you want further examples, please refere to the [examples?](#examples) section. <br>

<br>

# <a name='install'></a> INSTALL? <sub><sub>[Back to top](#top)</sub></sub> 

There are two ways to install **tcheasy**.<br>
The easy way is to use pip: <br>

<br>

```terminal
$ pip install tcheasy
```

<br>

The other option is to `git clone` the project and then run: 

<br>

```terminal
$ pip install 'path-to-your-clone'
```

<br>

If you want to tinker with your code, run the pip install with `-e`. <br>


<br>

# <a name='sorpa'></a> WHERE IS SORPA? <sub><sub>[Back to top](#top)</sub></sub> 

**Mr. Tcheasy** comes packed with his friend **Sorpa**!

<img src="https://user-images.githubusercontent.com/52833906/149335771-cf8fd80b-aacb-49a9-9776-e16874cc016f.png" alt="Sorpa ~" style="width:60%;">

<br>

`sorpa()` is a python function which shows you the passed parameters, names, declartions and hints of your targeted python function at runtime. <br>

<br>

The import is as easy as the import for **tcheasy**. Just:

<br>

```python
from tcheasy import sorpa
```

<br>

This function takes as input the function (`func`) you want to analyse and the locals (`loc`). <br>
As soon as you passed those two arguments, you get a handy dict which sorted the passed parameters, your declared parameter (during function definition) & python hints. <br>
For example, lets consider the following test function:

<br>

```python
# we define our test function (called 'test_function') with the parameters a, b & c
# also we add some type hinting
def test_function(a:int, b:str, c:float = .1) -> dict:
    """Our test function. Proper docstring skipped """

    # get our local variables
    loc = locals()

    # lets consider we already imported 'sorpa'
    # we set decorated to 'False' to tell the algorithmn
    # that we are not within a decorator scope.
    sortedParameters = sorpa(
        func = test_function, 
        loc = loc,
        decorated = False
        )

    return sortedParameters
```

<br>

Now we can call the function with some arguments (e.g. `test_function(5, b="some-string")`) and get as a return the following:

<br>

```python
>> {
        'positional': {'a': 5, 'b': 'some-string', 'c': 0.1},
        'args':[],
        'kwargs':{},
        'hinting':{'a': <class 'int'>, 'b': <class 'str'>, 'c': <class 'float'>},
        'declared': ['a', 'b', 'c'],
        'self':{'available':False, 'value':None}
   }
```

<br>

# <a name='examples'></a> EXAMPLES? <sub><sub>[Back to top](#top)</sub></sub> 

To get some examples, please check out the **[examples](https://github.com/No9005/tcheasy/tree/main/examples)** directory (on github). <br>
There you will find examples for **Mr. Tcheasy's** & and his friend **Sorpa's** usecases.
