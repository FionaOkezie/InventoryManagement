class XMLProduct:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def to_xml(self):
        return f"<product><name>{self.name}</name><price>{self.price}</price></product>"

class JSONProductAdapter:
    def __init__(self, xml_product):
        self.xml_product = xml_product

    def to_json(self):
        return {
            "name": self.xml_product.name,
            "price": self.xml_product.price
        }
