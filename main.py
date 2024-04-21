#
# Solver for a single loop magnetic core or a branched core consisting of a central part and two parallel branches
#
# Dr. Dmitriy Makhnovskiy, City College Plymouth, England
# 21.04.2024
#

# Constants
pi = 3.1415926535897932384626433832795
mu0 = 4.0 * pi * 1.0e-7  # vacuum magnetic permeability (H/m)

# Input parameters
mu = 1540.0  # core relative magnetic permeability (dimensionless)
g = 0.2  # gap (mm) in the single loop or central part
N = 50  # number of turns of the coil
I = 0.5  # current (A) through the coil
branch = 2  # single loop core (1) or branched core (2)

# If the single loop core (otherwise ignore):
l1 = 0.0  # length of the core in mm
A1 = 0.0  # cross-section of the core in mm^2

# If the branched core (otherwise ignore):
lc = 29.3  # length of the central part in mm
Ac = 123.21  # cross-section of the central part in mm^2
lb = 59.1  # length of each branch part in mm
Ab = 61.605  # cross-section of the branch part in mm^2

# Calculations
g = g * 1.0e-3  # gap length in m
if branch == 1:
    A1 = A1 * 1.0e-6  # area in m^2
    l1 = l1 * 1.0e-3  # length in m minus the gap
    R1 = (l1 - g) / (mu * mu0 * A1) + g / (mu0 * A1)  # total reluctance
    Flux1 = I * N / R1  # magnetic flux (Wb) in the core
    B1 = Flux1 / A1  # magnetic induction (T) in the core
    L1 = N ** 2 / R1  # coil inductance (H)
    mue1 = l1 / (mu0 * A1 * R1)  # effective permeability
elif branch == 2:
    lc = lc * 1.0e-3  # length in m
    lb = lb * 1.0e-3  # length in m
    Ac = Ac * 1.0e-6  # area in m^2
    Ab = Ab * 1.0e-6  # area in m^2
    Rc = (lc - g) / (mu * mu0 * Ac) + g / (mu0 * Ac)  # reluctance of the central part
    Rb = lb / (mu * mu0 * Ab)  # reluctance of the branch part
    R2 = Rc + Rb / 2.0  # total reluctance of the core consisting of the central part and two parallel branches
    Flux2 = I * N / R2  # magnetic flux (Wb) in the central part
    Bc = Flux2 / Ac  # magnetic induction (T) in the central part
    Bb = Flux2 / (2.0 * Ab)  # magnetic induction (T) in the branch part
    L2 = N ** 2 / R2  # coil inductance (H)
    mue2 = (lc / Ac + lb / (2.0 * Ab)) / (mu0 * R2)  # effective permeability of the core with the gap

print('')
# Output parameters
if branch == 1:
    print('SINGLE LOOP CORE:')
    print('Reluctance R = ', "{:.3e}".format(R1), ' 1/H')
    print('Inductance factor AL =  ', "{:.3e}".format(1.0 / R1), ' H (Inductance = AL x N^2)')
    print('Magnetic flux Ф = ', "{:.3e}".format(Flux1), ' Wb')
    print('Magnetic induction B = ', "{:.3e}".format(B1), ' T')
    print('Coil inductance L = ', "{:.3e}".format(L1), ' H')
    print('Effective permeability mu_e = ', round(mue1, 3))
elif branch == 2:
    print('BRANCHED CORE:')
    print('Total reluctance R = ', "{:.3e}".format(R2), ' 1/H')
    print('Inductance factor AL =  ', "{:.3e}".format(1.0 / R2), ' H (Inductance = AL x N^2)')
    print('Reluctance of the central part Rc = ', "{:.3e}".format(Rc), ' 1/H')
    print('Reluctance of the branch part Rb = ', "{:.3e}".format(Rb), ' 1/H')
    print('Magnetic flux in the central part Фc = ', "{:.3e}".format(Flux2), ' Wb')
    print('Magnetic induction in the central part Bc = ', "{:.3e}".format(Bc), ' T')
    print('Magnetic induction in the branch part Bb = ', "{:.3e}".format(Bb), ' T')
    print('Coil inductance L = ', "{:.3e}".format(L2), ' H')
    print('Effective permeability mu_e = ', round(mue2, 3))
