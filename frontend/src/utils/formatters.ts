import dayjs from 'dayjs'

export const formatNumber = (num: number): string => {
  return num.toLocaleString('zh-CN')
}

export const formatCurrency = (amount: number, currency: string = 'USD'): string => {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency,
  }).format(amount)
}

export const formatPercent = (value: number, decimals: number = 2): string => {
  return `${(value * 100).toFixed(decimals)}%`
}

export const formatDate = (date: string | Date, format: string = 'YYYY-MM-DD'): string => {
  return dayjs(date).format(format)
}

export const formatDateTime = (date: string | Date): string => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

export const calculateCTR = (clicks: number, impressions: number): number => {
  if (impressions === 0) return 0
  return clicks / impressions
}

export const calculateCPC = (spend: number, clicks: number): number => {
  if (clicks === 0) return 0
  return spend / clicks
}

export const calculateCVR = (orders: number, clicks: number): number => {
  if (clicks === 0) return 0
  return orders / clicks
}

export const calculateACoS = (spend: number, sales: number): number => {
  if (sales === 0) return 0
  return spend / sales
}

export const calculateROAS = (sales: number, spend: number): number => {
  if (spend === 0) return 0
  return sales / spend
}

export const clamp = (value: number, min: number, max: number): number => {
  return Math.min(Math.max(value, min), max)
}

export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: NodeJS.Timeout | null = null
  return (...args: Parameters<T>) => {
    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}
