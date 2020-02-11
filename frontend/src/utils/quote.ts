const herefordFeeByDeposit:  Record<15 | 20 | 25, number> = {
  15: 30,
  20: 25,
  25: 20,
}

export function getHerefordFee(deposit: 15 | 20 | 25): number {
  return herefordFeeByDeposit[deposit]
}