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
statements like ``*a++``. The package can't handle all cases, but it just can't
handle operations on the left-hand-side of assignment statements like 
``*b++ = *(a++) + k``. The ``++`` operation on ``b`` must be done after the
fact.


Basic Examples
--------------
Let's start with the import statement (there's only one necessary class)::

    >>> import pointer.pointer as ptr

Now let's create a pointer object (we'll start with an empty one for now)::

    >>> p = ptr()
    >>> print p  # 'print' optional at command line
    <Empty pointer>

Now let's point it to an array of "double's"::

    >>> a = [1, 2, 3]
    >>> p.ref(a)  # C equiv: 'p = &a'
    >>> print p
    <Pointer to index=0 of obj(<type 'list'>)=[1, 2, 3]>

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
    >>> print p
    <Pointer to index=0 of obj(<type 'list'>)=[5, 2, 3]>
    
    

Contact
-------
Any questions, bugs, or success stories may be sent to the `author`_


.. _author: mailto:tisimst@gmail.com