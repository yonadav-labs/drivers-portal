
export function capitalize(name: string): string {
  return name.split(',').map(x => x.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join(' ')).join(', ')
}