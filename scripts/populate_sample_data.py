#!/usr/bin/env python
"""
Script to populate sample data for Cultura AI
"""
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cultura_ai.settings')
django.setup()

from apps.stories.models import Story, StoryCollection, StoryRating, StoryInteraction
from apps.games.models import Game, GameSession, Achievement, UserAchievement
from apps.analytics.models import LanguageUsage, FeatureUsage, ContentPerformance
from django.contrib.auth import get_user_model

User = get_user_model()


def create_sample_stories():
    """Create sample stories"""
    print("Creating sample stories...")
    
    stories_data = [
        {
            'title': 'The Wise Hare and the Elephant',
            'content': '''Long ago in the forests of Mount Kenya, there lived a clever hare named Sungura. Despite his small size, Sungura was known throughout the forest for his quick wit and wisdom.

One dry season, when water became scarce, the mighty elephant Tembo decided that he alone should drink from the remaining water hole. He chased away all the other animals, claiming the water as his own.

The animals were desperate. They gathered and pleaded with Sungura to help them. "How can I, a small hare, challenge the mighty elephant?" Sungura asked.

But Sungura was clever. He went to Tembo and said, "Great Tembo, I have heard that you are the strongest animal in all of Kenya. But I wonder, are you stronger than the elephant who lives on the other side of the mountain?"

Tembo's pride was wounded. "Impossible! There is no elephant stronger than me!"

Sungura led Tembo to a deep well and pointed down. "Look, there he is!" In the water's reflection, Tembo saw another elephant looking back at him.

Enraged, Tembo charged at his reflection, falling deep into the well. Sungura quickly gathered all the animals, and together they pulled Tembo out, but only after he promised to share the water with everyone.

From that day forward, all animals shared the water hole equally, and Tembo learned that wisdom is often more powerful than strength.''',
            'summary': 'A clever hare outsmarts a selfish elephant to ensure all animals can share the water during a drought.',
            'language': 'ki',
            'cultural_origin': 'Kikuyu',
            'category': 'wisdom',
            'difficulty': 'beginner',
            'author': 'Traditional Kikuyu Folktale',
            'featured': True,
            'views': 234,
            'likes': 45
        },
        {
            'title': 'Lwanda Magere, the Stone Man',
            'content': '''In the land of the Luo people, near the shores of Lake Victoria, there lived a great warrior named Lwanda Magere. He was no ordinary man, for his body was made of stone, making him invincible in battle.

Lwanda Magere protected his people from all enemies. Arrows bounced off his stone skin, spears shattered against his chest, and no weapon could harm him. The Luo people lived in peace under his protection.

But the neighboring tribes grew jealous of the Luo's prosperity and safety. They plotted together, trying to find a way to defeat the stone man. Many warriors tried and failed, their weapons useless against Lwanda Magere's stone body.

Finally, they devised a cunning plan. They sent a beautiful woman to marry Lwanda Magere, hoping she would discover his weakness. The woman, though reluctant, agreed to help her people.

After their marriage, she observed Lwanda Magere carefully. One day, she noticed that when he cast his shadow, the shadow was not made of stone but was soft like any ordinary man's shadow.

She reported this discovery to her people. The next time Lwanda Magere went to battle, the enemy warriors ignored his stone body and attacked his shadow instead. When they pierced his shadow with their spears, Lwanda Magere fell, for his shadow was his only weakness.

The Luo people mourned their great protector. Where Lwanda Magere fell, a great rock formation appeared, which stands to this day near Kisumu, reminding all of the brave stone man who gave his life for his people.

The story teaches us that everyone has a weakness, and that betrayal from within is often more dangerous than any external enemy.''',
            'summary': 'The legend of Lwanda Magere, the invincible stone warrior of the Luo people, and how his only weakness was discovered.',
            'language': 'luo',
            'cultural_origin': 'Luo',
            'category': 'heroic',
            'difficulty': 'intermediate',
            'author': 'Traditional Luo Legend',
            'featured': True,
            'views': 456,
            'likes': 78
        },
        {
            'title': 'The Origin of the Baobab Tree',
            'content': '''The Kamba people tell of how the great baobab tree came to be, with its roots reaching toward the sky and its branches buried in the earth.

Long ago, when the world was young and the gods still walked among mortals, there lived a proud and beautiful tree. This tree was the most magnificent in all the land, with lush green leaves, sweet fruits, and flowers that perfumed the entire forest.

The tree became vain about its beauty. It looked down upon the other plants and animals, refusing to provide shade for weary travelers or shelter for birds and animals. "I am too beautiful to be touched by such common creatures," the tree would say.

The other trees pleaded with the proud tree to be kind and helpful, as all trees should be. But the beautiful tree only laughed and preened its leaves, admiring its own reflection in the nearby stream.

Ngai, the supreme god of the Kamba people, watched this behavior with growing displeasure. He had created all plants to serve and help each other and the animals. The proud tree's selfishness went against the natural order.

One day, Ngai decided to teach the tree a lesson. He called upon the great winds and the spirits of the earth. In a mighty display of power, Ngai uprooted the proud tree and replanted it upside down.

Now the tree's roots reached toward the sky, and its branches were buried in the earth. Its beautiful leaves withered, and its trunk became thick and strange-looking. The tree could no longer admire its reflection or refuse help to others.

But Ngai was not cruel. He gave the upside-down tree special gifts: its trunk could store water for the dry seasons, its fruit would be nutritious and healing, and its bark could be used for medicine and rope. The tree would serve others whether it wanted to or not.

This is how the baobab tree came to be. Even today, when you see a baobab with its roots reaching toward the sky, remember the lesson: true beauty comes from helping others, not from pride and vanity.

The Kamba people still use every part of the baobab tree - its fruit for food, its bark for medicine, and its hollow trunk for shelter and water storage during droughts.''',
            'summary': 'How the proud and vain tree was turned upside down by Ngai to become the humble and useful baobab tree.',
            'language': 'kam',
            'cultural_origin': 'Kamba',
            'category': 'origin',
            'difficulty': 'advanced',
            'author': 'Traditional Kamba Folktale',
            'featured': False,
            'views': 189,
            'likes': 62
        },
        {
            'title': 'The Girl Who Married a Star',
            'content': '''Among the Kikuyu people, there is a beautiful tale of a young woman named Wanjiku who fell in love with a star.

Wanjiku was the most beautiful girl in her village, with skin that glowed like moonlight and eyes that sparkled like dewdrops. Many young men sought her hand in marriage, but Wanjiku's heart belonged to someone else entirely.

Every night, she would climb to the highest hill and gaze at the brightest star in the sky. She would sing to it and tell it about her day, and she believed the star sang back to her in the whisper of the wind.

Her parents grew worried. "Wanjiku," her mother said, "you must choose a husband from among the young men of our village. You cannot marry a star!"

But Wanjiku's love was true and deep. One night, as she sang to her beloved star, a handsome young man appeared before her. His skin shimmered with silver light, and his eyes held the depth of the night sky.

"I am Njata, the star you have been singing to," he said. "Your love has given me the power to take human form. Will you come with me to my home in the sky?"

Without hesitation, Wanjiku took his hand. Together, they rose into the night sky, higher and higher, until they reached the star's celestial home.

In the sky realm, Wanjiku lived in a palace made of starlight and moonbeams. She was happy, but she missed her family and the earth below. Njata, seeing her sadness, would allow her to visit earth, but only at night when he could accompany her.

The people of her village would sometimes see Wanjiku dancing in the moonlight, more beautiful than ever, with her star husband beside her. They say that on clear nights, if you look carefully at the brightest star, you can still see Wanjiku there, watching over her earthly home.

This story teaches us that true love knows no boundaries, and that sometimes the heart sees beauty and connection where others see only impossibility.

Young Kikuyu girls still sing to the stars, hoping that their pure love might be answered from the heavens above.''',
            'summary': 'A beautiful Kikuyu tale of a young woman who falls in love with a star and is taken to live in the celestial realm.',
            'language': 'ki',
            'cultural_origin': 'Kikuyu',
            'category': 'romance',
            'difficulty': 'intermediate',
            'author': 'Traditional Kikuyu Folktale',
            'featured': False,
            'views': 523,
            'likes': 91
        },
        {
            'title': 'Why the Tortoise Has a Cracked Shell',
            'content': '''The Luo people tell this amusing tale of how the tortoise got his distinctive cracked shell pattern.

Long ago, Tortoise had a smooth, beautiful shell that was the envy of all the animals. He was very proud of his shell and would spend hours polishing it until it gleamed in the sunlight.

One year, there was a great feast in the sky kingdom, and all the birds were invited. Tortoise heard about this magnificent feast and desperately wanted to attend, but he had no wings to fly.

Being clever, Tortoise went to the birds and said, "My dear friends, I have heard about the wonderful feast in the sky. Though I cannot fly, I am known for my wisdom and good manners. Surely the sky people would benefit from my presence at their feast?"

The birds, who respected Tortoise's wisdom, agreed to help. Each bird gave Tortoise one feather, and soon he had enough feathers to make wings. But Tortoise had a cunning plan.

"Before we go," Tortoise said, "we should all take new names for this special occasion. I shall be called 'All of You.'"

The birds thought this was a wonderful idea and each chose a new name for the feast.

When they arrived in the sky kingdom, the hosts welcomed them warmly. "Welcome, birds! We have prepared a magnificent feast for all of you!"

Tortoise immediately stepped forward. "Thank you! Since I am called 'All of You,' this feast must be entirely for me!"

Before the birds could protest, Tortoise began eating everything - the honey cakes, the roasted nuts, the sweet fruits, and the palm wine. He ate and ate until his belly was round and full, leaving nothing for the birds.

The birds were furious at Tortoise's trickery. In their anger, they took back their feathers, leaving Tortoise stranded in the sky with no way to get down.

Tortoise called down to his wife on earth, "Bring all the soft things from our house - the mats, the cushions, the cloth - and spread them outside so I can jump down safely!"

But the birds, still angry, got to Tortoise's wife first. "Tortoise says to bring all the hard things from your house - the stones, the pots, the farming tools - and spread them outside!"

Tortoise's wife, trusting the birds, gathered all the hard objects and spread them beneath the tree where Tortoise would land.

When Tortoise jumped from the sky, he crashed down onto the hard stones and pots. His beautiful smooth shell cracked into many pieces with a loud CRACK!

Tortoise survived, but his shell was forever marked with the cracks from his fall. Even today, all tortoises carry the pattern of cracks on their shells, reminding everyone of the consequences of greed and trickery.

The birds learned to be more careful about whom they trust, and Tortoise learned that cleverness without kindness often leads to trouble.

This is why, when Luo children see a tortoise, they remember this story and learn that greed and deception will always catch up with you in the end.''',
            'summary': 'A humorous Luo tale explaining how the tortoise got his cracked shell through his own greed and trickery.',
            'language': 'luo',
            'cultural_origin': 'Luo',
            'category': 'humor',
            'difficulty': 'beginner',
            'author': 'Traditional Luo Folktale',
            'featured': False,
            'views': 678,
            'likes': 127
        }
    ]
    
    for story_data in stories_data:
        story, created = Story.objects.get_or_create(
            title=story_data['title'],
            defaults=story_data
        )
        if created:
            print(f"Created story: {story.title}")


