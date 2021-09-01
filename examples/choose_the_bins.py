
import sys
sys.path.append('./../')

figure_path = '../figures/'

from pylab import *

x = linspace(0,1,500)
y = sin( 10*x ) + ( rand( len( x ) ) - .5 )

from bindata import bindata

X, Y = bindata( x, y, bins = [0, .1, .2, .3, .4, .5, 1] ).apply()

plot( x, y, '.', alpha = .3)
plot( X, Y, 'o' )

savefig( figure_path + 'choose_the_bins.svg', bbox_inches = 'tight' )


show()
