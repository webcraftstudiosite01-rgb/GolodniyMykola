/**
 * Next-Level Interactive Engine for Restaurant 'Голодний Микола'
 * Features:
 * - Ultra-Smooth Organic Trout Pond Physics (Flawless boundary steering, zero spinning bugs)
 * - Interactive Gastronomic Sommelier (Pairing Kumpel craft beer & homemade infusions)
 * - 360° Panoramic Virtual Tour Viewer ("3D-Тур по залах")
 * - Interactive Banquet Budget & Menu Calculator
 * - Interactive Floorplan Table Selector
 * - VIP Mykola Certificate Generator
 * - Water Droplet Click Ripples & Luxury Button Sheen
 * - Shopping Cart & Instant AJAX Booking
 */

// ==========================================
// 1. SHOPPING CART ENGINE
// ==========================================
const CART_STORAGE_KEY = 'mykola_cart_items_v2';
let currentOrderType = 'delivery'; // 'delivery' or 'takeaway'

function getCart() {
    try {
        const stored = localStorage.getItem(CART_STORAGE_KEY);
        return stored ? JSON.parse(stored) : [];
    } catch (e) {
        return [];
    }
}

function saveCart(cart) {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart));
    updateCartUI();
}

function addToCart(id, name, price, weight, imageUrl) {
    let cart = getCart();
    const existing = cart.find(item => item.id == id);
    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({
            id: id,
            name: name,
            price: parseFloat(price),
            weight: weight || '',
            image: imageUrl || '',
            quantity: 1
        });
    }
    saveCart(cart);
    showToast(`«${name}» додано до кошика!`);
}

function updateCartItemQty(id, delta) {
    let cart = getCart();
    const item = cart.find(i => i.id == id);
    if (!item) return;

    item.quantity += delta;
    if (item.quantity <= 0) {
        cart = cart.filter(i => i.id != id);
    }
    saveCart(cart);
}

function removeCartItem(id) {
    let cart = getCart().filter(i => i.id != id);
    saveCart(cart);
}

function clearCart() {
    saveCart([]);
}

function updateCartUI() {
    const cart = getCart();
    const totalCount = cart.reduce((acc, item) => acc + item.quantity, 0);

    ['floating-cart-badge', 'nav-cart-badge', 'mobile-nav-cart-badge'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerText = totalCount;
    });

    const container = document.getElementById('cart-items-container');
    if (!container) return;

    if (cart.length === 0) {
        container.innerHTML = `
            <div class="text-center py-10 text-stone-500">
                <i class="fa-solid fa-basket-shopping text-4xl mb-3 opacity-40"></i>
                <p class="text-base font-medium">Ваш кошик наразі порожній</p>
                <p class="text-xs text-stone-600 mt-1">Оберіть найсмачніші галицькі страви з нашого меню!</p>
            </div>
        `;
    } else {
        container.innerHTML = cart.map(item => `
            <div class="flex items-center justify-between p-3 rounded-2xl bg-stone-900/80 border border-stone-800 gap-3">
                <div class="flex items-center space-x-3 min-w-0">
                    ${item.image ? `<img src="${item.image}" alt="${item.name}" class="w-12 h-12 rounded-xl object-cover border border-stone-700 flex-shrink-0">` : `<div class="w-12 h-12 rounded-xl bg-stone-800 flex items-center justify-center text-amber-500 flex-shrink-0"><i class="fa-solid fa-utensils"></i></div>`}
                    <div class="min-w-0">
                        <h4 class="text-sm font-bold text-white truncate">${item.name}</h4>
                        <p class="text-xs text-stone-400">${item.price} грн ${item.weight ? '• ' + item.weight : ''}</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3 flex-shrink-0">
                    <div class="flex items-center space-x-1.5 bg-stone-950 px-2 py-1 rounded-xl border border-stone-800">
                        <button onclick="updateCartItemQty('${item.id}', -1)" class="w-6 h-6 rounded-lg text-stone-400 hover:text-white hover:bg-stone-800 flex items-center justify-center font-bold text-sm">-</button>
                        <span class="w-6 text-center text-xs font-bold text-white">${item.quantity}</span>
                        <button onclick="updateCartItemQty('${item.id}', 1)" class="w-6 h-6 rounded-lg text-stone-400 hover:text-white hover:bg-stone-800 flex items-center justify-center font-bold text-sm">+</button>
                    </div>
                    <span class="text-sm font-bold text-amber-400 w-20 text-right">${(item.price * item.quantity).toFixed(0)} грн</span>
                    <button onclick="removeCartItem('${item.id}')" class="text-stone-500 hover:text-red-400 p-1">
                        <i class="fa-solid fa-trash-can text-xs"></i>
                    </button>
                </div>
            </div>
        `).join('');
    }

    const subtotal = cart.reduce((acc, item) => acc + (item.price * item.quantity), 0);
    const isTakeaway = currentOrderType === 'takeaway';
    const discount = isTakeaway ? subtotal * 0.10 : 0;
    const total = subtotal - discount;

    const subtotalDisplay = document.getElementById('cart-subtotal-display');
    if (subtotalDisplay) subtotalDisplay.innerText = `${subtotal.toFixed(0)} грн`;

    const discountRow = document.getElementById('cart-discount-row');
    const discountDisplay = document.getElementById('cart-discount-display');
    if (discountRow && discountDisplay) {
        if (isTakeaway && subtotal > 0) {
            discountRow.classList.remove('hidden');
            discountDisplay.innerText = `-${discount.toFixed(0)} грн (-10%)`;
        } else {
            discountRow.classList.add('hidden');
        }
    }

    const totalDisplay = document.getElementById('cart-total-display');
    if (totalDisplay) totalDisplay.innerText = `${total.toFixed(0)} грн`;

    const deliveryCostDisplay = document.getElementById('cart-delivery-cost');
    if (deliveryCostDisplay) {
        if (isTakeaway) {
            deliveryCostDisplay.innerText = 'Самовивіз (безкоштовно)';
        } else if (subtotal >= 1700) {
            deliveryCostDisplay.innerHTML = '<span class="text-emerald-400 font-bold">Безкоштовно!</span>';
        } else {
            deliveryCostDisplay.innerText = 'За тарифом (безкоштовно від 1700 грн)';
        }
    }
}

