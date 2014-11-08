import json

from six import iteritems

from schematics.types.base import (BaseType, NumberType, IntType, LongType, FloatType,
                                   DecimalType, BooleanType)
from schematics.types.compound import ModelType, ListType

__version__ = '1.0'


SCHEMATIC_TYPE_TO_JSON_TYPE = {
    NumberType: 'number',
    IntType: 'integer',
    LongType: 'integer',
    FloatType: 'number',
    DecimalType: 'number',
    BooleanType: 'boolean',
}

# Schema Serialization

# Parameters for serialization to JSONSchema
schema_kwargs_to_schematics = {
    'maxLength': 'max_length',
    'minLength': 'min_length',
    'pattern': 'regex',
    'minimum': 'min_value',
    'maximum': 'max_value',
}


def jsonschema_for_fields(model):
    properties = {}
    required = []
    for field_name, field_instance in iteritems(model._fields):
        serialized_name = getattr(field_instance, 'serialized_name', None) or field_name

        if isinstance(field_instance, ModelType):
            properties[serialized_name] = jsonschema_for_model(field_instance.model_class)

        elif isinstance(field_instance, ListType):
            properties[serialized_name] = jsonschema_for_model(field_instance.model_class, 'array')

        # Convert field as single model
        elif isinstance(field_instance, BaseType):
            properties[serialized_name] = {
                "type": SCHEMATIC_TYPE_TO_JSON_TYPE.get(field_instance.__class__, 'string')
            }
            for js_key, schematic_key in iteritems(schema_kwargs_to_schematics):
                value = getattr(field_instance, schematic_key, None)
                if value is not None:
                    properties[serialized_name][js_key] = value

        if getattr(field_instance, 'required', False):
            required.append(serialized_name)

    return properties, required


def jsonschema_for_model(model, _type='object'):

    properties, required = jsonschema_for_fields(model)

    schema = {
        'type': 'object',
        'title': model.__name__,
        'properties': properties,
    }

    if required:
        schema['required'] = required

    if _type == 'array':
        schema = {
            'type': 'array',
            'title': '%s Set' % (model.__name__),
            'items': schema,
        }

    return schema


def to_jsonschema(model):
    """Returns a representation of this schema class as a JSON schema."""
    return json.dumps(jsonschema_for_model(model))
