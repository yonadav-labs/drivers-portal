export interface Policy {
  id: string,
  policy_number: string,
  certificate_of_liability: string,
  fh1_document: string,
  insurance_document: string,
  premium: number
}

export interface PolicyList extends Pick<Policy, 'id' | 'policy_number'> {}

export interface PolicyPayment {
  id: string,
  name: string,
  payment_date: Date | undefined,
  payment_due_date: Date,
  payment_amount: number,
  fee_amount: number,
  status: string,
  is_deposit: boolean,
  is_paid: boolean,
  stripe_fee: number,
  plaid_fee: number
}

export interface PolicyDetail extends Policy {
  payments: PolicyPayment[],
  tlc_number: string,
  vehicle_vin: string,
  license_plate: string,
  [key: string]: any
}