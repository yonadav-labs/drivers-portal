import { client } from '@/store/api'

import { format } from 'date-fns';

import { StripeChargePayload, PlaidChargePayload } from '@/@types/payment';
import { 
  QuoteProcess, QuoteProcessPayload, QuoteSoftFallout,
  QuoteProcessCalcVariations, QuoteProcessOptionsPayload, QuoteProcessOptions,
  QuoteProcessDocuments, QuoteProcessDocumentsAccidentReport,
  QuoteProcessPayment
  
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

/*
* Quote Process Documents
*/ 

export async function retrieveQuoteProcessDocuments(): Promise<QuoteProcessDocuments> {
  const response = await client.get(`quote/quote_process_documents/retrieve/`)
  return response.data
}

export async function updateQuoteProcessDocumentsFile(field:string, file: File | ''): Promise<QuoteProcessDocuments> {
  const formData = new FormData();
  formData.append(field, file)
  const response = await client.patch(`quote/quote_process_documents/upload_file/`, formData)
  return response.data
}

export async function updateQuoteProcessDocuments(payload: {is_submitted_for_review?: boolean, is_broker_of_record_signed?: boolean, phone?: string}): Promise<{ id: string, is_submitted_for_review: boolean, phone: string}> {
  const { is_submitted_for_review, is_broker_of_record_signed, phone } = payload;
  const response = await client.patch(`quote/quote_process_documents/update/`, { is_submitted_for_review, is_broker_of_record_signed, phone })
  return response.data
}


/*
* Quote Process Documents Accident Report
*/


export async function createQuoteProcessDocumentsAccidentReport(file: File): Promise<QuoteProcessDocumentsAccidentReport> {
  const formData = new FormData();
  formData.append('accident_report', file)
  const response = await client.post(`quote/quote_process_documents_accident_report/create/`, formData)
  return response.data
}

export async function updateQuoteProcessDocumentsAccidentReport(id:string, file: File): Promise<QuoteProcessDocumentsAccidentReport> {
  const formData = new FormData();
  formData.append('accident_report', file)
  const response = await client.put(`quote/quote_process_documents_accident_report/${id}/update/`, formData)
  return response.data
}

export async function deleteQuoteProcessDocumentsAccidentReport(id: string): Promise<void> {
  await client.delete(`quote/quote_process_documents_accident_report/${id}/delete/`)
}

/*
* Quote Process Payment
*/

export async function retrieveQuoteProcessPayment(): Promise<QuoteProcessPayment> {
  const response = await client.get(`quote/quote_process_payment/retrieve/`)
  return response.data
}

export async function payDepositStripe(charge: StripeChargePayload): Promise<any> {
  const response = await client.post(`/quote/quote_process_payment/pay/stripe/`, charge)
  return response.data
}

export async function payDepositPlaid(charge: PlaidChargePayload): Promise<any> {
  const response = await client.post(`/quote/quote_process_payment/pay/plaid/`, charge)
  return response.data
}