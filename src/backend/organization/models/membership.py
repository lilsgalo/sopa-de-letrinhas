from django.db import models
from django.contrib.auth import get_user_model

from src.backend.core.models import BaseModel
from src.backend.organization.models.organization import Organization

__all__ = ["Membership"]

class RoleChoices(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    TEACHER = 'teacher', 'Teacher'
    STUDENT  = 'student', 'Student'

class Membership(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="membership")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="membership")
    role = models.CharField(max_length=16, choices=RoleChoices.choices)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        unique_together = ("user", "organization")

    def __str__(self):
        return f"{self.user} - {self.organization} ({self.role})"