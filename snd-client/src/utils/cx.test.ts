import { describe, it, expect } from "vitest"

import { cx } from "./cx"

describe.concurrent("cx", () => {
  it.each([
    [["w-100"], "w-100"],
    [["w-100", "h-100"], "w-100 h-100"],
    [["w-100", "h-100", "color-blue"], "w-100 h-100 color-blue"],
    [["w-100", true], "w-100"],
    [["w-100", false], "w-100"],
    [["w-100", null], "w-100"],
    [["w-100", undefined], "w-100"],
    [["w-100", undefined, "h-100"], "w-100 h-100"],
    [[undefined, "h-100"], "h-100"],
    [[undefined], ""],
    [["  w-100", " "], "w-100"],
  ])("cx(%p) === %p", (classes, result) => {
    expect(cx(...classes)).toBe(result)
  })
})
