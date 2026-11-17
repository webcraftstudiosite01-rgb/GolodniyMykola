from django.contrib import admin
from .models import (
    MenuCategory,
    Dish,
    RestaurantHall,
    RestaurantService,
    Promotion,
    TableReservation,
    DeliveryOrder,
    GuestReview,
)


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active', 'dish_count')
    list_editable = ('order', 'is_active')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def dish_count(self, obj):
        return obj.dishes.count()
    dish_count.short_description = 'Кількість страв'


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'weight', 'badge', 'is_hit', 'is_trout', 'is_available', 'order')
    list_filter = ('category', 'is_hit', 'is_trout', 'is_spicy', 'is_vegetarian', 'is_available')
    list_editable = ('price', 'is_hit', 'is_available', 'order')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(RestaurantHall)
class RestaurantHallAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'floor', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(RestaurantService)
class RestaurantServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'badge', 'is_active', 'order')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'order')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(TableReservation)
class TableReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'date', 'time', 'guests_count', 'hall', 'has_mykola', 'status', 'created_at')
    list_filter = ('status', 'date', 'has_mykola', 'hall')
    list_editable = ('status',)
    search_fields = ('name', 'phone', 'email', 'special_requests')
    readonly_fields = ('created_at',)


@admin.register(DeliveryOrder)
class DeliveryOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'phone', 'order_type', 'total_price', 'status', 'created_at')
    list_filter = ('order_type', 'status', 'created_at')
    list_editable = ('status',)
    search_fields = ('order_number', 'customer_name', 'phone', 'address')
    readonly_fields = ('created_at', 'items_json', 'subtotal', 'discount', 'total_price')


@admin.register(GuestReview)
class GuestReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'city', 'rating', 'source', 'is_published')
    list_filter = ('rating', 'is_published', 'source')
    list_editable = ('is_published',)
    search_fields = ('author', 'text')
