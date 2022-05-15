import type { Ref } from 'vue'
import type { Validation, ValidationArgs } from '@vuelidate/core'
import useErrorsStore from '~/store/useErrors'

export default function <
  T extends { [key in keyof Vargs]: any },
  Vargs extends ValidationArgs = ValidationArgs,
  >(vuelidate: Ref<Validation<Vargs, T>>, noErrorsAction: () => Promise<void>, successRequestAction?: () => void) {
  const errors = useErrorsStore()

  errors.$reset()
  vuelidate.value.$touch()

  if (vuelidate.value.$error) {
    for (const error of vuelidate.value.$errors)
      errors.addError(error.$message.toString())
  }
  else {
    noErrorsAction().then(() => {
      if (successRequestAction && errors.errors.length === 0)
        successRequestAction()
    })
  }
}
