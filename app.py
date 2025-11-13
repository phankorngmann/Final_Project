from flask import Flask,render_template
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

import routes
if __name__ == '__main__':
    app.run(debug=True)

# --- Product Data ---
# TO CHANGE A PRODUCT IMAGE: Edit the value inside the "image" key below.
# Ensure the new image file exists inside the static/img/ folder!
PRODUCT_DATA = [
    # MEN'S IMAGE 1 (Used on Men's page)
    {"id": 1, "name": "Classic Chronograph", "category": "Accessories", "collection": "men",
     "image": "img/10F25TSS028_White (1).jpg", "price": 450.00, "is_new": False, "is_sale": False,
     "original_price": None},

    # WOMEN'S IMAGE 1 (Used on Women's page)
    {"id": 2, "name": "Minimalist Linen Jacket", "category": "Apparel", "collection": "women",
     "image": "img/10F25SHSW005_White (1).jpg", "price": 129.99, "is_new": False, "is_sale": True,
     "original_price": 169.00},

    # ACCESSORY IMAGE 1 (Used on Men's and Women's pages)
    {"id": 3, "name": "Hand-stitched Leather Wallet", "category": "Leather Goods", "collection": "accessories",
     "image": "img/10F25SHLW015_GREY-(1).jpg", "price": 79.50, "is_new": True, "is_sale": False, "original_price": None},

    # ACCESSORY IMAGE 2 (Used on Men's and Women's pages)
    {"id": 4, "name": "Ceramic Coffee Mug", "category": "Homeware", "collection": "accessories",
     "image": "img/10S25DPA018_Beige (1).jpg", "price": 19.00, "is_new": False, "is_sale": False, "original_price": None},

    # WOMEN'S IMAGE 2 (Used on Women's page)
    {"id": 5, "name": "Essential White Tee", "category": "Apparel", "collection": "women",
     "image": "img/10F25SKIW009_White (1).jpg", "price": 49.99, "is_new": True, "is_sale": False, "original_price": None},

    # MEN'S IMAGE 2 (Used on Men's page)
    {"id": 6, "name": "Noise Cancelling Headphones", "category": "Tech", "collection": "men",
     "image": "img/10F25KNI003_Beige-(1).jpg", "price": 299.99, "is_new": False, "is_sale": True,
     "original_price": 349.00},

    # ACCESSORY IMAGE 3 (Used on Men's and Women's pages)
    {"id": 7, "name": "Travel Backpack", "category": "Accessories", "collection": "accessories",
     "image": "img/10F25TSS028_White (1).jpg", "price": 85.00, "is_new": False, "is_sale": False,
     "original_price": None},

    # WOMEN'S IMAGE 3 (Used on Women's page)
    {"id": 8, "name": "Structured Pleat Trouser", "category": "Apparel", "collection": "women",
     "image": "img/10F25TSLW009_Grey Melange (1) (1).jpg", "price": 110.00, "is_new": False, "is_sale": False,
     "original_price": None},

    # MEN'S IMAGE 3 (Used on Men's page)
    {"id": 9, "name": "Oversized Merino Sweater", "category": "Apparel", "collection": "men",
     "image": "img/10F25SHL013_Blue (1).jpg", "price": 180.00, "is_new": True, "is_sale": False,
     "original_price": None},
]

# --- Journal Data ---
# TO CHANGE A JOURNAL IMAGE: Edit the value inside the "image" key below.
JOURNAL_POSTS = [
    {
        "id": 1,
        "title": "The Art of the Capsule Wardrobe",
        "slug": "capsule-wardrobe",
        "date": "October 15, 2025",
        "author": "Ava K.",
        "snippet": "Discover the core principles of minimalist fashion and how to curate a timeless wardrobe with fewer, better pieces.",
        "image": "img/54.png",  # <--- CHANGE JOURNAL IMAGE 1 HERE
        "content": "For too long, fashion has been about excess. The capsule wardrobe movement rejects this by focusing on high-quality, interchangeable basics. Start by defining a color palette of 4-5 neutral shades, then invest in timeless cuts. This approach not only saves time but drastically reduces your environmental footprint. It’s about quality over quantity."
    },
    {
        "id": 2,
        "title": "Ethical Sourcing: Beyond the Label",
        "slug": "ethical-sourcing",
        "date": "September 28, 2025",
        "author": "Ethan M.",
        "snippet": "We dive deep into the supply chain to explain what 'ethically made' truly means for our leather goods and apparel.",
        "image": "img/55.png",  # <--- CHANGE JOURNAL IMAGE 2 HERE
        "content": "Transparency is key to true ethical sourcing. It means knowing the origin of every material, from the cotton farm to the finished stitch. At AURORA, we partner exclusively with certified B-Corp factories that guarantee fair wages and safe working conditions. Our commitment goes beyond legal requirements to ensure every product tells a story of integrity."
    },
    {
        "id": 3,
        "title": "Five Minimalist Home Essentials",
        "slug": "home-essentials",
        "date": "September 1, 2025",
        "author": "Ava K.",
        "snippet": "Bring the calming aesthetic of minimalism into your living space with these five must-have items.",
        "image": "img/56.png",  # <--- CHANGE JOURNAL IMAGE 3 HERE
        "content": "Minimalism isn't just clothing; it's a lifestyle. Start with items that combine form and function, like a high-quality ceramic mug, a versatile wool throw, or clean-lined shelving. The goal is to maximize utility while minimizing visual clutter, creating a sanctuary of calm in your home."
    }
]
# --- Python Route Functions ---

@app.route('/')
def home():
    """Renders the homepage with the first 5 products as featured."""
    # This route shows the first 5 products.
    products_to_display = PRODUCT_DATA[:5]
    return render_template('index.html', products=products_to_display)

@app.route('/shop')
def shop_all():
    """Renders the general shop page with all products."""
    # This route shows ALL products. If you want it to show a filtered list,
    # change 'products=PRODUCT_DATA' to a filtered list (e.g., products=PRODUCT_DATA[:3]).
    return render_template(
        'collection.html',
        products=PRODUCT_DATA,
        collection_title="All Products"
    )

@app.route('/men')
def shop_men():
    """Renders the Men's collection page, filtering by 'men' and general 'accessories'."""
    men_products = [p for p in PRODUCT_DATA if p['collection'] in ('men', 'accessories')]
    return render_template(
        'collection.html',
        products=men_products,
        collection_title="Men's Collection"
    )

@app.route('/women')
def shop_women():
    """Renders the Women's collection page, filtering by 'women' and general 'accessories'."""
    women_products = [p for p in PRODUCT_DATA if p['collection'] in ('women', 'accessories')]
    return render_template(
        'collection.html',
        products=women_products,
        collection_title="Women's Collection"
    )

# The /contact route now expects a 'success' parameter
import routes


@app.route('/cart')
def cart_page():
    """Renders the shopping cart page."""
    # NOTE: This is empty for now, but the template handles the empty state.
    cart_items = []
    return render_template('cart.html', cart_items=cart_items)


@app.route('/journal')
def journal_listing():
    """Renders the main journal index page with all post snippets."""
    return render_template(
        'journal_listing.html',
        posts=JOURNAL_POSTS
    )


@app.route('/journal/<int:post_id>')
def journal_post(post_id):
    """Renders an individual journal post based on its ID."""

    post = next((p for p in JOURNAL_POSTS if p['id'] == post_id), None)

    if post is None:
        return render_template('404.html'), 404

    return render_template('journal_post.html', post=post)


# --- Error Handler ---
@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors using the custom 404.html template."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    # Run the application
    app.run(debug=True)
