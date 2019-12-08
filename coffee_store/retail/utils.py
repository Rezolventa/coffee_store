
def clear_obj(obj):
    all_obj = obj.objects.all()
    for obj in all_obj:
        obj.delete()

'''
def smart_print(obj):
    print(type(obj), str(obj))

def get_model_data(model):
    fields = model._meta.get_fields()
    class_table = [object for object in model.objects.all()]
    #for object in obj.objects.all()
    fields = [field[1] for field in fields]
    smart_print(fields)
    smart_print(class_table)
    return {'fields': fields, 'class_table': class_table}'''