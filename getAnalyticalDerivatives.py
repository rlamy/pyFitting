import sympy

# Mappings between sympy and numpy

NUMPY_TRANSLATIONS = {
    'amax': 'max_',
    'amin': 'min_',
    'angle': 'arg',
    'arccos': 'acos',
    'arccosh': 'acosh',
    'arcsin': 'asin',
    'arcsinh': 'asinh',
    'arctan': 'atan',
    'arctan2': 'atan2',
    'arctanh': 'atanh',
    'ceil': 'ceiling',
    'e': 'E',
    'imag': 'im',
    'inf': 'oo',
    'log': 'ln',
    'matrix': 'Matrix',
    'real': 're'}

def getDiff(independentVars, function_string, varsDiff):
    """
    This function makes the analytical derivative 
    of a  "function(independentVars, varsDiff)" over variable(s) "varsDiff"
    Returns a list of strings
    Example:
    f(x,a, b) = a*x**2+b*x
    independentVars = ["x"]
    function = "a*x**2+b*x"
    varsDiff = ["a", "b"]
    return ["2*x", "x"]
    """
    diffs = []
    # There is a problem if variables are not a list 
    independentVars = list(independentVars)
    varsDiff = list(varsDiff)
    
    # Define all the variables as sympy.Symbols
    for v in independentVars + varsDiff:
        sympy.var(v)
    # Define the function "f" and change it into a sympy expression
    checkFunction = True
    while checkFunction:
        try:
            exec "f = %s" % (function_string)
            checkFunction = False
        except NameError as inst:
            # find the function to be changed into a sympy expression
            # and check if the name is different from numpy
            op = inst.message.split("'")[1]
            if op in NUMPY_TRANSLATIONS:
                opNew = "sympy."+NUMPY_TRANSLATIONS[op]
            elif op in dir(sympy):
                opNew = "sympy."+ op
            else:
                print("Warning: %s does not exist in sympy" % op)
                print("No analytical derivatives are used")
                return None
            function_string = function_string.replace(op, opNew)
        
     # Do the loop over the variables varsDiff
    for variableToDiff in varsDiff:
        exec "derivative = sympy.diff(f,%s)" % variableToDiff
        derivative = str(derivative)
        # We must check if the derivative is not a constant, 
        # as it can give problems with the jacobian
        # i.e. must have the same lenght of 'x' data
        for var in independentVars:
            if var not in derivative:
                derivative = "%s*%s/%s" % (derivative, var, var)
        diffs.append(derivative)
    return diffs

if __name__ == "__main__":
    f = "b1*gamma(x/b4)+b2/x**b3"
    derivList = "b1,b2,b3,b4".split(",")
    derivs = getDiff("x",f, derivList)
    for d in derivs:
        print d