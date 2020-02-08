
export function capitalize(name: string): string {
  return name.split(',').map(x => x.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join(' ')).join(', ')
}

export function currency(value: number): string {
  if (!value) {
    return '$0';
  }
  const val = value.toFixed(2);
  return '$' + val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

export function beautyCurrency(value: number): string {
  const res = currency(value)
  return res.substring(res.length - 3) === '.00' ? res.substring(0, res.length - 3) : res
}