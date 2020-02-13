export interface StripeCharge {
  name?: string,
  email?: string,
  source?: string,
  cardId?: string
}

export interface StripeChargePayload {
  source: string
  card_id: string
  name: string 
}

export interface PlaidChargePayload {
  public_token: string,
  account_id: string,
}
