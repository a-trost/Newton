sticker_csv = "badges/management/commands/stickerlist.csv"

# Full path to your django project directory
your_djangoproject_home = "/home/alex/newton/"
import django
from datetime import date
import sys, os
from os import listdir
import re

sys.path.append(your_djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newton.settings")

django.setup()
import random
from django.core.management.base import BaseCommand, CommandError
from brain.models import StudentRoster, CurrentClass, Classroom
from badges.models import Sticker
# from brain.scripts.webscrape import run_all_teachers
from ixl.models import IXLSkill, IXLSkillScores, IXLStats

import csv

STICKERS = ['monsterhigh2.png', 'everafterhigh3.png', 'legowolverine.png','donatello.png',
            'minion1.png', 'monsterhigh3.png', 'toad.png', 'legobatman.png', 'everafterhigh4.png', 'beastboy.png',
            'peach.png', 'anna.png', 'luigi.png', 'steve.png', 'elsa.png', 'mater.png', 'monsterhigh1.png',
            'legosuperman.png', 'henrydanger.png', 'r2d2.png', 'mickey.png', 'jake.png', 'blastoise.png',
            'pokeball.png', 'stormtrooper.png', 'minion3.png',  'everafterhigh1.png',
            'monsterhighlogo.png', 'minion2.png', 'yoshi.png', 'olaf.png', 'finn.png',
            'littleeinsteinsquincy.png', 'scoobydoo.png', 'bb8.png', 'spongebob.png', 'mike.png', 'everafterhigh2.png',
            'cyborg.png', 'squidward.png', 'legoblackpanther.png', 'patrick.png', 'clifford.png', 'baymax.png',
            'woody.png', 'simon.png', 'creeper.png', 'mariostar.png', 'legoblackwidow.png', 'anger.png',
            'mikey.png', 'darthvader.png', 'legospiderman.png', 'leonardo.png', 'pikachu.png', 'sully.png',
            'charizard.png', 'captainman.png', 'wildstyle.png', 'optimusprime.png',
            'alvin.png', 'benny.png', 'dory.png', 'nemo.png', 'curiousgeorge.png', 'raphael.png',
             'starlord.png', 'minnie.png', 'littleeinsteinsjune.png', 'lightingmcqueen.png',
            'buzzlightyear.png', 'bowser.png', 'legocaptainamerica.png', 'littleeinsteinsleo.png',
            'emmett.png', 'robin.png', 'theodore.png', 'legowonderwoman.png', 'mario.png', 'joy.png', 'moana.png', 'maui.png',
            'ninjagogreen.png','ninjagoblue.png','ninjagoblack.png','ninjagored.png',]


class Command(BaseCommand):
    help = 'Makes sticker objects for achievements'

    def add_arguments(self, parser):
        # add arguments here if you need some customization
        pass

    def handle(self, *args, **options):
        # Get the CSV into an object
        random.shuffle(STICKERS)
        dataReader = csv.reader(open(sticker_csv), delimiter=',', quotechar='"')
        # For row in the CSV, get name, slug, description
        for row in dataReader:
            if row[0] != 'name':  # Ignore the header row, import everything else
                name = row[0]
                slug = row[1]
                description = row[2]
                image = "static/images/stickers/{}".format(STICKERS.pop())
                category = row[3]
                order = row[4]
                obj, created = Sticker.objects.update_or_create(slug=slug,
                                                                defaults={'name': name, 'description': description,
                                                                          'image': image, 'category': category,
                                                                          'order': order, },
                                                                )

        print(STICKERS)
        # Leftovers: ['dory.png', 'leonardo.png', 'anger.png', 'toad.png', 'everafterhigh2.png', 'lightingmcqueen.png', 'pikachu.png', 'charizard.png']