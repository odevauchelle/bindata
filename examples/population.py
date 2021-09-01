
import sys
sys.path.append('./../')

figure_path = '../figures/'

from pylab import *

x = linspace(0,1,500)
y = sin( 10*x ) + ( rand( len( x ) ) - .5 )

from bindata import bindata

b = bindata( x, y, nbins = 15 )


print( b.nb )

# print( b.apply()[0] )

print( b.apply( empty_as_nan = False )  )

# savefig( figure_path + 'population.svg', bbox_inches = 'tight' )
#
#
show()
