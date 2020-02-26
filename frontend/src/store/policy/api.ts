import { client } from '@/store/api'
import { PolicyList, PolicyDetail } from '@/@types/policy'


export async function listPolicies(): Promise<PolicyList[]> {
  const response = await client.get(`policy/list/`)
  return response.data
}

export async function retrievePolicy(id: string): Promise<PolicyDetail> {
  const response = await client.get(`policy/retrieve/${id}/`)
  return response.data
}