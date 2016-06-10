"""
===================
- Using deque(maxlen=N) creates a fixed-sized queue.
from collections import deque

===================
import heapq # nlargest, nsmallest | args (nums, arr)
>> heapq.nsmallest(3, portfolio, key=lambda s: s['price'])

The nlargest() and nsmallest() functions are most appropriate if you are trying
to find a relatively small number of items. If you are simply trying to find
the single smallest or largest item (N=1), it is faster to use min() and max()
===================
d = {}
for key, value in pairs:
    if key not in d:
        d[key] = []
    d[key].append(value)

# collections
d = defaultdict(list)
for key, value in pairs:
    d[key].append(value)
===================
An OrderedDict can be particularly useful when you want to build a mapping
that you may want to later serialize or encode into a different format.

from collections import OrderedDict

    d = OrderedDict()
    d['foo'] = 1
    d['bar'] = 2
    d['spam'] = 3
    d['grok'] = 4

>> import json
>> json.dumps(d)
'{"foo": 1, "bar": 2, "spam": 3, "grok": 4}'
===================
Removing Duplicates from a Sequence while Maintaining Order

def dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item) if val not in seen:
        yield item
        seen.add(val)
===================
>> a = slice(2, 4)
>> items[2:4]
[2, 3]
>> items[a]
[2, 3]

p = a.indices(len(str)) -> reduce of max in slice
===================
words = [
       'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
       'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
       'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
       'my', 'eyes', "you're", 'under'
]
from collections import Counter word_counts = Counter(words)
top_three = word_counts.most_common(3)
print(top_three)
    # Outputs [('eyes', 8), ('the', 5), ('look', 4)]

>> word_counts['eyes']
8
===================
from operator import itemgetter

rows_by_fname = sorted(rows, key=itemgetter('fname'))
rows_by_uid = sorted(rows, key=itemgetter('uid'))
===================
>> from functools import partial
>> basetwo = partial(int, base=2)
>> basetwo.__doc__ = 'Convert base 2 string to an int.'
>> basetwo('10010')
18
===================
class functools.partialmethod(func, *args, **keywords)
Return a new partialmethod descriptor which behaves like partial except
that it is designed to be used as a method definition rather than being
directly callable.
===================
Apply function of two arguments cumulatively to the items of sequence, from
left to right, so as to reduce the sequence to a single value. For example,
reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates ((((1+2)+3)+4)+5).
===================
Transforms a function into a single-dispatch generic function.

To define a generic function, decorate it with the @singledispatch decorator.
Note that the dispatch happens on the type of the first argument, create your
function accordingly:

>>> from functools import singledispatch
>>> @singledispatch
... def fun(arg, verbose=False):
...     if verbose:
...         print("Let me just say,", end=" ")
...     print(arg)
To add overloaded implementations to the function, use the register() attribute
 of the generic function. It is a decorator, taking a type parameter and
 decorating a function implementing the operation for that type:

>>>
>>> @fun.register(int)
... def _(arg, verbose=False):
...     if verbose:
...         print("Strength in numbers, eh?", end=" ")
...     print(arg)
...
>>> @fun.register(list)
... def _(arg, verbose=False):
...     if verbose:
...         print("Enumerate this:")
...     for i, elem in enumerate(arg):
...         print(i, elem)
===================
from functools import wraps
def logged(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print func.__name__ + " was called"
        return func(*args, **kwargs)
    return with_logging

@logged
def f(x):
   does some math
   return x + x * x

print f.__name__  # prints 'f'
print f.__doc__   # prints 'does some math'
===================
The groupby() function works by scanning a sequence and finding sequential
“runs” of identical values (or values returned by the given key function)

# Iterate in groups
for date, items in groupby(rows, key=itemgetter('date')):
    print(date)
    for i in items:
        print(' ', i)
===================

===================
===================
===================
===================
===================
===================
===================
===================
===================
===================
===================
===================
===================
===================
===================
===================
===================
===================
===================
===================
===================
"""

