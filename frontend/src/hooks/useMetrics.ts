import { useState, useEffect } from 'react'
import { metricsAPI } from '@/services/api'

export interface MetricData {
  impressions: number
  clicks: number
  ctr: number
  spend: number
  cpc: number
  orders: number
  cvr: number
  acos: number
  roas: number
}

export const useMetrics = (campaignId?: string, dateRange?: [string, string]) => {
  const [data, setData] = useState<MetricData | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    const fetchMetrics = async () => {
      setLoading(true)
      setError(null)
      try {
        const response = await metricsAPI.getCampaignMetrics({
          account_id: campaignId,
          start_date: dateRange?.[0],
          end_date: dateRange?.[1]
        })
        setData(response.data)
      } catch (err) {
        setError(err as Error)
      } finally {
        setLoading(false)
      }
    }

    if (campaignId && dateRange) {
      fetchMetrics()
    }
  }, [campaignId, dateRange])

  return { data, loading, error, refetch: () => setLoading(true) }
}
