const QUANTITY_PLANS = [500, 1000, 2000];

const LABELS = {
  product: "\u94dc\u677f\u7eb8\u4e0d\u5e72\u80f6",
  cut: {
    dieCut: "\u6a21\u5207",
    trimCut: "\u88c1\u5207"
  },
  lamination: {
    glossy: "\u8986\u4eae\u819c",
    matte: "\u8986\u54d1\u819c"
  },
  extra: {
    none: "",
    pureGold: "\u7eaf\u70eb\u91d1",
    laserSilver: "\u70eb\u9559\u5c04\u94f6",
    colorGoldSilver: "\u5f69\u8272\u5370\u5237+\u70eb\u91d1/\u94f6"
  }
};

const GROUPED_TIER_RULES = {
  glossy: {
    none: [
      { match: { width: 5, heightMin: 5, heightMax: 8 }, prices: { 500: 60, 1000: 70, 2000: 95 } },
      { match: { width: 5, height: 10 }, prices: { 500: 88, 1000: 105, 2000: 150 } },
      { match: { width: 6, height: 7 }, prices: { 500: 79, 1000: 94, 2000: 132 } },
      { match: { width: 6, height: 8 }, prices: { 500: 85, 1000: 102, 2000: 145 } },
      { match: { width: 6, height: 10 }, prices: { 500: 104, 1000: 124, 2000: 176 } },
      { match: { width: 7, height: 10 }, prices: { 500: 110, 1000: 129, 2000: 202 } }
    ],
    pureGold: [
      { match: { width: 5, heightMin: 5, heightMax: 8 }, prices: { 500: 184, 1000: 194, 2000: 331 } },
      { match: { width: 5, height: 10 }, prices: { 500: 218, 1000: 235, 2000: 385 } },
      { match: { width: 6, height: 7 }, prices: { 500: 203, 1000: 218, 2000: 368 } },
      { match: { width: 6, height: 8 }, prices: { 500: 209, 1000: 226, 2000: 381 } },
      { match: { width: 6, height: 10 }, prices: { 500: 274, 1000: 294, 2000: 399 } }
    ],
    colorGoldSilver: [
      { match: { width: 3, height: 4 }, prices: { 500: 221, 1000: 226, 2000: 409 } },
      { match: { width: 5, heightMin: 5, heightMax: 8 }, prices: { 500: 246, 1000: 256, 2000: 449 } },
      { match: { width: 5, height: 10 }, prices: { 500: 283, 1000: 300, 2000: 503 } },
      { match: { width: 6, height: 6 }, prices: { 500: 258, 1000: 272, 2000: 475 } },
      { match: { width: 6, height: 7 }, prices: { 500: 265, 1000: 280, 2000: 486 } },
      { match: { width: 6, height: 8 }, prices: { 500: 271, 1000: 288, 2000: 499 } },
      { match: { width: 6, height: 9 }, prices: { 500: 314, 1000: 332, 2000: 506 } },
      { match: { width: 6, height: 10 }, prices: { 500: 359, 1000: 379, 2000: 511 } },
      { match: { width: 7, height: 8 }, prices: { 500: 329, 1000: 348, 2000: 508 } },
      { match: { width: 7, height: 10 }, prices: { 500: 425, 1000: 444, 2000: 517 } },
      { match: { width: 8, height: 10 }, prices: { 500: 455, 1000: 476, 2000: 558 } },
      { match: { width: 9, height: 10 }, prices: { 500: 469, 1000: 507, 2000: 580 } }
    ]
  },
  matte: {
    none: [
      { match: { width: 5, heightMin: 5, heightMax: 7 }, prices: { 500: 72, 1000: 84, 2000: 114 } },
      { match: { width: 6, height: 6 }, prices: { 500: 86, 1000: 102, 2000: 142 } },
      { match: { width: 6, height: 7 }, prices: { 500: 94, 1000: 111, 2000: 155 } },
      { match: { width: 6, height: 8 }, prices: { 500: 101, 1000: 121, 2000: 170 } },
      { match: { width: 5, height: 10 }, prices: { 500: 105, 1000: 124, 2000: 176 } },
      { match: { width: 6, height: 10 }, prices: { 500: 124, 1000: 147, 2000: 208 } },
      { match: { width: 7, height: 10 }, prices: { 500: 131, 1000: 153, 2000: 239 } }
    ],
    pureGold: [
      { match: { width: 5, heightMin: 5, heightMax: 8 }, prices: { 500: 221, 1000: 233, 2000: 398 } },
      { match: { width: 5, height: 10 }, prices: { 500: 261, 1000: 280, 2000: 458 } },
      { match: { width: 6, height: 7 }, prices: { 500: 243, 1000: 260, 2000: 438 } },
      { match: { width: 6, height: 8 }, prices: { 500: 250, 1000: 270, 2000: 454 } },
      { match: { width: 6, height: 10 }, prices: { 500: 328, 1000: 351, 2000: 475 } },
      { match: { width: 7, height: 10 }, prices: { 500: 383, 1000: 405, 2000: 491 } }
    ],
    colorGoldSilver: [
      { match: { width: 2, height: 2 }, prices: { 500: 274, 1000: 281, 2000: 504 } },
      { match: { width: 2, height: 3 }, prices: { 500: 274, 1000: 281, 2000: 504 } },
      { match: { width: 2, height: 4 }, prices: { 500: 274, 1000: 281, 2000: 504 } },
      { match: { width: 3, height: 4 }, prices: { 500: 274, 1000: 281, 2000: 504 } },
      { match: { width: 5, heightMin: 5, heightMax: 8 }, prices: { 500: 296, 1000: 308, 2000: 539 } },
      { match: { width: 5, height: 10 }, prices: { 500: 339, 1000: 358, 2000: 600 } },
      { match: { width: 6, height: 7 }, prices: { 500: 317, 1000: 334, 2000: 580 } },
      { match: { width: 6, height: 8 }, prices: { 500: 325, 1000: 344, 2000: 595 } },
      { match: { width: 6, height: 10 }, prices: { 500: 430, 1000: 453, 2000: 610 } },
      { match: { width: 7, height: 10 }, prices: { 500: 509, 1000: 531, 2000: 617 } },
      { match: { width: 8, height: 10 }, prices: { 500: 545, 1000: 570, 2000: 666 } },
      { match: { width: 9, height: 10 }, prices: { 500: 562, 1000: 607, 2000: 692 } }
    ]
  }
};

