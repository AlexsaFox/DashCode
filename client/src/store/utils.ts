import useErrorsStore from './useErrors'

export function processCommonErrors(response: any) {
  const errors = useErrorsStore()
  if (response.__typename === 'ValidationError') {
    const { fields } = response
    for (const { details } of fields)
      errors.addError(details)
  }
  else if (response.__typename === 'RequestValueError') {
    const { details } = response
    errors.addError(details)
  }
}

export function nullIfEmpty(str?: string) {
  return str === '' ? null : str
}
