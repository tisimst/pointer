# -*- coding: utf-8 -*-
"""
A class to imitate C/C++ pointers
"""
import math
import inspect

class pointer:
    def __init__(self, obj=None, name=None, idx=0, parent=None):
        """
        Create a new pseudo-pointer.
        
        Parameters
        ----------
        obj : object
            Any python object to be "pointed to".
        name : str
            The actual name that is being used to identify the object
        idx : int
            The index of the array that is being pointed at (Default: 0)
        parent : dict
            The python namespace that contains the actual object that is 
            being "pointed to". If not given manually, it is assumed that 
            the object exists within the current scope of the assignment. 
            If the object is a "raw" object (such as an ``int``, ``float``,
            etc.), then a dummy dict is created to store the value.
        
        Examples
        --------
        ::
            
            >>> p = pointer()  # an empty pointer just itching to be used
            >>> p
            < empty pointer>
            
            >>> a = 1
            >>> p = pointer(a)  # now pointing at the object called "a"
            >>> p
            < pointer to a >
            
            >>> arr = [1, 2, 3]
            >>> p = pointer(arr)  # now pointing at the array called "arr"
            >>> p
            < pointer to index=0 of arr >
            
        """
        # Test the input parameters
        assert isinstance(idx, int), 'kwarg "idx" must be an int >= 0'
        
        self._name = None
        
        if obj is not None:
            if parent is None or not isinstance(parent, dict):
                parent = inspect.currentframe(1).f_locals
            if name is not None:
                try:
                    parent[name]
                except KeyError:
                    raise KeyError("Sorry, {:} wasn't found in the namespace provided".format(name))
                else:
                    self._name = name
                    self._parentdict = parent
            else:
                # When the name isn't manually given, it is possible to
                # point to the wrong object if another object has same
                # value as the one trying to be pointed at (mostly only
                # an issue for pointers to integer objects).
                for k,v in parent.iteritems():
                    if obj is v:
                        self._name = k
                        self._parentdict = parent
                        break
                    
            # If raw object was input, like '1'
            if self._name is None:
                self._name = '_raw_data_'
                self._parentdict = {self._name: obj}
        else:
            # If raw object was input, like '1'
            self._name = '_raw_data_'
            self._parentdict = {self._name: obj}
                
        self._obj = obj
        self._idx = idx
            
    def __str__(self):
        if self._obj is None:
            return '< empty pointer >'
        elif not (hasattr(self._obj, '__iter__') or \
            hasattr(self._obj, '__getitem__')):
            return '< pointer to {:} >'.format(self._name)
        else:
            return '< pointer to index={:} of {:} >'.format(self._idx, 
                self._name)
    
    def __repr__(self):
        return str(self)
        
    def __len__(self):
        obj = self._parentdict[self._name]
        try:
            mylen = len(obj)
        except TypeError:
            mylen = 1
        return mylen
        
    def __getitem__(self, idx):
        if isinstance(self._obj, pointer):
            return self._parentdict[self._name]
        else:
            if not hasattr(self._obj, '__iter__') and \
                not hasattr(self._obj, '__getitem__') and idx==0:
                return self._parentdict[self._name]
            elif isinstance(idx, slice):
                obj = self._parentdict[self._name]
                return [obj[ii] for ii in xrange(*idx.indices(len(obj)))]
            elif isinstance(idx, int):
                if idx<0:
                    idx += len(self._obj)
                if idx>=len(self._obj):
                    raise IndexError, 'Index ({:}) is out of range'.format(idx)
                return self._parentdict[self._name][idx]
            else:
                raise TypeError, 'Invalid argument type'
    
    def __setitem__(self, idx, val):
        if isinstance(self._obj, pointer):
            self._parentdict[self._name] = val
        else:
            if not hasattr(self._obj, '__iter__') and idx==0:
                self._parentdict[self._name] = val
            else:
                self._parentdict[self._name][idx] = val
    
    def __add__(self, val):
        assert val==math.floor(val), 'Value must be an integer'
        return pointer(self._parentdict[self._name], self._idx + val,
            name = self._name, parent=self._parentdict)
    
    def __sub__(self, val):
        assert val==math.floor(val), 'Value must be an integer'
        return pointer(self._parentdict[self._name], self._idx - val,
            name = self._name, parent=self._parentdict)
    
    def copy(self):
        """
        Emulates ``q = p`` when p is a pointer and we want to create a new
        pointer to the same object without creating ties between p and q.
        """
        return pointer(self._parentdict[self._name], self._idx,
            name = self._name, parent=self._parentdict)
    
    @property
    def d(self):
        """
        Emulates ``*p``, which means "de-reference p and return the value of
        the object it points to".
        """
        if isinstance(self._parentdict[self._name], pointer):
            v = self._parentdict[self._name]
        else:
            try:
                v = self._parentdict[self._name][self._idx]
            except (TypeError, IndexError):
                v = self._parentdict[self._name]
        return v
            
    @property
    def pp(self):
        """
        Emulates ``p++``, which means "increment p"
        """
        self._idx = self._idx + 1
        return self
    
    @property
    def mm(self):
        """
        Emulates ``p--``, which means "decrement p"
        """
        self._idx = self._idx - 1
        return self
    
    def setd(self, val):
        """
        Emulates ``*p = ...``, which means "set the dereferenced value to..."
        """
        try:
            self._parentdict[self._name][self._idx] = val
            self._obj[self._idx] = val
        except TypeError:
            self._parentdict[self._name] = val
            self._obj = val
    
    # def ref(self, obj=None, idx=0, name=None, parent=None):
        # """
        # Emulates ``p = &a``, which means "point p to the address of a"
        # """
        # self.__init__(obj, idx, name, parent)
        
    @property
    def dpp(self):
        """
        Emulates ``*p++``, which means "dereference p, then increment p"
        """
        tmp = self.d
        self.pp
        return tmp

    @property
    def dmm(self):
        """
        Emulates ``*p--``, which means "dereference p, then decrement p"
        """
        tmp = self.d
        self.mm
        return tmp

