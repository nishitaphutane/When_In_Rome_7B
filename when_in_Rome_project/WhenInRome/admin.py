from django.contrib import admin
from WhenInRome.models import City, Recommendation, Review, UserProfile, Upvote

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name' , 'views', 'likes')

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'views', 'url', 'category')  

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'recommendation', 'rating')

admin.site.register(City, CityAdmin)
admin.site.register(Recommendation, RecommendationAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserProfile)
admin.site.register(Upvote)
