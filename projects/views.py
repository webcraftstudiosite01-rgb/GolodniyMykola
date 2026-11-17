import json
import uuid
from django.contrib import messages
from django.db.models import Prefetch, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, FormView, ListView, TemplateView

from .forms import TableReservationForm, DeliveryOrderForm
from .models import (
    Dish,
    DeliveryOrder,
    GuestReview,
    MenuCategory,
    Promotion,
    RestaurantHall,
    RestaurantService,
    TableReservation,
)


class HomeView(TemplateView):
    """Головна сторінка ресторану 'Голодний Микола'."""
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = MenuCategory.objects.filter(is_active=True).prefetch_related('dishes')
        context['hit_dishes'] = Dish.objects.filter(is_available=True, is_hit=True).select_related('category')[:8]
        if not context['hit_dishes'].exists():
            context['hit_dishes'] = Dish.objects.filter(is_available=True).select_related('category')[:8]
        context['halls'] = RestaurantHall.objects.all()[:4]
        context['services'] = RestaurantService.objects.all()[:6]
        context['promotions'] = Promotion.objects.filter(is_active=True)[:4]
        context['reviews'] = GuestReview.objects.filter(is_published=True)[:6]
        context['reservation_form'] = TableReservationForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TableReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            messages.success(
                request,
                f"Щиро дякуємо, {reservation.name}! Ваше бронювання на {reservation.date} о {reservation.time} успішно прийнято. Адміністратор закладу незабаром зателефонує Вам для підтвердження."
            )
            return redirect('home')
        context = self.get_context_data()
        context['reservation_form'] = form
        messages.error(request, "Будь ласка, перевірте коректність заповнення полів форми бронювання.")
        return render(request, self.template_name, context)


class MenuView(TemplateView):
    """Повне інтерактивне меню ресторану зі швидкими категоріями, пошуком та кошиком."""
    template_name = 'projects/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = MenuCategory.objects.filter(is_active=True).prefetch_related(
            Prefetch('dishes', queryset=Dish.objects.filter(is_available=True))
        )
        context['categories'] = categories
        context['total_dishes_count'] = Dish.objects.filter(is_available=True).count()
        return context


class AboutView(TemplateView):
    """Сторінка 'Хто ми' — історія, традиції, Музей Микол та броварня."""
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['halls'] = RestaurantHall.objects.all()
        context['services'] = RestaurantService.objects.all()
        return context


class ServicesListView(TemplateView):
    """Каталог усіх послуг ресторану (Весілля, Банкети, Сімейний відпочинок тощо)."""
    template_name = 'projects/services_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = RestaurantService.objects.all()
        context['halls'] = RestaurantHall.objects.all()
        return context


class ServiceDetailView(DetailView):
    """Детальна сторінка конкретної послуги."""
    model = RestaurantService
    template_name = 'projects/service_detail.html'
    context_object_name = 'service'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other_services'] = RestaurantService.objects.exclude(pk=self.object.pk)[:4]
        context['reservation_form'] = TableReservationForm(initial={'event_type': self.object.title})
        return context


class ReservationView(FormView):
    """Окрема сторінка онлайн-бронювання столика або банкетного залу."""
    template_name = 'projects/reservation.html'
    form_class = TableReservationForm
    success_url = reverse_lazy('reservation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['halls'] = RestaurantHall.objects.all()
        context['promotions'] = Promotion.objects.filter(is_active=True)
        return context

    def form_valid(self, form):
        reservation = form.save()
        messages.success(
            self.request,
            f"Щиро дякуємо, {reservation.name}! Ваша заявка на бронювання столика на {reservation.date} о {reservation.time} отримана. Наш адміністратор зв'яжеться з Вами протягом 15 хвилин!"
        )
        return super().form_valid(form)


class DeliveryView(TemplateView):
    """Сторінка доставки та самовивозу з інформацією про зони та кошиком."""
    template_name = 'projects/delivery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_dishes'] = Dish.objects.filter(is_available=True, is_hit=True)[:6]
        return context


class ContactView(TemplateView):
    """Сторінка контактів, карти проїзду та графіку роботи."""
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservation_form'] = TableReservationForm()
        return context


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class ApiReserveView(View):
    """AJAX обробка швидкого бронювання зі сторінки або модального вікна."""
    def post(self, request, *args, **kwargs):
        try:
            name = request.POST.get('name', '').strip()
            phone = request.POST.get('phone', '').strip()
            date = request.POST.get('date', '').strip()
            time = request.POST.get('time', '').strip()
            guests_count = int(request.POST.get('guests_count', 2))
            hall = request.POST.get('hall', '').strip()
            event_type = request.POST.get('event_type', '').strip()
            has_mykola = request.POST.get('has_mykola') in ['true', 'on', '1', True]
            special_requests = request.POST.get('special_requests', '').strip()

            if not name or not phone or not date or not time:
                return JsonResponse({'status': 'error', 'message': "Будь ласка, заповніть обов'язкові поля: ім'я, телефон, дату та час."}, status=400)

            reservation = TableReservation.objects.create(
                name=name,
                phone=phone,
                date=date,
                time=time,
                guests_count=guests_count,
                hall=hall,
                event_type=event_type,
                has_mykola=has_mykola,
                special_requests=special_requests
            )

            return JsonResponse({
                'status': 'success',
                'message': f"Дякуємо, {name}! Ваше бронювання на {date} ({time}) зареєстровано під номером #{reservation.id}. Ми зателефонуємо Вам для підтвердження.",
                'reservation_id': reservation.id
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class ApiOrderView(View):
    """AJAX оформлення замовлення доставки або самовивозу з кошика."""
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            name = data.get('customer_name', '').strip()
            phone = data.get('phone', '').strip()
            order_type = data.get('order_type', 'delivery')
            address = data.get('address', '').strip()
            desired_time = data.get('desired_time', 'Якомога швидше')
            payment_method = data.get('payment_method', 'Готівка або картка при отриманні')
            comment = data.get('comment', '').strip()
            items = data.get('items', [])

            if not name or not phone:
                return JsonResponse({'status': 'error', 'message': "Будь ласка, вкажіть Ваше ім'я та телефон."}, status=400)

            if not items:
                return JsonResponse({'status': 'error', 'message': 'Ваш кошик порожній!'}, status=400)

            subtotal = sum(float(item.get('price', 0)) * int(item.get('quantity', 1)) for item in items)
            # Самовивіз має знижку 10%
            discount = subtotal * 0.10 if order_type == 'takeaway' else 0.0
            total_price = subtotal - discount

            order_number = f"GM-{uuid.uuid4().hex[:6].upper()}"

            order = DeliveryOrder.objects.create(
                order_number=order_number,
                customer_name=name,
                phone=phone,
                order_type=order_type,
                address=address,
                desired_time=desired_time,
                payment_method=payment_method,
                comment=comment,
                items_json=json.dumps(items, ensure_ascii=False),
                subtotal=subtotal,
                discount=discount,
                total_price=total_price
            )

            return JsonResponse({
                'status': 'success',
                'order_number': order_number,
                'total_price': total_price,
                'discount': discount,
                'message': f"Замовлення #{order_number} успішно оформлено! Шеф уже готує Ваші галицькі смаколики."
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
