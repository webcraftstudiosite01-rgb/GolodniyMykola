import os
import sys
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projects.settings')
django.setup()

from django.utils.text import slugify
from projects.models import (
    MenuCategory,
    Dish,
    RestaurantHall,
    RestaurantService,
    Promotion,
    GuestReview
)

def populate():
    print("Clearing old data...")
    Dish.objects.all().delete()
    MenuCategory.objects.all().delete()
    RestaurantHall.objects.all().delete()
    RestaurantService.objects.all().delete()
    Promotion.objects.all().delete()
    GuestReview.objects.all().delete()

    print("Creating Categories & Dishes...")
    with open('cleaned_menu.json', encoding='utf-8') as f:
        data = json.load(f)

    category_icons = {
        'ГАСТРО МЕНЮ': 'fa-solid fa-crown',
        'НА ЗИМНО': 'fa-solid fa-snowflake',
        'САЛАТИ': 'fa-solid fa-leaf',
        'ГАРЯЧІ ПЕРЕКУСИ': 'fa-solid fa-fire-burner',
        'БАНОШІ ТА ВАРЕНИКИ': 'fa-solid fa-bowl-food',
        'ЗУПИ': 'fa-solid fa-mug-hot',
        'ПСТРУГ': 'fa-solid fa-fish',
        'МИКОЛИНЕ М’ЯСИДЛО': 'fa-solid fa-drumstick-bite',
        'СОУСИ ДО М’ЯСА': 'fa-solid fa-pepper-hot',
        'ХЛІБ ТА ДОДАТКИ': 'fa-solid fa-bread-slice',
        'ДЕСЕРТИ': 'fa-solid fa-cake-candles',
        'ЛЬОДИ': 'fa-solid fa-ice-cream',
        'ДЛЯ МИКОЛОК': 'fa-solid fa-child-reaching',
        'НАПОЇ': 'fa-solid fa-beer-mug-empty',
        'Баняк Зупи': 'fa-solid fa-cauldron'
    }

    category_objs = {}
    for i, cat_name in enumerate(data['categories']):
        cat_slug = slugify(cat_name, allow_unicode=True) or f"cat-{i+1}"
        cat_obj, _ = MenuCategory.objects.get_or_create(
            name=cat_name,
            defaults={
                'slug': cat_slug,
                'icon': category_icons.get(cat_name, 'fa-solid fa-utensils'),
                'order': i + 1,
                'is_active': True,
                'description': f"Традиційні галицькі авторські страви категорії «{cat_name}»"
            }
        )
        category_objs[cat_name] = cat_obj

    print(f"Created {len(category_objs)} categories.")

    dishes_created = 0
    slug_counts = {}
    for i, item in enumerate(data['dishes']):
        cat_name = item.get('category_name')
        cat_obj = category_objs.get(cat_name)
        if not cat_obj:
            cat_obj = list(category_objs.values())[0]

        name = item.get('name', 'Страва').strip()
        base_slug = slugify(name, allow_unicode=True) or f"dish-{i+1}"
        slug = base_slug
        if slug in slug_counts:
            slug_counts[slug] += 1
            slug = f"{base_slug}-{slug_counts[slug]}"
        else:
            slug_counts[slug] = 0

        # hit check
        is_hit = False
        is_trout = False
        if 'пструг' in name.lower() or 'пструг' in cat_name.lower():
            is_trout = True
            is_hit = True
        elif 'борщ' in name.lower() or 'банош' in name.lower() or 'вареник' in name.lower() or 'ребр' in name.lower() or 'лосос' in name.lower() or 'ялови' in name.lower():
            is_hit = True

        Dish.objects.create(
            category=cat_obj,
            name=name,
            slug=slug,
            price=item.get('price', 150.0),
            weight=item.get('weight', ''),
            description=item.get('description', ''),
            image_url=item.get('image', ''),
            badge=item.get('badge', 'Хіт' if is_hit else ''),
            is_hit=is_hit,
            is_trout=is_trout,
            is_spicy='гостр' in (item.get('description', '') + name).lower(),
            is_vegetarian='пісн' in (item.get('description', '') + name).lower() or 'овоч' in (item.get('description', '') + name).lower(),
            is_available=True,
            order=i + 1
        )
        dishes_created += 1

    print(f"Created {dishes_created} dishes.")

    # Halls
    halls_data = [
        {
            'name': 'Урочиста зала',
            'slug': 'urochysta-zala',
            'capacity': 'до 230 гостей',
            'floor': '2 поверх',
            'description': 'Найбільша та найсвятковіша банкетна зала комплексу. Нейтральний вишуканий інтер’єр у світлих тонах дозволяє реалізувати будь-яку концепцію декору — від величного українського весілля до офіційної міжнародної конференції.',
            'features': 'Місткість до 230 осіб при банкетній розсадці\nСценічне регульоване освітлення та прожектори\nВеликий екран, мультимедійний проектор, мікрофони\nОкрема зона для ведучого, діджея та живої музики\nПросторий хол для велком-дрінку та кенді-бару',
            'image': '/static/images/hall_urochysta.jpeg',
            'order': 1
        },
        {
            'name': 'Зала з каміном',
            'slug': 'zala-z-kaminom',
            'capacity': '30–50 гостей',
            'floor': '2 поверх',
            'description': 'Особливий простір в європейському аристократичному галицькому стилі з діючим дров’яним каміном, теплим деревом та власним мальовничим балконом. Ідеальне місце для камерних ювілеїв, хрестин та душевних сімейних святкувань.',
            'features': 'Справжній дров’яний камін з живим вогнем\nВласний видовий балкон з панорамою на подвір’я та озеро\nПовна автономність та ізоляція від інших залів\nПреміальний посуд та індивідуальне сервірування\nМожливість підключення власної акустики',
            'image': '/static/images/hall_kamin.jpeg',
            'order': 2
        },
        {
            'name': 'Головна зала зі ставком',
            'slug': 'holovna-zala-zi-stavkom',
            'capacity': 'до 140 гостей',
            'floor': '1 поверх',
            'description': 'Серце ресторану з унікальним подвійним басейном-акваріумом, де плаває жива карпатська форель. Гості можуть обрати рибу просто із залу, спостерігати за роботою відкритої пекарні та відчути справжній колорит гостинного Львова.',
            'features': 'Внутрішня частина живого ставка з фореллю\nВид на відкриту пекарню та автентичні печі\nЗручні дерев’яні столи, дивани та автентичні галицькі деталі\nЖиві камерні виступи під рояль щоп’ятниці та у вихідні\nПрямий вихід на літню терасу',
            'image': '/static/images/hall_interior.jpeg',
            'order': 3
        },
        {
            'name': 'Літнє подвір’я та тераса біля озера',
            'slug': 'litnie-podviria-terasa',
            'capacity': 'до 180 гостей',
            'floor': 'Подвір’я та берег ставка',
            'description': 'Мальовнича зелена оаза на свіжому повітрі: затишні альтанки, набережна вздовж ставка з прохолодною водою, квітучі клумби та літній бар зі свіжим пивом «Кумпель» з власної броварні.',
            'features': 'Зовнішня відкрита частина ставка для спортивної риболовлі\nОкремі затишні дерев’яні альтанки для компаній від 6 до 25 осіб\nЛітній бар з фірмовим кеговим пивом та домашнім квасом\nСвіже повітря подалі від міського шуму\nВечірня романтична ілюмінація ліхтарів',
            'image': '/static/images/restaurant_lake.jpg',
            'order': 4
        },
        {
            'name': 'Дитячий простір та ферма «Хатка для звірятка»',
            'slug': 'dytiachy-prostir',
            'capacity': 'до 60 дітей та батьків',
            'floor': 'Подвір’я та дитяча кімната',
            'description': '«Відпочиваючи з дітьми — відпочиньте від дітей!». Величезний ігровий майданчик з гірками та лазанками, сезонна міні-ферма з доброзичливими кізоньками та курочками, а всередині — тепла ігрова кімната з професійними турботливими нянями.',
            'features': 'Професійні аніматори та няні щодня\nМіні-ферма з домашніми тваринками (можна годувати та гладити)\nВеликий майданчик на м’якому газоні з безпечним покриттям\nОкреме корисне дитяче меню «Для Миколок»\nМайстер-класи з ліплення вареників та випікання булочок',
            'image': '/static/images/kids_farm.jpg',
            'order': 5
        }
    ]

    for h in halls_data:
        RestaurantHall.objects.create(**h)
    print(f"Created {len(halls_data)} restaurant halls.")

    # Services
    services_data = [
        {
            'title': 'Сімейний відпочинок з дітьми',
            'slug': 'simeinyi-vidpochynok-z-ditmy',
            'short_description': 'Величезний майданчик, міні-ферма «Хатка для звірятка», турботливі няні та спеціальне меню для малечі.',
            'description': 'Відпочиваючи з дітьми у «Голодному Миколі», Ви справді відпочиваєте від турбот! У нашому зеленому подвір’ї облаштовано великий сучасний дитячий майданчик з безпечними гірками, канатами, лазанками та гойдалками. Поруч розташована улюблениця всіх малюків — сезонна міні-ферма «Хатка для звірятка», де дітки можуть познайомитися з кізоньками та домашніми птахами. Всередині ресторану працює затишна дитяча кімната з іграшками, розвиваючими іграми, розмальовками та професійними нянями. А шеф-кухар створив особливе, смачне та корисне дитяче меню «Для Миколок».',
            'icon': 'fa-solid fa-children',
            'image': '/static/images/kids_farm.jpg',
            'order': 1
        },
        {
            'title': 'Весілля у галицьких традиціях',
            'slug': 'vesillia',
            'short_description': 'Урочисті зали до 230 гостей, мальовнича виїзна церемонія біля озера, вишукане банкетне меню.',
            'description': 'Весілля у «Голодному Миколі» — це подія, яку гості згадуватимуть роками з теплом та захопленням. Ми пропонуємо величну «Урочисту залу» (до 230 осіб) зі світлим нейтральним інтер’єром, професійним сценічним світлом, екраном та звуком. На березі ставка облаштовується неймовірно красива зона для виїзної весільної церемонії та фотосесії. Наші кухарі приготують багатий весільний стіл зі щедрими галицькими смаколиками, козацьким столом, запеченою рибою та авторськими стравами, а уважний сервіс зробить Ваше свято бездоганним.',
            'icon': 'fa-solid fa-heart',
            'image': '/static/images/hall_urochysta.jpeg',
            'order': 2
        },
        {
            'title': 'Бенкети, ювілеї та дні народження',
            'slug': 'benkety-iuvilei-ta-dni-narodzhennia',
            'short_description': 'Щедрі столи, жива музика, зали на будь-яку кількість гостей та знижка 15% у будні дні.',
            'description': 'Незалежно від того, плануєте Ви пишний ювілей на 100 гостей чи камерне святкування дня народження у колі найближчих — у нас є ідеальний простір. Для великих подій — «Урочиста зала», для камерних зустрічей — аристократична «Зала з каміном» на 30–50 осіб з балконом та дров’яним вогнищем. А при бронюванні банкету з понеділка по четвер діє приємна знижка 15% на все меню!',
            'icon': 'fa-solid fa-champagne-glasses',
            'image': '/static/images/celebration.jpg',
            'order': 3
        },
        {
            'title': 'Корпоративи та свята компаній',
            'slug': 'korporatyvy',
            'short_description': 'Командні заходи, тімбілдінги на свіжому повітрі біля озера, риболовля та банкетне обслуговування.',
            'description': 'Запланували корпоратив? Цього достатньо — про все інше подбаємо ми! Маємо колосальний досвід проведення корпоративних заходів будь-якого масштабу. На території можна організувати як офіційну частину з презентаціями та виступами (проектори, звук, мікрофони), так і неформальний відпочинок: спортивну риболовлю форелі, пивні дегустації від броварні «Кумпель», квести та запальну дискотеку.',
            'icon': 'fa-solid fa-briefcase',
            'image': '/static/images/corporate_hall.jpg',
            'order': 4
        },
        {
            'title': 'Затишні вечері під рояль',
            'slug': 'zatyshni-vecheri',
            'short_description': 'Діючий камін, камерні концерти під фортепіано щоп’ятниці та у вихідні, авторське галицьке вино.',
            'description': 'Після метушливого дня немає нічого кращого, ніж поринути в теплу атмосферу «Голодного Миколи». Потріскування дров у каміні, аромат задимленого бограчу та свіжоспеченого в печі хліба, келих крафтового вина або пива Кумпель. Щойно настає п’ятниця, субота чи неділя (з 18:00 до 20:00), зал наповнюється чарівними звуками живого фортепіано, перетворюючи звичайну вечерю на справжню естетичну насолоду.',
            'icon': 'fa-solid fa-music',
            'image': '/static/images/dinner_ambiance.jpg',
            'order': 5
        },
        {
            'title': 'Миколина крамничка крафту',
            'slug': 'kramnytsia',
            'short_description': 'Крафтові сири, фірмові ковбаси, карпатські наливки, свіжий хліб з пекарні та подарункові кошики.',
            'description': 'У нашій фірмовій крамничці на території ресторану кожен гість може придбати найкращі галицькі делікатеси додому або у подарунок близьким. Ми виготовляємо власні м’ясні делікатеси, коптимо рибу, печемо хліб на заквасці та варимо пиво. Також у продажу подарункові кошики різного розміру та опція «Склади кошик собі сам».',
            'icon': 'fa-solid fa-basket-shopping',
            'image': '/static/images/shop_craft.jpg',
            'order': 6
        },
        {
            'title': 'Конференції та ділові події',
            'slug': 'konferentsii',
            'short_description': 'Мультимедійне обладнання, екран, лазерна указка, повний супровід та авторські кава-брейки.',
            'description': '«Голодний Микола» пропонує сучасну платформу для бізнес-заходів, тренінгів та конференцій. До Ваших послуг окреме меню на coffee-break, комплексні ділові обіди, повний комплект обладнання (проектор, великий екран, презентер, якісний звук та радіомікрофони, швидкісний Wi-Fi). Професійний підхід гарантує успіх Вашої події.',
            'icon': 'fa-solid fa-chalkboard-user',
            'image': '/static/images/hall_urochysta.jpeg',
            'order': 7
        }
    ]

    for s in services_data:
        RestaurantService.objects.create(**s)
    print(f"Created {len(services_data)} services.")

    # Promotions
    promotions_data = [
        {
            'title': 'Особлива шана кожному Миколі!',
            'slug': 'shana-mykolam',
            'badge': 'Для всіх Микол',
            'description': 'Кожен гість на ім’я Микола отримує фірмову іменну подушку «М’яке місце для Миколи», частування на вибір (келих пива «Кумпель», крафтовий лимонад чи чарочку фірмової господаревої самогонки) та право на портрет у Музеї Микол!',
            'terms': 'Діє щодня без обмежень. Достатньо показати будь-який документ, що посвідчує ім’я.',
            'image': '/static/images/restaurant_ext.jpg',
            'order': 1
        },
        {
            'title': 'Знижка 15% на бенкети у будні дні',
            'slug': 'znyzhka-15-na-benkety',
            'badge': '-15% у будні',
            'description': 'Плануйте Ваше свято з вигодою: при бронюванні банкету або дня народження з понеділка по четвер (Пн-Чт) надається приємна знижка 15% на все банкетне меню ресторану.',
            'terms': 'Діє на замовлення банкетів від 10 гостей з Пн по Чт.',
            'image': '/static/images/celebration.jpg',
            'order': 2
        },
        {
            'title': 'Знижка 10% на самовивіз (Takeaway)',
            'slug': 'znyzhka-10-samovyviz',
            'badge': '-10% самовивіз',
            'description': 'Замовляйте улюблені галицькі страви на нашому сайті заздалегідь та забирайте їх особисто з ресторану зі знижкою 10%. Швидко, гаряче та вигідно!',
            'terms': 'Автоматично розраховується при виборі типу замовлення "Самовивіз".',
            'image': '/static/images/dinner_ambiance.jpg',
            'order': 3
        },
        {
            'title': 'Лови свій пструг — шеф приготує!',
            'slug': 'lovy-svii-pstruh',
            'badge': 'Жива форель',
            'description': 'Беріть вудочку на нашій набережній, витягайте свіжу форель просто з озера, а кухарі «Голодного Миколи» миттєво підсмажать її на деревному вугіллі або підкоптять до Вашого столу.',
            'terms': 'Вудочки та наживка надаються безкоштовно для гостей ресторану.',
            'image': '/static/images/restaurant_lake.jpg',
            'order': 4
        }
    ]

    for p in promotions_data:
        Promotion.objects.create(**p)
    print(f"Created {len(promotions_data)} promotions.")

    # Reviews
    reviews_data = [
        {
            'author': 'Оксана та Тарас Мельник',
            'city': 'Львів',
            'rating': 5,
            'text': 'Святкували наше весілля в Урочистій залі на 140 людей. Це просто казка! Зала простора, надзвичайно гарне світло, сервіс на найвищому рівні. Гості були в захваті від риби, яку самі ловили перед банкетом у ставку, та задимленого бограчу. Окрема подяка пану Миколі за гостинність!',
            'source': 'Google Відгуки',
            'date': '2 тижні тому'
        },
        {
            'author': 'Микола Ковальчук',
            'city': 'Київ',
            'rating': 5,
            'text': 'Як тільки зайшов і сказав, що я Микола — одразу настрій піднявся на 100%! Подушка для Миколи, келих крижаного пива Кумпель від господаря, смачнюща ковбаса та найкращий банош у моєму житті. Тепер це мій обов’язковий пункт зупинки щоразу, коли приїжджаю до Львова.',
            'source': 'Google Відгуки',
            'date': 'Місяць тому'
        },
        {
            'author': 'Ірина Васильченко',
            'city': 'Івано-Франківськ',
            'rating': 5,
            'text': 'Ідеальне місце для сімейного відпочинку. Діти 3 години бавилися на майданчику та бігали до кізоньок на міні-фермі під наглядом няні, а ми з чоловіком спокійно вечеряли біля каміна під живу музику рояля. Форель на вугіллі — шедевр!',
            'source': 'TripAdvisor',
            'date': '3 тижні тому'
        },
        {
            'author': 'Андрій Демкович (IT Soft)',
            'city': 'Львів',
            'rating': 5,
            'text': 'Проводили тут річний корпоратив компанії на 90 осіб. Організація 10/10: проектор, звук, ведучий, шалена смачна кухня. Риболовля на форель викликала у всієї команди справжній азарт. Дякуємо адміністрації!',
            'source': 'Google Відгуки',
            'date': '2 місяці тому'
        }
    ]

    for r in reviews_data:
        GuestReview.objects.create(**r)
    print(f"Created {len(reviews_data)} reviews.")

    print("ALL SEED DATA INSERTED SUCCESSFULLY!")

if __name__ == '__main__':
    populate()
