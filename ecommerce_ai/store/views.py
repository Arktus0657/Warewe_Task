from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem, UserInteraction  
from django.db.models import F
from store.recommendations import get_recommended_products_for_user



def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return redirect('product_list')
    return render(request, 'store/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        item.quantity += 1
    item.save()
    return redirect('cart')


@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    return render(request, 'store/cart.html', {'items': items})

@login_required
def like_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    UserInteraction.objects.create(
        user=request.user,
        product=product,
        action='like'
    )
    return redirect('product_list')


@login_required
def dislike_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    UserInteraction.objects.create(
        user=request.user,
        product=product,
        action='dislike'
    )
    return redirect('product_list')



def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    interaction, created = UserInteraction.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={"view_count": 0}
    )

    # Increment view count safely
    UserInteraction.objects.filter(
        id=interaction.id
    ).update(view_count=F("view_count") + 1)

    interaction.refresh_from_db()

    return render(request, "store/product_detail.html", {
        "product": product,
        "interaction": interaction,
    })



@login_required
def like_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    UserInteraction.objects.update_or_create(
        user=request.user,
        product=product,
        defaults={'action': 'like'}
    )

    return redirect('product_detail', product_id=product.id)

@login_required
def dislike_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    UserInteraction.objects.update_or_create(
        user=request.user,
        product=product,
        defaults={'action': 'dislike'}
    )

    return redirect('product_detail', product_id=product.id)

@login_required
def recommended_products(request):
    products = get_recommended_products_for_user(request.user)
    return render(request, "store/recommendations.html", {
        "products": products
    })