if __name__=='__main__':
    """
    The example below comes from the 'Numerical Methods Presentations' by
    Professor John Carroll, Dublin City University
    www.math.ysu.edu/~faires/Numerical-Methods/Beamer
    
    It is a transcription of C-code to show how pointer objects may be used.
    
    Original Code
    =============
    
    /*
    *   ROMBERG ALGORITHM 4.2
    *   
    *   To approximate I = integral ( ( f(x) dx ) ) from a to b:
    *   
    *   INPUT:   endpoints a, b; integer n > 0.
    *
    *   OUTPUT:  an array R. ( R(2,n) is the approximation to I. )
    *
    *   R is computed by rows; only 2 rows saved in storage   
    */
    
    #include<stdio.h>
    #include<math.h>
    #define true 1
    #define false 0
    
    main()
    {
       double R[2][15]; 
       double A,B,H,X,SUM;
       int I,J,K,L,M,N,OK;
    
       double F(double);
       void INPUT(int *, double *, double *, int *);
    
       INPUT(&OK, &A, &B, &N);
       /* STEP 1 */ 
       if (OK) { 
          H = (B - A);
          R[0][0] = (F(A) + F(B)) / 2.0 * H;
          /* STEP 2 */ 
          printf("Initial Data:\n"); 
          printf("Limits of integration = [%12.8f, %12.8f]\n", A, B);
          printf("Number of rows = %3d\n", N);
          printf("\nRomberg Integration Table:\n");
          printf("\n%12.8f\n\n", R[0][0]);
          /* STEP 3 */ 
          for (I=2; I<=N; I++) { 
    	 /* STEP 4 */  
    	 /* approximation from Trapezoidal method */ 
    	 SUM = 0.0;
    	 M =  exp((I - 2) * log(2.0)) + 0.5;
    	 for (K=1; K<=M; K++) SUM = SUM + F(A + (K - 0.5) * H);
    	 R[1][0] = (R[0][0] + H * SUM) / 2.0;
    	 /* STEP 5 */ 
    	 /* extrapolation */    
    	 for (J=2; J<=I; J++) {
    	    L = exp(2* (J - 1) * log(2.0)) + 0.5;
    	    R[1][J-1] = R[1][J-2]+(R[1][J-2]-R[0][J-2])/(L - 1.0);
    	 }
    	 /* STEP 6 */ 
    	 for (K=1; K<=I; K++) printf(" %11.8f",R[1][K-1]); 
    	 printf("\n\n");
    	 /* STEP 7 */ 
    	 H = H / 2.0;   
    	 /* since only two rows are kept in storage, this step */
    	 /* is to prepare for the next row */
    	 /* update row 1 of R */                
    	 /* STEP 8 */ 
    	 for (J=1; J<=I; J++) R[0][J-1] = R[1][J-1];
          }
       }
       /* STEP 9 */ 
       return 0; 
    }
    
    /* Change function F for a new problem */
    double F(double X)
    {
       double f; 
    
       f = sin(X);
       return f;
    }
    
    void INPUT(int *OK, double *A, double *B, int *N)
    {
       char AA;
    
       printf("This is Romberg integration.\n\n");
       printf("Has the function F been created in the program immediately preceding\n");
       printf("the INPUT function?\n");
       printf("Enter Y or N\n");
       scanf("%c",&AA);
       if ((AA == 'Y') || (AA == 'y')) {
          *OK = false;
          while (!(*OK)) {
    	 printf("Input lower limit of integration and ");
    	 printf("upper limit of integration\n");
    	 printf("separated by a blank\n");
    	 scanf("%lf %lf", A, B);
    	 if (*A > *B) printf("Lower limit must be less than upper limit\n");
    	 else *OK = true;
          } 
          *OK = false;
          while (!(*OK)) {
    	 printf("Input number of rows - no decimal point\n");
    	 scanf("%d", N);
    	 if (*N > 0) *OK = true;
    	 else printf("Number must be a positive integer\n");
          }
       }
       else {
          printf("The program will end so that the function F can be created\n");
          *OK = false;
       }
    }
    
    """
    
    # We need to define these functions first since python doesn't support
    # function prototyping outside of class definitions
    def F(X):
