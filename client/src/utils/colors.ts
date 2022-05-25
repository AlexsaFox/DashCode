import { crc32 } from './crc32'

function hexToRGB(hex: string) {
  if (hex.indexOf('#') === 0)
    hex = hex.slice(1)

  // convert 3-digit hex to 6-digits.
  if (hex.length === 3)
    hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2]

  if (hex.length !== 6)
    throw new Error('Invalid HEX color.')

  const r = parseInt(hex.slice(0, 2), 16)
  const g = parseInt(hex.slice(2, 4), 16)
  const b = parseInt(hex.slice(4, 6), 16)
  return { r, g, b }
}

function RGBToHex(rgb: { r: number; g: number; b: number }) {
  const RHex = rgb.r.toString(16).padStart(2, '0')
  const GHex = rgb.g.toString(16).padStart(2, '0')
  const BHex = rgb.b.toString(16).padStart(2, '0')
  return `#${RHex}${GHex}${BHex}`
}

export function getContrastingColor(color: string) {
  const { r, g, b } = hexToRGB(color)
  return (r * 0.299 + g * 0.587 + b * 0.114) > 186
    ? '#1A2641'
    : '#ffffff'
}

export function getTagColor(tag: string) {
  const hashsum = crc32(tag)
  const r = ((hashsum) & 0xFF) % 178 + 50
  const g = ((hashsum >> 8) & 0xFF) % 178 + 50
  const b = ((hashsum >> 16) & 0xFF) % 178 + 50
  return RGBToHex({ r, g, b })
}
