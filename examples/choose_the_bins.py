
import sys
sys.path.append('./../')

figure_path = '../figures/'

from pylab import *

with open('seed.txt') as the_file :
    seed( int( the_file.readline() ) )

x = linspace(0,1,500)
y = sin( 10*x ) + ( rand( len( x ) ) - .5 )

from bindata import bindata

X, Y = bindata( x, y, bins = linspace(0,.5,10) ).apply()

plot( x, y, '.', alpha = .3)
plot( X, Y, 'o' )

# savefig( figure_path + 'choose_the_bins.svg', bbox_inches = 'tight' )


show()
