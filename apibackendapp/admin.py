from django.contrib import admin

from .models import Project, UserDetails, department, employee
# from rest_framework.authtoken.models import Token


# Register Department
admin.site.register(department)


# Inline class to display Many-To-Many relationship inside Employee Admin
class ProjectInline(admin.TabularInline):
    # Use the intermediate/junction table
    model = Project.employees.through

    # Number of empty rows for adding relationships
    extra = 1


# Customize Employee Admin panel
class EmployeeAdmin(admin.ModelAdmin):
    # Attach ProjectInline to Employee admin page
    inlines = [ProjectInline]


# Register Employee with customized EmployeeAdmin
admin.site.register(employee, EmployeeAdmin)
# admin.site.register(Token)  # Register Token model for authentication
admin.site.register(UserDetails)  # Register UserDetails model for user information



# Register Project
admin.site.register(Project)