const DIMENSION_SAMPLE_RULES = {
  glossy: {
    colorGoldSilver: {
      500: [
        [3, 4, 221],
        [5, 5, 246],
        [5, 6, 246],
        [5, 7, 246],
        [5, 8, 246],
        [5, 10, 283],
        [6, 6, 258],
        [6, 7, 265],
        [6, 8, 271],
        [6, 9, 314],
        [6, 10, 359],
        [7, 8, 329],
        [7, 10, 425],
        [8, 10, 455],
        [9, 10, 469]
      ],
      1000: [
        [3, 4, 226],
        [5, 5, 256],
        [5, 6, 256],
        [5, 7, 256],
        [5, 8, 256],
        [5, 10, 300],
        [6, 6, 272],
        [6, 7, 280],
        [6, 8, 288],
        [6, 9, 332],
        [6, 10, 379],
        [7, 8, 348],
        [7, 10, 444],
        [8, 10, 476],
        [9, 10, 507]
      ],
      2000: [
        [3, 4, 409],
        [5, 5, 449],
        [5, 6, 449],
        [5, 7, 449],
        [5, 8, 449],
        [5, 10, 503],
        [6, 6, 475],
        [6, 7, 486],
        [6, 8, 499],
        [6, 9, 506],
        [6, 10, 511],
        [7, 8, 508],
        [7, 10, 517],
        [8, 10, 558],
        [9, 10, 580]
      ]
    }
  },
  matte: {
    colorGoldSilver: {
      500: [
        [2, 2, 274],
        [2, 3, 274],
        [2, 4, 274],
        [3, 4, 274],
        [3, 9, 296],
        [5, 5, 296],
        [5, 6, 296],
        [5, 7, 296],
        [5, 8, 296],
        [5, 10, 339],
        [6, 7, 317],
        [6, 8, 325],
        [6, 10, 430],
        [7, 10, 509],
        [8, 10, 545],
        [9, 10, 562]
      ],
      1000: [
        [2, 2, 281],
        [2, 3, 281],
        [2, 4, 281],
        [3, 4, 281],
        [3, 9, 308],
        [5, 5, 308],
        [5, 6, 308],
        [5, 7, 308],
        [5, 8, 308],
        [5, 10, 358],
        [6, 7, 334],
        [6, 8, 344],
        [6, 10, 453],
        [7, 10, 531],
        [8, 10, 570],
        [9, 10, 607]
      ],
      2000: [
        [2, 2, 504],
        [2, 3, 504],
        [2, 4, 504],
        [3, 4, 504],
        [3, 9, 539],
        [5, 5, 539],
        [5, 6, 539],
        [5, 7, 539],
        [5, 8, 539],
        [5, 10, 600],
        [6, 7, 580],
        [6, 8, 595],
        [6, 10, 610],
        [7, 10, 617],
        [8, 10, 666],
        [9, 10, 692]
      ]
    }
  }
};

