from django.contrib import admin
from .models import Task, Balance, Withdrawal

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'validated', 'completed', 'created_at')
    list_filter = ('platform', 'validated')
    actions = ['validate_tasks']

    def validate_tasks(self, request, queryset):
        for task in queryset:
            task.validated = True
            task.completed = True
            task.save()
            balance, _ = Balance.objects.get_or_create(user=task.user)
            balance.coins += task.coins_reward
            balance.save()
        self.message_user(request, f"{queryset.count()} tâches validées et coins ajoutés")
    validate_tasks.short_description = "Valider et créditer les tâches sélectionnées"

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user', 'method', 'amount_cad', 'status', 'created_at')
    actions = ['mark_as_paid']

    def mark_as_paid(self, request, queryset):
        queryset.update(status='paid')
        self.message_user(request, "Retraits marqués comme payés")
    mark_as_paid.short_description = "Marquer comme payé"
