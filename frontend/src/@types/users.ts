import { QuoteStatus } from './quote'

export interface User {
  id: string,
  email: string, 
  has_usable_password: boolean,
  quote_status?: QuoteStatus,
  has_policy: boolean
}