const RANGE_PADDING = 1;
const MAX_INTERPOLATION_DISTANCE = 3;
const BASELINE_DATA_URL = "/static/sticker_baseline.json";

let capturedBaselineData = null;
let capturedBaselineIndex = new Map();

function buildExpandedTierSamples() {
  const expandedRules = {};

  Object.entries(GROUPED_TIER_RULES).forEach(([laminationCode, extraRules]) => {
    expandedRules[laminationCode] = {};

    Object.entries(extraRules).forEach(([extraCode, tierRules]) => {
      expandedRules[laminationCode][extraCode] = {};

      QUANTITY_PLANS.forEach((quantity) => {
        const sampleMap = new Map();

        tierRules.forEach((rule) => {
          const widths = rule.match.width != null ? [rule.match.width] : [];
          const heightStart = rule.match.height != null ? rule.match.height : rule.match.heightMin;
          const heightEnd = rule.match.height != null ? rule.match.height : rule.match.heightMax;
          if (!widths.length || heightStart == null || heightEnd == null) {
            return;
          }

          widths.forEach((width) => {
            for (let height = heightStart; height <= heightEnd; height += 1) {
              const key = `${width}*${height}`;
              sampleMap.set(key, [width, height, rule.prices[quantity]]);
            }
          });
        });

        expandedRules[laminationCode][extraCode][quantity] = Array.from(sampleMap.values());
      });
    });
  });

  return expandedRules;
}

const EXPANDED_TIER_SAMPLE_RULES = buildExpandedTierSamples();

const productType = document.getElementById("productType");
const sizeInput = document.getElementById("sizeInput");
const quantityBase = document.getElementById("quantityBase");
const styleCount = document.getElementById("styleCount");
const priceScale = document.getElementById("priceScale");
const customerName = document.getElementById("customerName");
const resultText = document.getElementById("resultText");
const calcButton = document.getElementById("calcButton");
const resetButton = document.getElementById("resetButton");
const copyButton = document.getElementById("copyButton");
const baselineStatus = document.getElementById("baselineStatus");
const chips = Array.from(document.querySelectorAll(".chip"));

function bootstrapChipMeta() {
  const groupCodes = {
    cut: ["dieCut", "trimCut"],
    lamination: ["glossy", "matte"],
    extra: ["pureGold", "colorGoldSilver"]
  };

  const groupLabels = {
    cut: ["\u6a21\u5207", "\u88c1\u5207"],
    lamination: ["\u8986\u4eae\u819c", "\u8986\u54d1\u819c"],
    extra: [
      "\u7eaf\u70eb\u91d1",
      "\u5f69\u8272\u5370\u5237+\u70eb\u91d1/\u94f6"
    ]
  };

  Object.entries(groupCodes).forEach(([groupName, codes]) => {
    const groupChips = Array.from(document.querySelectorAll(`.chip[data-group="${groupName}"]`));
    groupChips.forEach((chip, index) => {
      if (codes[index]) {
        chip.dataset.code = codes[index];
      }
      if (groupLabels[groupName][index]) {
        chip.textContent = groupLabels[groupName][index];
      }
    });
  });
}

