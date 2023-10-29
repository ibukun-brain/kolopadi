from django.db import models


class Gender(models.TextChoices):
    Male = ("Male", "Male")
    Female = ("Female", "Female")
    Other = ("Other", "Other")


class TransactionType(models.TextChoices):
    Debit = ("D", "Debit")
    Credit = ("C", "Credit")
    AirtimeRecharge = ("Airtime Recharge", "Airtime Recharge")
    DataServices = ("Data Services", "Data Services")
    TvSubscription = ("Tv Subscription", "Tv Subscription")


class VTPassTransactionStatus(models.TextChoices):
    Initiated = ("initiated", "Initiated")
    Delivered = ("delivered", "Delivered")
    Pending = ("pending", "Pending")


class TransferStatus(models.TextChoices):
    Success = ("SUCCESSFUL", "SUCCESSFUL")
    Failed = ("FAILED", "FAILED")
    Pending = ("PENDING", "PENDING")


class IdentityType(models.TextChoices):
    NIN = ("National Identification Number", "National Identification Number")
    Passport = ("Passport", "Passport")
    DrivingLicense = ("Driving License", "Driving License")
    VoterCard = ("Voter Card", "Voter Card")


class Status(models.TextChoices):
    Pending = ("Pending", "Pending")
    Verified = ("Verified", "Verified")
    Failed = ("Failed", "Failed")
