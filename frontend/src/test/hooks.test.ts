// Frontend unit tests — AISNP-45 · Owner: DELTA
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'

// Mock fetch globally
const mockFetch = vi.fn()
global.fetch = mockFetch

describe('useStocks hook', () => {
  beforeEach(() => { vi.useFakeTimers() })
  afterEach(() => { vi.useRealTimers(); vi.clearAllMocks() })

  it('calls fetchStocks on mount', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => ({
        quotes: [{ symbol: 'NVDA', name: 'NVIDIA', price: 880, change: 5,
                   change_pct: 0.57, prev_close: 875, volume: 50000000,
                   data_source: 'yahoo_finance', last_updated: new Date().toISOString() }],
        last_updated: new Date().toISOString()
      })
    })

    const { useStocks } = await import('../hooks/useStocks')
    const { result } = renderHook(() => useStocks())

    await act(async () => { await Promise.resolve() })
    expect(mockFetch).toHaveBeenCalledWith(expect.stringContaining('/stocks'))
    expect(result.current.stockData).toHaveLength(1)
    expect(result.current.stockData[0].symbol).toBe('NVDA')
  })

  it('retains last data on error', async () => {
    mockFetch
      .mockResolvedValueOnce({ ok: true, json: async () => ({
        quotes: [{ symbol: 'NVDA', name: 'NVIDIA', price: 880, change: 0,
                   change_pct: 0, prev_close: 880, volume: 0,
                   data_source: 'yahoo_finance', last_updated: new Date().toISOString() }],
        last_updated: new Date().toISOString() }) })
      .mockRejectedValueOnce(new Error('Network error'))

    const { useStocks } = await import('../hooks/useStocks')
    const { result } = renderHook(() => useStocks())

    await act(async () => { await Promise.resolve() })
    expect(result.current.stockData).toHaveLength(1)

    await act(async () => {
      vi.advanceTimersByTime(5000)
      await Promise.resolve()
    })
    // Data retained, error set
    expect(result.current.stockData).toHaveLength(1)
    expect(result.current.stockError).toBeTruthy()
  })

  it('polls every 5 seconds', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => ({
        quotes: [{ symbol: 'AMD', name: 'AMD', price: 165, change: 1,
                   change_pct: 0.6, prev_close: 164, volume: 10000000,
                   data_source: 'yahoo_finance', last_updated: new Date().toISOString() }],
        last_updated: new Date().toISOString()
      })
    })
    const { useStocks } = await import('../hooks/useStocks')
    renderHook(() => useStocks())
    await act(async () => { await Promise.resolve() })
    const callsAfterMount = mockFetch.mock.calls.length
    await act(async () => { vi.advanceTimersByTime(5000); await Promise.resolve() })
    expect(mockFetch.mock.calls.length).toBeGreaterThan(callsAfterMount)
  })
})

describe('useNews hook', () => {
  afterEach(() => { vi.clearAllMocks() })

  it('fetches news on mount', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => ({
        articles: [{ title: 'AI News', source: 'TechCrunch', url: 'https://example.com',
                     published_at: new Date().toISOString(), summary: 'Summary', image_url: '' }],
        country: 'US', total: 1
      })
    })

    const { useNews } = await import('../hooks/useNews')
    const { result } = renderHook(() => useNews('US'))

    await act(async () => { await Promise.resolve() })
    expect(mockFetch).toHaveBeenCalledWith(expect.stringContaining('country=US'))
    expect(result.current.articles).toHaveLength(1)
  })

  it('refetches when country changes', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => ({ articles: [], country: 'DE', total: 0 })
    })

    const { useNews } = await import('../hooks/useNews')
    let country = 'US'
    const { rerender } = renderHook(() => useNews(country))
    await act(async () => { await Promise.resolve() })

    country = 'DE'
    rerender()
    await act(async () => { await Promise.resolve() })

    expect(mockFetch).toHaveBeenCalledTimes(2)
    expect(mockFetch).toHaveBeenLastCalledWith(expect.stringContaining('country=DE'))
  })

  it('sets error on fetch failure', async () => {
    mockFetch.mockRejectedValue(new Error('Network error'))
    const { useNews } = await import('../hooks/useNews')
    const { result } = renderHook(() => useNews('US'))
    await act(async () => { await Promise.resolve() })
    expect(result.current.newsError).toBeTruthy()
    expect(result.current.articles).toHaveLength(0)
  })
})
