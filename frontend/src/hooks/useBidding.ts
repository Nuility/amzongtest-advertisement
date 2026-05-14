import { useState } from 'react'
import { biddingAPI } from '@/services/api'

export interface BiddingStrategy {
  name: string
  description: string
  parameters: Record<string, any>
}

export const useBidding = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  const executeBidding = async (
    strategyName: string,
    keywordIds: string[],
    targetMetrics: Record<string, number>
  ) => {
    setLoading(true)
    setError(null)
    try {
      const response = await biddingAPI.executeBidding({
        strategy_name: strategyName,
        keyword_ids: keywordIds,
        ...targetMetrics
      })
      return response.data
    } catch (err) {
      setError(err as Error)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const getStrategies = async () => {
    setLoading(true)
    try {
      const response = await biddingAPI.getBiddingLogs({ limit: 100 })
      return response.data
    } catch (err) {
      setError(err as Error)
      throw err
    } finally {
      setLoading(false)
    }
  }

  return { executeBidding, getStrategies, loading, error }
}
