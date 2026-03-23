from django.contrib import admin
from WhenInRome.models import City, Recommendation, Review, UserProfile, Upvote 

#fills the slug field automatically based on the name of the city or title of the recommendation (all)

class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


#Displays information in list view
class RecommendationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'city', 'user') 

#Displays information in list view
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'recommendation', 'rating')


#Registering the models with admin site
admin.site.register(City, CityAdmin)
admin.site.register(Recommendation, RecommendationAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserProfile)
admin.site.register(Upvote)
