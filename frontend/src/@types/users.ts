import { QuoteStatus } from './quote'

export interface User {
  id: string,
  email: string, 
  has_usable_password: boolean,
  quoteprocess?: string,
  quote_status?: QuoteStatus,
  has_policy: boolean
}