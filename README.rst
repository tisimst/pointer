=================================
``pointer`` Package Documentation
=================================


Overview
--------
The ``pointer`` package was designed for the specific use (though certainly not
restricted to it) of aiding the manual conversion of native C/C++ code to
Python when the original C/C++ code makes use of pointers/pointer arithmetic.

The implementation aims to imitate the same functionality of pointers whether
the object that is being pointed to is an array of objects or a single object,
with as minimal amount of extra coding as possible when using compound
statements like ``*a++``. The package can't handle all cases, like compound
operations on the left-hand-side of assignment statements like:: 
    
    *b++ = *(a++) + k 

The ``++`` operation on ``b`` must be done in a separate statement afterwards,
like::

    *b = *(a++) + k
    b++


Basic Examples
--------------
Let's start with the import statement (there's only one necessary class)::

    >>> import pointer.pointer as ptr

Now let's create a pointer object (we'll start with an empty one for now)::

    >>> p = ptr()
    >>> p  # 'print' optional at command line
    < empty pointer >

Now let's point it to an array of "double's"::

    >>> a = [1, 2, 3]
    >>> p = ptr(a)  # C equiv: 'p = &a'
    >>> p
    < pointer to index=0 of a >

How about de-referencing?::

    >>> p.d  # C equiv: '*p'
    1
    
That wasn't all that interesting. Indexing works the same with pointers::

    >>> p[0]
    1
    >>> p[1]
    2
    >>> p[:]  # slicing supported
    [1, 2, 3]

Okay, now what if we want to change the value were are currently pointing at?::

    >>> p.setd(5)  # C equiv: '*p = 5'
    >>> p[:]
    [5, 2, 3]
    
Now let's see if the "pointing" actually works like we think it should::

    >>> a = 1  # a regular int
    >>> p = ptr(a)
    >>> p.d  # we expect the result to be 1
    1
    >>> p.setd(3)  # now we expect 'a' to be 3
    >>> a
    3
    >>> a = 45  # now let's see if the pointer updated...
    >>> p.d
    45
    
and sure enough, the pointer maintained ties with the original object, even
though ``a`` is technically an immutable object in this example. If there is more
than one object with the same value like::

    >>> a = 1
    >>> b = 1
    
Then we should be explicit about the variable name we are pointing at (especially
for ``int`` and ``float`` objects::

    >>> p = ptr(b, 'b')
    >>> p
    < pointer to b >
    

Contact
-------
Any questions, bugs, or success stories may be sent to the `author`_


.. _author: mailto:tisimst@gmail.com
