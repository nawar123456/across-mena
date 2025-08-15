from django.urls import path
from .views import get_fees_and_import_fees_for_sub_chapter_to_sari,ChapterList,get_fees_and_import_fees_for_sub_chapter_with_notes, ChapterSectionDetailView, ChaptersWithNotesAPIView, FeeList, NoteChapterList, NoteFeeList, NoteSectionList, NoteSubChapterList, NotesByChapterAPIView, NotesByFeeAPIView, NotesBySectionAPIView, NotesBySubChapterAPIView, SearchView, SectionDetailView, SectionList, SectionsWithNotesAPIView, Sub_ChapterList, SubChaptersWithNotesAPIView, get_fees_and_import_fees_for_sub_chapter
from . import views


urlpatterns = [
    # returns all section
    # path('haidarasections/', views.SectionViewSet),


    path('sections/', SectionList.as_view(), name='sections'),

    # returns all chapters

    path('chapters/', ChapterList.as_view(), name='chapters'),
   
    # returns all sub_chapter
    
    path('sub_chapters/', Sub_ChapterList.as_view(), name='sub_chapters'),
   
    # returns all decriptions (fee)

    path('fee/', FeeList.as_view(), name='fee'),
   
    # returns every section depending on the id for the section
    
    path('section/<int:id>/', SectionDetailView.as_view(), name='section-detail'),
    
    # returns every chapter depending on the id for the chapter
    
    path('chapter/<str:id>/', ChapterSectionDetailView.as_view(), name='chapter-detail'),
    
    # returns every chapter depending on the id for the section
    
    path('api/section/<str:section_id>/', views.get_chapters_for_section, name='get_chapters_for_section'),
    
    # returns every sub_chapter depending on the id for the chapter
    
    path('api/chapter/<str:chapter_id>/', views.get_sub_chapters_for_chapter, name='get_sub_chapters_for_chapter'),
    # returns every decriptions (fee) depending on the id for the sub_chapter
    
    path('api/sub_chapter/<str:sub_chapter_id>/', views.get_fees_for_sub_chapter, name='get_fees_for_sub_chapter'),
    
    # returns every decriptions (fee) with import and export rules depending on the id for the sub_chapter
    
    path('api/sub_chapter_with_import/<str:sub_chapter_id>/', views.get_fees_and_import_fees_for_sub_chapter, name='get_fees_and_import_fees_for_sub_chapter'),
    path('api/sub_chapter_with_import_to_sari/<str:sub_chapter_id>/', views.get_fees_and_import_fees_for_sub_chapter_to_sari, name='get_fees_and_import_fees_for_sub_chapter'),

    # returns notes depending on the id for the section 
    
    path('api/notes_by_section/<str:section_id>/', NotesBySectionAPIView.as_view(), name='notes_by_section'),
    
    # returns notes depending on the id for the chapter 
   
    path('api/notes_by_chapter/<str:chapter_id>/', NotesByChapterAPIView.as_view(), name='notes_by_chapter'),
    
    # returns notes depending on the id for the sub_chapter 
   
    path('api/notes_by_subchapter/<str:subchapter_id>/', NotesBySubChapterAPIView.as_view(), name='notes_by_subchapter'),
   
    # returns notes depending on the id for the decriptions (fee)
    
    path('api/notes_by_fee/<str:fee_id>/', NotesByFeeAPIView.as_view(), name='notes_by_fee'),
    
    # returns all notes for the all section
   
    path('notesection/', NoteSectionList.as_view(), name=' all_note_section'),
   
    # returns all notes for the all chapter
   
    path('notechapter/', NoteChapterList.as_view(), name=' all_note_chapter'),

    # returns all notes for the all sub_chapter
   
    path('notesubchapter/', NoteSubChapterList.as_view(), name=' all_note_sub_chapter'),

    # returns all notes for the all decriptions (fee)
   
    path('notefee/', NoteFeeList.as_view(), name=' all_note_fee'),
 
    #return all sections along with the notes for each section

    path('api/sections_with_notes/', SectionsWithNotesAPIView.as_view(), name='sections_with_notes'),
 
    #return all chapters along with the notes for each chapter
    
    path('api/chapters_with_notes/', ChaptersWithNotesAPIView.as_view(), name='chapters_with_notes'),

    #return all subchapters along with the notes for each subchapter

    path('api/subchapters_with_notes/', SubChaptersWithNotesAPIView.as_view(), name='subchapters_with_notes'),

    path('api/fees_and_import_fees/<str:sub_chapter_id>/', get_fees_and_import_fees_for_sub_chapter_with_notes, name='fees_and_import_fees'),
    #searching
    path('search/', SearchView.as_view(), name='search-view'),
    # second-description
    path('second-description/<str:id_desc>/', views.SecondDescription.as_view(), name='second-description'),


     















]
