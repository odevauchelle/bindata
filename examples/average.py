
import sys
sys.path.append('./../')

figure_path = '../figures/'

from pylab import *

with open('seed.txt') as the_file :
    seed( int( the_file.readline() ) )

x = linspace(0,1,500)
y = 2*x + sin( 10*x ) + ( rand( len( x ) ) - .5 )

from bindata import bindata

b  = bindata( x, y, drop_outliers = False )
X, Y = b.apply()

print(b.nb)

plot( x, y, '.', alpha = .3, label = 'Raw' )
plot( X, Y, '-o', label = 'Binned' )
legend()
# savefig( figure_path + 'average.svg', bbox_inches = 'tight' )




show()
