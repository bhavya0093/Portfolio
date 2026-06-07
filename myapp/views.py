from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from .models import Profile, Skill, Project, Service, Experience, Certificate, ContactMessage

def portfolio_home(request):
    # Retrieve the first profile entry (there should typically be only one)
    profile = Profile.objects.first()
    
    # Skills grouped by category for layout styling
    skills = Skill.objects.all()
    skills_by_category = {}
    for skill in skills:
        skills_by_category.setdefault(skill.category, []).append(skill)
    
    # Services, Experiences, Certificates
    services = Service.objects.all()
    experiences = Experience.objects.all()
    certificates = Certificate.objects.all()
    
    # Projects handling (supports server-side filters if requested via query params)
    query = request.GET.get('q', '').strip()
    selected_category = request.GET.get('category', '').strip()
    
    projects = Project.objects.all()
    
    # Get all distinct categories for category filtering pills
    all_categories = Project.objects.values_list('category', flat=True).distinct()
    all_categories = sorted([cat for cat in all_categories if cat])
    
    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(technologies__icontains=query)
        )
    
    if selected_category and selected_category != 'All':
        projects = projects.filter(category=selected_category)
        
    context = {
        'profile': profile,
        'skills_by_category': skills_by_category,
        'projects': projects,
        'all_categories': all_categories,
        'services': services,
        'experiences': experiences,
        'certificates': certificates,
        'query': query,
        'selected_category': selected_category,
    }
    
    return render(request, 'myapp/index.html', context)

def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Simple server-side validation
        if not name or not email or not subject or not message:
            return JsonResponse({
                'success': False,
                'message': 'All fields are required. Please fill out the entire form.'
            }, status=400)
            
        try:
            # Create contact message entry
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            return JsonResponse({
                'success': True,
                'message': 'Thank you! Your message has been sent successfully.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'An error occurred: {str(e)}'
            }, status=500)
            
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)

