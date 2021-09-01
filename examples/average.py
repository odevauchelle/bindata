
import sys
sys.path.append('./../')

figure_path = '../figures/'

from pylab import *

x = linspace(0,1,500)
y = sin( 10*x ) + ( rand( len( x ) ) - .5 )

from bindata import bindata
X, Y = bindata( x, y ).apply()

plot( x, y, '.', alpha = .3, label = 'Raw' )
plot( X, Y, '-o', label = 'Binned' )
legend()
# savefig( figure_path + 'average.svg', bbox_inches = 'tight' )


show()
