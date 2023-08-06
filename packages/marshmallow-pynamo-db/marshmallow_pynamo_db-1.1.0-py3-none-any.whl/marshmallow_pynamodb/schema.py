import typing

from marshmallow import Schema, SchemaOpts, fields, post_load
from marshmallow.schema import SchemaMeta
from marshmallow_enum import EnumField
from pynamodb.attributes import DiscriminatorAttribute
from pynamodb.models import Model
from six import iteritems

from marshmallow_pynamodb.convert import attribute2field
from marshmallow_pynamodb.fields import PynamoNested


class ModelOpts(SchemaOpts):
    def __init__(self, meta, **kwargs):
        SchemaOpts.__init__(self, meta, **kwargs)
        self.model = getattr(meta, "model", None)
        self.partial_fields = []


class ModelMeta(SchemaMeta):
    @classmethod
    def get_declared_fields(mcs, klass, cls_fields, inherited_fields, dict_cls):
        """Get Declared Fields."""
        declared_fields = super(ModelMeta, mcs).get_declared_fields(
            klass, cls_fields or [], inherited_fields or [], dict_cls
        )
        if klass.opts.model:
            model_list = [klass.opts.model]
            for model in model_list:
                attributes = model.get_attributes()
                model.attributes = dict()
                for attr_name, attribute in iteritems(attributes):
                    if declared_fields.get(attr_name):
                        continue

                    if isinstance(attribute, DiscriminatorAttribute):
                        continue

                    field = attribute2field(attribute)

                    if field == PynamoNested:
                        instance_of = type(attribute)

                        class Meta:
                            model = instance_of

                        sub_model = type(
                            instance_of.__name__, (ModelSchema,), {"Meta": Meta}
                        )
                        field = field(sub_model)
                    elif field == fields.List:

                        if not attribute.element_type:
                            field = field(fields.Raw)
                        else:

                            class Meta:
                                model = attribute.element_type

                            element_type = type(
                                attribute.element_type.__name__,
                                (ModelSchema,),
                                {"Meta": Meta},
                            )
                            field = field(PynamoNested(element_type))
                    elif field == EnumField:
                        field = field(attribute.enum_type, by_value=True)
                    else:
                        field = field()

                    field_name = (
                        attribute.attr_name if attribute.attr_name else attr_name
                    )
                    if (
                        attribute.is_hash_key
                        or attribute.is_range_key
                        or not attribute.null
                    ):
                        field.required = attribute.default is None
                        if attribute.is_hash_key:
                            klass.opts.hash_key = field_name
                        elif attribute.is_range_key:
                            klass.opts.range_key = field_name

                    # The `default` argument in PynamoDB
                    # is equivalent to `load_default` argument in Marshmallow
                    # Example: for a UTCDateTimeAttribute, default value
                    # must be a datetime object:
                    # Datetime obj (from Pynamo default) -> String (DynamoDB)
                    # Payload Input (Json) -> Datetime obj
                    # (from Marshmallow load_default) -> String (DynamoDB)
                    if hasattr(field, "load_default"):
                        field.load_default = attribute.default
                    else:
                        field.missing = attribute.default  # marshmallow <=3.12

                    # Add pynamodb attributes with null=True
                    if attribute.null is True:
                        field.allow_none = True

                    declared_fields[field_name] = field
        return declared_fields


class ModelSchema(Schema, metaclass=ModelMeta):
    OPTIONS_CLASS = ModelOpts

    def load(self, *args, **kwargs):
        """Override load to add pre-generated partial fields."""
        partial = kwargs.pop("partial", None)
        if partial is not None and self.opts.partial_fields:
            if isinstance(partial, set):
                partial = list(partial)
            if isinstance(partial, list):
                partial += self.opts.partial_fields
        elif self.opts.partial_fields:
            partial = self.opts.partial_fields
        kwargs["partial"] = partial
        return super(ModelSchema, self).load(*args, **kwargs)

    def dump(self, obj: typing.Any, *args, **kwargs):
        """Serialize an object to native Python data types.

        According to this Schema's fields.

        """

        def convert_to_values(
            original: Model, converted: typing.Dict[typing.Any, typing.Any]
        ):
            """Convert PynamoDB instance to Dict.

            Using model.attribute_values to unpack data.
            Some keys will return another pynamodb instance
            instead dict.
            """
            if isinstance(obj, dict):
                return obj
            for key in original.attribute_values:
                if (
                    getattr(original.attribute_values[key], "attribute_values", None)
                    is not None
                ):
                    converted[key] = convert_to_values(
                        original.attribute_values[key], {}
                    )
                else:
                    converted[key] = original.attribute_values[key]
            return converted

        converted = {
            key: None
            for key in self.declared_fields
            if self.declared_fields[key].allow_none is True
        }

        dict_obj = convert_to_values(obj, converted)
        return super(ModelSchema, self).dump(dict_obj, *args, **kwargs)

    @post_load
    def hydrate_pynamo_model(self, data, **kwargs):
        """Hydrate PynamoDB Model."""
        hash_key = data.pop(getattr(self.opts, "hash_key", None), None)
        range_key = data.pop(getattr(self.opts, "range_key", None), None)

        if hash_key or range_key:  # this is Model
            return self.opts.model(hash_key=hash_key, range_key=range_key, **data)
        else:  # this is a MapAttribute
            # Remove null fields
            non_null_data = {key: data[key] for key in data if data[key] is not None}
            return self.opts.model(**non_null_data)
