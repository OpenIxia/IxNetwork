from ixnetwork_restpy.base import Base
from ixnetwork_restpy.steps import Steps


class Multivalue(Base):
    def __init__(self, parent, href):
        super(Multivalue, self).__init__(parent)        
        self._href = href
        self._pattern = None

    def _format_value(self, value):
        if self._properties['format'] == 'bool':
            return '%s%s' % (value[0].upper(), value[1:])
        return value

    @property
    def Pattern(self):
        """The current pattern represented as a string.

        Returns: str
        """
        if self._pattern is None:
            self._custom_select()
        if self._properties['pattern'] == 'singleValue':
            self._pattern = self._format_value(self._properties['singleValue']['value'])
        elif self._properties['pattern'] == 'counter':
            start = self._format_value(self._properties['counter']['start'])
            step = self._format_value(self._properties['counter']['step'])
            if self._properties['counter']['direction'] == 'decrement':
                self._pattern = 'Dec: %s, %s' % (start, step)
            else:
                self._pattern = 'Inc: %s, %s' % (start, step)
        elif self._properties['pattern'] == 'valueList':
            self._pattern = 'List: %s' % (', '.join(self._properties['values']))
        elif self._properties['pattern'] == 'repeatableRandomRange':
            min_value = self._properties['repeatableRandomRange']['min']
            max_value = self._properties['repeatableRandomRange']['max']
            step_value = self._properties['repeatableRandomRange']['step']
            seed = self._properties['repeatableRandomRange']['seed']
            self._pattern = 'Randr: %s, %s, %s, %s' % (min_value, max_value, step_value, seed)
        elif self._properties['pattern'] == 'repeatableRandom':
            fixed_value = self._properties['repeatableRandom']['fixed']
            mask_value = self._properties['repeatableRandom']['mask']
            seed = self._properties['repeatableRandom']['seed']
            count = self._properties['repeatableRandom']['count']
            self._pattern = 'Randb: %s, %s, %s, %s' % (fixed_value, mask_value, seed, count)
        elif self._properties['pattern'] == 'random':
            self._pattern = 'Rand'
        elif self._properties['pattern'] == 'alternate':
            self._pattern = 'Alt: %s' % self._format_value(self._properties['alternate']['value'])
        elif self._properties['pattern'] == 'customDistributed':
            values = []
            for value_pair in self._properties['customDistributed']['values']:
                values.append('(%s, %s)' % (self._format_value(value_pair['arg1']), value_pair['arg2']))
            algorithm = self._properties['customDistributed']['algorithm']
            mode = self._properties['customDistributed']['mode']
            self._pattern = 'Dist: %s, %s, [%s]' % (algorithm, mode, ','.join(values))
        elif self._properties['pattern'] == 'custom':
            increments = []
            if 'increment' in self._properties['custom'].keys():
                self._add_increments(increments, self._properties['custom']['increment'])
            start = self._properties['custom']['start']
            step = self._properties['custom']['step']
            self._pattern = 'Custom: %s, %s, [%s]' % (start, step, ','.join(increments))
        elif self._properties['pattern'] == 'string':
            self._pattern = self._properties['string']['pattern']
        return self._pattern

    def _add_increments(self, increments, increment):
        for item in increment:
            child_increments = []
            if 'increment' in item.keys():
                self._add_increments(child_increments, item['increment'])     
            increments.append('(%s, %s, [%s])' % (item['value'], item['count'], ','.join(child_increments)))

    def __str__(self):
        return self.Pattern

    def __repr__(self):
        return self.Pattern

    def __eq__(self, other):
        return self.Pattern == other

    @property
    def Info(self):
        info = 'Multivalue: %s\n' % self.Source
        info += '\tFormat: %s\n' % self.Format
        info += '\tCount: %s\n' % self.Count
        info += '\tValid Patterns: %s\n' % ' '.join(self.AvailablePatterns)
        return info

    @property
    def Format(self):
        self.Pattern
        return self._properties['format']

    @property
    def Source(self):
        self.Pattern
        return self._properties['source']
    
    @property
    def Count(self):
        self.Pattern
        return self._properties['count']

    @property
    def AvailablePatterns(self):
        """list(str): returns a list of methods in this class that are valid for setting a pattern for this multivalue"""
        self.Pattern
        for unsupported in ['shared', 'subset']:
            self._properties['availablePatterns'].remove(unsupported)
        return self._properties['availablePatterns']

    @property
    def AvailableEnums(self):
        """list(str): if the format of the multivalue is enum this will return a list of possible enum choices that can be used when setting patterns"""
        self.Pattern
        return self._properties['enums']

    @property
    def Values(self):
        """list(str): returns a list of the values encapsulated by the pattern, format and count"""
        self.Pattern
        return self._properties['values']

    def Single(self, value):
        """Set the pattern to a single value"""
        self._set_pattern('singleValue', {'value': value})

    def Alternate(self, alternating_value):
        """Set the pattern to alternating"""
        self._set_pattern('alternate', {'value': alternating_value})

    def Increment(self, start_value=None, step_value=None):
        """Set the pattern to incrementing"""
        payload = {
            'direction': 'increment'
        }
        if start_value is not None:
            payload['start'] = start_value
        if step_value is not None:
            payload['step'] = step_value
        self._set_pattern('counter', payload)

    def Decrement(self, start_value=None, step_value=None):
        """Set the pattern to decrementing"""
        payload = {
            'direction': 'decrement'
        }
        if start_value is not None:
            payload['start'] = start_value
        if step_value is not None:
            payload['step'] = step_value
        self._set_pattern('counter', payload)

    def ValueList(self, values):
        """Set the pattern to valueList"""
        self._set_pattern('valueList', {'values': values})

    def RandomRange(self, min_value=None, max_value=None, step_value=None, seed=None):
        """Set the repeatable random range pattern

        Args:
            min_value (str): Minimum value according to the format property
            max_value (str): Maximum value according to the format property
            step_value (str): Step value accoroding to the format property
            seed (int): Seed value
        """
        payload = {
            'min': min_value,
            'max': max_value,
            'step': step_value,
            'seed': seed
        }
        self._set_pattern('repeatableRandomRange', payload)

    def RandomMask(self, fixed_value=None, mask_value=None, seed=None, count=None):
        """Set the repeatable random pattern

        Args:
            fixed_value (str): Minimum value according to the format property
            mask_value (str): Maximum value according to the format property
            seed (int): Seed value 
            count (int): Count value
        """        
        payload = {
            'fixed': fixed_value,
            'mask': mask_value,
            'seed': seed,
            'count': count
        }
        self._set_pattern('repeatableRandom', payload)

    def Random(self):
        self._set_pattern('random')

    def Distributed(self, algorithm=None, mode=None, values=None):
        """Set the pattern to customDistributed

        Args:
            algorithm (str[enum:percentage|weighted|autoEven|autoGeometric]): The algorithm of the distribution
            mode (str[enum:perDevice|perTopology|perPort]): The mode of the distribution
            values (list[tuple(value, weight)]): A list of values and weights
        """
        formatted_values = None
        if values is not None:
            formatted_values = []
            for value in values:
                formatted_values.append({'arg1': self._format_value(value[0]), 'arg2': value[1]})
        payload = {
            'algorithm': algorithm,
            'mode': mode,
            'values': formatted_values
        }
        self._set_pattern('customDistributed', payload)

    def ValueList(self, values=None):
        """Set the pattern to valueList
        """
        formatted_values = None
        if values is not None:
            formatted_values = []
            for value in values:
                formatted_values.append(self._format_value(value))
        payload = {
            'values': formatted_values
        }
        self._set_pattern('valueList', payload)

    def String(self, string_pattern=None):
        """Set the pattern to a string pattern

        Args:
            string_pattern (str): A string pattern
                Examples:
                    Test-{Inc:1,1}
                    Test-{"A", "B", "C"}
                    hex_{Dec:0xFFFF}
                    Test-{Inc:100}-{"A", "B"}-{Dec:3, 1, 3}
        """
        payload = {
            'pattern': string_pattern
        }
        self._set_pattern('string', payload)

    def Custom(self, start_value=None, step_value=None, increments=None):
        """Set the pattern to custom

        Args:
            start_value (str): A start value according to the format
            step_value (str): A step value according to the format
            increments (list[tuple(value, count, list[increments])]): Customize the start and step values by adding sibling and/or nested increments.
                The list contains 0..n increments.
                Each increment is a tuple that consists of a value according to the format, a count and any nested increments.
        """
        payload = {
            'start': start_value,
            'step': step_value
        }
        self._set_pattern('custom', payload)
        self._connection._delete('%s/custom/increment' % self._properties['href'])
        self._add_custom_increments('%s/custom' % self._properties['href'], increments)
        self._custom_select()

    def _add_custom_increments(self, href, increments):
        if increments is not None:
            href = '%s/increment' % href
            for increment in increments:
                payload = {
                    'value': increment[0],
                    'count': increment[1]
                }
                
                response = self._connection._create(href, payload)
                self._add_custom_increments(response['links'][0]['href'], increment[2])

    def Steps(self, Description=None, Enabled=None, Owner=None, Value=None):
        """Get the list of possible Steps for this multivalue.
        A Steps object provides the ability to set a step value for a multivalue pattern.
        The most common step is the port step which 'steps' the multivalue pattern by a value as it crosses from port to port.

        Returns:
            list(obj(ixnetwork_restpy.steps.Steps)): A list of Steps objects
        """
        from ixnetwork_restpy.steps import Steps
        return Steps(self)._select(locals())

    def _set_pattern(self, pattern, payload=None):
        self.Pattern
        href = '%s/%s' % (self._href, pattern)
        if payload is not None:
            for key in payload.copy():
                if payload[key] is None:
                    payload.pop(key)
        if bool(payload) is False:
            payload = None
        if pattern == self._properties['pattern']:
            self._connection._update(href, payload)
        elif payload is not None:
            self._connection._create(href, payload)
        else:
            self._connection._update(self._href, {'pattern': pattern})
        self._custom_select()

    def _custom_select(self):
        payload = {
            'selects': [
                {
                    'from': self._href,
                    'properties': ['*'],
                    'children': [
                        {
                            'child': '(singleValue|alternate|random|repeatableRandom|repeatableRandomRange|counter|valueList|custom|customDistributed|increment|string)',
                            'properties': ['*'],
                            'filters': []
                        }
                    ],
                    'inlines': []
                }
            ]
        }
        end = self._href.index('ixnetwork') + len('ixnetwork')
        url = '%s/operations/select' % self._href[0:end]
        self._set_properties(self._connection._execute(url, payload)[0])
