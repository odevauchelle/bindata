
import numpy as np


class bindata :

    def __init__( self, *data, bins = 'linear', nbins = 10 ) :

        self.nb_variables = len(data)
        x = data[0]

        ################
        # Create bins
        ################

        if bins == 'linear' :
            self.bins = np.linspace( min(x), max(x), nbins )

        elif bins == 'log' :
            self.bins = np.logspace( np.log10( min(x) ), np.log10( max(x) ), nbins )

        else :
            self.bins = bins

        ################
        # Distribute data in bins
        ################

        indices = np.digitize( x, self.bins )

        self.data = [ [ ] ]*( len( self.bins ) + 1 )
        self.nb = [ 0 ]*( len( self.bins ) + 1 )

        for index in set( indices ) :

            selection = indices == index
            self.nb[ index ] = sum( selection )
            self.data[ index ] = [ data[ selection ] for data in data ]

    def get( self, stat = 'mean', empty_as_nan = True ) :

        if stat == 'mean' :
            stat = np.mean

        output = []

        for bin in self.data :

            output += [ [ stat( bin ) for bin in bin ] ]

            if empty_as_nan and len( output[-1] ) == 0 :
                output[-1] = [ np.nan ]*self.nb_variables

        return tuple( np.array( output ).T )

if __name__ == '__main__' :

    from pylab import *

    x = linspace(0,1,500)
    y = sin( 10*x ) + ( rand( len( x ) ) - .5 )

    plot(x,y,'.', alpha = .3)


    b = bindata( x, y )

    print(b.nb)

    errorbar( *b.get(), *b.get(std)[::-1], 'o' )
    show()


    # print(help(std))

    # print( len( binned_data.data ) )

    # print( distribute_in_bins( x, bins ) )


# def bin_data( x, y, bins = None, nb_bins = 10, **statistics ) :
#
#     if statistics == {} :
#         statistics = { 'mean' : np.mean }
#

#
#     output = { 'bins' : bins, 'nb_points' : [] }
#
#     for key in statistics.keys() :
#
#         output[key] = [ [], [] ]
#
#     print(bins)
#
#     indices = np.digitize( x, bins )
#
#     for index in set( indices ) :
#
#         selection = indices == index
#
#         output['nb_points'] += [ sum(selection) ]
#
#         for key in statistics.keys() :
#
#             output[key][0] += [ statistics[key]( x[ selection ] ) ]
#             output[key][1] += [ statistics[key]( y[ selection ] ) ]
#
#     return output
