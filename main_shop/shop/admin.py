from django.contrib import admin
from .models import Product, ProductSize, ProductImage, Category, Size



# Register your models here.

admin.site.register(Size)

class ProductImageInLine(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductSizeInLine(admin.TabularInline):
    model = ProductSize
    extra = 1

class SizeAdmin(admin.ModelAdmin):
    list_display = ('name')
    list_filter = ('name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'main_image')
    search_fields = ('name', 'category', 'price', 'main_image')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductSizeInLine, ProductImageInLine]

@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'stock')
    search_fields = ('product', 'size', 'stock')
    list_filter = ('product', 'size', 'stock')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    search_fields = ('producr', 'image')
    list_filter = ('product',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    search_fields = ('name',)
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}
