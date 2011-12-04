
# Based on moon.py, from John Walker. 
# http://bazaar.launchpad.net/~keturn/py-moon-phase/trunk/view/head:/moon.py
# Note: I've tweaked the original constants for better precision!
#
#
# Original license header:
#
# #  moon.py, based on code by John Walker (http://www.fourmilab.ch/)
# #  ported to Python by Kevin Turner <acapnotic@twistedmatrix.com>
# #  on June 6, 2001 (JDN 2452066.52491), under a full moon.
# #
# #  This program is in the public domain: "Do what thou wilt shall be
# #  the whole of the law".
#

"""Functions to find the phase of the moon.

Ported from \"A Moon for the Sun\" (aka moontool.c), a program by the
venerable John Walker.  He used algoritms from \"Practical Astronomy
With Your Calculator\" by Peter Duffett-Smith, Second Edition.

For the full history of the code, as well as references to other
reading material and other entertainments, please refer to John
Walker's website,
http://www.fourmilab.ch/
(Look under the Science/Astronomy and Space heading.)

"""

from math import sin, cos, floor, sqrt, pi, tan, atan
import bisect
import time

# Precision used when describing the moon's phase in textual format,
# in phase_string().
PRECISION = 0.05
_NEW =   0 / 4.0
_FIRST = 1 / 4.0
_FULL = 2 / 4.0
_LAST = 3 / 4.0
_NEXTNEW = 4 / 4.0





class AstronomicalConstants:

    # JDN stands for Julian Day Number
    # Angles here are in degrees

    # 1980 January 0.0 in JDN
    epoch = 2444239.0

    # Ecliptic longitude of the Sun at epoch 1980.0
    ecliptic_longitude_epoch = 278.833540

    # Ecliptic longitude of the Sun at perigee
    ecliptic_longitude_perigee = 282.596403

    # Eccentricity of Earth's orbit
    eccentricity = 0.016718

    # Semi-major axis of Earth's orbit, in kilometers
    sun_smaxis = 1.49585e8

    # Sun's angular size, in degrees, at semi-major axis distance
    sun_angular_size_smaxis = 0.533128

    ## Elements of the Moon's orbit, epoch 1980.0

    # Moon's mean longitude at the epoch
    moon_mean_longitude_epoch = 64.975464
    # Mean longitude of the perigee at the epoch
    moon_mean_perigee_epoch = 349.383063

    # Mean longitude of the node at the epoch
    node_mean_longitude_epoch = 151.950429

    # Inclination of the Moon's orbit
    moon_inclination = 5.145396

    # Eccentricity of the Moon's orbit
    moon_eccentricity = 0.054900

    # Moon's angular size at distance a from Earth
    moon_angular_size = 0.5181

    # Semi-mojor axis of the Moon's orbit, in kilometers
    moon_smaxis = 384401.0
    # Parallax at a distance a from Earth
    moon_parallax = 0.9507

    # Synodic month (new Moon to new Moon), in days
    synodic_month = 29.53058868

    # Base date for E. W. Brown's numbered series of lunations (1923 January 16)
    lunations_base = 2423436.0

    ## Properties of the Earth

    earth_radius = 6378.16

c = AstronomicalConstants()

# Little handy mathematical functions.

fixangle = lambda a: a - 360.0 * floor(a/360.0)
torad = lambda d: d * pi / 180.0
todeg = lambda r: r * 180.0 / pi
dsin = lambda d: sin(torad(d))
dcos = lambda d: cos(torad(d))

NEW = 1
WAXING_CRESCENT = 2
FIRST_QUARTER = 3
WAXING_GIBBOUS = 4
FULL = 5
WANING_GIBBOUS = 6
LAST_QUARTER = 7
WANING_CRESCENT = 8


def phase_n(p):
    phase_ns = (
        (_NEW + PRECISION, NEW),
        (_FIRST - PRECISION, WAXING_CRESCENT),
        (_FIRST + PRECISION, FIRST_QUARTER),
        (_FULL - PRECISION, WAXING_GIBBOUS),
        (_FULL + PRECISION, FULL),
        (_LAST - PRECISION, WANING_GIBBOUS),
        (_LAST + PRECISION, LAST_QUARTER),
        (_NEXTNEW - PRECISION, WANING_CRESCENT),
        (_NEXTNEW + PRECISION, NEW))

    i = bisect.bisect([a[0] for a in phase_ns], p)

    return phase_ns[i][1]

def phase_string(p):
    phase_strings = { NEW: "new",
                      WAXING_CRESCENT: "waxing crescent",
                      FIRST_QUARTER: "first quarter",
                      WAXING_GIBBOUS: "waxing gibbous",
                      FULL: "full",
                      WANING_GIBBOUS: "waning gibbous",
                      LAST_QUARTER: "last quarter",
                      WANING_CRESCENT: "waning crescent" }
    return phase_strings[p]


def kepler(m, ecc):
    """Solve the equation of Kepler."""

    epsilon = 1e-6

    m = torad(m)
    e = m
    while 1:
        delta = e - ecc * sin(e) - m
        e = e - delta / (1.0 - ecc * cos(e))

        if abs(delta) <= epsilon:
            break

    return e


