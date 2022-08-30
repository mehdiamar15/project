from boards import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('boards/<int:board_id>/', views.board_topics, name='board_topics'),
    path('records/', views.recordsmng, name='recordsmng'),
    path('recordsmng_ajax/', views.recordsmng_ajax, name='recordsmng_ajax'),
    path('pmta_config_ajax/', views.pmta_config_ajax, name='pmta_config_ajax'),
    
    
    path('boards/<int:board_id>/new/', views.new_topics, name='new_topics'),
    path('boards/<int:board_id>/topics/<int:topic_id>', views.topic_posts, name='topic_posts'),
    path('boards/<int:board_id>/topics/<int:topic_id>/reply', views.reply_topic, name='reply_topic'),
    path('boards/<int:board_id>/topics/<int:topic_id>/posts/<int:post_id>/edit/', views.PostUpdateView.as_view(), name='edit_post'),

]