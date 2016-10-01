from django.contrib import admin

from .models import Band, Album, Song


class BandAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'albums', 'songs')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ['name']

    fields = ('name', 'description', 'image', 'image_tag',)
    readonly_fields = ('image_tag',)

    def albums(self, obj):
        return len(obj.album_set.all())

    def songs(self, obj):
        return len(obj.song_set.all())


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'band', 'songs')
    list_filter = ('name', 'band')
    search_fields = ('name', 'band')
    ordering = ('name', 'band')

    fields = ('name', 'band', 'image', 'image_tag',)
    readonly_fields = ('image_tag',)

    def songs(self, obj):
        return len(obj.song_set.all())


class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'band', 'album', 'duration')
    list_filter = ('name', 'band', 'album')
    search_field = ('name', 'band', 'album')
    ordering = ('name', 'band', 'album')

    fields = ('name', 'duration', 'band', 'album', 'song_file', 'song_tag', 'image', 'image_tag')
    readonly_fields = ('image_tag', 'song_tag', 'duration')


admin.site.register(Band, BandAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
