def ToXYZ(x,y,w,f):
    coef = 1.08
    x_origin=100
    y_origin=30
    tomato_size=60

    x=int(x*coef+(w/2)+x_origin)
    z=int(y*coef+y_origin)
    y=int(tomato_size*f/w)-200
    s = [x,y,z]
    return s
