# from rest_framework import serializers
# from .models import Post
# class PostSerializer(serializers.ModelSerializer):
#     video_url = serializers.SerializerMethodField()

#     class Meta:
#         model = Post
#         fields = ['id', 'title', 'category', 'video_url']

#     def get_video_url(self, obj):
#         request = self.context.get('request')
#         if obj.demonstration: # Use your actual field name here
#             url = request.build_absolute_uri(obj.demonstration.url)
#             # This ensures the emulator can find your computer
#             return url.replace("127.0.0.1", "10.0.2.2").replace("localhost", "10.0.2.2")
#         return ""
from rest_framework import serializers
from .models import Post
class PostSerializer(serializers.ModelSerializer):
    # Dito, sinasabi natin na gagawa tayo ng custom field na ang pangalan ay "demonstration"
    demonstration = serializers.SerializerMethodField()

    class Meta:
        model = Post
        # Isasama natin ang "demonstration" sa JSON output
        fields = ['id', 'title', 'category', 'demonstration']

    # Ito ang logic para makuha ang video link
    def get_demonstration(self, obj):
        request = self.context.get('request')
        
        # Sine-check muna kung may laman ang field sa database para hindi mag-crash
        if obj.demonstration: 
            # Dito kinukuha ang link ng file mula sa database field na 'demonstration'
            url = request.build_absolute_uri(obj.demonstration.url)
            
            # Emulator Fix
            return url.replace("127.0.0.1", "10.0.2.2").replace("localhost", "10.0.2.2")
        return ""