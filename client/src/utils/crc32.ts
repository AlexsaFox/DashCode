const CRCTable = (() => {
  let c
  const crcTable = []
  for (let n = 0; n < 256; n++) {
    c = n
    for (let k = 0; k < 8; k++)
      c = ((c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1))

    crcTable[n] = c
  }
  return crcTable
})()

export function crc32(text: string) {
  let crc = 0 ^ (-1)

  for (let i = 0; i < text.length; i++)
    crc = (crc >>> 8) ^ CRCTable[(crc ^ text.charCodeAt(i)) & 0xFF]

  return (crc ^ (-1)) >>> 0
}
