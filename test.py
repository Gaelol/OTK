class Product:
    """
    Crée un Produit
    :param name: un string
    :param euro: un float
    :param dollar : un float
    :type list_ingredient : une list
    :return price_euro : le prix en euro
    :return price_dollar : le prix en dollar
    :return get_sorted_ingredients : liste triée des ingrédients
    """

    def __init__(self, name="", euro=1, dollar=1.2, list_ingredient=[]):
        self._name = name
        self.euro = euro
        self.dollar = dollar
        self.list_ingredient = list_ingredient


    def add_ingredient(self, *ingredients):
        for ing in ingredients:
            self.list_ingredient.append(ing)
        return self.list_ingredient


    def get_sorted_ingredients(self):
        sortedIng = sorted(self.list_ingredient)
        return sortedIng


    @property
    def name(self):
        return self._name


    @property
    def price_euro(self):
        if self.euro != self.dollar / 1.2:
            self.euro = self.dollar / 1.2
        return self.euro


    @price_euro.setter
    def price_euro(self, value):
        self.euro = value
        self.dollar = value * 1.2


    @property
    def price_dollar(self):
        if self.dollar != self.euro * 1.2:
            self.dollar = self.euro * 1.2
        return self.dollar


    @price_dollar.setter
    def price_dollar(self, value):
        self.dollar = value
        self.euro = value / 1.2