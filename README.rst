JSON Schematics: JSONSchema for Schematics
==========================================

JSON Schematics is an MIT Licensed python library for converting Schematics Schemas into JSONSchemas.

.. code-block:: python
    from schematics.models import Model
    from schematics.types import StringType, URLType, IntType, LongType, DecimalType
    from schematics.types.compound import ModelType, ListType

    import jsonschematics

    class BankAccount(Model):
        account_id = LongType(required=True)
        amount = DecimalType()


    class BirthPlace(Model):
        name = StringType(required=True)


    class Person(Model):
        name = StringType(required=True)
        website = URLType()
        age = IntType()
        birth_place = ModelType(BirthPlace)
        bank_accounts = ListType(ModelType(BankAccount))

    json_schema = jsonschematics.to_jsonschema(Person)

    print json_schema
    """
    {u'properties': {u'age': {u'type': u'integer'},
                     u'bank_accounts': {u'items': {u'properties': {u'account_id': {u'type': u'integer'},
                                                                   u'amount': {u'type': u'number'}},
                                                   u'required': [u'account_id'],
                                                   u'title': u'BankAccount',
                                                   u'type': u'array'},
                                        u'title': u'BankAccount Set',
                                        u'type': u'array'},
                     u'birth_place': {u'properties': {u'name': {u'type': u'string'}},
                                      u'required': [u'name'],
                                      u'title': u'BirthPlace',
                                      u'type': u'object'},
                     u'name': {u'type': u'string'},
                     u'website': {u'type': u'string'}},
     u'required': [u'name'],
     u'title': u'Person',
     u'type': u'object'}
    """

Contribute
----------

#. Fork the repository on GitHub to start making your changes to the **master** branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request.
