# polynomial-solver
Finds the roots of polynomials using some mathematical theorems:

First it uses a result from Mean Value Theorem that states 
>Let f(x) be a polynomial with a derivative f'(x) that has roots c1, c2, c..n. Then f(x) has at most one root in the intervals (-infinity, c1], (c1, c2], (c2, c3], ..., (cn,infinity)

Essentially the roots of a polynomial lie between the roots of it's derivative. This result means if you can find the roots of f'(x) you have some idea of where the roots of f(x) are.

Secondly once we have the intervals in which the roots lie we can apply the bisection method of root estimation to find the roots. This is another recursive function that works as follows:

  1. Split the interval for which the root lies in half
  2. Check to see whether the root lies in the first or second half (using intermediate value theorem and the fact that there are no turning points in the interval)
  3. Repeat steps 1-2 with the half of the interval that the root lies in
  4. Once the interval is small enough you have an accurate approximation of the root
  
  
The algorithm ties these two results together by recursively finding the roots of f'(x), then searching in each of the intervals between those roots for the roots of f(x).
