import { client } from '@/store/api'

import { QuoteProcess, QuoteProcessPayload } from '@/@types/quote';

export async function createQuoteProcess(data: QuoteProcessPayload): Promise<QuoteProcess> {
  const response = await client.post(`quote/quote_process/create/`, data)
  return response.data
}

export async function retrieveQuoteProcessById(id: string): Promise<QuoteProcess> {
  const response = await client.get(`quote/quote_process/${id}/`)
  return response.data
}

export async function updateQuoteProcess(email: string, data: QuoteProcessPayload): Promise<QuoteProcess> {
  const response = await client.patch(`quote/quote_process/${email}/`, data)
  return response.data
}