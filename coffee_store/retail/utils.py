
def clear_obj(obj):
    all_obj = obj.objects.all()
    for obj in all_obj:
        obj.delete()