from django.contrib import admin
from .models import MockItem
from .models import MockSlot
from .models import MockCondition
from .models import MockLog


class ConditionInline(admin.TabularInline):
    fieldsets = [
        ('键', {'fields': ['key']}),
        ('值', {'fields': ['value']}),
        ('比较类型', {'fields': ['compFunc']}),
    ]
    model = MockCondition
    extra = 0


class SlotAdmin(admin.ModelAdmin):
    fieldsets = [
        ('返回值', {'fields': ['value']}),
        ('描述', {'fields': ['desc']}),
        ('激活状态', {'fields': ['active']}),
        ('所属Item', {'fields': ['mockItem']}),
    ]
    inlines = [ConditionInline]
    search_fields = ['desc']


class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        ('是否激活', {'fields': ['activeType']}),
        ('未激活使用的转发路径', {'fields': ['redirect']}),
        ('匹配失败使用的转发路径', {'fields': ['finalTarget']}),
        ('目标URL', {'fields': ['url']}),
    ]
    search_fields = ['url']

admin.site.register(MockSlot, SlotAdmin)
admin.site.register(MockItem, ItemAdmin)
admin.site.register(MockLog)


