from django.shortcuts import redirect

def redirect_shop(request):
    return redirect('items_list_url', permanent=True)