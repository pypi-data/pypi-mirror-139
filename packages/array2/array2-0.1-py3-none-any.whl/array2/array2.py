import array
class array2():
    """
    Use integrated array module to implement 2d array.

    Parameters
    ----------
        sizey : int
            The total lines of the 2d array.

        sizex : int
            The total rows of the 2d array.

        type : char, default: 'i'
            The type of the data in 2d array.
            You can choose from b/B/u/h/H/i/I/l/L/q/Q/f/d.
            Here is a reference of typecode, what they represent in C, and their minimum size in byte.
            'b', signed char, 1
            'B', unsigned char, 1
            'u', Py_UNICODE, 2
            'h', signed short, 2
            'H', unsigned short, 2
            'i', signed int, 2
            'I', unsigned int, 2
            'l', signed long, 4
            'L', unsigned long, 4
            'q', signed long long, 8
            'Q', unsigned long long, 8
            'f', float, 4
            'd', double, 8

        init : int/list, default: 0
            How the 2d array will be filled.
        
    Methods    
    ----------
        __getitem__ : use a list of 2 numbers to get the corresponding data in 2d array.
                    e.g. x = a[2,3]

        __setitem__ : use a list of 2 numbers and a value to change the corresponding data in 2d array.
                    e.g. a[2,3] = 1

        __repr__ : output the 2d array in a nice nested list format
                    e.g. print(a)
    """    
    def __init__(self, sizey, sizex, type = 'i', init = 0):
        self.x = sizex
        self.y = sizey
        if isinstance(init, int):
            self.a = array.array(type, [init] * sizex * sizey)
        elif isinstance(init, list):
            self.a = array.array(type, init)
        else:
            print('Error! array2 only accept int/list as init')
    def __repr__(self):
        article = '['
        line = '['
        for i in range(self.y):
            for j in range(i*self.x, i*self.x + self.x):
                line = line + str(self.a[j]) + ', '
            article += line[:-2] + '],\n '
            line = '['
        return article[:-3] + ']'
    def __getitem__(self, pos):
        y, x = pos[0], pos[1]
        return self.a[y*self.x + x]
    def __setitem__(self, pos, value):
        y, x = pos[0], pos[1]
        self.a[y*self.x + x] = value
        return None