function setOrderType(type) {
    currentOrderType = type;
    const btnDel = document.getElementById('btn-order-delivery');
    const btnTake = document.getElementById('btn-order-takeaway');
    const addrGroup = document.getElementById('order-address-group');
    const addrInput = document.getElementById('order-address');

    if (type === 'takeaway') {
        if (btnTake) btnTake.className = 'px-4 py-1.5 rounded-lg text-xs font-bold transition-all bg-amber-500 text-stone-950 shadow';
        if (btnDel) btnDel.className = 'px-4 py-1.5 rounded-lg text-xs font-bold transition-all text-stone-300 hover:text-white';
        if (addrGroup) addrGroup.classList.add('hidden');
        if (addrInput) addrInput.removeAttribute('required');
    } else {
        if (btnDel) btnDel.className = 'px-4 py-1.5 rounded-lg text-xs font-bold transition-all bg-amber-500 text-stone-950 shadow';
        if (btnTake) btnTake.className = 'px-4 py-1.5 rounded-lg text-xs font-bold transition-all text-stone-300 hover:text-white';
        if (addrGroup) addrGroup.classList.remove('hidden');
        if (addrInput) addrInput.setAttribute('required', 'true');
    }
    updateCartUI();
}

function openCartModal() {
    const modal = document.getElementById('cart-modal');
    if (modal) {
        modal.classList.remove('hidden');
        updateCartUI();
    }
}

function closeCartModal() {
    const modal = document.getElementById('cart-modal');
    if (modal) modal.classList.add('hidden');
}

function openBookingModal(initialHall, initialEvent, initialTable) {
    const modal = document.getElementById('booking-modal');
    if (modal) {
        modal.classList.remove('hidden');
        const dateInput = document.getElementById('modal-booking-date');
        if (dateInput && !dateInput.value) {
            const today = new Date().toISOString().split('T')[0];
            dateInput.value = today;
            dateInput.min = today;
        }
        if (initialHall) {
            const hallSelect = modal.querySelector('select[name="hall"]');
            if (hallSelect) hallSelect.value = initialHall;
        }
        if (initialTable) {
            const req = modal.querySelector('textarea[name="special_requests"]');
            if (req) req.value = `Бажаний столик: ${initialTable}\n` + req.value;
        }
    }
}

function closeBookingModal() {
    const modal = document.getElementById('booking-modal');
    if (modal) modal.classList.add('hidden');
}

function showToast(message) {
    let toast = document.getElementById('mykola-toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'mykola-toast';
        toast.className = 'fixed top-24 right-6 z-50 px-5 py-3.5 rounded-2xl bg-amber-500 text-stone-950 font-bold text-sm shadow-2xl transition-all duration-300 transform translate-y-[-20px] opacity-0 flex items-center space-x-2 border border-amber-300';
        document.body.appendChild(toast);
    }
    toast.innerHTML = `<i class="fa-solid fa-circle-check text-stone-950 text-base"></i><span>${message}</span>`;
    toast.style.transform = 'translateY(0)';
    toast.style.opacity = '1';

    setTimeout(() => {
        toast.style.transform = 'translateY(-20px)';
        toast.style.opacity = '0';
    }, 3200);
}

