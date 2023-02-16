
import sys
sys.path.append('./../')

figure_path = '../figures/'

from pylab import *

with open('seed.txt') as the_file :
    seed( int( the_file.readline() ) )

x = linspace(0,1,200)
y = sin( 10*x ) + ( rand( len( x ) ) - .5 )

from bindata import bindata

bd = bindata( x, y, bins = linspace(0.2,.6,10), drop_outliers = True )
X, Y = bd.apply()

plot( x, y, '.', alpha = .3)
plot( X, Y, 'o' )

for bin_boundary in bd.bins :
    axvline( bin_boundary, color = 'k', alpha = .1 )

savefig( figure_path + 'choose_the_bins.svg', bbox_inches = 'tight' )


show()
