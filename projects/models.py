from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class MenuCategory(models.Model):
    """Категорія страв у меню ресторану (наприклад: Баноші та вареники, Пструг, Зупи)."""
    name = models.CharField('Назва категорії', max_length=120)
    slug = models.SlugField('URL Slug', max_length=140, unique=True)
    icon = models.CharField(
        'Іконка / Клас FontAwesome',
        max_length=60,
        blank=True,
        default='fa-solid fa-utensils',
        help_text='Наприклад: fa-solid fa-fish, fa-solid fa-bowl-food'
    )
    description = models.TextField('Опис категорії', blank=True)
    order = models.PositiveIntegerField('Порядок сортування', default=0)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        verbose_name = 'Категорія меню'
        verbose_name_plural = 'Категорії меню'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Dish(models.Model):
    """Страва або напій у меню ресторану 'Голодний Микола'."""
    category = models.ForeignKey(
        MenuCategory,
        on_delete=models.CASCADE,
        related_name='dishes',
        verbose_name='Категорія'
    )
    name = models.CharField('Назва страви', max_length=200)
    slug = models.SlugField('URL Slug', max_length=220, unique=True)
    price = models.DecimalField('Ціна (грн)', max_digits=8, decimal_places=2)
    weight = models.CharField('Вага / Порція', max_length=50, blank=True, help_text='Наприклад: 350 г, 1 л')
    description = models.TextField('Опис страви / Складники', blank=True)
    image_url = models.CharField('URL фотографії страви', max_length=500, blank=True)
    badge = models.CharField('Бейдж / Позначка', max_length=50, blank=True, help_text='Наприклад: Хіт, Новинка, Зі ставка')
    is_hit = models.BooleanField('Хіт ресторану', default=False)
    is_trout = models.BooleanField('З власного ставка (жива риба)', default=False)
    is_spicy = models.BooleanField('Гостре', default=False)
    is_vegetarian = models.BooleanField('Пісне / Вегетаріанське', default=False)
    is_available = models.BooleanField('В наявності', default=True)
    order = models.PositiveIntegerField('Порядок сортування', default=0)

    class Meta:
        verbose_name = 'Страва'
        verbose_name_plural = 'Меню страв'
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} — {self.price} грн"


class RestaurantHall(models.Model):
    """Зала або локація ресторану (Урочиста, З каміном, Тераса зі ставком тощо)."""
    name = models.CharField('Назва зали', max_length=150)
    slug = models.SlugField('URL Slug', max_length=160, unique=True)
    capacity = models.CharField('Місткість', max_length=80, help_text='Наприклад: до 230 гостей')
    floor = models.CharField('Розташування', max_length=80, blank=True, default='1 поверх')
    description = models.TextField('Опис зали та атмосфери')
    features = models.TextField(
        'Особливості та обладнання',
        blank=True,
        help_text='Кожен пункт з нового рядка'
    )
    image = models.CharField('Зображення зали', max_length=300, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Зала ресторану'
        verbose_name_plural = 'Зали та локації'
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.capacity})"

    def feature_list(self):
        if not self.features:
            return []
        return [f.strip() for f in self.features.split('\n') if f.strip()]


class RestaurantService(models.Model):
    """Послуги ресторану (Весілля, Бенкети, Корпоративи, Сімейний відпочинок тощо)."""
    title = models.CharField('Назва послуги', max_length=180)
    slug = models.SlugField('URL Slug', max_length=200, unique=True)
    short_description = models.CharField('Короткий опис', max_length=300)
    description = models.TextField('Детальний опис послуги')
    icon = models.CharField('Іконка FontAwesome', max_length=60, default='fa-solid fa-champagne-glasses')
    image = models.CharField('Зображення', max_length=300, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Послуга'
        verbose_name_plural = 'Послуги ресторану'
        ordering = ['order']

    def __str__(self):
        return self.title


class Promotion(models.Model):
    """Акції, бонуси та спеціальні пропозиції ресторану."""
    title = models.CharField('Заголовок акції', max_length=200)
    slug = models.SlugField('URL Slug', max_length=220, unique=True)
    badge = models.CharField('Бейдж (напр. -15%, -10%, Для Микол)', max_length=60)
    description = models.TextField('Опис акції')
    terms = models.CharField('Умови дії', max_length=255, blank=True)
    image = models.CharField('Зображення', max_length=300, blank=True)
    is_active = models.BooleanField('Активна акція', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Акція'
        verbose_name_plural = 'Акції та знижки'
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.badge})"


