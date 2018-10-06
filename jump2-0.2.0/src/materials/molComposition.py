#coding=utf-8
'''
Created on Oct 24, 2017

@author: Yuhao Fu
'''
from __future__ import unicode_literals
from django.db import models

class MolComposition(models.Model):
    """
    Molecular Composition
    
    Relationships:
        composition
            |- structure
            |- element
        
    Attributes:
        composition
            |- formula: normalized composition. i.e. PbTiO3
            |- generic: generalized composition. i.e. ABO3
            |- mass: mass per formula.
            # ---------- database ----------
            |- structure_set
            |- element_set
            # ---------- build-in ----------
            |- structures
            |- elements
            
    分子的化学式类。
    
    关系:
        composition
            |- structure
            |- element
        
    属性:
        composition
            |- formula:约化的化学式。如，PbTiO3。
            |- generic:广义化学式。如，ABO3。
            |- mass:分子质量。
            # ---------- database ----------
            |- structure_set
            |- element_set
            # ---------- build-in ----------
            |- structures
            |- elements
    """
    # relationship
    element_set=models.ManyToManyField('MolElement')
    
    formula=models.CharField(primary_key=True, max_length=255)
    generic=models.CharField(max_length=255, blank=True, null=True)
    mass=models.FloatField(null=True)
    
    class Meta:
        app_label='materials'
        db_table='molComposition'
        default_related_name='composition_set'
        
    def __str__(self):
        return self.formula
    
    _structures=None
    @property
    def structures(self):
        """
        structures for the composition.
        
        属于该化学式的结构。
        """
        if self._structures is None:
            self._structures=[]
        return self._structures
    @structures.setter
    def structures(self, structures):
        """
        assign the value. Note that it will cover the previous value.
        
        Arguments:
            structures: collection of strucutre's object.
            
        Returns:
            True if the assignment is successful. Conversely, False.
            
        ‘structures’属性的set方法。注意：该方法将会清除以前的数据。
        
        参数：
            structures:结构对象集合。
            
        返回：
            布尔值（True/False）。
        """
        import warnings
        from materials.molStructure import MolStructure
        
        for structure in structures:
            if not isinstance(structure, MolStructure):
                warnings.warn('invalid type')
                return False
        self._structures=structures
        return True
    def add_strucutre(self, structure):
        """
        add a structure to this composition.
        
        Arguments:
            structure: structure's object.
            
        Returns:
            True if add a structure successfully. Conversely, False.
            
        添加一个结构到该化学式中。
        
        参数：
            structure:结构对象。
            
        返回：
            布尔值（True/False）。
        """
        from utils.check import exist
        
        if not exist(structure, self.structures, 'strucutre'):
            self.structures.append(structure)
            structure.composition=self
            return True
        else:
            return False
        
    _elements=None
    @property
    def elements(self):
        """
        elements for the composition.
        
        该化学式包含的元素。
        """
        from cache.cachedMolCompositionProvider import CachedMolCompositionProvider
        
        if self._elements is None:
            if not CachedMolCompositionProvider().get(self.formula):
                self._elements=[]
            else:
                self._elements=list(self.element_set.all())
        return self._elements
    @elements.setter
    def elements(self, elements):
        """
        assign the value. Note that it will cover the previous value.
        
        Arguments:
            elements: collection of element's object.
            
        Returns:
            True if the assignment is successful. Conversely, False.
            
        ‘elements’属性的set方法。注意：该方法将会清除以前的数据。
        
        参数：
            elements:元素对象集合。
            
        返回：
            布尔值（True/False）。
        """
        import warnings
        from materials.molElement import MolElement
        
        for element in elements:
            if not isinstance(element, MolElement):
                warnings.warn('invalid type')
                return False
        self._elements=elements
        return True
    def add_element(self, element):
        """
        add a element to this composition.
        
        Arguments:
            element: element's object or symbol.
            
        Returns:
            True if add a element successfully. Conversely, False.
            
        添加一个元素到这个化学式中。
        
        参数：
            element:元素对象或元素符号。
            
        返回：
            布尔值（True/False）。
        """
        from utils.check import exist
        from cache.cachedMolElementProvider import CachedMolElementProvider
        
        if not exist(element, self.elements, 'element'):
            if isinstance(element, basestring): # symbol
                symbol=element
                element=CachedMolElementProvider().get(symbol)
            self.elements.append(element)
            element.compositions.append(self) # update composition
            return True
        else:
            return False
    def get_element(self, symbol):
        """
        get the element's object with the given symbol.
        
        Arguments:
            symbol: element's symbol.
        
        Returns:
            element's object if it exists. Conversely, return the None.
            
        从化学式中获取给定符号的元素对象。
        
        参数：
            symbol:元素符号。如，H
        
        返回：
            如果结构中存在该元素，返回元素对象。否则，返回 None。
        """
        
        for element in self.elements:
            if element.symbol == symbol:
                return element
        return None
    def del_element(self, index_or_element, isUpdatedInfo=False, isPersist=False):
        """
        delete a element from this composition. Note that it will delete this element's object from other related classes's objects.
        
        Arguments:
            index_or_element: element's index, symbol or object.
            isUpdatedInfo (default=False): whether to update the composition and symmetry information (include the site, operation, wyckoffSite, spacegroup). 
            isPersist (default=False): whether to save to the database.
            
        从化学式中删除一个元素。注意：当删除元素时，基于程序效率上的考虑（可能会多次对结构进行操作，可以在所有的操作完成后，更新内存中内建的结构关联信息以及同步数据库中的数据），
        程序默认不会更新结构（更新化学式，删除与该元素关联的所有原子对象，等）
        
        参数：
            index_or_element:其值可以是元素在结构的元素属性数组中的索引（index）、元素符号或元素对象。
            isUpdatedInfo (default=False): 是否更新结构的其他关联数据信息（化学式、不等价位置，等）。
            isPersist (default=False):是否持久化，即将结构保存到数据库中。
            
        返回：
            布尔值（True/False）。
        """
        import warnings
        from materials.molElement import MolElement
        
        element=None
        if isinstance(index_or_element, int):
            index=index_or_element
            if index < 0 or index > len(self.elements):
                warnings.warn('beyond the range of elementary index')
                return False
            element=self.elements[index]
        elif isinstance(index_or_element, basestring):
            symbol=index_or_element
            element=self.get_element(symbol)
            if element is None:
                warnings.warn("can't find out this %s in the structure" % symbol)
                return False
        elif isinstance(index_or_element, MolElement):
            element=index_or_element
            if not element in self.elements:
                warnings.warn("this element isn't in this structure")
                return False
        else:
            warnings.warn('unrecognized index_or_element')
            return False
        
        # delete all atoms of this element
        for atom in list(element.atoms):
            if len(self.structures) != 1:
                warnings.warn("exist more than one structure in element.structures array, don't know which structure the element belong to")
                return None
            self.structures[0].del_atom(atom, isUpdatedInfo=False, isPersist=False)
        if isPersist:
            self.update(isPersist=isPersist)
        elif isUpdatedInfo and not isPersist:
            self.update(isPersist=False)       
        return True
        
    def create(self, formula, isPersist, **kwargs):
        """
        create a composition object.
        
        Arguments:
            formula: normalized composition. i.e. Pb1TiO3
                Note that need to be also given when atomic number of element is 1.
            isPersit: if True, save to database. Conversely, only run in memory.
            
            kwargs:
                structures: collection of structure's object.
                elements: collection of element's object or symbol.
                generic: generalized composition. i.e. ABO3
                
        创建一个化学式对象。
        
        参数：
            formula:约化的化学式。注意：当化学式中的元素的化学计量比等于1时，需要显示指定其计量比。如，Pb1TiO3。
            isPersit:是否持久化，即将结构保存到数据库中。

            kwargs:
                structures:结构对象集合。
                elements:元素对象或元素化学式的集合。
                generic:广义化学式。如，ABO3。
        
        返回：
            化学式对象。
        """   
        import re
        from cache.cachedMolElementProvider import CachedMolElementProvider
        from materials.molStructure import MolStructure
        from materials.molElement import MolElement
        
        self.formula=formula
        if isPersist:
            self.save()
        
        raw_formula=re.split('([0-9.]+)', formula)[:-1]
        mass=0
        
        element_symbols=[]
        for i in xrange(0, len(raw_formula), 2):
            element=CachedMolElementProvider().get(raw_formula[i])
            element_symbols.append(element.symbol)
            multi=float(raw_formula[i+1])
            mass += element.mass*multi
            
            if not 'elements' in kwargs:
                self.add_element(element)
                if isPersist:
                    self.element_set.add(element)
        
        if 'elements' in kwargs:
            elements=kwargs['elements']
            if len(elements) != len(element_symbols):
                raise ValueError('missing some element in elements')
            tmp=[element.symbol for element in elements]
            for element in elements:
                if isinstance(element, basestring):
                    symbol=element
                    tmp.append(symbol)
                elif isinstance(element, MolElement):
                    symbol=element.symbol
                    tmp.append(symbol)
                else:
                    raise ValueError('unrecognized element')

            for symbol in element_symbols:
                flag=False
                for stmp in tmp:
                    if stmp == symbol:
                        flag=True
                if not flag:
                    raise ValueError('missing %s' %symbol)
            for element in elements:
                if isinstance(element, basestring):
                    symbol=element
                    element=CachedMolElementProvider().get(symbol)
                self.add_element(element)
                if isPersist:
                    self.element_set.add(element)
                
        self.mass=mass
        
        if 'structures' in kwargs:
            structures=kwargs['structures']
            for structure in structures:
                if not isinstance(structure, MolStructure):
                    raise ValueError('unrecognized structure in structures')
                self.add_strucutre(structure)
                if isPersist:
                    self.structure_set.add(structure)
        if 'generic' in kwargs:
            generic=kwargs['generic']
            self.generic=generic
            
        if isPersist:
            self.save()
                
        return self
    
    