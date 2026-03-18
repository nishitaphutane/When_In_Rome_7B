from django.contrib import admin
from WhenInRome.models import City, Recommendation, Review, UserProfile, Upvote

class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # Like CategoryAdmin in Rango

class RecommendationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'city', 'user')  # Like PageAdmin in Rango

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'recommendation', 'rating')

admin.site.register(City, CityAdmin)
admin.site.register(Recommendation, RecommendationAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserProfile)
admin.site.register(Upvote)