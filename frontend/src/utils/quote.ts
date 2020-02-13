const herefordFeeByDeposit:  Record<15 | 20 | 25 | 40, number> = {
  15: 30,
  20: 25,
  25: 20,
  40: 45,
}

const monthsByDeposit: Record<15 | 20 | 25 | 40, number> = {
  15: 9,
  20: 9,
  25: 9,
  40: 3,
}

export function getHerefordFee(deposit: number): number {
  return herefordFeeByDeposit[deposit as 15 | 20 | 25 | 40] || 0
}

export function getPaymentsByDeposit(deposit: number): number {
  return monthsByDeposit[deposit as 15 | 20 | 25 | 40] || 0
}