// ==========================================
// 2. ULTRA-SMOOTH ORGANIC TROUT POND SIMULATOR
// (Fixed: No wall corner glitching, natural boid steering)
// ==========================================
const TroutPondGame = {
    canvas: null,
    ctx: null,
    animId: null,
    state: 'idle',
    biteTimer: null,
    biteTimeoutTimer: null,
    fish: [],
    ripples: [],
    floatPos: { x: 0, y: 0, active: false, vy: 0 },

    init() {
        this.canvas = document.getElementById('trout-pond-canvas');
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext('2d');
        this.resize();
        window.addEventListener('resize', () => this.resize());

        // Spawn 6 trout with natural steering properties
        this.fish = [];
        for (let i = 0; i < 6; i++) {
            const angle = Math.random() * Math.PI * 2;
            this.fish.push({
                x: 60 + Math.random() * (this.canvas.width - 120),
                y: 60 + Math.random() * (this.canvas.height - 120),
                currentAngle: angle,
                targetAngle: angle,
                speed: 1.1 + Math.random() * 0.6,
                length: 36 + Math.random() * 18,
                wiggle: Math.random() * 10,
                wiggleSpeed: 0.12 + Math.random() * 0.06
            });
        }

        this.startLoop();
    },

    resize() {
        if (!this.canvas) return;
        const rect = this.canvas.getBoundingClientRect();
        this.canvas.width = rect.width;
        this.canvas.height = rect.height;
    },

    castRod() {
        if (this.state === 'casting' || this.state === 'waiting' || this.state === 'biting') return;
        this.state = 'casting';

        const btn = document.getElementById('pond-action-btn');
        const status = document.getElementById('pond-status-text');
        if (btn) {
            btn.innerText = 'Закидаємо вудку...';
            btn.className = 'w-full py-4 rounded-2xl bg-stone-800 text-stone-400 font-bold text-xs uppercase cursor-not-allowed';
        }
        if (status) status.innerHTML = '<span class="text-amber-400 animate-pulse">Вудка летить у воду...</span>';

        setTimeout(() => {
            this.floatPos = {
                x: this.canvas.width * 0.45 + (Math.random() * 60 - 30),
                y: this.canvas.height * 0.5 + (Math.random() * 40 - 20),
                active: true,
                vy: 0
            };
            this.addRipple(this.floatPos.x, this.floatPos.y, 4, 35);
            this.state = 'waiting';

            if (btn) btn.innerText = 'Чекаємо покльовки...';
            if (status) status.innerHTML = '<span class="text-stone-300">Поплавок на воді. Слідкуйте за рухом!</span>';

            const biteDelay = 2200 + Math.random() * 2200;
            this.biteTimer = setTimeout(() => {
                this.triggerBite();
            }, biteDelay);
        }, 700);
    },

    triggerBite() {
        if (this.state !== 'waiting') return;
        this.state = 'biting';

        const btn = document.getElementById('pond-action-btn');
        const status = document.getElementById('pond-status-text');
        if (btn) {
            btn.innerText = '💥 КЛЮЄ! ТЯГНИ!';
            btn.className = 'w-full py-4 rounded-2xl bg-gradient-to-r from-red-600 via-amber-500 to-red-600 text-white font-black text-sm uppercase shadow-2xl animate-bounce cursor-pointer btn-sheen';
            btn.onclick = () => this.hookFish();
        }
        if (status) status.innerHTML = '<strong class="text-red-400 text-sm animate-pulse">КЛЮЄ! ШВИДКО ТЯГНІТЬ!</strong>';

        for (let i = 0; i < 4; i++) {
            setTimeout(() => {
                this.addRipple(this.floatPos.x, this.floatPos.y, 8, 50);
            }, i * 300);
        }

        this.biteTimeoutTimer = setTimeout(() => {
            if (this.state === 'biting') this.missFish();
        }, 3400);
    },

    hookFish() {
        if (this.state !== 'biting') return;
        clearTimeout(this.biteTimeoutTimer);
        this.state = 'caught';

        const weight = Math.floor(390 + Math.random() * 150);
        const promoCode = 'PSTRUG-MYKOLA-' + Math.floor(100 + Math.random() * 900);

        for (let i = 0; i < 8; i++) {
            this.addRipple(this.floatPos.x + (Math.random() * 40 - 20), this.floatPos.y + (Math.random() * 40 - 20), 12, 60);
        }

        const modal = document.getElementById('pond-trophy-modal');
        if (modal) {
            document.getElementById('trophy-weight').innerText = `${weight} грамів`;
            document.getElementById('trophy-promo').innerText = promoCode;
            modal.classList.remove('hidden');
        }

        this.resetGame();
    },

    missFish() {
        this.state = 'idle';
        this.floatPos.active = false;
        const btn = document.getElementById('pond-action-btn');
        const status = document.getElementById('pond-status-text');
        if (btn) {
            btn.innerText = '🎣 Закинути вудку знову';
            btn.className = 'w-full py-4 rounded-2xl bg-amber-500 hover:bg-amber-400 text-stone-950 font-bold text-xs uppercase shadow transition-all btn-sheen';
            btn.onclick = () => this.castRod();
        }
        if (status) status.innerHTML = '<span class="text-stone-400">Ех, форель зірвалася з гачка! Спробуйте ще раз.</span>';
    },

    resetGame() {
        this.state = 'idle';
        this.floatPos.active = false;
        const btn = document.getElementById('pond-action-btn');
        const status = document.getElementById('pond-status-text');
        if (btn) {
            btn.innerText = '🎣 Закинути вудку ще раз';
            btn.className = 'w-full py-4 rounded-2xl bg-amber-500 hover:bg-amber-400 text-stone-950 font-bold text-xs uppercase shadow transition-all btn-sheen';
            btn.onclick = () => this.castRod();
        }
        if (status) status.innerHTML = '<span class="text-stone-300">Вітаємо з уловом! Натисніть кнопку, щоб спробувати знову.</span>';
    },

    addRipple(x, y, maxR, maxLife) {
        this.ripples.push({ x, y, r: 2, maxR, life: maxLife, maxLife });
    },

    startLoop() {
        const render = () => {
            this.update();
            this.draw();
            this.animId = requestAnimationFrame(render);
        };
        this.animId = requestAnimationFrame(render);
    },

    // Smooth angle difference utility
    normalizeAngle(diff) {
        while (diff < -Math.PI) diff += Math.PI * 2;
        while (diff > Math.PI) diff -= Math.PI * 2;
        return diff;
    },

    update() {
        const w = this.canvas.width;
        const h = this.canvas.height;
        const margin = 55;

        // Fish smooth organic steering
        this.fish.forEach(f => {
            f.wiggle += f.wiggleSpeed;

            // Boundary avoidance vector
            let steerX = 0;
            let steerY = 0;

            if (f.x < margin) steerX += (margin - f.x) / margin;
            if (f.x > w - margin) steerX -= (f.x - (w - margin)) / margin;
            if (f.y < margin) steerY += (margin - f.y) / margin;
            if (f.y > h - margin) steerY -= (f.y - (h - margin)) / margin;

            if (steerX !== 0 || steerY !== 0) {
                // Steer away from walls toward pond center
                f.targetAngle = Math.atan2(steerY, steerX);
            } else {
                // Gentle wandering in open water
                if (Math.random() < 0.02) {
                    f.targetAngle += (Math.random() - 0.5) * 0.5;
                }
            }

            // Smoothly interpolate currentAngle toward targetAngle (max turn rate 0.045 rad/frame)
            const angleDiff = this.normalizeAngle(f.targetAngle - f.currentAngle);
            const maxTurn = 0.045;
            f.currentAngle += Math.sign(angleDiff) * Math.min(Math.abs(angleDiff), maxTurn);

            // Move forward
            f.x += Math.cos(f.currentAngle) * f.speed;
            f.y += Math.sin(f.currentAngle) * f.speed;

            // Hard clamp so fish never leave water
            f.x = Math.max(25, Math.min(w - 25, f.x));
            f.y = Math.max(25, Math.min(h - 25, f.y));
        });

        // Update ripples
        for (let i = this.ripples.length - 1; i >= 0; i--) {
            const r = this.ripples[i];
            r.r += 0.75;
            r.life -= 1;
            if (r.life <= 0) this.ripples.splice(i, 1);
        }

        // Float bobbing
        if (this.floatPos.active) {
            if (this.state === 'biting') {
                this.floatPos.vy = Math.sin(Date.now() * 0.02) * 5;
            } else {
                this.floatPos.vy = Math.sin(Date.now() * 0.003) * 1.5;
            }
        }
    },

    draw() {
        const ctx = this.ctx;
        const w = this.canvas.width;
        const h = this.canvas.height;

        // Clear water background
        ctx.fillStyle = '#07160f';
        ctx.fillRect(0, 0, w, h);

        const grad = ctx.createRadialGradient(w/2, h/2, 20, w/2, h/2, Math.max(w, h));
        grad.addColorStop(0, '#0f2f21');
        grad.addColorStop(0.7, '#081c13');
        grad.addColorStop(1, '#05110c');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, w, h);

        // Water caustics
        const time = Date.now() * 0.001;
        ctx.fillStyle = 'rgba(16, 185, 129, 0.03)';
        for (let c = 0; c < 3; c++) {
            ctx.beginPath();
            ctx.ellipse(
                w * 0.3 + Math.sin(time + c) * 40,
                h * 0.4 + Math.cos(time + c * 1.5) * 30,
                w * 0.25,
                h * 0.2,
                time * 0.1,
                0,
                Math.PI * 2
            );
            ctx.fill();
        }

        // Draw Swimming Trout with natural silhouettes
        this.fish.forEach(f => {
            ctx.save();
            ctx.translate(f.x, f.y);
            ctx.rotate(f.currentAngle);

            // Soft shadow beneath fish
            ctx.fillStyle = 'rgba(2, 10, 6, 0.45)';
            ctx.beginPath();
            ctx.ellipse(4, 4, f.length * 0.5, 6, 0, 0, Math.PI * 2);
            ctx.fill();

            // Trout body (olive-silver gradient)
            const bodyGrad = ctx.createLinearGradient(0, -5, 0, 5);
            bodyGrad.addColorStop(0, 'rgba(40, 95, 65, 0.85)');
            bodyGrad.addColorStop(0.5, 'rgba(85, 150, 110, 0.9)');
            bodyGrad.addColorStop(1, 'rgba(140, 185, 155, 0.7)');

            ctx.fillStyle = bodyGrad;
            ctx.beginPath();
            ctx.ellipse(0, 0, f.length * 0.5, 5.5, 0, 0, Math.PI * 2);
            ctx.fill();

            // Trout lateral pink/reddish sheen
            ctx.fillStyle = 'rgba(220, 80, 80, 0.4)';
            ctx.beginPath();
            ctx.ellipse(f.length * 0.05, 0, f.length * 0.35, 1.8, 0, 0, Math.PI * 2);
            ctx.fill();

            // Pectoral fin
            ctx.fillStyle = 'rgba(130, 190, 150, 0.5)';
            ctx.beginPath();
            ctx.ellipse(f.length * 0.18, 4, 5, 2, 0.4, 0, Math.PI * 2);
            ctx.fill();

            // Undulating Tail Fin
            const tailWiggle = Math.sin(f.wiggle) * 4.5;
            ctx.beginPath();
            ctx.moveTo(-f.length * 0.5, 0);
            ctx.quadraticCurveTo(
                -f.length * 0.65, tailWiggle * 0.5,
                -f.length * 0.75, -5.5 + tailWiggle
            );
            ctx.lineTo(-f.length * 0.75, 5.5 + tailWiggle);
            ctx.closePath();
            ctx.fillStyle = 'rgba(100, 165, 130, 0.75)';
            ctx.fill();

            ctx.restore();
        });

        // Draw Ripples
        this.ripples.forEach(r => {
            const alpha = r.life / r.maxLife;
            ctx.strokeStyle = `rgba(245, 158, 11, ${alpha * 0.45})`;
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.ellipse(r.x, r.y, r.r, r.r * 0.55, 0, 0, Math.PI * 2);
            ctx.stroke();
        });

        // Draw Float if active
        if (this.floatPos.active) {
            const fx = this.floatPos.x;
            const fy = this.floatPos.y + this.floatPos.vy;

            // Float shadow
            ctx.fillStyle = 'rgba(0,0,0,0.5)';
            ctx.beginPath();
            ctx.ellipse(fx + 2, fy + 4, 6, 3, 0, 0, Math.PI * 2);
            ctx.fill();

            // Float lower body
            ctx.fillStyle = '#f5f5f4';
            ctx.beginPath();
            ctx.arc(fx, fy + 2, 5, 0, Math.PI);
            ctx.fill();

            // Float upper body
            ctx.fillStyle = '#dc2626';
            ctx.beginPath();
            ctx.arc(fx, fy + 2, 5, Math.PI, Math.PI * 2);
            ctx.fill();

            // Antenna
            ctx.strokeStyle = '#f59e0b';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(fx, fy - 3);
            ctx.lineTo(fx, fy - 12);
            ctx.stroke();

            // Antenna tip
            ctx.fillStyle = '#fbbf24';
            ctx.beginPath();
            ctx.arc(fx, fy - 12, 2.5, 0, Math.PI * 2);
            ctx.fill();
        }
    }
};