function getChipCode(chip) {
  if (chip.dataset.code) {
    return chip.dataset.code;
  }

  const text = chip.textContent.trim();
  const textMap = {
    "\u6a21\u5207": "dieCut",
    "\u88c1\u5207": "trimCut",
    "\u8986\u4eae\u819c": "glossy",
    "\u8986\u54d1\u819c": "matte",
    "\u7eaf\u70eb\u91d1": "pureGold",
    "\u70eb\u9559\u5c04\u94f6": "laserSilver",
    "\u5f69\u8272\u5370\u5237+\u70eb\u91d1/\u94f6": "colorGoldSilver"
  };
  return textMap[text] || "";
}

function getActiveCode(groupName) {
  const active = document.querySelector(`.chip.active[data-group="${groupName}"]`);
  return active ? getChipCode(active) : "";
}

function parseSize(raw) {
  const normalized = raw.replace(/[xX\uff0a\u00d7]/g, "*").trim();
  const parts = normalized.split("*").map((item) => Number(item.trim()));
  if (parts.length !== 2 || parts.some((item) => Number.isNaN(item) || item <= 0)) {
    return null;
  }

  return {
    width: parts[0],
    height: parts[1]
  };
}

function getArea(size) {
  return size.width * size.height;
}

function normalizeSize(size) {
  const sides = [size.width, size.height].sort((left, right) => left - right);
  return {
    width: sides[0],
    height: sides[1]
  };
}

function getSizeRuleKey(size) {
  const normalizedSize = normalizeSize(size);
  return `${normalizedSize.width}*${normalizedSize.height}`;
}

function getBaselineGroupKey(product, cutCode, laminationCode, extraCode) {
  return [product, cutCode, laminationCode, normalizeExtraCode(extraCode)].join("|");
}

function describeBaselineSelection(cutCode, laminationCode, extraCode) {
  const parts = [LABELS.cut[cutCode], LABELS.lamination[laminationCode]];
  const normalizedExtraCode = normalizeExtraCode(extraCode);
  if (normalizedExtraCode && normalizedExtraCode !== "none") {
    parts.push(LABELS.extra[normalizedExtraCode]);
  }
  return parts.filter(Boolean).join("-");
}

function buildCapturedBaselineIndex(data) {
  const nextIndex = new Map();

  if (!data || !Array.isArray(data.groups)) {
    return nextIndex;
  }

  data.groups.forEach((group) => {
    const groupKey = getBaselineGroupKey(
      data.product,
      group.cutCode,
      group.laminationCode,
      group.extraCode
    );
    const sizeMap = new Map();

    group.rows.forEach((row) => {
      sizeMap.set(row.size, row.prices || {});
    });

    nextIndex.set(groupKey, sizeMap);
  });

  return nextIndex;
}

function getCapturedBaselinePrice(size, product, cutCode, laminationCode, extraCode, quantity) {
  const groupKey = getBaselineGroupKey(product, cutCode, laminationCode, extraCode);
  const sizeMap = capturedBaselineIndex.get(groupKey);
  if (!sizeMap) {
    return null;
  }

  const prices = sizeMap.get(getSizeRuleKey(size));
  const price = prices ? prices[String(quantity)] : null;
  return typeof price === "number" ? price : null;
}

function getCapturedBaselineRow(size, product, cutCode, laminationCode, extraCode) {
  const groupKey = getBaselineGroupKey(product, cutCode, laminationCode, extraCode);
  const sizeMap = capturedBaselineIndex.get(groupKey);
  return sizeMap ? sizeMap.get(getSizeRuleKey(size)) || null : null;
}

function updateBaselineStatus(message, isFallback = false) {
  if (!baselineStatus) {
    return;
  }

  if (isFallback) {
    baselineStatus.classList.add("is-fallback");
  } else {
    baselineStatus.classList.remove("is-fallback");
  }
  const value =
    typeof baselineStatus.querySelector === "function"
      ? baselineStatus.querySelector("strong")
      : null;
  if (value) {
    value.textContent = message;
  }
}