#        f = math.sin(X)
        f = 1./math.sqrt(math.pi)*math.exp(-X**2.0)
        return f
    
    def INPUT(
        OK,  # int *
        A,  # double *
        B,  # double *
        N  # int *
        ):
        print 'This is Romberg integration.\n'
        print 'Has the function F been created in the program immediately preceding'
        print 'the INPUT function?'
        AA = raw_input('Enter Y or N: ')
        if AA=='Y' or AA == 'y':
            OK.setd(False)
            while not OK.d:
                print 'Input lower limit of integration and upper limit of integration'
                AB = raw_input('separated by a blank: ')
                AB = AB.split(' ')
                if len(AB)==2 and not any([AB[0]=='', AB[1]=='']):
                    A.setd(float(AB[0]))
                    B.setd(float(AB[1]))
                    if A.d>B.d:
                        print 'Lower limit must be less than upper limit'
                    else:
                        OK.setd(True)
                else:
                    print 'Two values must be entered.'
            OK.setd(False)
            while not OK.d:
                n = raw_input('Input number of rows (no decimal point): ')
                N.setd(int(n))
                if N.d>0:
                    OK.setd(True)
                else:
                    print 'Number must be a positive integer'
        else:
            print 'The program will end so that the function F can be created'
            OK.setd(False)
    
    # Initiate the necessary pointers
    OK = pointer()
    A = pointer()
    B = pointer()
    N = pointer()

    # Gather inputs
    INPUT(OK, A, B, N)

    # Now that we have the values, we can discard the pointer parts
    OK = OK.d    
    A = A.d
    B = B.d
    N = N.d
    
    # STEP 1
    if OK:
        # Initialize the necessary data arrays
        R = pointer([pointer([None]*N), pointer([None]*N)])
        FTOL = 1e-8  # convergence tolerance
        H = (B - A)
        R[0][0] = (F(A) + F(B)) / 2.0 * H
        # STEP 2
        print 'Initial Data:' 
        print 'Limits of integration = [%12.8f, %12.8f]'%(A, B)
        print 'Number of rows = %3d'%(N)
        print '\nRomberg Integration Table:'
        print '\n%12.8f'%(R[0][0])
        # STEP 3 
        for I in xrange(2, N+1):
            # STEP 4
            # approximation from Trapezoidal method
            SUM = 0.0
            M =  math.exp((I - 2) * math.log(2.0)) + 0.5
            K = 1
            for K in xrange(int(M)+1):
#            while K<=M:
                SUM = SUM + F(A + (K - 0.5) * H)
#                K += 1
            R[1][0] = (R[0][0] + H * SUM) / 2.0
            # STEP 5
            # extrapolation
            for J in xrange(2, I+1):
               L = 4**(J - 1)
               R[1][J-1] = R[1][J-2]+(R[1][J-2]-R[0][J-2])/(L - 1.0)
            # STEP 6
            line = ''
            for K in xrange(1, I+1):
                line += ' %11.8f'%(R[1][K-1])
            print line
            
            # STEP 6.5 (I added this one)
            if I>3:
                # Check to see if the last diagonal values converged within tolerance
                CHECK1 = math.fabs(R[0][I-2] - R[1][I-1])<=FTOL
                CHECK2 = math.fabs(R[0][I-3] - R[1][I-2])<=FTOL
                if CHECK1 and CHECK2:
                    print 'Last element not changing within %12.8e for last two iterations.'%FTOL
                    print 'Algorithm terminated at F = %12.8f after %d iterations'%(R[1][I-1], I)
                    break

            # STEP 7
            H = H / 2.0
            # since only two rows are kept in storage, this step
            # is to prepare for the next row
            # update row 1 of R
            # STEP 8
            for J in xrange(1, I+1):
                R[0][J-1] = R[1][J-1]
                            
