import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models, transaction
from django.utils import timezone

from base.models import BaseModel
from payment.models import StripeCharge
from hellosign_app.models import HelloSignSignatureRequest
from hellosign_app.utils import create_t_and_c_signature_request
from quote.constants import (
    TLC_YEAR_INTERVAL_CHOICES, DMV_YEAR_INTERVAL_CHOICES, POINTS_CHOICES,
    QUOTE_PROCESS_DEPOSIT_CHOICES, QUOTE_PROCESS_DEDUCTIBLE_CHOICES,
    FAULT_ACCIDENTS_CHOICES, QUOTE_STATUS_CREATED, QUOTE_STATUS_CHOICES,
    QUOTE_STATUS_DOCS, ACCIDENTS_72_CHOICES, VEHICLE_OWNER_CHOICES,
    QUOTE_PROCESS_DEPOSIT_40
)
from quote.managers import QuoteProcessQuerySet
from quote.utils import (
  get_quote_status, get_hereford_fee)
from quote.quote_calc import get_quote_variations

# Create your models here.
class QuoteProcess(BaseModel):

    user = models.OneToOneField(
        verbose_name='User',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    base_type = models.ForeignKey(
      verbose_name='Base Type',
      to='importer.BaseType',
      on_delete=models.SET_NULL,
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

    # New questions
    vehicle_owner = models.CharField(
        verbose_name='Vehicle Owner',
        max_length=12,
        choices=VEHICLE_OWNER_CHOICES,
        null=True,
        blank=True
    )
    dash_cam = models.BooleanField(
        verbose_name='Dash Cam',
    )
    accidents_72_months = models.CharField(
        verbose_name='Accidents in last 72 months',
        max_length=3,
        choices=ACCIDENTS_72_CHOICES,
        null=True,
        blank=True
    )
    vehicle_is_hybrid = models.BooleanField(
        verbose_name='Vehicle is hybrid',
    )
    dwi_36_months = models.BooleanField(
      verbose_name='DWI or DUI violation within the past 36 months',
    )
    fault_accident_pedestrian = models.BooleanField(
      verbose_name='Fault accident w/ pedestrian/bicyclist 24 months',
    )
    speeding_violation =models.BooleanField(
      verbose_name='Speeding violation > 30 MPH within the last 24 months',
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
        verbose_name='Deposit (%)',
        choices=QUOTE_PROCESS_DEPOSIT_CHOICES,
        blank=True,
        null=True
    )
    deductible = models.PositiveIntegerField( 
        verbose_name='Physical Coverage ($)', # Phsyical Coverage
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

    is_hereford = models.BooleanField(
      verbose_name="Is Hereford",
      default=False
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
        self.user = user
        self._create_process_documents()
        self.update_status()
        self.save()
      
    def set_quote_variations(self):
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
          if settings.HELLOSIGN_ENABLED:
            hsr = create_t_and_c_signature_request(
              self.email,
              self.tlc_name,
              self.insurance_policy_number
            )
            QuoteProcessDocuments.objects.create(
              hsr=hsr,
              quote_process=self,
              requires_broker_of_record="hereford" in self.insurance_carrier_name.lower()
            )
          else:
            QuoteProcessDocuments.objects.create(
              quote_process=self,
              requires_broker_of_record=False
            )

    def _create_variations(self):
      with transaction.atomic():
        variations = self.variations
        if variations:
          variations.delete()
        variations = get_quote_variations(self)
        deductibles = variations.pop('deductible', {})
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
        'documents', instance.quote_process.user.email, 
        filename
    )
    
class QuoteProcessDocuments(BaseModel):
    quote_process = models.OneToOneField(
        verbose_name='Quote Process',
        to=QuoteProcess,
        on_delete=models.CASCADE
    )

    # Documents
    requires_broker_of_record = models.BooleanField(
        verbose_name='Require Broker of Record Change',
        default=False
    )
    is_broker_of_record_signed = models.BooleanField(
        verbose_name='Broker of Record Change',
        default=False
    )
    broker_record_file = models.FileField(
        verbose_name='Broker Record Signed',
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

    loss_run = models.FileField(
        verbose_name='Loss Run Document',
        upload_to=quote_process_document_upload_to,
        null=True,
        blank=True
    )

    vehicle_title = models.FileField(
        verbose_name='Vehicle Title or Bill of Sale or MV-50',
        upload_to=quote_process_document_upload_to,
        null=True,
        blank=True
    )

    base_letter = models.FileField(
        verbose_name='Base Letter',
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

    hsr = models.OneToOneField(
      verbose_name='HelloSign Request',
      to=HelloSignSignatureRequest,
      on_delete=models.SET_NULL,
      null=True,
      blank=True
    )

    doc_fields = [
        'dmv_license_front_side',
        'dmv_license_back_side',
        'tlc_license_front_side',
        'tlc_license_back_side',
        'base_letter',
        'proof_of_address',
        'defensive_driving_certificate'
    ]

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
      created = self._state.adding is True
      was_submitted = self.is_submitted_for_review
      
      super().save(*args, **kwargs)
      
      if created or (not was_submitted and self.is_submitted_for_review):
        self.quote_process.update_status()

    def get_documents_filled_count(self):
        acc = 0
        
        for doc in self.doc_fields:
            if getattr(self, doc, None):
                acc += 1
        return acc

    def get_minimum_accident_reports(self):
      return int(''.join(
        filter(
          lambda x: x.isdigit(), 
          self.quote_process.fault_accidents_last_months
        )
      ))

    def check_ready_for_review(self):
      broker_of_record_done = not self.requires_broker_of_record or \
        self.is_broker_of_record_signed

      has_dmv = self.dmv_license_front_side and self.dmv_license_back_side
      has_tlc = self.tlc_license_front_side and self.tlc_license_back_side
      hereford_docs = self.quote_process.is_hereford or \
        (self.loss_run and self.vehicle_title)

      return broker_of_record_done and has_dmv and has_tlc and \
        hereford_docs and \
        self.quoteprocessdocumentsaccidentreport_set.filter(
          accident_report__isnull=False
        ).count() >= self.get_minimum_accident_reports()

    def set_is_submitted_for_review(self):
      self.is_submitted_for_review = True
      self.save()
      self.quote_process.update_status()


def quote_process_document_accident_upload_to(instance, filename):
    return os.path.join(
        'documents', 'accidents', 
        instance.quote_process_documents.quote_process.user.email, 
        filename
    )

class QuoteProcessDocumentsAccidentReport(BaseModel):
    quote_process_documents = models.ForeignKey(
        verbose_name='Quote Process Documents',
        on_delete=models.CASCADE,
        to=QuoteProcessDocuments
    )

    accident_report = models.FileField(
        verbose_name='Accident Report',
        upload_to=quote_process_document_accident_upload_to,
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

    deposit_payment_amount = models.DecimalField(
        verbose_name='Deposit Payment Amount',
        max_digits=7,
        decimal_places=2
    )

    deposit_percentage = models.PositiveIntegerField(
        verbose_name='Deposit (%)',
        choices=QUOTE_PROCESS_DEPOSIT_CHOICES,
        blank=True,
        null=True
    )

    liability_amount = models.DecimalField(
      verbose_name='Liability Amount',
      help_text="Just in case you want to show the amount to the user",
      max_digits=7,
      decimal_places=2,
      blank=True,
      null=True
    )

    physical_amount = models.DecimalField(
      verbose_name='Physical Amount',
      help_text="Just in case you want to show the amount to the user",
      max_digits=7,
      decimal_places=2,
      blank=True,
      null=True
    )

    has_third_party_deposit = models.BooleanField(
      verbose_name='Has Third Party Deposit Coverage',
      default=False,
      choices=((True, "Yes"), (False, "No"))
    )

    third_party_name = models.CharField(
      verbose_name='Third Party Name',
      max_length=255,
      blank=True,
      null=True
    )

    third_party_amount = models.DecimalField(
      verbose_name='Third Party Covered Amount',
      max_digits=7,
      decimal_places=2,
      blank=True,
      null=True
    )

    payment_date = models.DateTimeField(
        verbose_name='Payment Date',
        null=True,
        blank=True
    )

    stripe_charge = models.OneToOneField(
      verbose_name='Stripe Charge',
      to=StripeCharge,
      on_delete=models.SET_NULL,
      null=True,
      blank=True
    )
  
    @property
    def is_paid(self):
      return self.payment_date

    def clean(self):
      errors = {}
      has_liability = self.liability_amount is not None
      has_physical = self.physical_amount is not None
      has_third_party_deposit = self.has_third_party_deposit

      if has_liability and not has_physical or has_physical and not has_liability:
        raise ValidationError("Both liability and phisical fields must be blank or set")
      
      if has_liability and has_physical:
        if (self.liability_amount + self.physical_amount) != self.official_hereford_quote:
          raise ValidationError("The sum of liability and physical must be equal to the official hereford quote")
      
      if has_third_party_deposit:
        if not self.third_party_name:
          errors["third_party_name"] = "This field is required."
        if not self.third_party_amount:
          errors["third_party_amount"] = "This field is required."
        elif self.deposit_payment_amount - self.third_party_amount < 0:
          errors["third_party_amount"] = "Amount cannot be greater than deposit amount."
      
      if len(errors) > 0:
        raise ValidationError(errors)

    def save(self, *args, **kwargs):
      created = self._state.adding is True
      if not created:
        was_paid = QuoteProcessPayment.objects.get(id=self.pk).is_paid
      else:
        was_paid = False
      
      super().save(*args, **kwargs)
      print(was_paid, not was_paid and self.is_paid)
      
      if created or (not was_paid and self.is_paid):
        self.quote_process.update_status()

    def mark_as_paid(self, charge):
      self.stripe_charge = charge
      self.payment_date = timezone.now()
      self.save()
      self.quote_process.update_status()

    def get_monthly_payment(self):
      deposit = self.deposit_percentage or self.quote_process.deposit
      months = 2 if deposit == QUOTE_PROCESS_DEPOSIT_40 else 9
      return (float(self.official_hereford_quote) * (1-(deposit/100)))/months

    def get_hereford_fee(self):
      deposit = self.deposit_percentage or self.quote_process.deposit
      return get_hereford_fee(deposit)

    def get_deposit(self):
      deposit = self.deposit_percentage or self.quote_process.deposit
      total_deposit = float(self.official_hereford_quote) * (deposit/100)
      if self.third_party_amount:
        return total_deposit - float(self.third_party_amount)
      else:
        return total_deposit

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
