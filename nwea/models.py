from datetime import date
from django.db import models

from brain.models import StudentRoster


class RITBand(models.Model):
    ALGEBRA = 1
    NUMBER = 2
    MEASUREMENT = 3
    GEOMETRY = 4

    DOMAIN_CHOICES = (
        (ALGEBRA, 'Operations and Algebraic Thinking'),
        (NUMBER, 'Number and Operations'),
        (MEASUREMENT, 'Measurement and Data'),
        (GEOMETRY, 'Geometry'),)

    PROBLEM = 1
    PATTERN = 2
    PLACEVALUE = 3
    BASE_TEN = 4
    FRACTIONS = 5
    MEASUREMENT_SUB = 6
    DATA = 7
    SHAPES = 8

    SUBDOMAIN_CHOICES = (
        (PROBLEM, 'Represent and Solve Problems'),
        (PATTERN, 'Analyze Patterns and Relationships'),
        (PLACEVALUE, 'Understand Place Value, Counting, and Cardinality'),
        (BASE_TEN,'Number and Operations in Base Ten'),
        (FRACTIONS, 'Number and Operations - Fractions'),
        (MEASUREMENT_SUB, 'Geometric Measurement and Problem Solving'),
        (DATA, 'Represent and Interpret Data'),
        (SHAPES, 'Reason with Shapes Attributes, & Coordinate Plane'),
    )
    RIT_CHOICES = (
        (111, '111'),
        (121, '121'),
        (131, '131'),
        (141, '141'),
        (151, '151'),
        (161, '161'),
        (171, '171'),
        (181, '181'),
        (191, '191'),
        (201, '201'),
        (211, '211'),
        (221, '221'),
        (231, '231'),
        (241, '241'),
    )

    domain = models.CharField(choices=DOMAIN_CHOICES,max_length=255 )
    subdomain = models.CharField(choices=SUBDOMAIN_CHOICES, max_length=255)
    rit_band = models.PositiveIntegerField(choices=RIT_CHOICES, default=151)

    def __str__(self):
        return 'Domain: {}, SubDomain: {}, Band: {}'.format(self.domain, self.subdomain, self.rit_band)

    class Meta:
        verbose_name = 'RIT Band'
        verbose_name_plural = 'RIT Bands'
        ordering = ['domain', 'subdomain', 'rit_band']


class NWEASkill(models.Model):
    rit_band = models.ForeignKey(RITBand, on_delete=models.CASCADE)
    skill = models.CharField(max_length=255)
    ixl_match = models.CharField(max_length=7, blank=True)

    def __str__(self):
        output = 'Dom: {} Sub: {} RIT: {} Skill: {}'.format(self.rit_band.domain,
                                                            self.rit_band.subdomain,
                                                            self.rit_band.rit_band,
                                                            self.skill)
        if self.ixl_match:
            output = output + ', IXL Match: ' + self.ixl_match
        return output

    class Meta:
        verbose_name = 'NWEA Skill'
        verbose_name_plural = 'NWEA Skills'
        ordering = ['rit_band', 'skill']


