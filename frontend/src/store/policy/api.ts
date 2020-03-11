import { client } from '@/store/api'
import { PolicyList, PolicyDetail } from '@/@types/policy'
import { StripeChargePayload, PlaidChargePayload } from '@/@types/payment';


export async function listPolicies(): Promise<PolicyList[]> {
  const response = await client.get(`policy/list/`)
  return response.data
}

export async function retrievePolicy(id: string): Promise<PolicyDetail> {
  const response = await client.get(`policy/retrieve/${id}/`)
  return response.data
}

export async function payPaymentStripe({ id, charge}: {id: string, charge: StripeChargePayload}): Promise<any> {
  const response = await client.post(`policy/payment/${id}/pay/stripe/`, charge)
  return response.data
}

export async function payPaymentPlaid({ id, charge}: {id: string, charge: PlaidChargePayload}): Promise<any> {
  const response = await client.post(`policy/payment/${id}/pay/plaid/`, charge)
  return response.data
}
