from django.core.management.base import BaseCommand
from store.models import Category, Product
from django.utils.text import slugify


CATEGORIES = [
    {"name": "Men", "icon": "👔"},
    {"name": "Women", "icon": "👗"},
    {"name": "Footwear", "icon": "👟"},
    {"name": "Accessories", "icon": "👜"},
    {"name": "Electronics", "icon": "📱"},
    {"name": "Sports", "icon": "🏃"},
    {"name": "Beauty", "icon": "💄"},
    {"name": "Kids", "icon": "🧸"},
]

PRODUCTS = [
    # Men
    {"name": "Classic Oxford Shirt", "category": "Men", "brand": "Arrow", "price": 1299, "original_price": 2499, "rating": 4.3, "reviews_count": 842, "is_featured": True, "is_new": False,
     "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600&q=80",
     "description": "A timeless classic Oxford shirt crafted from 100% premium cotton. Perfect for both office and casual wear with its versatile solid design."},
    {"name": "Slim Fit Chinos", "category": "Men", "brand": "Levis", "price": 1899, "original_price": 3499, "rating": 4.5, "reviews_count": 1243, "is_featured": True, "is_new": False,
     "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=600&q=80",
     "description": "Slim fit chinos in a stretch fabric blend for all-day comfort. A wardrobe essential for modern men."},
    {"name": "Graphic Tee - Minimal", "category": "Men", "brand": "H&M", "price": 599, "original_price": 999, "rating": 4.1, "reviews_count": 567, "is_featured": False, "is_new": True,
     "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&q=80",
     "description": "Relaxed fit graphic t-shirt made from soft jersey cotton. Features a minimal print design."},
    {"name": "Casual Linen Blazer", "category": "Men", "brand": "Marks & Spencer", "price": 3499, "original_price": 5999, "rating": 4.6, "reviews_count": 328, "is_featured": True, "is_new": False,
     "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&q=80",
     "description": "Breathable linen blazer perfect for summer occasions. Unlined and relaxed fit for maximum comfort."},
    {"name": "Jogger Track Pants", "category": "Men", "brand": "Nike", "price": 2199, "original_price": 3499, "rating": 4.4, "reviews_count": 921, "is_featured": False, "is_new": True,
     "image_url": "https://images.unsplash.com/photo-1594938298603-c8148c4b4923?w=600&q=80",
     "description": "Comfortable jogger pants with elastic waistband and drawstring. Ideal for workouts and casual wear."},

    # Women
    {"name": "Floral Wrap Dress", "category": "Women", "brand": "Zara", "price": 2199, "original_price": 3999, "rating": 4.7, "reviews_count": 1567, "is_featured": True, "is_new": True,
     "image_url": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=600&q=80",
     "description": "Elegant floral wrap dress with a V-neckline and tie-waist detail. Perfect for brunches, parties and summer outings."},
    {"name": "High-Waist Denim Jeans", "category": "Women", "brand": "Levis", "price": 2499, "original_price": 4499, "rating": 4.5, "reviews_count": 2134, "is_featured": True, "is_new": False,
     "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=600&q=80",
     "description": "Classic high-waist straight-leg jeans in stretch denim. Flattering fit with 5-pocket styling."},
    {"name": "Oversized Knit Sweater", "category": "Women", "brand": "Mango", "price": 1799, "original_price": 2999, "rating": 4.3, "reviews_count": 743, "is_featured": False, "is_new": True,
     "image_url": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=600&q=80",
     "description": "Cozy oversized knit sweater in a soft wool-blend. Relaxed drop-shoulder silhouette."},
    {"name": "Satin Slip Skirt", "category": "Women", "brand": "H&M", "price": 999, "original_price": 1799, "rating": 4.2, "reviews_count": 456, "is_featured": True, "is_new": False,
     "image_url": "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=600&q=80",
     "description": "Elegant satin slip skirt with an elasticated waist. A versatile piece that can be dressed up or down."},
    {"name": "Linen Co-ord Set", "category": "Women", "brand": "AND", "price": 2899, "original_price": 4999, "rating": 4.6, "reviews_count": 892, "is_featured": True, "is_new": True,
     "image_url": "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=600&q=80",
     "description": "Breezy linen co-ord set featuring a relaxed shirt and wide-leg pants. Perfect for vacation or work-from-home."},

    # Footwear
    {"name": "Air Cushion Sneakers", "category": "Footwear", "brand": "Nike", "price": 4999, "original_price": 7999, "rating": 4.8, "reviews_count": 3241, "is_featured": True, "is_new": False,
     "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&q=80",
     "description": "Iconic air-cushion sneakers with responsive foam midsole. Breathable mesh upper keeps feet cool all day."},
    {"name": "Leather Chelsea Boots", "category": "Footwear", "brand": "Clarks", "price": 6499, "original_price": 9999, "rating": 4.6, "reviews_count": 1123, "is_featured": True, "is_new": False,
     "image_url": "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=600&q=80",
     "description": "Premium full-grain leather Chelsea boots with elastic side gussets. Durable rubber sole for everyday wear."},
    {"name": "Block Heel Sandals", "category": "Footwear", "brand": "Steve Madden", "price": 2299, "original_price": 3999, "rating": 4.4, "reviews_count": 678, "is_featured": False, "is_new": True,
     "image_url": "https://images.unsplash.com/photo-1535043934128-cf0b28d52f95?w=600&q=80",
     "description": "Trendy block heel sandals with adjustable ankle strap. Comfortable for all-day wear."},
    {"name": "Canvas Low-Top Sneakers", "category": "Footwear", "brand": "Converse", "price": 3299, "original_price": 4999, "rating": 4.5, "reviews_count": 2876, "is_featured": False, "is_new": False,
     "image_url": "https://images.unsplash.com/photo-1463100099107-aa0980c362e6?w=600&q=80",
     "description": "Classic canvas low-top sneakers. A timeless style that goes with everything."},

    # Accessories
    {"name": "Minimalist Leather Watch", "category": "Accessories", "brand": "Fossil", "price": 8999, "original_price": 14999, "rating": 4.7, "reviews_count": 1543, "is_featured": True, "is_new": False,
     "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&q=80",
     "description": "Slim minimalist watch with genuine leather strap. Japanese quartz movement with 3 ATM water resistance."},
    {"name": "Structured Tote Bag", "category": "Accessories", "brand": "Coach", "price": 5999, "original_price": 9999, "rating": 4.5, "reviews_count": 876, "is_featured": True, "is_new": True,
     "image_url": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=600&q=80",
     "description": "Structured tote bag in pebbled leather with zip closure and interior pockets. Work-to-weekend versatility."},
    {"name": "Aviator Sunglasses", "category": "Accessories", "brand": "RayBan", "price": 4499, "original_price": 7500, "rating": 4.8, "reviews_count": 2134, "is_featured": True, "is_new": False,
     "image_url": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=600&q=80",
     "description": "Classic polarized aviator sunglasses with UV400 protection. Gold metal frame with teardrop lenses."},

    # Electronics
    {"name": "True Wireless Earbuds", "category": "Electronics", "brand": "Sony", "price": 9999, "original_price": 14999, "rating": 4.7, "reviews_count": 4521, "is_featured": True, "is_new": True,
     "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600&q=80",
     "description": "Industry-leading noise cancelling wireless earbuds with 30hr battery life. Crystal clear sound quality."},
    {"name": "Smart Fitness Band", "category": "Electronics", "brand": "Mi", "price": 2499, "original_price": 3999, "rating": 4.4, "reviews_count": 8932, "is_featured": True, "is_new": False,
     "image_url": "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=600&q=80",
     "description": "Advanced fitness tracker with heart rate monitor, SpO2, sleep tracking and 14-day battery life."},
    {"name": "Wireless Charging Pad", "category": "Electronics", "brand": "Anker", "price": 1499, "original_price": 2499, "rating": 4.3, "reviews_count": 3241, "is_featured": False, "is_new": False,
     "image_url": "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=600&q=80",
     "description": "Fast wireless charging pad compatible with all Qi-enabled devices. LED indicator and anti-slip design."},

    # Sports
    {"name": "Compression Running Tights", "category": "Sports", "brand": "Adidas", "price": 2499, "original_price": 3999, "rating": 4.5, "reviews_count": 1432, "is_featured": False, "is_new": True,
     "image_url": "https://images.unsplash.com/photo-1556906781-9a412961a28b?w=600&q=80",
     "description": "High-performance compression tights with moisture-wicking fabric. Four-way stretch for full range of motion."},
    {"name": "Yoga Mat Premium", "category": "Sports", "brand": "Decathlon", "price": 1299, "original_price": 1999, "rating": 4.6, "reviews_count": 2341, "is_featured": False, "is_new": False,
     "image_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=600&q=80",
     "description": "Extra-thick 6mm yoga mat with superior grip and alignment lines. Non-slip bottom prevents sliding."},
]


class Command(BaseCommand):
    help = 'Seed database with sample products and categories'

    def handle(self, *args, **options):
        self.stdout.write('Seeding categories...')
        cat_map = {}
        for c in CATEGORIES:
            cat, _ = Category.objects.get_or_create(
                slug=slugify(c['name']),
                defaults={'name': c['name'], 'icon': c['icon']}
            )
            cat_map[c['name']] = cat

        self.stdout.write('Seeding products...')
        for p in PRODUCTS:
            cat = cat_map.get(p['category'])
            if not cat:
                continue
            slug = slugify(p['name'])
            Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'category': cat,
                    'name': p['name'],
                    'brand': p.get('brand', ''),
                    'price': p['price'],
                    'original_price': p.get('original_price'),
                    'rating': p.get('rating', 4.0),
                    'reviews_count': p.get('reviews_count', 0),
                    'is_featured': p.get('is_featured', False),
                    'is_new': p.get('is_new', False),
                    'image_url': p.get('image_url', ''),
                    'description': p.get('description', ''),
                    'stock': 50,
                }
            )

        self.stdout.write(self.style.SUCCESS(
            f'Done! {Category.objects.count()} categories, {Product.objects.count()} products.'
        ))
