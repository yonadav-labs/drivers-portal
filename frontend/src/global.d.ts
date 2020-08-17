export { }
declare global {
  interface Window { Plaid: { create: (payload: any) => any }, Stripe: any, EF: any }
}