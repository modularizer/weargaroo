import math


a = 6378137
b = 6356752.3142
eqtr_r = (b**2)/a
pole_r = (a**2)/b
r = (1/3)*(2*a + b)


def get_r(lat, alt):
    theta = math.pi * lat/180
    t = math.tan(theta)
    t2 = t ** 2
    _a = a ** -2
    _b = b ** -2
    r = ((1 + t2)/(_a + _b * t2))**0.5
    return r + alt

def get_xyz(lat, lng, alt):
    theta = math.pi * lat / 180
    t = math.tan(theta)
    t2 = t ** 2
    _a = a ** -2
    _b = b ** -2
    r = ((1 + t2) / (_a + _b * t2)) ** 0.5 + alt
    y = r * math.sin(t)
    h = math.pi * lng / 180
    x = r * math.sin(h)
    projection_r = (x **2 + y **2)**0.5
    z = (projection_r ** 2 + r **2) ** 0.5
    return x, y, z, r

def dist(lat0, lng0, alt0, lat1, lng1, alt1):
    # print(lat0, lng0, alt0, lat1, lng1, alt1)
    x0, y0, z0, r0 = get_xyz(lat0, lng0, alt0)
    x1, y1, z1, r1 = get_xyz(lat1, lng1, alt1)
    # print(x0, y0, z0, r0)
    # print(x1, y1, z1, r1)
    dx = x1 - x0
    dy = y1 - y0
    dz = z1 - z0
    chord = (dx**2 + dy **2 + dz **2) ** 0.5
    avg_r = (r0 + r1)/2
    angle = math.asin(chord/avg_r)
    # print(avg_r, angle)
    d = angle * avg_r
    return d

def speed_test(*a, n=100):
    import time
    t0 = time.monotonic_ns()
    for _ in range(n):
        dist(*a)
    t1 = time.monotonic_ns()
    print(((t1 - t0)/n)/1e9)



