from django.contrib import admin
from WhenInRome.models import City, Recommendation, Review, UserProfile, Upvote, VisitedCity 

#fills the slug field automatically based on the name of the city or title of the recommendation (all)


#Displays information in list view
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'recommendation', 'rating')

#Displays information in list view
class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name','country','description')
    
#Displays information in list view
class RecommendationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    
    def upvote_count(self, obj):
        return obj.upvote_count
    
    upvote_count.short_description = 'Upvotes'
    list_display = ('city', 'user', 'title', 'description', 'location', 'upvote_count')

class UserProfileAdmin(admin.ModelAdmin):
    def follower_count(self, obj):
        return obj.followers.count()
    
    def following_count(self, obj):
        return UserProfile.objects.filter(followers=obj.user).count()
    
    follower_count.short_description = 'Followers'
    following_count.short_description = 'Following'
    
    list_display = ('user', 'follower_count', 'following_count')

admin.site.register(City, CityAdmin)
admin.site.register(Recommendation, RecommendationAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserProfile , UserProfileAdmin)
admin.site.register(Upvote)
admin.site.register(VisitedCity)
