from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from io import BytesIO
from xhtml2pdf import pisa
from apps.order.models import Order, Shipping

from rest_framework.decorators import api_view
from rest_framework.response import Response


@login_required
def admin_order_pdf(request, order_id):
    if not request.user.is_superuser:
        return HttpResponse("Unauthorized", status=403)

    order = get_object_or_404(Order, pk=order_id)
    
    # Construct the path to the HTML template
    template_path = 'order_pdf_template.html'

    # Render the PDF using the template
    pdf_content = render_to_pdf(template_path, {'order': order})
    
    if pdf_content:
        # Return the PDF as a response
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=%s.pdf' % order_id
        return response
    else:
        return HttpResponse("Failed to generate PDF", status=500)

def render_to_pdf(template_path, context_dict={}):
    template = get_template(template_path)
    html = template.render(context_dict)
    result = BytesIO()
    
    # Use UTF-8 encoding for broader character support
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        return result.getvalue()
    else:
        # Proper error handling with logging
        print("PDF generation error:", pdf.err)
        return None

@api_view(['POST'])
def calculate_shipping(request):
    order_total = request.data.get('order_total', 0)
    
    # Assuming Free Shipping is available for orders over $50
    if order_total >= 50:
        shipping_option = Shipping.objects.get(name='Free Shipping')
    else:
        shipping_option = Shipping.objects.get(name='Flat Rate')
    
    shipping_cost = shipping_option.rate
    
    return Response({'shipping_cost': shipping_cost})


# from io import BytesIO
# from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.template.loader import get_template
# from django.http import HttpResponse
# from xhtml2pdf import pisa
# from apps.order.models import Order
# import os

# TEMPLATE_DIR = os.path.join(settings.BASE_DIR, 'apps.order.templates.order_pdf_template.html')

# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     result = BytesIO()
    
#     # Use UTF-8 encoding for broader character support
#     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
#     if not pdf.err:
#         return result.getvalue()
#     else:
#         # Proper error handling with logging
#         print("PDF generation error:", pdf.err)
#         return None

# @login_required
# def admin_order_pdf(request, order_id):
#     if not request.user.is_superuser:
#         return HttpResponse("Unauthorized", status=403)

#     order = get_object_or_404(Order, pk=order_id)
    
#     # Validate if order belongs to the user or the user is authorized to view it
    
#     pdf_content = render_to_pdf(TEMPLATE_DIR, {'order': order})  # Use the provided HTML template
    
#     if pdf_content:
#         response = HttpResponse(pdf_content, content_type='application/pdf')
#         response['Content-Disposition'] = 'inline; filename=%s.pdf' % order_id
#         return response
#     else:
#         return HttpResponse("Failed to generate PDF", status=500)


# from io import BytesIO

# from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.template.loader import get_template
# from django.http import HttpResponse

# from xhtml2pdf import pisa

# # from order.api.serializers import OrderSerializer, OrderItemSerializer
# from apps.order.models import Order

# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

#     if not pdf.err:
#         return result.getvalue()
    
#     return None

# @login_required
# def admin_order_pdf(request, order_id):
#     if request.user.is_superuser:
#         order = get_object_or_404(Order, pk=order_id)
#         pdf = render_to_pdf('order_pdf.html', {'order': order})

#         if pdf:
#             response = HttpResponse(pdf, content_type='application/pdf')
#             content = "attachment; filename=%s.pdf" % order_id
#             response['Content-Disposition'] = content

#             return response
    
#     return HttpResponse("Not Found")