// ==========================================
// 3. GASTRO SOMMELIER: KUMPEL BEER & TINCTURE PAIRING
// ==========================================
const GastroSommelier = {
    pairings: {
        'fish': {
            title: 'До свіжої риби та пструга зі ставка',
            beer: 'Пиво «Кумпель Галицьке Світле»',
            beerDesc: 'Класичне нефільтроване світле лагерного типу з легким хмелевим післясмаком. Ідеально підкреслює ніжний смак форелі на вугіллі.',
            beerPrice: 160,
            tincture: 'Лимонівка на карпатському меду',
            tinctureDesc: 'Освіжаюча авторська настоянка на свіжому цитриновому фреші та лісовому меді.',
            tincturePrice: 95
        },
        'meat': {
            title: 'До миколиного м’ясидла та стейків',
            beer: 'Пиво «Кумпель Бурштинове Преміум»',
            beerDesc: 'Насичене, з глибоким карамельним солодовим тілом та м’якою гірчинкою. Бездоганно поєднується з яловичиною та ковбасами.',
            beerPrice: 175,
            tincture: 'Фірмова Хрінівка від пана Миколи',
            tinctureDesc: 'Міцна настоянка на свіжому корені хріну з додаванням дикого меду — гордість нашого закладу.',
            tincturePrice: 95
        },
        'soups': {
            title: 'До задимленого бограчу та баняку борщу',
            beer: 'Пиво «Кумпель Темне Оксамитове»',
            beerDesc: 'Щільне темне пиво з шоколадно-кавовими нотками смаженого солоду. Створює багату гармонію з гарячими печеними стравами.',
            beerPrice: 170,
            tincture: 'Галицька Зубрівка та Перцівка',
            tinctureDesc: 'Пряна настоянка на травах та червоному гострому перці, що зігріває душу.',
            tincturePrice: 90
        },
        'desserts': {
            title: 'До пляцків, сирників та десертів',
            beer: 'Крафтовий медовий Квас із печі',
            beerDesc: 'Натуральний живий хлібний квас на заквасці з додаванням м’яти та меду.',
            beerPrice: 95,
            tincture: 'Карпатська Вишнівка на лісових ягодах',
            tinctureDesc: 'Густа, солодко-терпка ягідна настоянка ручної роботи пана Миколи.',
            tincturePrice: 105
        }
    },

    selectCategory(catKey) {
        const data = this.pairings[catKey];
        if (!data) return;

        document.querySelectorAll('.sommelier-pill').forEach(btn => {
            if (btn.getAttribute('data-cat') === catKey) {
                btn.className = 'sommelier-pill px-4 py-2.5 rounded-2xl text-xs font-bold transition-all bg-amber-500 text-stone-950 shadow whitespace-nowrap btn-sheen';
            } else {
                btn.className = 'sommelier-pill px-4 py-2.5 rounded-2xl text-xs font-bold transition-all bg-stone-900 text-stone-300 hover:text-white border border-stone-800 whitespace-nowrap';
            }
        });

        const titleEl = document.getElementById('somm-title');
        const beerNameEl = document.getElementById('somm-beer-name');
        const beerDescEl = document.getElementById('somm-beer-desc');
        const beerPriceEl = document.getElementById('somm-beer-price');
        const tincNameEl = document.getElementById('somm-tinc-name');
        const tincDescEl = document.getElementById('somm-tinc-desc');
        const tincPriceEl = document.getElementById('somm-tinc-price');

        if (titleEl) titleEl.innerText = data.title;
        if (beerNameEl) beerNameEl.innerText = data.beer;
        if (beerDescEl) beerDescEl.innerText = data.beerDesc;
        if (beerPriceEl) beerPriceEl.innerText = `${data.beerPrice} грн`;
        if (tincNameEl) tincNameEl.innerText = data.tincture;
        if (tincDescEl) tincDescEl.innerText = data.tinctureDesc;
        if (tincPriceEl) tincPriceEl.innerText = `${data.tincturePrice} грн`;

        const addBeerBtn = document.getElementById('somm-add-beer-btn');
        const addTincBtn = document.getElementById('somm-add-tinc-btn');

        if (addBeerBtn) {
            addBeerBtn.onclick = () => addToCart('somm-beer-' + catKey, data.beer, data.beerPrice, '1 л', '');
        }
        if (addTincBtn) {
            addTincBtn.onclick = () => addToCart('somm-tinc-' + catKey, data.tincture, data.tincturePrice, '50 мл', '');
        }
    }
};

