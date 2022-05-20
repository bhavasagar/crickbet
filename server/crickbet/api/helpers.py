def last_or_create(db_model, **kwargs):
    created = False                
    if not db_model.objects.filter(**kwargs).exists():
        created = True
        return (db_model.objects.create(**kwargs), created)
    return (db_model.objects.filter(**kwargs).last(), created)

def get_ball_num(ds_over_num):
    if int(ds_over_num) == float(ds_over_num):
        return int(ds_over_num)*6
    o, b = str(ds_over_num).split('.')
    return int(o)*6 + int(b)