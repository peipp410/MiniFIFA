from django.db import models


class player(models.Model):
    ID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=255)


class playerBasic(models.Model):
    ID = models.IntegerField(primary_key=True)
    Age = models.IntegerField()
    Height = models.IntegerField()
    Weight = models.IntegerField()
    Nationality = models.CharField(max_length=255)
    Positions = models.CharField(max_length=255)
    Club = models.CharField(max_length=255)


class playerClub(models.Model):
    ID = models.IntegerField(primary_key=True)
    Club = models.CharField(max_length=255)
    ClubNumber = models.IntegerField()
    ClubJoined = models.IntegerField()

    class Meta:
        unique_together = ('ID', 'Club')


class playerPhoto(models.Model):
    ID = models.IntegerField(primary_key=True)
    PhotoUrl = models.CharField(max_length=255)


class playerModel(models.Model):
    ID = models.IntegerField(primary_key=True)
    PaceTotal = models.IntegerField()
    ShootingTotal = models.IntegerField()
    PassingTotal = models.IntegerField()
    DribblingTotal= models.IntegerField()
    DefendingTotal = models.IntegerField()
    PhysicalityTotal = models.IntegerField()
    Overall = models.IntegerField()
    Potential = models.IntegerField()


class playerDisplay(models.Model):
    ID = models.IntegerField(primary_key=True)
    Crossing = models.IntegerField()
    Finishing = models.IntegerField()
    HeadingAccuracy = models.IntegerField()
    ShortPassing = models.IntegerField()
    Volleys = models.IntegerField()
    Dribbling = models.IntegerField()
    Curve = models.IntegerField()
    FKAccuracy = models.IntegerField()
    LongPassing = models.IntegerField()
    BallControl = models.IntegerField()
    Acceleration = models.IntegerField()
    SprintSpeed = models.IntegerField()
    Agility = models.IntegerField()
    Reactions = models.IntegerField()
    Balance = models.IntegerField()
    ShotPower = models.IntegerField()
    Jumping = models.IntegerField()
    Stamina = models.IntegerField()
    Strength = models.IntegerField()
    LongShots = models.IntegerField()
    Aggression = models.IntegerField()
    Interceptions = models.IntegerField()
    Positioning = models.IntegerField()
    Vision = models.IntegerField()
    Penalties = models.IntegerField()
    Composure = models.IntegerField()
    Marking = models.IntegerField()
    StandingTackle = models.IntegerField()
    SlidingTackle = models.IntegerField()
    GKDiving = models.IntegerField()
    GKHandling = models.IntegerField()
    GKKicking = models.IntegerField()
    GKPositioning = models.IntegerField()
    GKReflexes = models.IntegerField()


class playerDetail(models.Model):
    ID = models.IntegerField(primary_key=True)
    FullName = models.CharField(max_length=255)
    ValueEUR = models.IntegerField()
    WageEUR = models.IntegerField()
    ClubPosition = models.CharField(max_length=255)
    ClubNumber = models.IntegerField()
    NationalTeam = models.CharField(max_length=255)
    PreferredFoot = models.CharField(max_length=255)
    IntReputation = models.IntegerField()
    AttackingWorkRate = models.CharField(max_length=255)
    DefensiveWorkRate = models.CharField(max_length=255)


class playerRating(models.Model):
    ID = models.IntegerField(primary_key=True)
    STRating = models.IntegerField()
    LWRating = models.IntegerField()
    LFRating = models.IntegerField()
    CFRating = models.IntegerField()
    RFRating = models.IntegerField()
    RWRating = models.IntegerField()
    CAMRating = models.IntegerField()
    LMRating = models.IntegerField()
    CMRating = models.IntegerField()
    RMRating = models.IntegerField()
    LWBRating = models.IntegerField()
    CDMRating = models.IntegerField()
    RWBRating = models.IntegerField()
    LBRating = models.IntegerField()
    CBRating = models.IntegerField()
    RBRating = models.IntegerField()
    GKRating = models.IntegerField()


class clubBasic(models.Model):
    Club = models.CharField(primary_key=True, max_length=255)
    League = models.CharField(max_length=255)
    LeagueId = models.IntegerField()
    Overall = models.IntegerField()
    Attack = models.IntegerField()
    Midfield = models.IntegerField()
    Defence = models.IntegerField()
    TransferBudget = models.IntegerField()
    DomesticPrestige = models.IntegerField()
    IntPrestige = models.IntegerField()
    Players = models.IntegerField()
    StartingAverageAge = models.DecimalField(max_digits=5, decimal_places=2)
    AllTeamAverageAge = models.DecimalField(max_digits=5, decimal_places=2)


class clubPhoto(models.Model):
    Club = models.CharField(primary_key=True, max_length=255)
    club_logo_url = models.CharField(max_length=255)
