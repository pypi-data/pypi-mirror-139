import xmatters.connection


class Property(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(Property, self).__init__(parent, data)
        self.id = data.get('id')  #: :vartype: str
        self.property_type = data.get('propertyType')  #: :vartype: str
        self.name = data.get('name')  #: :vartype: str
        self.description = data.get('description')  #: :vartype: str
        self.help_text = data.get('helpText')  #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Boolean(Property):
    def __init__(self, parent, data):
        super(Boolean, self).__init__(parent, data)
        self.default = data.get('default')  #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Hierarchy(Property):
    def __init__(self, parent, data):
        super(Hierarchy, self).__init__(parent, data)
        self.default = data.get('default')  #: :vartype: str
        self.delimiter = data.get('delimiter')  #: :vartype: str
        self.categories = data.get('categories', [])  #: :vartype: list
        self.paths = data.get('paths', [])  #: :vartype: list

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class MultLinkSelectList(Property):
    def __init__(self, parent, data):
        super(MultLinkSelectList, self).__init__(parent, data)
        self.items = data.get('items', [])  #: :vartype: list

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SingleSelectList(Property):
    def __init__(self, parent, data):
        super(SingleSelectList, self).__init__(parent, data)
        self.items = data.get('items', [])  #: :vartype: list

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Number(Property):
    def __init__(self, parent, data):
        super(Number, self).__init__(parent, data)
        self.default = data.get('default')  #: :vartype: str
        self.max_length = data.get('maxLength')  #: :vartype: int
        self.min_length = data.get('minLength')  #: :vartype: int
        self.units = data.get('units')  #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Password(Property):
    def __init__(self, parent, data):
        super(Password, self).__init__(parent, data)
        self.max_length = data.get('maxLength')  #: :vartype: int
        self.min_length = data.get('minLength')  #: :vartype: int
        self.pattern = data.get('pattern')  #: :vartype: str
        self.validate = data.get('validate')  #: :vartype: bool

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Text(Property):
    def __init__(self,parent, data):
        super(Text, self).__init__(parent, data)
        self.max_length = data.get('maxLength')  #: :vartype: int
        self.min_length = data.get('minLength')  #: :vartype: int
        self.pattern = data.get('pattern')  #: :vartype: str
        self.validate = data.get('validate')  #: :vartype: bool

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
