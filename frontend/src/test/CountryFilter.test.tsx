// CountryFilter component tests — AISNP-45 · Owner: DELTA
import { describe, it, expect, vi, afterEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { CountryFilter } from '../components/CountryFilter'

const mockFetch = vi.fn()
global.fetch = mockFetch

const mockCountries = [
  { iso2: 'US', name: 'United States', flag: '🇺🇸' },
  { iso2: 'DE', name: 'Germany', flag: '🇩🇪' },
  { iso2: 'JP', name: 'Japan', flag: '🇯🇵' },
]

afterEach(() => { vi.clearAllMocks() })

describe('CountryFilter component', () => {
  it('renders dropdown with countries from API', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => mockCountries
    })

    const onChange = vi.fn()
    render(<CountryFilter selected="US" onChange={onChange} />)

    await waitFor(() => {
      expect(screen.getByRole('combobox')).not.toBeDisabled()
    })

    const options = screen.getAllByRole('option')
    expect(options).toHaveLength(3)
    expect(options[0]).toHaveTextContent('United States')
    expect(options[1]).toHaveTextContent('Germany')
  })

  it('calls onChange when selection changes', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => mockCountries
    })

    const onChange = vi.fn()
    render(<CountryFilter selected="US" onChange={onChange} />)

    await waitFor(() => {
      expect(screen.getByRole('combobox')).not.toBeDisabled()
    })

    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'DE' } })
    expect(onChange).toHaveBeenCalledWith('DE')
  })

  it('shows disabled state while loading', () => {
    mockFetch.mockReturnValue(new Promise(() => {})) // never resolves
    const onChange = vi.fn()
    render(<CountryFilter selected="US" onChange={onChange} />)
    expect(screen.getByRole('combobox')).toBeDisabled()
  })

  it('has correct aria label for accessibility', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => mockCountries })
    render(<CountryFilter selected="US" onChange={vi.fn()} />)
    expect(screen.getByLabelText(/select country/i)).toBeInTheDocument()
  })
})
