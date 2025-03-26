from collections import defaultdict
from typing import Any
from uuid import UUID

from django import forms
from django.core import checks
from django.core.exceptions import ValidationError
from django.db import models
from django.db import models
from ulid import ULID


class GenericTablePrefixUlidField(models.UUIDField):
    def __init__(self, table_prefix, *args, **kwargs):
        if not table_prefix:
            raise TablePrefixEmptyError
        if not isinstance(table_prefix, str):
            raise TablePrefixMustBeStringError

        self.table_prefix = table_prefix

        kwargs["default"] = self.table_prefixed_ulid_generator(table_prefix)
        kwargs["editable"] = False
        kwargs["blank"] = True
        kwargs["db_comment"] = (
            "This field is a ULID being stored as a UUID. When used in the API (and "
            "everywhere outside the DB really), the ULID is shown with a "
            "'table_prefix' prepended to it. When querying the DB directly you'll need "
            "to remove this prefix and convert the ULID to UUIDs"
        )

        super().__init__(*args, **kwargs)

    @staticmethod
    def table_prefixed_ulid_generator(table_prefix: str):
        def new_ulid():
            return f"{table_prefix}_{ULID()}"

        return new_ulid

    def get_db_prep_value(self, value, connection, prepared=False):
        _, ulid_obj = self.convert_value_to_known_forms(self.table_prefix, value)

        if ulid_obj is None:
            return None

        return super().get_db_prep_value(ulid_obj.to_uuid(), connection, prepared)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        string_value, _ = self.convert_value_to_known_forms(self.table_prefix, value)
        return string_value

    def formfield(self, **kwargs):
        defaults = {
            "form_class": self.table_prefix_form_field_factory(self.table_prefix),
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        args.insert(0, self.table_prefix)

        # These fields are all forcibly set during __init__
        for field_name in (
            "default",
            "editable",
            "blank",
            "db_comment",
        ):
            if field_name in kwargs:
                del kwargs[field_name]
        return name, path, args, kwargs

    @classmethod
    def table_prefix_form_field_factory(cls, outer_table_prefix):
        class TablePrefixUlidPkFormField(forms.CharField):
            table_prefix = outer_table_prefix

            def prepare_value(self, value):
                str_value, _ = cls.convert_value_to_known_forms(
                    self.table_prefix,
                    value,
                )
                return str_value

            def to_python(self, value):
                str_value, _ = cls.convert_value_to_known_forms(
                    self.table_prefix,
                    value,
                )
                return str_value

        return TablePrefixUlidPkFormField

    @classmethod
    def convert_value_to_known_forms(
        cls,
        expected_table_prefix: str,
        input_value: Any,
    ) -> tuple[str | None, ULID | None]:
        if input_value is None:
            return None, None

        if isinstance(input_value, UUID):
            parsed_ulid = ULID.from_uuid(input_value)

        elif isinstance(input_value, ULID):
            parsed_ulid = input_value

        else:
            string_version = str(input_value)
            split = string_version.split("_")
            table_prefix = "_".join(split[:-1])
            ulid_string = split[-1]
            if table_prefix and table_prefix != expected_table_prefix:
                raise InvalidTablePrefixError

            try:
                parsed_ulid = ULID.from_str(ulid_string)
            except (AttributeError, ValueError) as e:
                raise InvalidDBIDError from e

        display_string = f"{expected_table_prefix}_{parsed_ulid}"
        return display_string, parsed_ulid


class TablePrefixUlidPkField(GenericTablePrefixUlidField):
    used_table_prefixes_to_fields: dict[
        str,
        list["TablePrefixUlidPkField"],
    ] = defaultdict(list)

    def __init__(self, table_prefix, *args, **kwargs):
        kwargs["primary_key"] = True

        super().__init__(table_prefix, *args, **kwargs)
        self.used_table_prefixes_to_fields[self.table_prefix].append(self)

    def check(self, **kwargs):
        errors = super().check(**kwargs)

        table_name_used_on = None
        for field in self.used_table_prefixes_to_fields[self.table_prefix]:
            if hasattr(field, "model"):
                current_field_table_name = field.model._meta.db_table  # noqa: SLF001
                if table_name_used_on is None:
                    table_name_used_on = current_field_table_name
                elif table_name_used_on != current_field_table_name:
                    errors.append(
                        checks.Error(
                            f"Duplicate table prefix found: {self.table_prefix}",
                            hint="Change either table's prefix to not conflict.",
                            obj=self,
                            id="common.E001",
                        ),
                    )

        return errors

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # These fields are all forcibly set during __init__
        for field_name in ("primary_key",):
            if field_name in kwargs:
                del kwargs[field_name]
        return name, path, args, kwargs


class TablePrefixEmptyError(ValidationError):
    def __init__(self):
        message = "Table Prefix cannot be empty."
        super().__init__(message)


class InvalidTablePrefixError(ValidationError):
    def __init__(self):
        message = (
            "Invalid DB ID. Table prefix is incorrect; this ID likely does "
            "not belong to this table."
        )
        super().__init__(message, code="invalid")


class InvalidDBIDError(ValidationError):
    def __init__(self):
        message = "Invalid DB ID."
        super().__init__(message, code="invalid")


class TablePrefixMustBeStringError(ValidationError):
    def __init__(self):
        message = "Table Prefix must be a string."
        super().__init__(message)


def generate_mock_db_id(table_prefix: str or None = None) -> str:
    if table_prefix is None:
        table_prefix = "fake"
    return f"{table_prefix}_{ULID()}"


class BaseDbModel(models.Model):
    id = TablePrefixUlidPkField(table_prefix="change_me")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
