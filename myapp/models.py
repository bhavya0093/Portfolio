from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200, help_text="e.g. Full Stack Developer & Designer")
    bio = models.TextField(help_text="Short introductory bio")
    about_me = models.TextField(help_text="Detailed personal description for About section")
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True, help_text="Main profile picture")
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=150)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True, help_text="X / Twitter URL")
    resume = models.FileField(upload_to='resumes/', blank=True, null=True, help_text="Upload CV/Resume PDF")
    logo_text = models.CharField(max_length=50, default="Portfolio", help_text="Logo text displayed in navbar")

    def __str__(self):
        return self.name

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Tools', 'Tools & Devops'),
        ('Other', 'Other/Soft Skills'),
    ]
    name = models.CharField(max_length=100)
    percentage = models.IntegerField(default=80, help_text="Skill level percentage (0 to 100)")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Frontend')

    def __str__(self):
        return f"{self.name} ({self.category} - {self.percentage}%)"

    class Meta:
        ordering = ['category', '-percentage']

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Short description of the project")
    detail_description = models.TextField(blank=True, null=True, help_text="Detailed project breakdown/features (optional)")
    image = models.ImageField(upload_to='projects/', blank=True, null=True, help_text="Project preview screenshot")
    category = models.CharField(max_length=100, help_text="e.g. Web App, Mobile, Game, UI/UX")
    technologies = models.CharField(max_length=250, help_text="Comma-separated technologies (e.g. Django, React, Bootstrap 5)")
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    featured = models.BooleanField(default=False, help_text="Display first or highlight on the home page")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        """Returns a list of technologies from the comma-separated string"""
        if self.technologies:
            return [tech.strip() for tech in self.technologies.split(',')]
        return []

    class Meta:
        ordering = ['-featured', '-created_at']

class Service(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="Bootstrap icon class name, e.g. bi-code-slash, bi-laptop, bi-palette")
    order = models.IntegerField(default=0, help_text="Display order")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']

class Experience(models.Model):
    company = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank if this is your current role")
    is_current = models.BooleanField(default=False, verbose_name="Current Role?")
    order = models.IntegerField(default=0, help_text="Display order (usually higher number is older)")

    def __str__(self):
        status = "Present" if self.is_current else (self.end_date.strftime("%Y-%b") if self.end_date else "")
        return f"{self.role} at {self.company} ({self.start_date.strftime('%Y-%b')} - {status})"

    class Meta:
        ordering = ['order', '-start_date']

class Certificate(models.Model):
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=150)
    issue_date = models.DateField()
    credential_id = models.CharField(max_length=150, blank=True, null=True)
    credential_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='certificates/', blank=True, null=True, help_text="Copy or preview of the certificate")
    order = models.IntegerField(default=0, help_text="Display order")

    def __str__(self):
        return f"{self.name} - {self.issuing_organization}"

    class Meta:
        ordering = ['order', '-issue_date']

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name}: {self.subject}"

    class Meta:
        ordering = ['-created_at']

