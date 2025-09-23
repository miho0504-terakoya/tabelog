from django.db import models

class Station(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="駅名")
    code = models.CharField(max_length=20, blank=True, null=True, verbose_name="駅コード")
    is_active = models.BooleanField(default=True, verbose_name="有効フラグ")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