function roundMoney(value) {
  return Math.round(value);
}

function formatPrice(value) {
  if (Number.isInteger(value)) {
    return String(value);
  }
  return value.toFixed(2).replace(/\.?0+$/, "");
}

function sortDimensions(size) {
  const sides = [size.width, size.height].sort((left, right) => left - right);
  return [sides[0], sides[1]];
}

function normalizeExtraCode(extraCode) {
  if (extraCode === "laserSilver") {
    return "pureGold";
  }
  return extraCode || "none";
}

function mergeSamples(primarySamples, secondarySamples) {
  const sampleMap = new Map();

  [...secondarySamples, ...primarySamples].forEach((sample) => {
    const [width, height, price] = sample;
    sampleMap.set(`${width}*${height}`, [width, height, price]);
  });

  return Array.from(sampleMap.values());
}

function matchesTierRule(size, match) {
  const normalizedSize = normalizeSize(size);
  if (match.width != null && normalizedSize.width !== match.width) {
    return false;
  }
  if (match.height != null && normalizedSize.height !== match.height) {
    return false;
  }
  if (match.heightMin != null && normalizedSize.height < match.heightMin) {
    return false;
  }
  if (match.heightMax != null && normalizedSize.height > match.heightMax) {
    return false;
  }
  return true;
}

function getGroupedTierPrice(size, laminationCode, extraCode, quantity) {
  const normalizedExtra = normalizeExtraCode(extraCode);
  const laminationRules = GROUPED_TIER_RULES[laminationCode];
  if (!laminationRules) {
    return null;
  }

  const tierRules = laminationRules[normalizedExtra];
  if (!Array.isArray(tierRules)) {
    return null;
  }

  const matchedRule = tierRules.find((rule) => matchesTierRule(size, rule.match));
  if (!matchedRule) {
    return null;
  }

  return matchedRule.prices[quantity] ?? null;
}

function getInterpolationSamples(laminationCode, extraCode, quantity) {
  const explicitSamples = DIMENSION_SAMPLE_RULES[laminationCode]?.[extraCode]?.[quantity] || [];
  const expandedSamples =
    EXPANDED_TIER_SAMPLE_RULES[laminationCode]?.[normalizeExtraCode(extraCode)]?.[quantity] || [];
  return mergeSamples(explicitSamples, expandedSamples);
}

function getInterpolationBounds(samples) {
  if (!Array.isArray(samples) || samples.length === 0) {
    return null;
  }

  const widths = samples.map(([width]) => width);
  const heights = samples.map(([, height]) => height);
  return {
    minWidth: Math.min(...widths),
    maxWidth: Math.max(...widths),
    minHeight: Math.min(...heights),
    maxHeight: Math.max(...heights)
  };
}

function isInterpolationCandidate(size, samples) {
  if (!Array.isArray(samples) || samples.length === 0) {
    return false;
  }

  const [targetWidth, targetHeight] = sortDimensions(size);
  const bounds = getInterpolationBounds(samples);
  if (!bounds) {
    return false;
  }

  if (
    targetWidth < bounds.minWidth - RANGE_PADDING ||
    targetWidth > bounds.maxWidth + RANGE_PADDING ||
    targetHeight < bounds.minHeight - RANGE_PADDING ||
    targetHeight > bounds.maxHeight + RANGE_PADDING
  ) {
    return false;
  }

  const nearestDistance = samples.reduce((best, [sampleWidth, sampleHeight]) => {
    const distance =
      Math.sqrt((targetWidth - sampleWidth) ** 2 + (targetHeight - sampleHeight) ** 2);
    return Math.min(best, distance);
  }, Number.POSITIVE_INFINITY);

  return nearestDistance <= MAX_INTERPOLATION_DISTANCE;
}