def create_sample_games():
    """Create sample games"""
    print("Creating sample games...")
    
    games_data = [
        {
            'name': 'Word Match Challenge',
            'description': 'Match English words with their Kikuyu, Luo, or Kamba translations',
            'game_type': 'word_match',
            'difficulty': 'easy',
            'time_limit': 300,  # 5 minutes
            'max_score': 100,
            'min_score_to_pass': 60,
            'source_language': 'en',
            'target_language': 'ki',
            'is_featured': True,
            'game_data': {
                'questions': [
                    {'english': 'water', 'kikuyu': 'mai', 'options': ['mai', 'mti', 'mbura', 'riua']},
                    {'english': 'tree', 'kikuyu': 'mti', 'options': ['mai', 'mti', 'mbura', 'riua']},
                    {'english': 'rain', 'kikuyu': 'mbura', 'options': ['mai', 'mti', 'mbura', 'riua']},
                    {'english': 'sun', 'kikuyu': 'riua', 'options': ['mai', 'mti', 'mbura', 'riua']},
                ]
            }
        },
        {
            'name': 'Cultural Quiz Master',
            'description': 'Test your knowledge of African cultures and languages',
            'game_type': 'cultural_quiz',
            'difficulty': 'medium',
            'time_limit': 600,  # 10 minutes
            'max_score': 150,
            'min_score_to_pass': 90,
            'source_language': 'en',
            'target_language': 'ki',
            'is_featured': True,
            'game_data': {
                'questions': [
                    {
                        'question': 'What is the traditional Kikuyu name for Mount Kenya?',
                        'options': ['Kirinyaga', 'Kilimanjaro', 'Kericho', 'Kisumu'],
                        'correct': 'Kirinyaga'
                    },
                    {
                        'question': 'Which lake is sacred to the Luo people?',
                        'options': ['Lake Turkana', 'Lake Nakuru', 'Lake Victoria', 'Lake Naivasha'],
                        'correct': 'Lake Victoria'
                    }
                ]
            }
        },
        {
            'name': 'Speed Translation',
            'description': 'Race against time to translate phrases correctly',
            'game_type': 'speed_translation',
            'difficulty': 'hard',
            'time_limit': 180,  # 3 minutes
            'max_score': 200,
            'min_score_to_pass': 120,
            'source_language': 'en',
            'target_language': 'luo',
            'is_featured': False,
            'game_data': {
                'phrases': [
                    {'english': 'Good morning', 'luo': 'Oyawore'},
                    {'english': 'Thank you', 'luo': 'Erokamano'},
                    {'english': 'How are you?', 'luo': 'Idhi nade?'},
                ]
            }
        }
    ]
    
    for game_data in games_data:
        game, created = Game.objects.get_or_create(
            name=game_data['name'],
            defaults=game_data
        )
        if created:
            print(f"Created game: {game.name}")