class TableReservation(models.Model):
    """Бронювання столика або банкету."""
    STATUS_CHOICES = (
        ('new', 'Нове бронювання'),
        ('confirmed', 'Підтверджено адміністратором'),
        ('completed', 'Завершено'),
        ('cancelled', 'Скасовано'),
    )

    name = models.CharField('Ім’я гостя', max_length=120)
    phone = models.CharField('Номер телефону', max_length=50)
    email = models.EmailField('Email', blank=True)
    date = models.DateField('Дата візиту')
    time = models.CharField('Час візиту', max_length=20)
    guests_count = models.PositiveIntegerField('Кількість гостей', default=2)
    hall = models.CharField('Обрана зала / зона', max_length=120, blank=True)
    event_type = models.CharField('Формат події', max_length=100, blank=True)
    has_mykola = models.BooleanField('Серед гостей є Микола (спецчастування)', default=False)
    special_requests = models.TextField('Особливі побажання / Риболовля', blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField('Дата створення заявки', auto_now_add=True)

    class Meta:
        verbose_name = 'Бронювання'
        verbose_name_plural = 'Бронювання столиків та залів'
        ordering = ['-created_at']

    def __str__(self):
        return f"Бронь: {self.name} на {self.date} {self.time} ({self.guests_count} ос.)"


class DeliveryOrder(models.Model):
    """Замовлення доставки або самовивозу з сайту."""
    ORDER_TYPE_CHOICES = (
        ('delivery', 'Доставка кур’єром по Львову'),
        ('takeaway', 'Самовивіз із ресторану (-10%)'),
    )
    STATUS_CHOICES = (
        ('pending', 'Очікує підтвердження'),
        ('preparing', 'Готується шеф-кухарем'),
        ('delivering', 'Кур’єр у дорозі / Очікує видачі'),
        ('completed', 'Виконано'),
        ('cancelled', 'Скасовано'),
    )

    order_number = models.CharField('Номер замовлення', max_length=40, unique=True)
    customer_name = models.CharField('Ім’я замовника', max_length=120)
    phone = models.CharField('Телефон', max_length=50)
    order_type = models.CharField('Тип замовлення', max_length=20, choices=ORDER_TYPE_CHOICES, default='delivery')
    address = models.CharField('Адреса доставки', max_length=250, blank=True)
    desired_time = models.CharField('Бажаний час', max_length=60, blank=True)
    payment_method = models.CharField('Спосіб оплати', max_length=60, default='Готівка або картка при отриманні')
    comment = models.TextField('Коментар до замовлення', blank=True)
    items_json = models.TextField('Склад замовлення (JSON)', default='[]')
    subtotal = models.DecimalField('Сума страв (грн)', max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField('Знижка (грн)', max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField('Підсумкова сума (грн)', max_digits=10, decimal_places=2, default=0)
    status = models.CharField('Статус замовлення', max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('Дата замовлення', auto_now_add=True)

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення доставки та самовивозу'
        ordering = ['-created_at']

    def __str__(self):
        return f"Замовлення #{self.order_number} від {self.customer_name} ({self.total_price} грн)"


class GuestReview(models.Model):
    """Відгуки реальних гостей про 'Голодний Микола'."""
    author = models.CharField('Ім’я гостя', max_length=120)
    city = models.CharField('Місто', max_length=100, default='Львів')
    rating = models.PositiveSmallIntegerField('Оцінка (1-5)', default=5)
    text = models.TextField('Текст відгуку')
    source = models.CharField('Джерело відгуку', max_length=80, default='Google Maps')
    date = models.CharField('Дата відгуку', max_length=50, default='Нещодавно')
    is_published = models.BooleanField('Опубліковано', default=True)

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки гостей'
        ordering = ['-id']

    def __str__(self):
        return f"{self.author} ({self.rating}★)"
