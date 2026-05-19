from django.contrib import admin
from django.utils.html import format_html
from .models import UserQuery


@admin.register(UserQuery)
class UserQueryAdmin(admin.ModelAdmin):
    """Админка для просмотра и управления запросами пользователей бота."""

    # ── Список записей ──────────────────────────────────────────────────
    list_display  = ("created_at", "user_badge", "command", "short_text", "short_result")
    list_filter   = ("command", "created_at")
    search_fields = ("username", "first_name", "user_id", "text", "result")
    date_hierarchy = "created_at"
    ordering      = ("-created_at",)
    list_per_page = 25

    # ── Детальная форма ─────────────────────────────────────────────────
    readonly_fields = ("user_id", "username", "first_name", "command",
                       "text", "result", "created_at")
    fieldsets = (
        ("👤 Пользователь", {
            "fields": ("user_id", "username", "first_name"),
        }),
        ("📨 Запрос", {
            "fields": ("command", "text", "created_at"),
        }),
        ("🤖 Ответ бота", {
            "fields": ("result",),
        }),
    )

    # ── Кастомные колонки ───────────────────────────────────────────────
    @admin.display(description="Пользователь")
    def user_badge(self, obj):
        name = obj.username or obj.first_name or "—"
        return format_html(
            '<span style="font-weight:bold">@{}</span> <small style="color:#888">({})</small>',
            name, obj.user_id
        )

    @admin.display(description="Текст сообщения")
    def short_text(self, obj):
        return obj.text[:60] + "…" if len(obj.text) > 60 else obj.text

    @admin.display(description="Результат")
    def short_result(self, obj):
        return obj.result[:60] + "…" if len(obj.result) > 60 else obj.result

    # Запрещаем создание записей вручную через админку
    def has_add_permission(self, request):
        return False