// ==========================================
// 4. 360° VIRTUAL TOUR VIEWER
// ==========================================
const VirtualTour = {
    currentHall: 'urochysta',
    halls: {
        'urochysta': {
            title: 'Урочиста зала',
            capacity: 'до 230 гостей (2 поверх)',
            desc: 'Велична зала у світлих тонах зі сценічним світлом, екраном, проектором та простором для живої музики і танців.',
            image: '/static/images/hall_urochysta.jpeg'
        },
        'kamin': {
            title: 'Зала з каміном',
            capacity: '30–50 гостей (2 поверх)',
            desc: 'Аристократичний простір з діючим дров’яним каміном, панорамним балконом на озеро та приватною атмосферою.',
            image: '/static/images/hall_kamin.jpeg'
        },
        'stavok': {
            title: 'Головна зала зі ставком',
            capacity: 'до 140 гостей (1 поверх)',
            desc: 'Внутрішня частина ставка з живою карпатською фореллю, вид на відкриту пекарню та рояль.',
            image: '/static/images/hall_interior.jpeg'
        },
        'terasa': {
            title: 'Літнє подвір’я та тераса біля озера',
            capacity: 'до 180 гостей (Подвір’я)',
            desc: 'Затишні альтанки вздовж води, спортивна риболовля форелі на вудку, сад та літній бар пива «Кумпель».',
            image: '/static/images/restaurant_lake.jpg'
        },
        'farm': {
            title: 'Дитячий простір та ферма «Хатка для звірятка»',
            capacity: 'до 60 дітей та батьків',
            desc: 'Ігровий майданчик з канатами, сезонна міні-ферма з кізоньками та курочками, тепла дитяча кімната з нянею.',
            image: '/static/images/kids_farm.jpg'
        }
    },

    open(hallKey) {
        this.currentHall = hallKey || 'urochysta';
        const modal = document.getElementById('virtual-tour-modal');
        if (modal) {
            modal.classList.remove('hidden');
            this.switchHall(this.currentHall);
        }
    },

    close() {
        const modal = document.getElementById('virtual-tour-modal');
        if (modal) modal.classList.add('hidden');
    },

    switchHall(hallKey) {
        this.currentHall = hallKey;
        const hall = this.halls[hallKey];
        if (!hall) return;

        document.getElementById('tour-hall-title').innerText = hall.title;
        document.getElementById('tour-hall-capacity').innerText = hall.capacity;
        document.getElementById('tour-hall-desc').innerText = hall.desc;
        const img = document.getElementById('tour-hall-img');
        if (img) img.src = hall.image;

        document.querySelectorAll('.tour-pill').forEach(btn => {
            if (btn.getAttribute('data-hall') === hallKey) {
                btn.className = 'tour-pill px-4 py-2 rounded-xl text-xs font-bold transition-all bg-amber-500 text-stone-950 shadow whitespace-nowrap btn-sheen';
            } else {
                btn.className = 'tour-pill px-4 py-2 rounded-xl text-xs font-bold transition-all bg-stone-900 text-stone-300 hover:text-white border border-stone-800 whitespace-nowrap';
            }
        });
    },

    bookCurrentHall() {
        const hall = this.halls[this.currentHall];
        this.close();
        openBookingModal(hall ? hall.title : '');
    }
};