def phase(phase_date=int(time.time())):
    """Calculate phase of moon as a fraction:

    The argument is the time for which the phase is requested,
    expressed in either a DateTime or by Julian Day Number.

    Returns a dictionary containing the terminator phase angle as a
    percentage of a full circle (i.e., 0 to 1), the illuminated
    fraction of the Moon's disc, the Moon's age in days and fraction,
    the distance of the Moon from the centre of the Earth, and the
    angular diameter subtended by the Moon as seen by an observer at
    the centre of the Earth."""

    # Calculation of the Sun's position

    # Convert to JDN
    phase_date = ((phase_date / 86400) + 1) + 2440587.5

    # date within the epoch
    day = phase_date - c.epoch

    # Mean anomaly of the Sun
    N = fixangle((360/365.2422) * day)
    # Convert from perigee coordinates to epoch 1980
    M = fixangle(N + c.ecliptic_longitude_epoch - c.ecliptic_longitude_perigee)

    # Solve Kepler's equation
    Ec = kepler(M, c.eccentricity)
    Ec = sqrt((1 + c.eccentricity) / (1 - c.eccentricity)) * tan(Ec/2.0)
    # True anomaly
    Ec = 2 * todeg(atan(Ec))
    # Suns's geometric ecliptic longuitude
    lambda_sun = fixangle(Ec + c.ecliptic_longitude_perigee)

    # Orbital distance factor
    F = ((1 + c.eccentricity * cos(torad(Ec))) / (1 - c.eccentricity**2))

    # Distance to Sun in km
    sun_dist = c.sun_smaxis / F
    sun_angular_diameter = F * c.sun_angular_size_smaxis

    ########
    #
    # Calculation of the Moon's position

    # Moon's mean longitude
    moon_longitude = fixangle(13.1763966 * day + c.moon_mean_longitude_epoch)

    # Moon's mean anomaly
    MM = fixangle(moon_longitude - 0.1114041 * day - c.moon_mean_perigee_epoch)

    # Moon's ascending node mean longitude
    # MN = fixangle(c.node_mean_longitude_epoch - 0.0529539 * day)

    evection = 1.2739 * sin(torad(2*(moon_longitude - lambda_sun) - MM))

    # Annual equation
    annual_eq = 0.1858 * sin(torad(M))

    # Correction term
    A3 = 0.37 * sin(torad(M))

    MmP = MM + evection - annual_eq - A3

    # Correction for the equation of the centre
    mEc = 6.2886 * sin(torad(MmP))

    # Another correction term
    A4 = 0.214 * sin(torad(2 * MmP))

    # Corrected longitude
    lP = moon_longitude + evection + mEc - annual_eq + A4

    # Variation
    variation = 0.6583 * sin(torad(2*(lP - lambda_sun)))

    # True longitude
    lPP = lP + variation

    #
    # Calculation of the Moon's inclination
    # unused for phase calculation.
    
    # Corrected longitude of the node
    # NP = MN - 0.16 * sin(torad(M))

    # Y inclination coordinate
    # y = sin(torad(lPP - NP)) * cos(torad(c.moon_inclination))

    # X inclination coordinate
    # x = cos(torad(lPP - NP))

    # Ecliptic longitude (unused?)
    # lambda_moon = todeg(atan2(y,x)) + NP

    # Ecliptic latitude (unused?)
    # BetaM = todeg(asin(sin(torad(lPP - NP)) * sin(torad(c.moon_inclination))))

    #######
    #
    # Calculation of the phase of the Moon

    # Age of the Moon, in degrees
    moon_age = lPP - lambda_sun

    # Phase of the Moon
    moon_phase = (1 - cos(torad(moon_age))) / 2.0

    # Calculate distance of Moon from the centre of the Earth
    moon_dist = (c.moon_smaxis * (1 - c.moon_eccentricity**2))\
                / (1 + c.moon_eccentricity * cos(torad(MmP + mEc)))

    # Calculate Moon's angular diameter
    moon_diam_frac = moon_dist / c.moon_smaxis
    moon_angular_diameter = c.moon_angular_size / moon_diam_frac

    # Calculate Moon's parallax (unused?)
    # moon_parallax = c.moon_parallax / moon_diam_frac

    pp = fixangle(moon_age) / 360.0
    ppn = phase_n(pp)

    res = {
        'phase_n': pp,
        'illuminated': moon_phase,
        'age': c.synodic_month * fixangle(moon_age) / 360.0 ,
        'distance': moon_dist,
        'angular_diameter': moon_angular_diameter,
        'sun_distance': sun_dist,
        'sun_angular_diameter': sun_angular_diameter,
        'phase': ppn,
        'phase_str': phase_string(ppn)
        }

    return res

#
##
#

if __name__ == '__main__':
    for i in xrange(-10,40):
        q = int(time.time()) + (i * 24 * 3600)
        mm=time.localtime(q)
        mm,dd=mm.tm_mon,mm.tm_mday
        m = phase(q)
        s = """%d %d: The moon is %g, %s, %.1f%%, %.1f days old (%g).""" %\
            (mm, dd, m['phase'], m['phase_str'], m['illuminated'] * 100, m['age'], m['distance'])
        print (s)