def create_sample_achievements():
    """Create sample achievements"""
    print("Creating sample achievements...")
    
    achievements_data = [
        {
            'name': 'First Steps',
            'description': 'Complete your first translation',
            'achievement_type': 'completion',
            'requirements': {'translations': 1},
            'points_reward': 10,
            'icon': '🎯',
            'badge_color': 'bronze'
        },
        {
            'name': 'Story Lover',
            'description': 'Read 5 different stories',
            'achievement_type': 'completion',
            'requirements': {'stories_read': 5},
            'points_reward': 25,
            'icon': '📚',
            'badge_color': 'silver'
        },
        {
            'name': 'Game Master',
            'description': 'Score 90% or higher in any game',
            'achievement_type': 'score',
            'requirements': {'game_score_percentage': 90},
            'points_reward': 50,
            'icon': '🏆',
            'badge_color': 'gold'
        },
        {
            'name': 'Speed Demon',
            'description': 'Complete a game in half the time limit',
            'achievement_type': 'speed',
            'requirements': {'time_percentage': 50},
            'points_reward': 30,
            'icon': '⚡',
            'badge_color': 'silver'
        },
        {
            'name': 'Cultural Explorer',
            'description': 'Interact with content in all 4 languages',
            'achievement_type': 'completion',
            'requirements': {'languages_used': 4},
            'points_reward': 75,
            'icon': '🌍',
            'badge_color': 'gold'
        }
    ]
    
    for achievement_data in achievements_data:
        achievement, created = Achievement.objects.get_or_create(
            name=achievement_data['name'],
            defaults=achievement_data
        )
        if created:
            print(f"Created achievement: {achievement.name}")