function interpolateDimensionSamples(size, laminationCode, extraCode, quantity) {
  const samples = getInterpolationSamples(laminationCode, extraCode, quantity);
  if (!isInterpolationCandidate(size, samples)) {
    return null;
  }

  const [targetWidth, targetHeight] = sortDimensions(size);

  for (const [sampleWidth, sampleHeight, samplePrice] of samples) {
    if (sampleWidth === targetWidth && sampleHeight === targetHeight) {
      return samplePrice;
    }
  }

  let numerator = 0;
  let denominator = 0;

  samples.forEach(([sampleWidth, sampleHeight, samplePrice]) => {
    const distance =
      Math.sqrt((targetWidth - sampleWidth) ** 2 + (targetHeight - sampleHeight) ** 2);
    const weight = 1 / distance ** 2;
    numerator += samplePrice * weight;
    denominator += weight;
  });

  if (denominator === 0) {
    return null;
  }

  return roundMoney(numerator / denominator);
}

function getDerivedGoldPrice(size, laminationCode, quantity, options = {}) {
  const nonePrice = getUnitPrice(size, laminationCode, "none", quantity, {
    skipDerived: true,
    cutCode: options.cutCode,
    product: options.product
  });
  const colorPrice = getUnitPrice(size, laminationCode, "colorGoldSilver", quantity, {
    skipDerived: true,
    cutCode: options.cutCode,
    product: options.product
  });

  if (typeof nonePrice !== "number" || typeof colorPrice !== "number") {
    return null;
  }

  return roundMoney(nonePrice + (colorPrice - nonePrice) * (2 / 3));
}

function getUnitPrice(size, laminationCode, extraCode, quantity, options = {}) {
  const product = options.product || LABELS.product;
  const cutCode = options.cutCode || "dieCut";
  const capturedPrice = getCapturedBaselinePrice(
    size,
    product,
    cutCode,
    laminationCode,
    extraCode,
    quantity
  );
  if (typeof capturedPrice === "number") {
    return capturedPrice;
  }

  const groupedTierPrice = getGroupedTierPrice(size, laminationCode, extraCode, quantity);
  if (typeof groupedTierPrice === "number") {
    return groupedTierPrice;
  }

  const dimensionPrice = interpolateDimensionSamples(size, laminationCode, extraCode, quantity);
  if (typeof dimensionPrice === "number") {
    return dimensionPrice;
  }

  if (!options.skipDerived && normalizeExtraCode(extraCode) === "pureGold") {
    const derivedGoldPrice = getDerivedGoldPrice(size, laminationCode, quantity, {
      cutCode,
      product
    });
    if (typeof derivedGoldPrice === "number") {
      return derivedGoldPrice;
    }
  }

  return null;
}

function buildHeader(product, size, cutCode, laminationCode, extraCode) {
  const parts = [LABELS.cut[cutCode], LABELS.lamination[laminationCode]];
  if (extraCode && extraCode !== "none") {
    parts.push(LABELS.extra[extraCode]);
  }
  return `${product} - ${size.width}*${size.height}\u5398\u7c73 - ${parts.join("-")}--`;
}

