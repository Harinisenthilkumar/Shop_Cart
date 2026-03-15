from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, Category, Cart, CartItem, WishlistItem, Order, OrderItem, Review
import json


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def home(request):
    featured = Product.objects.filter(is_featured=True)[:8]
    new_arrivals = Product.objects.filter(is_new=True)[:8]
    categories = Category.objects.all()
    trending = Product.objects.order_by('-reviews_count')[:8]
    return render(request, 'store/home.html', {
        'featured': featured,
        'new_arrivals': new_arrivals,
        'categories': categories,
        'trending': trending,
    })


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    search = request.GET.get('q', '')
    sort = request.GET.get('sort', 'newest')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    selected_category = None

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    if search:
        products = products.filter(Q(name__icontains=search) | Q(brand__icontains=search))

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-created_at')

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'search': search,
        'sort': sort,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    reviews = product.reviews.all().order_by('-created_at')
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = WishlistItem.objects.filter(user=request.user, product=product).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating and comment:
            Review.objects.update_or_create(
                product=product, user=request.user,
                defaults={'rating': rating, 'comment': comment}
            )
            messages.success(request, 'Review submitted!')
            return redirect('product_detail', slug=slug)

    return render(request, 'store/product_detail.html', {
    'product': product,
    'related': related,
    'reviews': reviews,
    'in_wishlist': in_wishlist,
    'size_list': ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    size = request.POST.get('size', '')
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, size=size)
    if not created:
        item.quantity += 1
        item.save()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'count': cart.item_count, 'message': 'Added to cart!'})
    messages.success(request, f'{product.name} added to cart!')
    return redirect(request.META.get('HTTP_REFERER', '/'))


def cart_view(request):
    cart = get_or_create_cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    action = request.POST.get('action')
    if action == 'increase':
        item.quantity += 1
        item.save()
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    elif action == 'remove':
        item.delete()
    return redirect('cart')


def toggle_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'login_required'}, status=401)
    product = get_object_or_404(Product, id=product_id)
    obj, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        obj.delete()
        return JsonResponse({'action': 'removed'})
    return JsonResponse({'action': 'added'})


@login_required
def wishlist(request):
    items = WishlistItem.objects.filter(user=request.user).select_related('product')
    return render(request, 'store/wishlist.html', {'items': items})


@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    if cart.item_count == 0:
        return redirect('cart')
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total,
            address=address,
            phone=phone,
            status='confirmed'
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order, product=item.product,
                quantity=item.quantity, price=item.product.price
            )
        cart.items.all().delete()
        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('order_success', order_id=order.id)
    return render(request, 'store/checkout.html', {'cart': cart})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_success.html', {'order': order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    wishlist_count = WishlistItem.objects.filter(user=request.user).count()
    return render(request, 'store/profile.html', {'orders': orders, 'wishlist_count': wishlist_count})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', '/'))
        messages.error(request, 'Invalid credentials.')
    return render(request, 'store/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, 'Account created! Welcome!')
            return redirect('home')
    return render(request, 'store/register.html')


def logout_view(request):
    logout(request)
    return redirect('home')
