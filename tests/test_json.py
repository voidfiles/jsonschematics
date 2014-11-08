import json
import unittest

from schematics.models import Model
from schematics.types import StringType, URLType, IntType, LongType, DecimalType
from schematics.types.compound import ModelType, ListType

from jsonschematics import to_jsonschema


class BankAccount(Model):
    account_id = LongType(required=True, min_value=0)
    amount = DecimalType()


class BirthPlace(Model):
    name = StringType(required=True, min_length=1, max_length=30)


class Person(Model):
    name = StringType(required=True)
    website = URLType()
    age = IntType()
    birth_place = ModelType(BirthPlace)
    bank_accounts = ListType(ModelType(BankAccount))


test_data = {
    'name': u'Joe Strummer',
    'website': 'http://soundcloud.com/joestrummer',
    'age': 15,
    'birth_place': {
        'name': 'Somewhere, World'
    },
    'bank_accounts': [{
        'account_id': long(123),
        'amount': 10.23,
    }, {
        'account_id': long(456),
        'amount': 100.54,
    }]
}

converted_schema_string = '{"required": ["name"], "type": "object", "properties": {"website": {"type": "string"}, "bank_accounts": {"items": {"required": ["account_id"], "type": "object", "properties": {"amount": {"type": "number"}, "account_id": {"minimum": 0, "type": "integer"}}, "title": "BankAccount"}, "type": "array", "title": "BankAccount Set"}, "age": {"type": "integer"}, "birth_place": {"required": ["name"], "type": "object", "properties": {"name": {"minLength": 1, "type": "string", "maxLength": 30}}, "title": "BirthPlace"}, "name": {"type": "string"}}, "title": "Person"}'


class TestModelFunctions(unittest.TestCase):

    def test_schema_serialization(self):
        val = to_jsonschema(Person)
        self.assertEquals(val, converted_schema_string)

    def test_validation_schema_validation(self):
        from jsonschema import validate

        person = Person(test_data)

        try:
            person.validate()
        except:
            self.fail("person.validate() raised Exception unexpectedly!")

        try:
            validate(test_data, json.loads(converted_schema_string))
        except:
            self.fail("jsonschema.validate() raised Exception unexpectedly!")
