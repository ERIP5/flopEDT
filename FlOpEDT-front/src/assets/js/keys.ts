import type { FlopAPI } from '@/assets/js/api'
import type { FlopWeek } from '@/assets/js/types'
import type { InjectionKey } from 'vue'
import { inject } from 'vue'

export const currentWeekKey = Symbol('currentWeekKey') as InjectionKey<FlopWeek>
export const apiKey = Symbol('api') as InjectionKey<FlopAPI>

export function requireInjection<T> (key: InjectionKey<T>, defaultValue?: T) {
  const resolved = inject(key, defaultValue)
  if (!resolved) {
    throw new Error(`${key} was not provided.`)
  }
  return resolved
}
