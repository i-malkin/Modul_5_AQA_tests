from enum import Enum
from typing import Any, get_type_hints, get_origin, get_args, Annotated
from src.main.api.generators.creations_rule import CreationsRule
import rstr, uuid, random


class RandomModelGenerator:
    @staticmethod
    def generate(cls: type) -> Any:
        type_hints = get_type_hints(cls, include_extras=True)
        init_data = {}

        for field_name, annotated_type in type_hints.items():
            rule = None
            actual_type = annotated_type

            if get_origin(annotated_type) is Annotated:
                actual_type, *annotations = get_args(annotated_type)
                for ann in annotations:
                    if isinstance(ann, CreationsRule):
                        rule = ann

            if rule:
                value = RandomModelGenerator._generate_from_regex(rule.regex, actual_type)
            elif isinstance(actual_type, type) and issubclass(actual_type, Enum):
                # Enum: уважаем дефолт, если он есть; иначе первое значение
                default = RandomModelGenerator._get_default(cls, field_name)
                value = default if default is not None else list(actual_type)[0]
            else:
                default = RandomModelGenerator._get_default(cls, field_name)
                if default is not None:
                    value = default
                else:
                    value = RandomModelGenerator._generate_value(actual_type)

            init_data[field_name] = value

        return cls(**init_data)

    @staticmethod
    def _get_default(cls: type, field_name: str) -> Any:
        # pydantic v2
        model_fields = getattr(cls, "model_fields", None)
        if model_fields and field_name in model_fields:
            return model_fields[field_name].default
        # pydantic v1 / обычный класс
        return getattr(cls, field_name, None)

    @staticmethod
    def _generate_from_regex(regex: str, field_type: type) -> Any:
        generated = rstr.xeger(regex)
        if field_type is int:
            return int(generated)
        if field_type is float:
            return float(generated)
        return generated

    @staticmethod
    def _generate_value(field_type: type) -> Any:
        if field_type is str:
            return str(uuid.uuid4())[:8]
        elif field_type is int:
            return random.randint(1, 9999)
        elif field_type is float:
            return round(random.uniform(0, 100.), 2)
        elif field_type is bool:
            return random.choice([True, False])
        elif field_type is list:
            return [str(uuid.uuid4())[:5]]
        elif isinstance(field_type, type):
            return RandomModelGenerator.generate(field_type)
        return None