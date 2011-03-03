from google.appengine.ext import db
from Magic import MagicSet
def edit(request, *args, **kwargs):
    if request.params.key:
        item = db.get(request.params.key)
        if item:
            return {'op':'upd', 'form': MagicSet.getFormClass(request)(instance=item)}
        else:
            request.status = 'Item does not exists'
            request.redirect(request.get_url())
    else:
        request.status = 'Key not provided'
        return {'op':'ins' ,'form':MagicSet.getFormClass(request)()}

def delete(request, *args, **kwargs):
    if request.params.key:
        item = db.get(request.params.key)
        if item:
            item.delete()
            request.status = 'Item is Deleted'
        else:
            request.status = 'Item does not exist'
    else:
        request.status = 'Key was not provided'
    request.redirect(request.get_url())

def save(request, *args, **kwargs):
    if request.params.key:
        item = db.get(request.params.key)
    form = MagicSet.getFormClass(request)(data=request.POST, instance=item)
    if form.is_valid():
        result=form.save(commit=False)
        result.put()
        request.status = 'Item is saved'
    else:
        request.status = 'Form is not Valid'
    request.redirect(request.get_url())

def index(request, *args, **kwargs):
    results =None
    result = {'items': MagicSet.getModelClass().all().fetch(limit=1000)}
    return result.update(locals())