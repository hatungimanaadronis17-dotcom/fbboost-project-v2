from django.contrib import admin
from .models import Task, Balance, Withdrawal

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'coins_reward', 'validated', 'created_at')
    list_filter = ('platform', 'validated')
    actions = ['validate_tasks']

    def validate_tasks(self, request, queryset):
        for task in queryset:
            if not task.validated:
                task.validated = True
                task.completed = True
                task.save()
                balance, _ = Balance.objects.get_or_create(user=task.user)
                balance.coins += task.coins_reward
                balance.save()
        self.message_user(request, f"{queryset.count()} tâches validées + coins ajoutés")
    validate_tasks.short_description = "Valider et créditer les tâches"

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user', 'method', 'amount_cad', 'status', 'created_at')
    actions = ['mark_paid']

    def mark_paid(self, request, queryset):
        queryset.update(status='paid')
        self.message_user(request, "Retraits marqués comme payés")
    mark_paid.short_description = "Marquer comme payé"

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'coins')