class NWEAScore(models.Model):
    FALL = 1
    WINTER = 2
    SPRING = 3

    FOURTEEN = '14-15'
    FIFTEEN = '15-16'
    SIXTEEN = '16-17'
    SEVENTEEN = '17-18'
    EIGHTEEN = '18-19'
    NINETEEN = '19-20'
    TWENTY = '20-21'
    TWENTYONE = '21-22'

    SESSION_CHOICES = (
        (FALL, 'Fall'),
        (WINTER, 'Winter'),
        (SPRING, 'Spring'),
    )

    YEAR_CHOICES = (
        (FOURTEEN, '14-15'),
        (FIFTEEN, '15-16'),
        (SIXTEEN, '16-17'),
        (SEVENTEEN, '17-18'),
        (EIGHTEEN, '18-19'),
        (NINETEEN, '19-20'),
        (TWENTY, '20-21'),
        (TWENTYONE, '21-22'),
    )


    student = models.ForeignKey(StudentRoster, on_delete=models.CASCADE)
    year = models.CharField(max_length=50, choices=YEAR_CHOICES, default=SEVENTEEN)
    season = models.CharField(max_length=50, choices=SESSION_CHOICES, default=FALL)
    subdomain1 = models.IntegerField(verbose_name="SubDomain 1")
    subdomain2 = models.IntegerField(verbose_name="SubDomain 2")
    subdomain3 = models.IntegerField(verbose_name="SubDomain 3")
    subdomain4 = models.IntegerField(verbose_name="SubDomain 4")
    subdomain5 = models.IntegerField(verbose_name="SubDomain 5")
    subdomain6 = models.IntegerField(verbose_name="SubDomain 6")
    subdomain7 = models.IntegerField(verbose_name="SubDomain 7")
    subdomain8 = models.IntegerField(verbose_name="SubDomain 8")


    def __str__(self):
        scores = ("{}, {}, {}, {}, {}, {}, {}, {}".format(self.subdomain1, self.subdomain2, self.subdomain3, self.subdomain4, self.subdomain5, self.subdomain6, self.subdomain7, self.subdomain8))
        return '{} {}: {} {} - {}'.format(self.student.first_name, self.student.last_name, self.season, self.year, scores)

    class Meta:
        verbose_name = 'NWEA Math Breakdown'
        verbose_name_plural = 'NWEA Math Breakdowns'
        unique_together = ("student", "year", "season")

class NWEAAverage(models.Model):
    FALL = 1
    WINTER = 2
    SPRING = 3

    FOURTEEN = '14-15'
    FIFTEEN = '15-16'
    SIXTEEN = '16-17'
    SEVENTEEN = '17-18'
    EIGHTEEN = '18-19'
    NINETEEN = '19-20'
    TWENTY = '20-21'
    TWENTYONE = '21-22'

    SESSION_CHOICES = (
        (FALL, 'Fall'),
        (WINTER, 'Winter'),
        (SPRING, 'Spring'),
    )

    YEAR_CHOICES = (
        (FOURTEEN, '14-15'),
        (FIFTEEN, '15-16'),
        (SIXTEEN, '16-17'),
        (SEVENTEEN, '17-18'),
        (EIGHTEEN, '18-19'),
        (NINETEEN, '19-20'),
        (TWENTY, '20-21'),
        (TWENTYONE, '21-22'),
    )

    student = models.ForeignKey(StudentRoster, on_delete=models.CASCADE)
    year = models.CharField(max_length=50, choices=YEAR_CHOICES, default=SIXTEEN)
    math_fall = models.IntegerField(blank=True, null=True)
    reading_fall = models.IntegerField(blank=True, null=True)
    lexile_fall = models.IntegerField(blank=True, null=True)
    math_winter = models.IntegerField(blank=True, null=True)
    reading_winter = models.IntegerField(blank=True, null=True)
    lexile_winter = models.IntegerField(blank=True, null=True)
    math_spring = models.IntegerField(blank=True, null=True)
    reading_spring = models.IntegerField(blank=True, null=True)
    lexile_spring = models.IntegerField(blank=True, null=True)

class NWEAGoal(models.Model):
    FOURTEEN = '14-15'
    FIFTEEN = '15-16'
    SIXTEEN = '16-17'
    SEVENTEEN = '17-18'
    EIGHTEEN = '18-19'
    NINETEEN = '19-20'
    TWENTY = '20-21'
    TWENTYONE = '21-22'

    YEAR_CHOICES = (
        (FOURTEEN, '14-15'),
        (FIFTEEN, '15-16'),
        (SIXTEEN, '16-17'),
        (SEVENTEEN, '17-18'),
        (EIGHTEEN, '18-19'),
        (NINETEEN, '19-20'),
        (TWENTY, '20-21'),
        (TWENTYONE, '21-22'),
    )

    student = models.ForeignKey(StudentRoster, on_delete=models.CASCADE)
    year = models.CharField(max_length=50, choices=YEAR_CHOICES, default=SIXTEEN)
    math_winter = models.IntegerField(blank=True, null=True)
    math_spring = models.IntegerField(blank=True, null=True)
    reading_winter = models.IntegerField(blank=True, null=True)
    reading_spring = models.IntegerField(blank=True, null=True)