def create_sample_analytics():
    """Create sample analytics data"""
    print("Creating sample analytics data...")
    
    # Create language usage data for the past 30 days
    from datetime import date, timedelta
    
    languages = ['en', 'ki', 'luo', 'kam']
    
    for i in range(30):
        current_date = date.today() - timedelta(days=i)
        
        for lang in languages:
            LanguageUsage.objects.get_or_create(
                language_code=lang,
                date=current_date,
                defaults={
                    'translation_requests': random.randint(10, 100),
                    'story_views': random.randint(5, 50),
                    'game_plays': random.randint(3, 30),
                    'tts_requests': random.randint(2, 20),
                    'unique_users': random.randint(5, 25),
                    'guest_users': random.randint(2, 15),
                }
            )
    
    # Create feature usage data
    features = [
        ('translation', 'translation'),
        ('story_reader', 'stories'),
        ('game_hub', 'games'),
        ('tts_generator', 'tts'),
        ('user_profile', 'profile'),
    ]
    
    for i in range(30):
        current_date = date.today() - timedelta(days=i)
        
        for feature_name, feature_type in features:
            FeatureUsage.objects.get_or_create(
                feature_name=feature_name,
                date=current_date,
                defaults={
                    'feature_type': feature_type,
                    'total_uses': random.randint(20, 200),
                    'unique_users': random.randint(10, 50),
                    'average_session_time': random.uniform(60, 600),  # 1-10 minutes
                    'success_rate': random.uniform(85, 99),
                    'error_rate': random.uniform(1, 15),
                    'average_response_time': random.uniform(0.5, 3.0),
                }
            )
    
    print("Created sample analytics data")


