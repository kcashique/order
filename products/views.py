
from django.shortcuts import (get_object_or_404,
                              render,
                              reverse,
                              redirect,
                              HttpResponseRedirect)
from .models import Product, Order, OrderItem
from .forms import ProductForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone

from django.contrib.auth.models import User




def homepage(request):
    context = {}

    # add the dictionary during initialization
    context["dataset"] = Product.objects.all()
    j= User.objects.get(pk=int(2))
    print(j)

    return render(request, "home.html", context)


def create_view(request):

    context = {}

    # add the dictionary during initialization
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        data = form.save(commit=False)
        data.creator = request.user
        data.updater = request.user
        data.save()
        return redirect("products:homepage")

    context['form'] = form
    return render(request, "products/create_products.html", context)


def list_view(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    context["dataset"] = Product.objects.all()

    return render(request, "products/product_list.html", context)

 # pass id attribute from urls


def detail_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    context["data"] = Product.objects.get(id=id)

    return render(request, "products/product_detail.html", context)

# update view for details


def update_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Product, id=id)
    print(obj)

    odr=None
    for order in Order.objects.all():
        odr=order

    obj1= Order.objects.get(pk=4)
    

    # pass the object as instance in form
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=obj)
        print(form)
        # save the data from the form and
        # redirect to detail_view
        if form.is_valid():
            data = form.save(commit=False)
            data.updater = request.user
            data.save()
            return reverse("products:product_detail_detail", kwargs={"id": data.id})

    # add form dictionary to context
    context["form"] = form

    return render(request, "products/product_update.html", context)

# delete view for details


def delete_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Product, id=id)

    if request.method == "POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return redirect("products:homepage")

    return render(request, "products/product_delete.html", context)

# class OrderSummaryView(LoginRequiredMixin, View):
#     def get(self, *args, **kwargs):
#         try:
#             order = Order.objects.get(user=self.request.user, ordered=False)
#             context = {
#                 'object': order
#             }
#             return render(self.request, 'products/order_summary.html', context)
#         except ObjectDoesNotExist:
#             messages.warning(self.request, "You do not have an active order")
#             return redirect("/")

def order_summary(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        context = {
            'object': order
        }
        return render(request, 'products/order_summary.html', context)
    except ObjectDoesNotExist:
        messages.warning(request, "You do not have an active order")
        return redirect("products:homepage")

@login_required
def add_to_cart(request, id):
    item = get_object_or_404(Product, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("products:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("products:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("products:order-summary")


@login_required
def remove_from_cart(request, id):
    item = get_object_or_404(Product, id=id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("products:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("products:product_detail", id=id)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("products:product_detail", id=id)


@login_required
def remove_single_item_from_cart(request, id):
    item = get_object_or_404(Product, id=id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("products:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("products:product_detail", id=id)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("products:product_detail", id=id)
