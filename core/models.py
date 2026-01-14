"""
Modèles de base réutilisables
"""
import uuid
from django.db import models


class BaseModel(models.Model):
    """
    Modèle abstrait de base avec UUID et timestamps
    Tous les modèles héritent de ce modèle
    """
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        help_text="Identifiant unique UUID"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date de dernière modification"
    )
    
    class Meta:
        abstract = True
        ordering = ['-created_at']
    
    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"


class TimestampedModel(models.Model):
    """Modèle avec timestamps uniquement (sans UUID)"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
