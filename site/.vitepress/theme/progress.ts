const KEY = 'eaia-progress'

export function getProgress(): string[] {
  try {
    return JSON.parse(localStorage.getItem(KEY) || '[]')
  } catch {
    return []
  }
}

export function isDone(id: string): boolean {
  return getProgress().includes(id)
}

export function markDone(id: string, on: boolean): void {
  const p = getProgress()
  const i = p.indexOf(id)
  if (on && i < 0) p.push(id)
  if (!on && i >= 0) p.splice(i, 1)
  try {
    localStorage.setItem(KEY, JSON.stringify(p))
  } catch {
    /* 隐私模式等场景下静默失败 */
  }
}
