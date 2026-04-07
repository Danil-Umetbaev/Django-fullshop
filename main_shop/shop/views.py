from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, TemplateView
from django.template.response import TemplateResponse


from .models import Category, ProductImage, Product, ProductSize, Size
from django.db.models import Q
# Create your views here.

class IndexView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = None
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.headers.get('HX-Request'):
            return TemplateResponse(request, 'shop/home_content.html', context)
        return TemplateResponse(request, self.template_name, context)


class CatalogView(TemplateView):
    template_name = 'base.html'

    FILTER_MAPPING = {
        'color': lambda queryset, value: queryset.filter(color__iexact=value),
        'min_price': lambda queryset, value: queryset.filter(price__gte=value),
        'max_price': lambda queryset, value: queryset.filter(price__lte=value),
        'size': lambda queryset, value: queryset.filter(product_size__size__name=value),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = kwargs.get('category_slug')
        categories = Category.objects.all()
        products = Product.objects.all().order_by('created_at')
        current_category = None
        if category_slug:
            current_category = get_object_or_404(Category, slug=category_slug)
            products = Product.objects.filter(category=current_category)

        query = self.request.GET.get('q')
        if query:
            products = products.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

        # Собираем параметры фильтрации, отбрасывая 'None', None и пустые строки
        filter_params = {}
        for param in self.FILTER_MAPPING:
            raw_value = self.request.GET.get(param)
            if raw_value in (None, '', 'None'):
                filter_params[param] = None
            else:
                filter_params[param] = raw_value

        # Применяем фильтры только для реальных значений
        for param, filter_func in self.FILTER_MAPPING.items():
            value = filter_params.get(param)
            if value is not None:
                products = filter_func(products, value)

        filter_params['q'] = query or ''

        context.update({
            'categories': categories,
            'products': products,
            'current_category': category_slug,
            'filter_params': filter_params,
            'sizes': Size.objects.all(),
            'search_query': query or ''
        })

        if self.request.GET.get('show_search') == 'true':
            context['show_search'] = True
        elif self.request.GET.get('reset_search') == 'true':
            context['reset_search'] = True

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.headers.get('HX-Request'):
            if context.get('show_search'):
                return TemplateResponse(request, 'shop/search_input.html', context)
            elif context.get('reset_search'):
                return TemplateResponse(request, 'shop/search_button.html', {})
            if request.GET.get('show_filters') == 'true':
                return TemplateResponse(request, 'shop/filter_modal.html', context)
            return TemplateResponse(request, 'shop/catalog.html', context)
        return TemplateResponse(request, self.template_name, context)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/base.html'
    slug_field = 'slug'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['categories'] = Category.objects.all()
        context['related_products'] = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
        context['product'] = product
        context['current_category'] = product.category.slug
        context['sizes'] = ProductSize.objects.filter(product=product)
        return context
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        if request.headers.get('HX-Request'):
            return TemplateResponse(request, 'shop/product_detail.html', context)
        return TemplateResponse(request, self.template_name, context)



