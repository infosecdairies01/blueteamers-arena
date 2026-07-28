from typing import TypeVar, Generic, Optional, List, Dict, Any, Type
from django.db import models

T = TypeVar("T", bound=models.Model)


class BaseRepository(Generic[T]):
    """
    Base Repository Pattern abstraction providing decoupled CRUD data access logic.
    """
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class

    def get_by_id(self, entity_id: Any) -> Optional[T]:
        try:
            return self.model_class.objects.get(pk=entity_id)
        except (self.model_class.DoesNotExist, ValueError):
            return None

    def list_all(self) -> models.QuerySet[T]:
        return self.model_class.objects.all()

    def filter_by(self, **kwargs) -> models.QuerySet[T]:
        return self.model_class.objects.filter(**kwargs)

    def create(self, **kwargs) -> T:
        return self.model_class.objects.create(**kwargs)

    def update(self, instance: T, **kwargs) -> T:
        for attr, value in kwargs.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance: T) -> bool:
        instance.delete()
        return True
