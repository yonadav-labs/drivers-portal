export interface Policy {
  id: string,
  policy_number: string,
  certificate_of_liability: string,
  fh1_document: string,
  insurance_document: string,
}

export interface PolicyList extends Pick<Policy, 'id' | 'policy_number'> {}

export interface PolicyDetail extends Policy {
  tlc_number: string,
  vehicle_vin: string,
  license_plate: string,
}