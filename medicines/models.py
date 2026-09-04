from django.db import models

class Medicine(models.Model):
    class Category(models.TextChoices):
        ANALGESIC = "analgesic", "Analgesic"
        ANTIBIOTIC = "antibiotic", "Antibiotic"
        ANTIPYRETIC = "antipyretic", "Antipyretic"
        ANTIHISTAMINE = "antihistamine", "Antihistamine"
        ANTI_INFLAMMATORY = "anti_inflammatory", "Anti-inflammatory"
        ANTACID = "antacid", "Antacid"
        ANTIVIRAL = "antiviral", "Antiviral"
        ANTIFUNGAL = "antifungal", "Antifungal"
        ANTIPARASITIC = "antiparasitic", "Antiparasitic"
        ANTIDIABETIC = "antidiabetic", "Antidiabetic"
        ANTIHYPERTENSIVE = "antihypertensive", "Antihypertensive"
        CARDIOVASCULAR = "cardiovascular", "Cardiovascular"
        RESPIRATORY = "respiratory", "Respiratory"
        GASTROINTESTINAL = "gastrointestinal", "Gastrointestinal"
        DERMATOLOGICAL = "dermatological", "Dermatological"
        VITAMIN_SUPPLEMENT = "vitamin_supplement", "Vitamin & Supplement"
        HORMONAL = "hormonal", "Hormonal"
        VACCINE = "vaccine", "Vaccine"
        OTHER = "other", "Other"

    class Unit(models.TextChoices):
        TABLET = "tablet", "Tablet"
        CAPSULE = "capsule", "Capsule"
        BOTTLE = "bottle", "Bottle"
        TUBE = "tube", "Tube"
        VIAL = "vial", "Vial"
        AMPULE = "ampoule", "Ampoule"
        SACHET = "sachet", "Sachet"
        PACK = "pack", "Pack"
        STRIP = "strip", "Strip"
        PIECE = "piece", "Piece"
        ROLL = "roll", "Roll"
        OTHER = "other", "Other"

    name = models.CharField(max_length=50)
    generic_name = models.CharField(max_length=100)
    category = models.CharField(choices=Category.choices, default=Category.ANALGESIC)
    unit = models.CharField(choices=Unit.choices, default=Unit.TABLET)
    manufacturer = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class PharmacyStock(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    expiary_date = models.DateField()
    reorder_level = models.IntegerField()
    updated_at = models.DateTimeField(auto_now_add=True)

