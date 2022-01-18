#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Olivier Devauchelle, 2021
#
# The original idea, and initial implementation, is from A.P. Petroff.

import numpy as np

def equal_size_bins( x, nbins ) :

    bin_size = int( len(x)/nbins )
    indices = []

    for i in range( nbins ) :
        indices += [ i ]*bin_size

    indices += [ indices[-1] + 1 ]*( len(x) - len( indices ) )
    indices = list( np.array(indices)[ np.argsort( x ) ] )

    return indices

def linear_bins( x, nbins, margin = 1e-6 ) :

    x_min, x_max = np.nanmin(x), np.nanmax(x)
    bin_size = ( x_max - x_min )/nbins
    margin *= bin_size
    x_min, x_max = x_min - margin, x_max + margin

    return np.linspace( x_min, x_max, nbins )

def log_bins( x, nbins, margin = 1e-6 ) :

    log_x = np.log( array( [ np.nanmin(x), np.nanmax(x) ] ) )

    return exp( linear_bins( log_x, nbins, margin ) )

class bindata :
    '''
    Stores data into bins.
    '''

    def __init__( self, *data, bins = 'linear', nbins = 10, indices = None, binning_data = 0 ) :
        '''
        Creates a bindata object, which stores data into bins.

        b = bindata( x, y, bins = 'linear', nbins = 10 )

        Arguments:
        x : A 1D list of data. The bining is based on x.
        y : Another list of data, which will be binned according to x. Same length as x.
        ... : Any number of additional data list.

        Keyword Arguments:
        bins : A monotonic list of bins. If 'linear', 'log' or 'equal_size', the bins will be created automatically.
        nbins : Number of bins. Overridden by bins.
        binning_data: The index of the data with respect to which the binning is done.

        Output:
        b : The bindata object that stores x and y into bins.
        '''

        self.nb_variables = len(data)
        x = data[binning_data]

        ################
        # Create bins
        ################

        if indices is None :

            try :
                bins + ''

                if bins == 'equal_size' :

                    self.bins = None
                    self.indices = equal_size_bins( x, nbins )

                else :

                    if bins == 'linear' :
                        self.bins = linear_bins( x, nbins )

                    elif bins == 'log' :
                        self.bins = log_bins( x, nbins )

            except :
                self.bins = bins

            self.indices = np.digitize( x, self.bins )

        else :
            self.bins = None
            self.indices = indices

        self.set_of_indices = set( self.indices )

        try :
            self.nbins = len( self.bins ) + 1
        except :
            self.nbins = len( self.set_of_indices )

        ################
        # Distribute data into bins
        ################

        self.data = [ [ ] ]*self.nbins
        self.nb = [ 0 ]*self.nbins

        for index in self.set_of_indices :

            selection = np.where( self.indices == index )[0]
            self.nb[ index ] = len( selection )
            self.data[ index ] = [ data[ selection ] for data in data ]


    def apply( self, stat = None, empty_as_nan = True ) :
        '''
        Evaluate a statistical function on each bin.

        X, Y = bindata.apply( stat = None, empty_as_nan = True )

        Arguments:
        stat : A function that applies to a 1D data set and returns a scalar (e.g. np.mean).
        empty_as_nan (Boolean) : whether empty bins result in np.nan.
        '''

        if stat is None :
            stat = np.mean

        output = []

        for bin in self.data :

            output += [ [ stat( bin ) for bin in bin ] ]

            if empty_as_nan and len( output[-1] ) == 0 :
                output[-1] = [ np.nan ]*self.nb_variables

        return tuple( np.array( output ).T )

########################
#
# Try it out
#
########################


if __name__ == '__main__' :

    from pylab import *

    # x = linspace(0,1,73)
    x = logspace( -2, 0, 105 )
    y = sin( 10*x ) + ( rand( len( x ) ) - .5 )

    plot( x, y, '.', alpha = .3)

    # print( equal_size_bins( y, 10 ) )

    b = bindata( x, y, bins = 'equal_size' )

    print(b.nb)

    errorbar( *b.apply(), *b.apply(std)[::-1], 'o' )

    bb = bindata(x)

    print( bb.apply() )

    show()