function openVirtualTourModal(hallKey) {
    VirtualTour.open(hallKey);
}

// ==========================================
// 5. INTERACTIVE BANQUET CALCULATOR
// ==========================================
const BanquetCalculator = {
    guests: 35,
    budgetPerPerson: 1200,
    format: 'Ювілей / День народження',

    init() {
        const guestsSlider = document.getElementById('calc-guests-slider');
        const budgetSlider = document.getElementById('calc-budget-slider');
        const formatSelect = document.getElementById('calc-format-select');

        if (guestsSlider) {
            guestsSlider.addEventListener('input', (e) => {
                this.guests = parseInt(e.target.value);
                this.update();
            });
        }
        if (budgetSlider) {
            budgetSlider.addEventListener('input', (e) => {
                this.budgetPerPerson = parseInt(e.target.value);
                this.update();
            });
        }
        if (formatSelect) {
            formatSelect.addEventListener('change', (e) => {
                this.format = e.target.value;
                this.update();
            });
        }

        this.update();
    },

    update() {
        const guestsVal = document.getElementById('calc-guests-val');
        const budgetVal = document.getElementById('calc-budget-val');
        if (guestsVal) guestsVal.innerText = `${this.guests} гостей`;
        if (budgetVal) budgetVal.innerText = `${this.budgetPerPerson} грн / особа`;

        const total = this.guests * this.budgetPerPerson;
        const weekdayDiscount = total * 0.15;
        const totalWithDiscount = total - weekdayDiscount;

        const totalEl = document.getElementById('calc-total-display');
        const discountEl = document.getElementById('calc-discount-display');
        const hallEl = document.getElementById('calc-recommended-hall');
        const menuEl = document.getElementById('calc-menu-summary');

        if (totalEl) totalEl.innerText = `${total.toLocaleString('uk-UA')} грн`;
        if (discountEl) discountEl.innerText = `${totalWithDiscount.toLocaleString('uk-UA')} грн (економія ${weekdayDiscount.toLocaleString('uk-UA')} грн)`;

        let recHall = 'Головна зала зі ставком';
        if (this.guests > 65) {
            recHall = 'Урочиста зала (до 230 гостей)';
        } else if (this.guests >= 25 && this.guests <= 65) {
            recHall = 'Зала з каміном (30–50 гостей)';
        } else {
            recHall = 'Головна зала або Тераса біля озера';
        }
        if (hallEl) hallEl.innerText = recHall;

        let menuSummary = '';
        if (this.budgetPerPerson >= 1600) {
            menuSummary = 'Преміум: Баняк борщу з ребрами, запечений пструг зі ставка, стейки, галицьке м’ясидло, крафтові сири, пиво Кумпель, святковий торт.';
        } else if (this.budgetPerPerson >= 1100) {
            menuSummary = 'Класичний: Пструг на вугіллі, макітри вареників, банош зі шкварками, асорті ковбас, салати, настоянки від пана Миколи.';
        } else {
            menuSummary = 'Базовий ситний: Задимлений бограч, фірмові ковбаски з печі, картопля по-галицьки, салати, квас та свіжий хліб.';
        }
        if (menuEl) menuEl.innerText = menuSummary;
    },

    bookWithEstimate() {
        openBookingModal(
            document.getElementById('calc-recommended-hall')?.innerText,
            this.format,
            `Розрахунок свята: ${this.guests} гостей по ${this.budgetPerPerson} грн/особа. Загальний бюджет: ~${(this.guests * this.budgetPerPerson).toLocaleString()} грн.`
        );
    }
};

