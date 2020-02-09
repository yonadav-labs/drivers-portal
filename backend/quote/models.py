import os

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models, transaction

from base.models import BaseModel

from quote.constants import (
    TLC_YEAR_INTERVAL_CHOICES, DMV_YEAR_INTERVAL_CHOICES, POINTS_CHOICES,
    QUOTE_PROCESS_DEPOSIT_CHOICES, QUOTE_PROCESS_DEDUCTIBLE_CHOICES,
    FAULT_ACCIDENTS_CHOICES, QUOTE_STATUS_CREATED, QUOTE_STATUS_CHOICES,
    QUOTE_STATUS_DOCS
)
from quote.managers import QuoteProcessQuerySet
from quote.utils import generate_variations, get_quote_status

# Create your models here.
class QuoteProcess(BaseModel):

    user = models.OneToOneField(
        verbose_name='User',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    # Step 1
    tlc_number = models.CharField(
        verbose_name='TLC #',
        max_length=7
    )
    tlc_name = models.CharField(
        verbose_name='TLC Name',
        max_length=255
    )

    # Step 2
    vehicle_vin = models.CharField(
        verbose_name='VIN #',
        max_length=17
    )
    vehicle_owner = models.CharField(
        verbose_name='Vehicle Owner',
        max_length=255
    )
    license_plate = models.CharField(
        verbose_name='License Plate #',
        max_length=20
    )
    base_name = models.CharField(
        verbose_name='Base Name',
        max_length=511
    )
    base_number = models.CharField(
        verbose_name='Base Number',
        max_length=6
    )
    base_type = models.CharField(
        verbose_name='Base Type',
        max_length=255,
        blank=True,
        null=True
    )
    vehicle_year = models.PositiveIntegerField(
        verbose_name='Vehicle Year',
        validators=[RegexValidator('^[1,2][0,9]\d{2}$')]
    )
    vehicle_weight = models.CharField(
        verbose_name='Vehicle Weight',
        max_length=8,
        null=True,
        blank=True
    )
    is_clean_air_vehicle = models.BooleanField(
        verbose_name='Is Clean air vehicle',
        blank=True,
        null=True
    )
    insurance_carrier_name = models.CharField(
        verbose_name='Insurance Carrier Name',
        max_length=255
    )
    insurance_policy_number = models.CharField(
        verbose_name='Policy Number',
        max_length=255
    )
    
    # Question Steps
    tlc_license_years = models.CharField(
        verbose_name='How long TLC License',
        max_length=3,
        choices=TLC_YEAR_INTERVAL_CHOICES
    )

    dmv_license_years = models.CharField(
        verbose_name='How long DMV License',
        max_length=3,
        choices=DMV_YEAR_INTERVAL_CHOICES
    )
    driver_points_last_months = models.CharField(
        verbose_name='Driver points in last 36 months',
        max_length=4,
        choices=POINTS_CHOICES
    )
    fault_accidents_last_months = models.CharField(
        verbose_name='Fault accidents in last 36 months',
        max_length=2,
        choices=FAULT_ACCIDENTS_CHOICES
    )
    defensive_driving_certificate = models.BooleanField(
        verbose_name='Defensive driving certificate',
    )
    accident_avoidance_system = models.BooleanField(
        verbose_name='Accident avoidance system',
    )

    # Step 4
    email = models.EmailField(
        verbose_name='Email'
    )

    # Step 5
    quote_amount = models.DecimalField(
        verbose_name='Quote Amount',
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True
    )
    deposit = models.PositiveIntegerField(
        verbose_name='Deposit',
        choices=QUOTE_PROCESS_DEPOSIT_CHOICES,
        blank=True,
        null=True
    )
    deductible = models.PositiveIntegerField( 
        verbose_name='Physical Coverage', # Phsyical Coverage
        choices=QUOTE_PROCESS_DEDUCTIBLE_CHOICES,
        blank=True,
        null=True
    )
    start_date = models.DateField(
        verbose_name="Start date",
        blank=True,
        null=True
    )
    status = models.CharField(
      max_length=7,
      choices=QUOTE_STATUS_CHOICES,
      default=QUOTE_STATUS_CREATED
    )

    objects = QuoteProcessQuerySet.as_manager()

    class Meta:
        verbose_name = 'Quote Process'
        verbose_name_plural = 'Quote Processes'
        ordering = ('-created', )
    
    def __str__(self):
        return f'Quote Process TLC #{self.tlc_number}. {self.tlc_name}'

    @property
    def quote_process_documents(self):
       return getattr(self, 'quoteprocessdocuments', None)

    @property
    def quote_process_payment(self):
       return getattr(self, 'quoteprocesspayment', None)

    @property
    def quote_policy(self):
      return getattr(self, 'policy', None)

    @property
    def is_ready_for_user(self):
      return self.deposit and self.start_date

    @property
    def variations(self):
      return getattr(self, 'quoteprocessvariations', None)

  
    def add_user(self, user):
        if self.is_ready_for_user:
          self.user = user
          self._create_process_documents()
          self.update_status()
          self.save()
      
    def set_quote_variations(self):
      if self.is_ready_for_user:
          self._create_variations()
          variations = self.variations

          if variations:
            self.quote_amount = self.quoteprocessvariations.liability_total
            
            if variations.physical_total:
              self.quote_amount += variations.physical_total
            self.save()

    def set_quote_status(self, status):
      self.status = status
      self.save()

    def update_status(self):
      status = get_quote_status(self)
      if not status == self.status:
        self.set_quote_status(status)


    def _create_process_documents(self):
        if not self.quote_process_documents:
          QuoteProcessDocuments.objects.create(
              quote_process=self
          )

    def _create_variations(self):
      with transaction.atomic():
        variations = self.variations
        if variations:
          variations.delete()
        if self.deposit:
          variations = generate_variations(self)
          deductibles = variations.pop('deductible')
          deductible_data = deductibles[self.deductible] if self.deductible \
            else {}
          QuoteProcessVariations.objects.create(
            quote_process=self,
            **{
              **variations,
              **deductible_data
            }
          )


def quote_process_document_upload_to(instance, filename):
    return os.path.join(
        'quote_process_documents', instance.email, str(instance.id), filename)
    
class QuoteProcessDocuments(BaseModel):
    quote_process = models.OneToOneField(
        verbose_name='Quote Process',
        to=QuoteProcess,
        on_delete=models.CASCADE
    )

    # Documents
    broker_of_record = models.FileField(
        verbose_name='Broker of Record Change',
        upload_to=quote_process_document_upload_to,
        null=True,
        blank=True
    )
    dmv_license_front_side = models.FileField(
        verbose_name='DMV License Front Side',
        upload_to=quote_process_document_upload_to,
        null=True,
        blank=True
    )
    
    dmv_license_back_side = models.FileField(
        verbose_name='DMV License Back Side',
        upload_to=quote_process_document_upload_to,
        null=True,
        blank=True
    )

    tlc_license_front_side = models.FileField(
        verbose_name='DMV License Front Side',
        upload_to=quote_process_document_upload_to,
        null=True,
        blank=True
    )

    tlc_license_back_side = models.FileField(
        verbose_name='TLC License Back Side',
        upload_to=quote_process_document_upload_to,
        null=True,
        blank=True
    )
    
    proof_of_address = models.FileField(
        verbose_name='Proof of Address',
        upload_to=quote_process_document_upload_to,
        null=True,
        blank=True
    )

    defensive_driving_certificate = models.FileField(
        verbose_name='Defensive Driving Certificate',
        upload_to=quote_process_document_upload_to,
        null=True,
        blank=True
    )

    is_submitted_for_review = models.BooleanField(
        verbose_name='Submmited for review',
        default=False
    )

    class Meta:
        verbose_name = 'Quote Process Documents'
        verbose_name_plural = 'Quote Process Documents'
        ordering = ('-created', )
    
    def __str__(self):
        return (
            'Quote Process Documents for #'
            f'{self.quote_process.tlc_number}. {self.quote_process.tlc_name}'
        )

    def save(self, *args, **kwargs):
      created = not self.pk
      was_submitted = self.is_submitted_for_review
      
      super().save(*args, **kwargs)
      
      if created or (not was_submitted and self.is_submitted_for_review):
        self.quote_process.update_status()

    def get_documents_filled_count(self):
        acc = 0
        doc_fields = [
            'broker_of_record',
            'dmv_license_front_side',
            'dmv_license_back_side',
            'tlc_license_front_side',
            'tlc_license_back_side',
            'proof_of_address',
            'defensive_driving_certificate'
        ]
        for doc in doc_fields:
            if getattr(self, doc, None):
                acc += 1
        return acc

class QuoteProcessDocumentsAciddentReport(BaseModel):
    quote_process_documents = models.ForeignKey(
        verbose_name='Quote Process Documents',
        on_delete=models.CASCADE,
        to=QuoteProcessDocuments
    )

    defensive_driving_certificate = models.FileField(
        verbose_name='Accident Report',
        upload_to=quote_process_document_upload_to,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Quote Process Documents Accident Report'
        verbose_name_plural = 'Quote Process Documents Accident Report'
        ordering = ('-created', )


class QuoteProcessPayment(BaseModel):
    quote_process = models.OneToOneField(
        verbose_name='Quote Process',
        to=QuoteProcess,
        on_delete=models.CASCADE,
    )

    official_hereford_quote = models.DecimalField(
        verbose_name='Official Hereford Quote',
        max_digits=7,
        decimal_places=2
    )

    payment_date = models.DateTimeField(
        verbose_name='Payment Date',
        null=True,
        blank=True
    )
  
    @property
    def is_paid(self):
      return self.payment_date

    def save(self, *args, **kwargs):
      created = not self.pk
      was_paid = self.is_paid
      
      super().save(*args, **kwargs)
      
      if created or (not was_paid and self.is_paid):
        self.quote_process.update_status()

    class Meta:
        verbose_name = 'Quote Process Payment'
        verbose_name_plural = 'Quote Process Payment'


class QuoteProcessVariations(BaseModel):
  quote_process = models.OneToOneField(
    verbose_name='Quote Process',
    to=QuoteProcess,
    on_delete=models.CASCADE,
  )

  liability_total = models.DecimalField(
    verbose_name='Liability total',
    max_digits=7,
    decimal_places=2
  )
  body_injury = models.DecimalField(
    verbose_name='Body injury',
    max_digits=7,
    decimal_places=2
  )
  property_damage = models.DecimalField(
    verbose_name='Property damage',
    max_digits=7,
    decimal_places=2
  )
  personal_injury_protection = models.DecimalField(
    verbose_name='Personal injury protection',
    max_digits=7,
    decimal_places=2
  )
  aditional_personal_injury_protection = models.DecimalField(
    verbose_name='Aditional personal injury protection',
    max_digits=7,
    decimal_places=2
  )
  uninsured_motorist = models.DecimalField(
    verbose_name='Uninsured motorist',
    max_digits=7,
    decimal_places=2
  )
  physical_total = models.DecimalField(
    verbose_name='Physical total',
    max_digits=7,
    decimal_places=2,
    blank=True,
    null=True
  )
  physical_comprehensive = models.DecimalField(
    verbose_name='Physical comprehensive',
    max_digits=7,
    decimal_places=2,
    blank=True,
    null=True
  )
  physical_collision = models.DecimalField(
    verbose_name='Physical collision',
    max_digits=7,
    decimal_places=2,
    blank=True,
    null=True
  )

  class Meta:
    verbose_name = "Quote Process Variations"
    verbose_name_plural = "Quote Process Variations"

  def __str__(self):
    return f"Quote Process Variations for {self.quote_process.email}"

class QuoteSoftFallout(BaseModel):
  name = models.CharField(
      verbose_name='Name',
      max_length=255
  )

  phone_number = models.CharField(
      verbose_name='Phone Number',
      max_length=255,
      blank=True,
      null=True
  )

  email = models.EmailField(
      verbose_name='Email'
  )

  class Meta:
    verbose_name = "Quote Soft Fallout"
    verbose_name_plural = "Quote Soft Fallouts"
    ordering = ('-created', )