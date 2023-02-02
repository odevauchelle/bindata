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

def equal_size_indices( x, nbins ) :

    n = len(x)
    bin_size = n//nbins
    total_nb_of_larger_bins = n%nbins

    indices = []
    nb_of_larger_bins = 0

    for i in range( nbins ) :
        if nb_of_larger_bins < total_nb_of_larger_bins :
            indices += [ i ]*( bin_size + 1 )
        else :
            indices += [ i ]*bin_size

    indices = list( np.array(indices)[ np.argsort( x ) ] )

    return indices

def linear_bins( x, nbins, margin = 1e-6 ) :

    x_min, x_max = np.nanmin(x), np.nanmax(x)
    bin_size = ( x_max - x_min )/nbins
    margin *= bin_size
    x_min, x_max = x_min - margin, x_max + margin

    return np.linspace( x_min, x_max, nbins )

def log_bins( x, nbins, margin = 1e-6 ) :

    log_x = np.log( np.array( [ np.nanmin(x), np.nanmax(x) ] ) )

    return np.exp( linear_bins( log_x, nbins, margin ) )

class bindata :
    '''
    Stores data into bins.
    '''

    def __init__( self, *data, bins = 'linear', nbins = 10, indices = None, binning_data = 0, as_array = True, drop_outliers = True ) :
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
        indices : A list of ingeger indices, if not None, overrides bins and nbins.
        binning_data: The index of the data with respect to which the binning is done.
        as_array (True): Whether to treat the data as numpy arrays
        drop_outliers (True): Whether to drop the data that lies outside the bins

        Output:
        b : The bindata object that stores x and y into bins.
        '''

        if as_array :
            data = np.array(data)

        self.nb_variables = len(data)
        x = data[binning_data]

        ################
        # Create bins
        ################

        if indices is None : # indices are not provided

            try : # bins is a string

                bins + ''

                if bins == 'equal_size' :

                    self.bins = None
                    self.indices = equal_size_indices( x, nbins )

                else :

                    if bins == 'linear' :
                        self.bins = linear_bins( x, nbins )

                    elif bins == 'log' :
                        self.bins = log_bins( x, nbins )

            except : # bins is a list of values
                self.bins = bins

            try : # indices already exist
                self.indices
            except : # indices are set by digitization into bins
                self.indices = np.digitize( x, self.bins ) # digitize

            self.set_of_indices = set( self.indices ) # only for the bins where there's something

            try : # if bins exist
                self.nbins = len(bins) + 1 # o|o|o|o
            except : # there are no bins, only indices
                self.nbins = len( self.set_of_indices )

        else : # indices are provided, bins are not necessary
            self.bins = bins # could be None
            self.indices = indices
            self.set_of_indices = set( self.indices )
            self.nbins = len( self.set_of_indices )

        if drop_outliers and not self.bins is None :

            self.nbins -= 2 # |o|o|
            self.indices -= 1
            self.indices = self.indices[ ( self.indices >= 0 )*( self.indices < self.nbins ) ]
            self.set_of_indices = set( self.indices )

        ################
        # Distribute data into bins
        ################

        self.data = [ [ ] ]*self.nbins
        self.nb = [ 0 ]*self.nbins

        for index in self.set_of_indices :

            selection = np.where( self.indices == index )[0]
            self.nb[ index ] = len( selection )
            self.data[ index ] = [ data[ selection ] for data in data ]


    def apply( self, stat = None, empty_as_nan = True, sorted = False ) :
        '''
        Evaluate a statistical function on each bin.

        X, Y = bindata.apply( stat = None, empty_as_nan = True, sorted = False )

        Arguments:
        stat : A function that applies to a 1D data set and returns a scalar (e.g. np.mean).
        empty_as_nan (Boolean) : whether empty bins result in np.nan.
        sorted (Boolean) : whether to sort the bins according to first data row
        '''

        if stat is None :
            stat = np.mean

        output = []

        for bin in self.data :

            output += [ [ stat( bin ) for bin in bin ] ]

            if len( output[-1] ) == 0 :
                output[-1] = [ np.nan ]*self.nb_variables

        output = np.array( output ).T

        if sorted :
            output = output[ :, np.argsort( output[0,:] ) ]

        if not empty_as_nan :
            output = output[ :, np.where( np.product( ~np.isnan( output ), axis = 0 ) )[ 0 ] ]

        return tuple( output )

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

    # bb = bindata(x)
    #
    # print( bb.apply() )

    show()
