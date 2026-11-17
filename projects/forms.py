from django import forms
from .models import TableReservation, DeliveryOrder


class TableReservationForm(forms.ModelForm):
    """Форма онлайн-бронювання столика."""
    class Meta:
        model = TableReservation
        fields = [
            'name',
            'phone',
            'email',
            'date',
            'time',
            'guests_count',
            'hall',
            'event_type',
            'has_mykola',
            'special_requests',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-stone-900/80 border border-stone-700/80 rounded-xl text-stone-100 placeholder-stone-500 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 transition-colors',
                'placeholder': 'Ваше ім’я'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-stone-900/80 border border-stone-700/80 rounded-xl text-stone-100 placeholder-stone-500 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 transition-colors',
                'placeholder': '+38 (0__) ___-__-__'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 bg-stone-900/80 border border-stone-700/80 rounded-xl text-stone-100 placeholder-stone-500 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 transition-colors',
                'placeholder': 'your@email.com (необов’язково)'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 bg-stone-900/80 border border-stone-700/80 rounded-xl text-stone-100 placeholder-stone-500 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 transition-colors'
            }),
            'time': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-stone-900/80 border border-stone-700/80 rounded-xl text-stone-100 placeholder-stone-500 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 transition-colors',
                'placeholder': '18:00'
            }),
            'guests_count': forms.NumberInput(attrs={
                'min': '1',
                'max': '150',
                'class': 'w-full px-4 py-3 bg-stone-900/80 border border-stone-700/80 rounded-xl text-stone-100 placeholder-stone-500 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 transition-colors',
                'placeholder': '2'
            }),
            'hall': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-stone-900/80 border border-stone-700/80 rounded-xl text-stone-100 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 transition-colors'
            }, choices=[
                ('', 'Оберіть залу (за бажанням)'),
                ('Головна зала зі ставком', 'Головна зала зі ставком з живою фореллю'),
                ('Зала з каміном', 'Зала з каміном (затишна, 30–50 осіб)'),
                ('Урочиста зала', 'Урочиста зала (банкетна, до 230 осіб)'),
                ('Літня тераса біля озера', 'Літня тераса біля озера'),
                ('Дитяча зона', 'Дитяча зона біля ігрового простору'),
            ]),
            'event_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-stone-900/80 border border-stone-700/80 rounded-xl text-stone-100 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 transition-colors'
            }, choices=[
                ('', 'Формат зустрічі'),
                ('Затишна вечеря', 'Затишна вечеря / обід'),
                ('День народження / Ювілей', 'День народження / Ювілей'),
                ('Весілля', 'Весілля'),
                ('Корпоратив', 'Корпоратив / Святкування компанії'),
                ('Сімейний відпочинок з дітьми', 'Сімейний відпочинок з дітьми'),
                ('Ділова зустріч / Конференція', 'Ділова зустріч / Конференція'),
            ]),
            'has_mykola': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 rounded border-stone-600 text-amber-500 focus:ring-amber-500 bg-stone-900'
            }),
            'special_requests': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-4 py-3 bg-stone-900/80 border border-stone-700/80 rounded-xl text-stone-100 placeholder-stone-500 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 transition-colors',
                'placeholder': 'Побажання щодо столика, риболовлі, алергій чи прикрашання...'
            }),
        }


class DeliveryOrderForm(forms.ModelForm):
    """Форма замовлення доставки або самовивозу."""
    class Meta:
        model = DeliveryOrder
        fields = [
            'customer_name',
            'phone',
            'order_type',
            'address',
            'desired_time',
            'payment_method',
            'comment',
        ]
