from django.db import models

class Staff(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class WorkAssignment(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='assignments')
    work_type = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    money = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        try:
            # work_type va quantity ni int ekanligiga ishonch hosil qilish
            work_type = int(self.work_type)
            quantity = int(self.quantity)
            if work_type <= 0 or quantity <= 0:
                raise ValueError("Ish turi va soni musbat bo'lishi shart")
            self.money = work_type * quantity
        except (ValueError, TypeError) as e:
            self.money = 0  # Xato bo'lsa money 0 qilib saqlaymiz
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.work_type} - {self.quantity}"

class Payment(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='payments')
    amount = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff.name} - {self.amount} - {self.date}"