function generateText() {
  const size = parseSize(sizeInput.value);
  if (!size) {
    resultText.value = "\u8bf7\u8f93\u5165\u6b63\u786e\u5c3a\u5bf8\uff0c\u683c\u5f0f\u4f8b\u5982 5*5";
    return;
  }

  const product = productType.value || LABELS.product;
  const styleNumber = Math.max(1, Number(styleCount.value) || 1);
  const scale = Math.max(0, Number(priceScale.value) || 1);
  const cutCode = getActiveCode("cut") || "dieCut";
  const laminationCode = getActiveCode("lamination") || "glossy";
  const extraCode = getActiveCode("extra") || "none";
  const capturedRow = getCapturedBaselineRow(size, product, cutCode, laminationCode, extraCode);
  const baselineLabel = describeBaselineSelection(cutCode, laminationCode, extraCode);
  const lines = [];
  lines.push(buildHeader(product, size, cutCode, laminationCode, extraCode));

  QUANTITY_PLANS.forEach((quantity) => {
    const unitPrice = getUnitPrice(size, laminationCode, extraCode, quantity, {
      cutCode,
      product
    });
    if (typeof unitPrice !== "number") {
      lines.push(`${styleNumber}款 ${quantity}个，当前基线未覆盖该尺寸/工艺组合`);
      return;
    }
    const totalPrice = unitPrice * styleNumber * scale;
    lines.push(`${styleNumber}\u6b3e ${quantity}\u4e2a\uff0c\u5171${formatPrice(totalPrice)}\u5143`);
  });

  lines.push("\u5305\u90ae\uff0c\u514d\u8d39\u8bbe\u8ba1\u5462~\uff08\u504f\u8fdc\u5730\u533a\u9700\u8865\u90ae\u8d39\uff09");
  lines.push("");
  lines.push("\u4eb2 \u73b0\u5728\u4e0b\u5355\u53ef\u4ee5\u53c2\u52a0\u6dd8\u5b9d\u6d3b\u52a88.5\u6298\u6298\u6263\u54e6!");
  if (customerName.value.trim()) {
    lines.push(`\u5ba2\u6237\u79f0\u547c\uff1a${customerName.value.trim()}`);
  }

  resultText.value = lines.join("\n");

  if (capturedRow) {
    updateBaselineStatus(`命中真实基线：${baselineLabel} / ${getSizeRuleKey(size)} / ${QUANTITY_PLANS.length}档`);
  } else if (capturedBaselineData) {
    updateBaselineStatus(`未命中真实基线：${baselineLabel} / ${getSizeRuleKey(size)}，已回退旧规则`, true);
  }
}

async function loadCapturedBaseline() {
  try {
    const response = await fetch(BASELINE_DATA_URL, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    capturedBaselineData = await response.json();
    capturedBaselineIndex = buildCapturedBaselineIndex(capturedBaselineData);
    updateBaselineStatus(
      `已加载 ${capturedBaselineData.groups.length} 组 / ${
        capturedBaselineData.groups.reduce((sum, group) => sum + group.rows.length, 0)
      } 条`
    );
    generateText();
  } catch (error) {
    updateBaselineStatus("真实基线加载失败，使用旧规则", true);
  }
}

function resetForm() {
  productType.selectedIndex = 0;
  sizeInput.value = "5*5";
  quantityBase.value = "500";
  styleCount.value = "1";
  priceScale.value = "1";
  customerName.value = "";

  chips.forEach((chip) => {
    chip.classList.remove("active");
  });

  const defaultCut = document.querySelector('.chip[data-group="cut"]');
  const defaultLamination = document.querySelector('.chip[data-group="lamination"]');
  if (defaultCut) {
    defaultCut.classList.add("active");
  }
  if (defaultLamination) {
    defaultLamination.classList.add("active");
  }

  generateText();
}

chips.forEach((chip) => {
  chip.addEventListener("click", () => {
    const { group } = chip.dataset;

    if (group === "extra") {
      const isActive = chip.classList.contains("active");
      document.querySelectorAll('.chip[data-group="extra"]').forEach((item) => {
        item.classList.remove("active");
      });
      if (!isActive) {
        chip.classList.add("active");
      }
    } else {
      document.querySelectorAll(`.chip[data-group="${group}"]`).forEach((item) => {
        item.classList.remove("active");
      });
      chip.classList.add("active");
    }

    generateText();
  });
});

[productType, sizeInput, quantityBase, styleCount, priceScale, customerName].forEach((element) => {
  element.addEventListener("input", generateText);
  element.addEventListener("change", generateText);
});

calcButton.addEventListener("click", generateText);
resetButton.addEventListener("click", resetForm);
copyButton.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(resultText.value);
    copyButton.textContent = "\u5df2\u590d\u5236";
    window.setTimeout(() => {
      copyButton.textContent = "\u70b9\u51fb\u590d\u5236";
    }, 1500);
  } catch (error) {
    copyButton.textContent = "\u590d\u5236\u5931\u8d25";
    window.setTimeout(() => {
      copyButton.textContent = "\u70b9\u51fb\u590d\u5236";
    }, 1500);
  }
});

bootstrapChipMeta();
generateText();
loadCapturedBaseline();
