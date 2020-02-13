export function getPlaidClient(onSuccess: (public_token: string, metadata: any) => void, onExit: (err: any, metadata: any) => void, onEvent: (eventName: any, metadata: any) => void): any  {
  //  @ts-ignore
  return window.Plaid.create({
    clientName: 'Stableins - Plaid',
    product: 'auth',
    env: process.env.VUE_APP_PLAID_ENV, 
    key: process.env.VUE_APP_PLAID_CLIENT_PUBLIC_KEY, 
    selectAccount: true,
    onExit,
    onEvent,
    onSuccess
  });
}

export function getStripeClient(): any {
  //  @ts-ignore
  return window.Stripe(process.env.VUE_APP_STRIPE_PUBLIC_KEY)
}