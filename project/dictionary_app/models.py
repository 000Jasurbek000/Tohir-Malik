from django.db import models


class DictionaryEntry(models.Model):
    CATEGORY_CHOICES = [
        ('green', 'Lug\'atda aynan berilgan'),
        ('yellow', 'Lug\'atda variantdoshi berilgan'),
        ('red', 'Lug\'atda uchramaydigan'),
        ('purple', 'Muallif nutqiga tegishli okkazional iboralar'),
    ]

    title = models.CharField(max_length=255, db_index=True)
    meaning = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True)
    variant_info = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    example = models.TextField(blank=True)
    pages = models.CharField(max_length=255, blank=True)
    source_file = models.CharField(max_length=50, blank=True)
    raw_row = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        unique_together = [('title', 'category')]

    def __str__(self):
        return self.title
