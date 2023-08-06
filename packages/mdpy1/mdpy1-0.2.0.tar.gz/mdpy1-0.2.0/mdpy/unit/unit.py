#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
file : unit.py
created time : 2021/09/28
author : Zhenyu Wei
version : 1.0
contact : zhenyuwei99@gmail.com
copyright : (C)Copyright 2021-2021, Zhenyu Wei and Southeast University
'''

import numpy as np
from copy import deepcopy
from . import BaseDimension, UNIT_PRECISION
from ..error import UnitDimensionDismatchedError
from .. import env

class Unit:
    def __init__(self, base_dimension:BaseDimension, relative_value) -> None:
        '''
        Parameters
        ----------
        base_dimension : BaseDimension
            the dimension of unit
        relative_value : int or float
            the relative value of ``self`` to the basic unit of ``base_dimension``
        '''        
        self._base_dimension = base_dimension
        self._relative_value = env.UNIT_FLOAT(relative_value) # The relative value to the normal unit like angstrom in Length 

    def is_dimension_less(self):
        '''
        is_dimension_less judges wether ``self`` is dimensionless

        Returns
        -------
        bool
            - True, the unit is dimensionless
            - False, the unit isn't dimensionless
        '''        
        if self._base_dimension.is_dimension_less():
            return True
        else:
            return False
    
    def set_relative_value_to_one(self):
        '''
        set_relative_value_to_one sets ``self.relative_value = 1``
        '''        
        self._relative_value = 1

    def __repr__(self):
        return (
            '<Unit object: %.2e %s at 0x%x>'
            %(self._relative_value, self._base_dimension.name, id(self))
        )

    def __str__(self):
        return (
            '%.2e %s' %(self._relative_value, self._base_dimension.name)
        )

    def __eq__(self, other) -> bool:
        err = np.abs((self._relative_value - other.relative_value)/self._relative_value)
        if (
            self._base_dimension == other.base_dimension and
            err < UNIT_PRECISION
        ):
            return True
        else:
            return False

    def __ne__(self, other) -> bool:
        return not self == other

    def __add__(self, other):
        if isinstance(other, Unit):
            if (
                self._base_dimension == other.base_dimension
            ):
                return deepcopy(self)
            else:
                raise UnitDimensionDismatchedError(
                    '%s and %s can\'t be added together'
                    %(self._base_dimension, other.base_dimension)
                )
        else:
            raise NotImplementedError(
                '+ between %s and mdpy.unit.Unit is not implemented' 
                %(type(other))
            )
    
    __iadd__ = __add__

    def __radd__(self, other):
        if isinstance(other, Unit):
            if (
                self._base_dimension == other.base_dimension
            ):
                return deepcopy(other)
            else:
                raise UnitDimensionDismatchedError(
                    '%s and %s can not be added'
                    %(other.base_dimension, self._base_dimension)
                )
        else:
            raise NotImplementedError(
                '+ between mdpy.unit.Unit and %s is not implemented' 
                %(type(other))
            )

    def __sub__(self, other):
        if isinstance(other, Unit):
            if (
                self._base_dimension == other.base_dimension
            ):
                return deepcopy(self)
            else:
                raise UnitDimensionDismatchedError(
                    '%s and %s can not be subbed'
                    %(self._base_dimension, other.base_dimension)
                )
        else:
            raise NotImplementedError(
                '- between %s and mdpy.unit.Unit is not implemented' 
                %(type(other))
            )

    __isub__ = __sub__

    def __rsub__(self, other):
        if isinstance(other, Unit):
            if (
                self._base_dimension == other.base_dimension
            ):
                return deepcopy(other)
            else:
                raise UnitDimensionDismatchedError(
                    '%s and %s can not be subbed'
                    %(other.base_dimension, self._base_dimension)
                )
        else:
            raise NotImplementedError(
                '- between mdpy.unit.Unit and %s is not implemented' 
                %(type(other))
            )

    def __mul__(self, other):
        if isinstance(other, Unit):
            return Unit(
                self._base_dimension * other.base_dimension,
                self._relative_value * other.relative_value
            )
        else:
            raise NotImplementedError(
                '* between %s and mdpy.unit.Unit is not implemented' 
                %(type(other))
            )

    __imul__ = __mul__
    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, Unit):
            return Unit(
                self._base_dimension / other.base_dimension,
                self._relative_value / other.relative_value
            )
        else:
            raise NotImplementedError(
                '/ between %s and mdpy.unit.Unit is not implemented' 
                %(type(other))
            )

    __itruediv__ = __truediv__

    def __rtruediv__(self, other):
        if isinstance(other, Unit):
            return Unit(
                other.base_dimension / self._base_dimension,
                other.relative_value / self._relative_value
            )
        elif isinstance(other, int) and other == 1:
            return Unit(
                self._base_dimension**-1,
                1 / self._relative_value
            )
        else:
            raise NotImplementedError(
                '/ between mdpy.unit.Unit and %s is not implemented' 
                %(type(other))
            )

    def __pow__(self, value):
        try:
            len(value)
        except:
            return Unit(
                self._base_dimension**value,
                self._relative_value**value
            )
        raise ValueError('The power term should be a single number')
        

    def sqrt(self):
        '''
        sqrt returns square root of Unit

        Returns
        -------
        Unit
            square root of ``self``
        '''        
        return Unit(
            self._base_dimension.sqrt(),
            np.sqrt(self._relative_value)
        )
            
    @property
    def unit_name(self):
        '''
        unit_name gets the name of the unit

        Returns
        -------
        str
            the name of unit
        '''        
        return self.base_dimension.name

    @property
    def base_dimension(self):
        '''
        base_dimension gets the dimension of the unit

        Returns
        -------
        BaseDimension
            the dimension of unit
        '''        
        return self._base_dimension

    @property
    def relative_value(self):
        '''
        relative_value gets the relative value to the basic unit

        Returns
        -------
        int or float
            the relative value to the basic unit
        '''        
        return self._relative_value