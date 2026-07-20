import { describe, it, expect } from "vitest";
import {
  formatScore,
  stressColor,
  stressBg,
  stressHex,
  stressLabel,
  recommendationLabel,
} from "@/utils/lib";

describe("formatScore", () => {
  it("formats integer scores", () => {
    expect(formatScore(74)).toBe("74");
    expect(formatScore(0)).toBe("0");
    expect(formatScore(100)).toBe("100");
  });

  it("rounds decimal scores", () => {
    expect(formatScore(74.6)).toBe("75");
    expect(formatScore(20.2)).toBe("20");
  });
});

describe("stressLabel", () => {
  it("returns correct labels", () => {
    expect(stressLabel(0)).toBe("Healthy");
    expect(stressLabel(15)).toBe("Healthy");
    expect(stressLabel(20)).toBe("Healthy");
    expect(stressLabel(21)).toBe("Monitor");
    expect(stressLabel(35)).toBe("Monitor");
    expect(stressLabel(40)).toBe("Monitor");
    expect(stressLabel(41)).toBe("Moderate");
    expect(stressLabel(55)).toBe("Moderate");
    expect(stressLabel(60)).toBe("Moderate");
    expect(stressLabel(61)).toBe("High Stress");
    expect(stressLabel(75)).toBe("High Stress");
    expect(stressLabel(80)).toBe("High Stress");
    expect(stressLabel(81)).toBe("Critical");
    expect(stressLabel(95)).toBe("Critical");
    expect(stressLabel(100)).toBe("Critical");
  });
});

describe("stressHex", () => {
  it("returns green for healthy", () => {
    expect(stressHex(10)).toBe("#22c55e");
  });

  it("returns yellow for monitor", () => {
    expect(stressHex(30)).toBe("#eab308");
  });

  it("returns orange for moderate", () => {
    expect(stressHex(50)).toBe("#f97316");
  });

  it("returns red for high", () => {
    expect(stressHex(70)).toBe("#ef4444");
  });

  it("returns dark red for critical", () => {
    expect(stressHex(90)).toBe("#dc2626");
  });
});

describe("stressColor", () => {
  it("returns tailwind text classes", () => {
    expect(stressColor(10)).toBe("text-stress-healthy");
    expect(stressColor(50)).toBe("text-stress-moderate");
    expect(stressColor(90)).toBe("text-stress-critical");
  });
});

describe("stressBg", () => {
  it("returns tailwind bg classes", () => {
    expect(stressBg(10)).toContain("bg-stress-healthy");
    expect(stressBg(50)).toContain("bg-stress-moderate");
    expect(stressBg(90)).toContain("bg-stress-critical");
  });
});

describe("recommendationLabel", () => {
  it("formats recommendation types", () => {
    expect(recommendationLabel("irrigate_immediately")).toBe("Irrigate Immediately");
    expect(recommendationLabel("irrigate_tonight")).toBe("Irrigate Tonight");
    expect(recommendationLabel("delay_irrigation")).toBe("Delay Irrigation");
    expect(recommendationLabel("monitor")).toBe("Monitor");
    expect(recommendationLabel("no_action")).toBe("No Action");
  });

  it("returns raw value for unknown types", () => {
    expect(recommendationLabel("unknown")).toBe("unknown");
  });
});
