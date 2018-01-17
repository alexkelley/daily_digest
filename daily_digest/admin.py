from django.contrib import admin

from .models import Quote, Quote_Author, Exercise


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('quote_text', 'times_served', 'date_last_served', 'pub_date')


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'times_served', 'date_last_served')    
    
# admin.site.register(Quote)
admin.site.register(Quote_Author)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Quote, QuoteAdmin)
