
import sys
sys.path.append('./../')

figure_path = '../figures/'

from pylab import *

with open('seed.txt') as the_file :
    seed( int( the_file.readline() ) )

x = linspace(0,1,500)
y = sin( 10*x ) + ( rand( len( x ) ) - .5 )

from bindata import bindata
b = bindata( x, y, nbins = 15 )
X, Y = b.apply( mean )
sigma_x, sigma_y = b.apply( std )

plot( x, y, '.', alpha = .3)
errorbar( X, Y, sigma_y, sigma_x, 'o', zorder = 10 )

# savefig( figure_path + 'not_just_averages.svg', bbox_inches = 'tight' )


show()
