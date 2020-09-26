from shapely import wkt
from shapely.geometry import Point

from django.shortcuts import render

from app.models import Shipping, Warehouse


def get_concentration(a_amount, a_percentage, b_amount, b_percentage):
    """
    Возвращает % концентрата после смешивания
    двух партий веществ разного объёма и разной концентрации
    https://www.mathcentre.ac.uk/resources/uploaded/mixing-concentrations.pdf
    """

    total_ore = a_amount + b_amount
    total_substance = a_amount / 100 * a_percentage + b_amount / 100 * b_percentage
    concentration = total_substance / total_ore * 100
    return round(concentration, 3)


def home(request):

    shippings = Shipping.objects.all()
    warehouse = Warehouse.objects.first()

    # Если отправлена форма
    if request.GET:

        # Инициируем временные значения склада
        warehouse.expecting_amount = warehouse.current_amount
        warehouse.expecting_sio2 = warehouse.current_sio2
        warehouse.expecting_fe = warehouse.current_fe

        # Строим полигон
        polygon = wkt.loads(warehouse.polygon)

        for shipping in shippings:

            # Возвращаем координаты в форму
            shipping.x = int(request.GET[f'{shipping.id}x'])
            shipping.y = int(request.GET[f'{shipping.id}y'])

            # Строим точку
            point = Point(shipping.x, shipping.y)

            # Если попали в полигон - просчитываем ожидания
            if polygon.contains(point):

                # SiO2
                warehouse.expecting_sio2 = get_concentration(
                    warehouse.expecting_amount,
                    warehouse.expecting_sio2,
                    shipping.current_load,
                    shipping.current_sio2,
                )

                # Fe
                warehouse.expecting_fe = get_concentration(
                    warehouse.expecting_amount,
                    warehouse.expecting_fe,
                    shipping.current_load,
                    shipping.current_fe,
                )

                # Кол-во
                warehouse.expecting_amount += shipping.current_load

    return render(request, 'home.html', {
        'shippings': shippings,
        'warehouse': warehouse,
    })
