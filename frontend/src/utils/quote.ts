const herefordFeeByDeposit:  Record<15 | 20 | 25, number> = {
  15: 30,
  20: 25,
  25: 20,
}

export function getHerefordFee(deposit: number): number {
  return herefordFeeByDeposit[deposit as 15 | 20 | 25] || 0
}