// ==========================================
// 6. INTERACTIVE TABLE FLOORPLAN SELECTOR
// ==========================================
function selectTable(tableId, tableName, capacity, hallName) {
    document.querySelectorAll('.table-node').forEach(t => t.classList.remove('active-table'));
    const target = document.getElementById(`tbl-${tableId}`);
    if (target) target.classList.add('active-table');

    const preview = document.getElementById('selected-table-preview');
    if (preview) {
        preview.innerHTML = `
            <div class="flex items-center justify-between p-3 rounded-2xl bg-amber-500/15 border border-amber-500/40 text-xs">
                <div>
                    <span class="font-bold text-white text-sm block">${tableName}</span>
                    <span class="text-stone-300">${hallName} • Місткість: ${capacity}</span>
                </div>
                <button onclick="openBookingModal('${hallName}', 'Бронювання столика', '${tableName}')" class="px-4 py-2 rounded-xl bg-amber-500 text-stone-950 font-bold text-xs uppercase shadow hover:bg-amber-400 transition-colors btn-sheen">
                    Забронювати
                </button>
            </div>
        `;
    }
}

// ==========================================
// 7. MYKOLA VIP CERTIFICATE GENERATOR
// ==========================================
function checkMykolaName(inputVal) {
    const val = (inputVal || '').trim().toLowerCase();
    const isMykola = val.includes('микол') || val.includes('mykola') || val.includes('николай') || val.includes('коло');
    const resultBox = document.getElementById('mykola-card-result');

    if (!resultBox) return;

    if (isMykola) {
        const serial = 'GM-' + Math.floor(10000 + Math.random() * 90000);
        resultBox.classList.remove('hidden');
        resultBox.innerHTML = `
            <div class="relative p-6 sm:p-8 rounded-3xl bg-gradient-to-br from-amber-950 via-[#1c2720] to-[#0d1611] border-2 border-amber-400 shadow-2xl overflow-hidden group">
                <div class="vip-card-shine absolute inset-0 pointer-events-none"></div>
                <div class="flex items-center justify-between mb-4">
                    <div class="flex items-center space-x-2">
                        <i class="fa-solid fa-crown text-amber-400 text-xl"></i>
                        <span class="text-xs uppercase font-serif tracking-widest text-amber-300 font-bold">Клуб Почесних Микол</span>
                    </div>
                    <span class="px-2.5 py-1 rounded-lg bg-amber-500/20 text-amber-300 font-mono text-xs border border-amber-500/40">${serial}</span>
                </div>
                <h3 class="text-2xl sm:text-3xl font-serif font-black text-white mb-2 capitalize">${inputVal.trim()}</h3>
                <p class="text-xs text-amber-200/90 leading-relaxed mb-6">
                    Власник цієї картки має право на персональну подушку «М'яке місце для Миколи», келих крафтового пива «Кумпель» від господаря та внесення портрета до Зали Слави Музею Микол.
                </p>
                <div class="flex flex-wrap items-center justify-between gap-4 pt-4 border-t border-amber-500/30 text-xs">
                    <span class="text-stone-400">Покажіть офіціанту або вкажіть у броні</span>
                    <button onclick="openBookingModal(null, 'Візит Миколи (VIP)', 'Картка ${serial} на ім\\'я ${inputVal.trim()}')" class="px-5 py-2.5 rounded-xl bg-amber-500 text-stone-950 font-bold uppercase tracking-wider hover:bg-amber-400 transition-colors shadow btn-sheen">
                        Використати при броні
                    </button>
                </div>
            </div>
        `;
    } else {
        resultBox.classList.remove('hidden');
        resultBox.innerHTML = `
            <div class="p-4 rounded-2xl bg-stone-900 border border-stone-800 text-xs text-stone-300 text-center">
                <p>Усі гості у «Голодному Миколі» бажані! А якщо з Вами прийде друг або родич на ім’я <strong>Микола</strong> — він отримає частування від закладу.</p>
            </div>
        `;
    }
}

// ==========================================
// 8. WATER RIPPLE ON CLICK
// ==========================================
function spawnWaterRipple(e) {
    // Avoid creating too many on touch/drag
    if (e.target.closest('input, textarea, select')) return;

    const ripple = document.createElement('div');
    ripple.className = 'water-ripple';
    ripple.style.left = `${e.clientX}px`;
    ripple.style.top = `${e.clientY}px`;
    document.body.appendChild(ripple);

    setTimeout(() => ripple.remove(), 800);
}

