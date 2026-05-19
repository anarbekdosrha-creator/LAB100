from django.db import models


class UserQuery(models.Model):
    """Хранит каждый запрос пользователя к боту."""

    COMMAND_CHOICES = [
        ("/start",   "Старт"),
        ("/help",    "Помощь"),
        ("/calc",    "Калькулятор"),
        ("/quote",   "Цитата"),
        ("/history", "История"),
        ("/clear",   "Очистка"),
        ("unknown",  "Неизвестная"),
    ]

    user_id    = models.BigIntegerField("ID пользователя")
    username   = models.CharField("Username", max_length=100, blank=True)
    first_name = models.CharField("Имя", max_length=100, blank=True)
    command    = models.CharField("Команда", max_length=20, choices=COMMAND_CHOICES, default="unknown")
    text       = models.TextField("Полный текст сообщения")
    result     = models.TextField("Результат бота", blank=True)
    created_at = models.DateTimeField("Время запроса", auto_now_add=True)

    class Meta:
        verbose_name        = "Запрос пользователя"
        verbose_name_plural = "Запросы пользователей"
        ordering            = ["-created_at"]

    def __str__(self):
        name = self.username or self.first_name or str(self.user_id)
        return f"[{self.created_at.strftime('%d.%m.%Y %H:%M')}] {name} → {self.command}"
