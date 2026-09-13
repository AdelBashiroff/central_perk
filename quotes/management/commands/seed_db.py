from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from characters.models import Character
from episodes.models import Episode
from quotes.models import Quote
from discussions.models import DiscussionThread

User = get_user_model()


class Command(BaseCommand):
    """
    Команда для заполнения базы данных начальными данными.
    Использование: python manage.py seed_db
    """
    
    help = 'Заполняет базу данных начальными данными'
    
    def handle(self, *args, **options):
        self.stdout.write('Начинаем заполнение базы данных...')
        
        # 1. Создаем пользователей
        users_data = [
            {'username': 'centralperk', 'password': 'friendspass', 'email': 'perk@friends.com'},
            {'username': 'rachel', 'password': 'green123', 'email': 'rachel@friends.com'},
            {'username': 'monica', 'password': 'geller123', 'email': 'monica@friends.com'},
            {'username': 'phoebe', 'password': 'buffay123', 'email': 'phoebe@friends.com'},
            {'username': 'joey', 'password': 'tribbiani123', 'email': 'joey@friends.com'},
            {'username': 'chandler', 'password': 'bing123', 'email': 'chandler@friends.com'},
            {'username': 'ross', 'password': 'geller123', 'email': 'ross@friends.com'},
        ]
        
        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={'email': user_data['email']}
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f'  ✅ Создан пользователь: {user.username}')
            users.append(user)
        
        # 2. Создаем персонажей
        characters_data = [
            {'name': 'Rachel Green', 'actor_name': 'Jennifer Aniston',
             'description': 'Модница, которая сбежала со своей свадьбы'},
            {'name': 'Monica Geller', 'actor_name': 'Courteney Cox',
             'description': 'Перфекционистка и отличный повар'},
            {'name': 'Phoebe Buffay', 'actor_name': 'Lisa Kudrow',
             'description': 'Эксцентричная массажистка и музыкант'},
            {'name': 'Joey Tribbiani', 'actor_name': 'Matt LeBlanc',
             'description': 'Актер, который любит еду и женщин'},
            {'name': 'Chandler Bing', 'actor_name': 'Matthew Perry',
             'description': 'Король сарказма, работает в аналитике'},
            {'name': 'Ross Geller', 'actor_name': 'David Schwimmer',
             'description': 'Палеонтолог, доктор наук'},
        ]
        
        characters = []
        for char_data in characters_data:
            character, created = Character.objects.get_or_create(
                name=char_data['name'],
                defaults={
                    'actor_name': char_data['actor_name'],
                    'description': char_data['description']
                }
            )
            if created:
                self.stdout.write(f'  ✅ Создан персонаж: {character.name}')
            characters.append(character)
        
        # 3. Создаем серии
        episodes_data = [
            {'title': 'The One Where It All Began', 'season': 1, 'episode_number': 1},
            {'title': 'The One with the Sonogram at the End', 'season': 1, 'episode_number': 2},
            {'title': 'The One with the Thumb', 'season': 1, 'episode_number': 3},
        ]
        
        episodes = []
        for ep_data in episodes_data:
            episode, created = Episode.objects.get_or_create(
                season=ep_data['season'],
                episode_number=ep_data['episode_number'],
                defaults={'title': ep_data['title']}
            )
            if created:
                self.stdout.write(f'  ✅ Создана серия: {episode}')
            episodes.append(episode)
        
        # 4. Создаем цитаты
        quotes_data = [
            {'text': "We were on a break!", 'character': characters[5], 'episode': episodes[0]},
            {'text': "How you doin'?", 'character': characters[3], 'episode': episodes[1]},
            {'text': "Could I BE any more...?", 'character': characters[4], 'episode': episodes[0]},
            {'text': "Oh. My. God.", 'character': characters[0], 'episode': episodes[2]},
            {'text': "I know!", 'character': characters[1], 'episode': episodes[1]},
            {'text': "Smelly Cat, smelly cat, what are they feeding you?",
             'character': characters[2], 'episode': episodes[0]},
            {'text': "Unagi!", 'character': characters[5], 'episode': episodes[2]},
            {'text': "Pivot! Pivot! Pivot!", 'character': characters[5], 'episode': episodes[1]},
        ]
        
        for quote_data in quotes_data:
            quote, created = Quote.objects.get_or_create(
                text=quote_data['text'],
                defaults={
                    'character': quote_data['character'],
                    'episode': quote_data['episode'],
                    'author': users[0]
                }
            )
            if created:
                self.stdout.write(f'  ✅ Создана цитата: {quote.text[:30]}...')
        
        # 5. Создаем темы обсуждений
        discussion_data = [
            {'title': 'Лучшая серия сериала?', 'content': 'Какая серия ваша любимая?', 'user': users[1]},
            {'title': 'Кто ваш любимый персонаж?', 'content': 'Голосуем!', 'user': users[2]},
        ]
        
        for disc_data in discussion_data:
            thread, created = DiscussionThread.objects.get_or_create(
                title=disc_data['title'],
                defaults={
                    'content': disc_data['content'],
                    'user': disc_data['user']
                }
            )
            if created:
                self.stdout.write(f'  ✅ Создана тема: {thread.title}')
        
        self.stdout.write(self.style.SUCCESS('✅ База данных успешно заполнена!'))