def create_story_collections():
    """Create sample story collections"""
    print("Creating story collections...")
    
    collections_data = [
        {
            'name': 'Wisdom Tales',
            'description': 'Stories that teach important life lessons and wisdom',
            'is_featured': True,
        },
        {
            'name': 'Heroes and Legends',
            'description': 'Tales of brave warriors and legendary figures',
            'is_featured': True,
        },
        {
            'name': 'Origin Stories',
            'description': 'Stories explaining how things came to be',
            'is_featured': False,
        }
    ]
    
    for collection_data in collections_data:
        collection, created = StoryCollection.objects.get_or_create(
            name=collection_data['name'],
            defaults=collection_data
        )
        
        if created:
            # Add relevant stories to collections
            if collection.name == 'Wisdom Tales':
                wisdom_stories = Story.objects.filter(category='wisdom')
                collection.stories.set(wisdom_stories)
            elif collection.name == 'Heroes and Legends':
                heroic_stories = Story.objects.filter(category='heroic')
                collection.stories.set(heroic_stories)
            elif collection.name == 'Origin Stories':
                origin_stories = Story.objects.filter(category='origin')
                collection.stories.set(origin_stories)
            
            print(f"Created collection: {collection.name}")


def main():
    """Run all sample data creation functions"""
    print("Populating Cultura AI with sample data...")
    
    create_sample_stories()
    create_sample_games()
    create_sample_achievements()
    create_sample_analytics()
    create_story_collections()
    
    print("\nSample data population completed successfully!")
    print("\nYou can now:")
    print("1. View stories at: http://localhost:8000/api/v1/stories/")
    print("2. View games at: http://localhost:8000/api/v1/games/")
    print("3. View analytics at: http://localhost:8000/api/v1/analytics/dashboard/")
    print("4. Access the admin panel at: http://localhost:8000/admin/")


if __name__ == '__main__':
    main()