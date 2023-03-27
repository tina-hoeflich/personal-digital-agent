import {test, expect} from 'vitest'

test ('test1', () => {
  expect(1).toBe(1)
})
test ('1+1', () => {
    expect(1+1).toEqual(2)
  })

  test ('1+2', () => {
    expect(1+2).toEqual(3)
  })