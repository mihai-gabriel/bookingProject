import json

from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.db.models import Q
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.http import JsonResponse

from .models import Hotel, Room, Order
from .forms import OrderForm


# Create your views here.
class HomePageView(TemplateView):
    template_name = "index.html"


class HotelsView(TemplateView):
    template_name = "hotels.html"

    def get_context_data(self, **kwargs):
        context = super(HotelsView, self).get_context_data(**kwargs)
        hotels = Hotel.objects.all()
        result = {}

        for hotel in hotels:
            letter = hotel.name[0].upper()
            if letter in result:
                result[letter].append(hotel)
            else:
                result[letter] = [hotel]

        context['result'] = result
        return context


class HotelDetailView(DetailView):
    template_name = "hotel.html"
    model = Hotel
    context_object_name = 'hotel'


class RoomDetailView(TemplateView):
    template_name = "room.html"

    def get_context_data(self, **kwargs):
        context = super(RoomDetailView, self).get_context_data(**kwargs)
        context['room'] = Room.objects.get(pk=self.kwargs['pk'])
        return context

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        order = OrderForm(initial={'room': kwargs['pk'], 'user': request.user})
        context['order_form'] = order

        return self.render_to_response(context)


class FAQView(TemplateView):
    template_name = "faq.html"


class RoomsView(TemplateView):
    def render_to_response(self, context, **response_kwargs):
        hotel = Hotel.objects.get(pk=context['pk'])
        result = {}
        for room in hotel.room_set.all():
            result[room.number] = room.available

        return JsonResponse(result)


class OrderProcessingView(TemplateView):
    template_name = "ordered_processed.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(OrderProcessingView, self).get(self, request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            room = order_form.cleaned_data['room']
            user = order_form.cleaned_data['user']
            full_name = order_form.cleaned_data['full_name']
            number_of_people = order_form.cleaned_data['number_of_people']
            start_date = order_form.cleaned_data['start_date']
            end_date = order_form.cleaned_data['end_date']

            # If the user is not the logged in user, do not save
            if user != request.user:
                return redirect("booking:room", pk=room.pk)

            if room.available:
                order = Order(room=room, user=user, full_name=full_name,
                              number_of_people=number_of_people,
                              start_date=start_date, end_date=end_date)
                order.save()
                room.available = False
                room.save()

        return self.get(request, *args, **kwargs)


def search_hotel(request):
    if request.method == "POST":
        post_data = json.loads(request.body)

        if len(post_data['search']) > 0:
            data = Hotel.objects.filter(
                Q(name__contains=post_data['search']) | Q(location__contains=post_data['search']))
            serialized_data = serialize("json", data)
            return JsonResponse({"search_result": serialized_data})

        return JsonResponse({})
    else:
        return redirect("booking:index")


def delete_order(request):
    if request.method == "POST":
        post_data = json.loads(request.body)

        try:
            order = Order.objects.get(pk=post_data['order'])
            order.room.available = True
            order.room.save()
            order.delete()
            return JsonResponse({"status": "ok"})
        except Order.DoesNotExist:
            return JsonResponse({"status": "error"})

    else:
        return redirect("booking:index")
