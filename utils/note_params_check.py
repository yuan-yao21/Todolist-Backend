def note_params_check(request):
    title = request.POST.get('title')
    textContent = request.POST.get('textContent')
    category = request.POST.get('category', 'default')

    errors = {}
    if not title:
        errors['title'] = 'Title is required.'
    if not textContent:
        errors['textContent'] = 'Text content is required.'

    return title, textContent, category, errors
