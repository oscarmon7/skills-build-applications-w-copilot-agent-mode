from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel', description='Team Marvel Superheroes')
        dc = Team.objects.create(name='DC', description='Team DC Superheroes')

        # Create Users
        users = [
            User(name='Tony Stark', email='tony@marvel.com', team=marvel, is_superhero=True),
            User(name='Steve Rogers', email='steve@marvel.com', team=marvel, is_superhero=True),
            User(name='Bruce Wayne', email='bruce@dc.com', team=dc, is_superhero=True),
            User(name='Clark Kent', email='clark@dc.com', team=dc, is_superhero=True),
        ]
        User.objects.bulk_create(users)

        # Refresh users with IDs
        users = list(User.objects.all())
        tony = next(u for u in users if u.name == 'Tony Stark')
        steve = next(u for u in users if u.name == 'Steve Rogers')
        bruce = next(u for u in users if u.name == 'Bruce Wayne')
        clark = next(u for u in users if u.name == 'Clark Kent')

        # Create Activities
        Activity.objects.create(user=tony, type='Iron Man Suit Training', duration=60, date=timezone.now().date())
        Activity.objects.create(user=steve, type='Shield Practice', duration=45, date=timezone.now().date())
        Activity.objects.create(user=bruce, type='Martial Arts', duration=90, date=timezone.now().date())
        Activity.objects.create(user=clark, type='Flight', duration=120, date=timezone.now().date())

        # Create Workouts
        w1 = Workout.objects.create(name='Super Strength', description='Strength workout for superheroes')
        w2 = Workout.objects.create(name='Agility Training', description='Agility and speed workout')
        w1.suggested_for.set([tony, steve, bruce, clark])
        w2.suggested_for.set([steve, clark])

        # Create Leaderboards
        Leaderboard.objects.create(team=marvel, points=200)
        Leaderboard.objects.create(team=dc, points=180)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data!'))
