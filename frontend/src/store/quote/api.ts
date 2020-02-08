import { client } from '@/store/api'

import { format } from 'date-fns';

import { 
  QuoteProcess, QuoteProcessPayload, QuoteSoftFallout,
  QuoteProcessCalcVariations, QuoteProcessOptionsPayload, QuoteProcessOptions,
  
 } from '@/@types/quote';

export async function createQuoteProcess(data: QuoteProcessPayload): Promise<QuoteProcess> {
  const response = await client.post(`quote/quote_process/create/`, data)
  return response.data
}

export async function retrieveQuoteProcessById(id: string): Promise<QuoteProcess> {
  const response = await client.get(`quote/quote_process/${id}/`)
  return response.data
}

export async function retrieveCalcQuoteProcessVariations(id: string): Promise<QuoteProcessCalcVariations> {
  const response = await client.get(`quote/quote_process/${id}/calc_variations/`)
  return response.data
}

export async function updateQuoteProcess(email: string, data: QuoteProcessPayload): Promise<QuoteProcess> {
  const response = await client.patch(`quote/quote_process/${email}/`, data)
  return response.data
}

export async function updateQuoteProcessOptions(id: string, data: QuoteProcessOptionsPayload): Promise<QuoteProcessOptions> {
  const response = await client.patch(`quote/quote_process/${id}/update_options/`, {
    ...data,
    start_date: format(new Date(data.start_date), 'yyyy-MM-dd')
  })
  return response.data
}

export async function updateQuoteProcessUser(id: string, email: string): Promise<{ email: string, magic_link: string}> {
  const response = await client.patch(`quote/quote_process/${id}/update_user/`, { email })
  return response.data
}


/*
* Quote Soft Fallout
*/

export async function createQuoteSoftFallout(data: QuoteSoftFallout): Promise<QuoteSoftFallout> {
  const response = await client.post(`quote/quote_soft_fallout/create/`, data)
  return response.data
}