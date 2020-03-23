const herefordFeeByDeposit:  Record<15 | 20 | 25 | 40 | 100, number> = {
  15: 30,
  20: 25,
  25: 20,
  40: 45,
  100: 0
}

const monthsByDeposit: Record<15 | 20 | 25 | 40 | 100, number> = {
  15: 9,
  20: 9,
  25: 9,
  40: 2,
  100: 1 // It should be 0, but we are counting one to avoid divisons by 0
}

export function getHerefordFee(deposit: number): number {
  return herefordFeeByDeposit[deposit as 15 | 20 | 25 | 40 | 100] || 0
}

export function getPaymentsByDeposit(deposit: number): number {
  return monthsByDeposit[deposit as 15 | 20 | 25 | 40 | 100] || 0
}