import { client } from '@/store/api'

export async function checkEmailExists(email: string): Promise<{ email: string }> {
  const response = await client.get(`users/${email}/exists`)
  return response.data
}