// ==========================================
// 9. AJAX BOOKING & ORDER
// ==========================================
async function handleAjaxBooking(e) {
    e.preventDefault();
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const feedback = document.getElementById('booking-feedback');
    const formData = new FormData(form);

    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerText = 'Надсилаємо заявку...';
    }

    try {
        const response = await fetch('/api/reserve/', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();

        if (response.ok && result.status === 'success') {
            if (feedback) {
                feedback.className = 'mt-4 p-4 rounded-xl text-sm font-medium bg-emerald-900/50 border border-emerald-500/40 text-emerald-200';
                feedback.innerHTML = `<i class="fa-solid fa-circle-check mr-2"></i>${result.message}`;
                feedback.classList.remove('hidden');
            }
            form.reset();
            showToast('Бронювання успішно зареєстровано!');
            setTimeout(() => {
                closeBookingModal();
                if (feedback) feedback.classList.add('hidden');
            }, 4500);
        } else {
            if (feedback) {
                feedback.className = 'mt-4 p-4 rounded-xl text-sm font-medium bg-red-900/50 border border-red-500/40 text-red-200';
                feedback.innerHTML = `<i class="fa-solid fa-circle-exclamation mr-2"></i>${result.message || 'Виникла помилка. Спробуйте ще раз.'}`;
                feedback.classList.remove('hidden');
            }
        }
    } catch (err) {
        if (feedback) {
            feedback.className = 'mt-4 p-4 rounded-xl text-sm font-medium bg-red-900/50 border border-red-500/40 text-red-200';
            feedback.innerText = 'Помилка мережі. Зателефонуйте нам: +38 (098) 229-22-22';
            feedback.classList.remove('hidden');
        }
    } finally {
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerText = 'Підтвердити бронювання';
        }
    }
}

async function submitDeliveryOrder(e) {
    e.preventDefault();
    const cart = getCart();
    const feedback = document.getElementById('order-feedback');
    const submitBtn = document.getElementById('order-submit-btn');

    if (cart.length === 0) {
        alert('Ваш кошик порожній! Оберіть страви перед замовленням.');
        return;
    }

    const payload = {
        customer_name: document.getElementById('order-customer-name').value,
        phone: document.getElementById('order-phone').value,
        order_type: currentOrderType,
        address: currentOrderType === 'takeaway' ? 'Самовивіз із ресторану (вул. Стрийська, 352)' : (document.getElementById('order-address') ? document.getElementById('order-address').value : ''),
        desired_time: document.getElementById('order-time').value || 'Якомога швидше',
        payment_method: document.getElementById('order-payment').value,
        comment: document.getElementById('order-comment').value,
        items: cart
    };

    submitBtn.disabled = true;
    submitBtn.innerText = 'Оформлюємо замовлення...';

    try {
        const response = await fetch('/api/order/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        const result = await response.json();

        if (response.ok && result.status === 'success') {
            feedback.className = 'mt-4 p-4 rounded-xl text-sm font-medium bg-emerald-900/50 border border-emerald-500/40 text-emerald-200';
            feedback.innerHTML = `
                <div class="space-y-1">
                    <p class="font-bold text-base"><i class="fa-solid fa-circle-check mr-2 text-emerald-400"></i>${result.message}</p>
                    <p class="text-xs text-stone-300">Сума до сплати: <strong>${result.total_price.toFixed(0)} грн</strong> (Знижка: ${result.discount.toFixed(0)} грн)</p>
                </div>
            `;
            feedback.classList.remove('hidden');
            clearCart();
            document.getElementById('ajax-order-form').reset();
            showToast('Замовлення успішно оформлено!');
            setTimeout(() => {
                closeCartModal();
                feedback.classList.add('hidden');
            }, 6000);
        } else {
            feedback.className = 'mt-4 p-4 rounded-xl text-sm font-medium bg-red-900/50 border border-red-500/40 text-red-200';
            feedback.innerHTML = `<i class="fa-solid fa-circle-exclamation mr-2"></i>${result.message || 'Помилка при оформленні.'}`;
            feedback.classList.remove('hidden');
        }
    } catch (err) {
        feedback.className = 'mt-4 p-4 rounded-xl text-sm font-medium bg-red-900/50 border border-red-500/40 text-red-200';
        feedback.innerText = 'Помилка з’єднання. Зателефонуйте оператору: +38 (098) 229-22-22';
        feedback.classList.remove('hidden');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerText = 'Оформити замовлення';
    }
}

function closeTrophyModal() {
    const m = document.getElementById('pond-trophy-modal');
    if (m) m.classList.add('hidden');
}

// DOM Ready initialization
document.addEventListener('DOMContentLoaded', () => {
    TroutPondGame.init();
    BanquetCalculator.init();

    // Mobile nav toggle
    const menuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');

    if (menuBtn && mobileMenu) {
        menuBtn.addEventListener('click', () => {
            const isHidden = mobileMenu.classList.contains('hidden');
            if (isHidden) {
                mobileMenu.classList.remove('hidden');
                if (menuIcon) {
                    menuIcon.classList.remove('fa-bars');
                    menuIcon.classList.add('fa-xmark');
                }
            } else {
                mobileMenu.classList.add('hidden');
                if (menuIcon) {
                    menuIcon.classList.remove('fa-xmark');
                    menuIcon.classList.add('fa-bars');
                }
            }
        });
    }

    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('[role="alert"]');
    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-8px)';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    updateCartUI();

    // Global water ripple listener
    window.addEventListener('click', (e) => {
        spawnWaterRipple(e);

        const bookingModal = document.getElementById('booking-modal');
        const cartModal = document.getElementById('cart-modal');
        const trophyModal = document.getElementById('pond-trophy-modal');
        const tourModal = document.getElementById('virtual-tour-modal');
        if (e.target === bookingModal) closeBookingModal();
        if (e.target === cartModal) closeCartModal();
        if (e.target === trophyModal) closeTrophyModal();
        if (e.target === tourModal) VirtualTour.close();
    });
});
