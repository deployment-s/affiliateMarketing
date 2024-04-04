from django.shortcuts import redirect, render, get_object_or_404
from .models import Product, Review

# Create your views here.
def Product_Page(request,pk,slug):

    product = get_object_or_404( Product, pk=pk, slug=slug)
    if request.method == 'POST':
        rating = request.POST.get('rating', 3)
        content = request.POST.get('content', '')

        if content:
            reviews = Review.objects.filter(created_by=request.user, product=product)

            if reviews.count() > 0:
                review = reviews.first()
                review.rating = rating
                review.content = content
                review.save()
            else:
                review = Review.objects.create(
                    product=product,
                    rating=rating,
                    content=content,
                    created_by=request.user
                )

            return redirect('products:product', pk=pk, slug=slug)
    return render(request, 'products/product.html', {'products': [product]})
