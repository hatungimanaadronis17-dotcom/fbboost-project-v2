from django.contrib import admin
from .models import Task, Balance, Withdrawal


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'coins_reward', 'validated', 'created_at')
    list_filter = ('platform', 'validated')


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'coins')


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user', 'method', 'amount_cad', 'status', 'created_at')
    actions = ['mark_as_paid']

    def mark_as_paid(self, request, queryset):
        queryset.update(status='paid')
        self.message_user(request, "Retraits marqués comme payés")
