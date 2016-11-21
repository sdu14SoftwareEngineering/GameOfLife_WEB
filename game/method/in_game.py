from django.http import HttpResponse

from game.tool import strategy


def get_field_test(request):
    field = strategy.one_gamer_strategy(strategy.field)
    strategy.field = field
    return HttpResponse(to_show(field))


def to_show(a):
    b = ''
    for aa in a:
        for aaa in aa:
            if aaa == 0:
                aaa = '&nbsp'
            b += str(aaa) + '&nbsp&nbsp'
        b += '<br>'
    b = '<a style="font-size:20px">' + b + '</a>'
    return b
