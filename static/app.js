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

const SIZE_TIER_AREA = 25;

const BRIGHT_BASE_TIER_PRICES = {
  500: {
    0: 41,
    1: 69,
    2: 102
  },
  1000: {
    0: 46,
    1: 81,
    2: 121
  },
  2000: {
    0: 64,
    1: 110,
    2: 173
  }
};

const BRIGHT_COLOR_GOLD_TIER_PRICES = {
  500: {
    micro: 249,
    0: 255,
    1: 283,
    2: 326,
    3: 446,
    4: 566
  },
  1000: {
    micro: 255,
    0: 260,
    1: 295,
    2: 345,
    3: 482,
    4: 618
  },
  2000: {
    micro: 465,
    0: 471,
    1: 517,
    2: 579,
    3: 645,
    4: 710
  }
};

const MATTE_RATIOS = {
  none: {
    500: 83 / 69,
    1000: 97 / 81,
    2000: 132 / 110
  },
  pureGold: {
    500: 255 / 212,
    1000: 268 / 224,
    2000: 458 / 381
  },
  laserSilver: {
    500: 255 / 212,
    1000: 268 / 224,
    2000: 458 / 381
  },
  colorGoldSilver: {
    500: 341 / 283,
    1000: 355 / 295,
    2000: 620 / 517
  }
};

const FOIL_SURCHARGE_RATIOS = {
  pureGold: {
    500: (212 - 69) / (283 - 69),
    1000: (224 - 81) / (295 - 81),
    2000: (381 - 110) / (517 - 110)
  },
  laserSilver: {
    500: (212 - 69) / (283 - 69),
    1000: (224 - 81) / (295 - 81),
    2000: (381 - 110) / (517 - 110)
  }
};

const DIMENSION_SAMPLE_RULES = {
  glossy: {
    colorGoldSilver: {
      500: [
        [1, 1, 249],
        [2, 2, 255],
        [2, 3, 255],
        [3, 3, 255],
        [5, 5, 283],
        [5, 10, 326],
        [6, 10, 413],
        [10, 10, 566]
      ],
      1000: [
        [1, 1, 255],
        [2, 2, 260],
        [2, 3, 260],
        [3, 3, 260],
        [5, 5, 295],
        [5, 10, 345],
        [6, 10, 436],
        [10, 10, 618]
      ],
      2000: [
        [1, 1, 465],
        [2, 2, 471],
        [2, 3, 471],
        [3, 3, 471],
        [5, 5, 517],
        [5, 10, 579],
        [6, 10, 588],
        [10, 10, 710]
      ]
    }
  },
  matte: {
    colorGoldSilver: {
      500: [
        [1, 5, 316],
        [2, 5, 316],
        [5, 5, 341],
        [5, 6, 341],
        [5, 7, 341],
        [5, 9, 341],
        [5, 10, 390],
        [6, 7, 365],
        [6, 8, 374]
      ],
      1000: [
        [1, 5, 324],
        [2, 5, 324],
        [5, 5, 355],
        [5, 6, 355],
        [5, 7, 355],
        [5, 9, 355],
        [5, 10, 412],
        [6, 7, 385],
        [6, 8, 396]
      ],
      2000: [
        [1, 5, 580],
        [2, 5, 580],
        [5, 5, 620],
        [5, 6, 620],
        [5, 7, 620],
        [5, 9, 620],
        [5, 10, 690],
        [6, 7, 667],
        [6, 8, 685]
      ]
    }
  }
};

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
const chips = Array.from(document.querySelectorAll(".chip"));

function bootstrapChipMeta() {
  const groupCodes = {
    cut: ["dieCut", "trimCut"],
    lamination: ["glossy", "matte"],
    extra: ["pureGold", "laserSilver", "colorGoldSilver"]
  };

  const groupLabels = {
    cut: ["\u6a21\u5207", "\u88c1\u5207"],
    lamination: ["\u8986\u4eae\u819c", "\u8986\u54d1\u819c"],
    extra: [
      "\u7eaf\u70eb\u91d1",
      "\u70eb\u9559\u5c04\u94f6",
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

function roundMoney(value) {
  return Math.round(value);
}

function formatPrice(value) {
  if (Number.isInteger(value)) {
    return String(value);
  }
  return value.toFixed(2).replace(/\.?0+$/, "");
}

function getAreaTier(area) {
  if (area <= 1) {
    return "micro";
  }
  return Math.max(0, Math.floor(area / SIZE_TIER_AREA));
}

function getTierPrice(area, quantity, tierPrices) {
  const tier = getAreaTier(area);
  const priceSet = tierPrices[quantity];
  if (tier === "micro") {
    return priceSet.micro ?? priceSet[0];
  }

  if (priceSet[tier] != null) {
    return priceSet[tier];
  }

  const numericTiers = Object.keys(priceSet)
    .filter((key) => key !== "micro")
    .map((key) => Number(key))
    .sort((left, right) => left - right);
  const lastTier = numericTiers[numericTiers.length - 1];
  const lastPrice = priceSet[lastTier];
  const prevTier = numericTiers[numericTiers.length - 2] ?? lastTier;
  const prevPrice = priceSet[prevTier];
  const stepPrice = lastTier === prevTier ? 0 : lastPrice - prevPrice;
  return lastPrice + stepPrice * (tier - lastTier);
}

function getBrightBasePrice(area, quantity) {
  return roundMoney(getTierPrice(area, quantity, BRIGHT_BASE_TIER_PRICES));
}

function getBrightColorGoldPrice(area, quantity) {
  return roundMoney(getTierPrice(area, quantity, BRIGHT_COLOR_GOLD_TIER_PRICES));
}

function getBrightPrice(area, quantity, extraCode) {
  const basePrice = getBrightBasePrice(area, quantity);

  if (extraCode === "none") {
    return basePrice;
  }

  if (extraCode === "colorGoldSilver") {
    return getBrightColorGoldPrice(area, quantity);
  }

  const fullFoilPrice = getBrightColorGoldPrice(area, quantity);
  const fullFoilSurcharge = fullFoilPrice - basePrice;
  const ratio = FOIL_SURCHARGE_RATIOS[extraCode][quantity];
  return roundMoney(basePrice + fullFoilSurcharge * ratio);
}

function sortDimensions(size) {
  const sides = [size.width, size.height].sort((left, right) => left - right);
  return [sides[0], sides[1]];
}

function interpolateDimensionSamples(size, laminationCode, extraCode, quantity) {
  const laminationRules = DIMENSION_SAMPLE_RULES[laminationCode];
  if (!laminationRules) {
    return null;
  }

  const extraRules = laminationRules[extraCode];
  if (!extraRules) {
    return null;
  }

  const samples = extraRules[quantity];
  if (!Array.isArray(samples) || samples.length === 0) {
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

function getUnitPrice(size, laminationCode, extraCode, quantity) {
  const dimensionPrice = interpolateDimensionSamples(size, laminationCode, extraCode, quantity);
  if (typeof dimensionPrice === "number") {
    return dimensionPrice;
  }

  const area = getArea(size);
  const normalizedExtra = extraCode || "none";
  const brightPrice = getBrightPrice(area, quantity, normalizedExtra);

  if (laminationCode === "glossy") {
    return brightPrice;
  }

  const ratio = MATTE_RATIOS[normalizedExtra][quantity];
  return roundMoney(brightPrice * ratio);
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
  const area = getArea(size);

  const lines = [];
  lines.push(buildHeader(product, size, cutCode, laminationCode, extraCode));

  QUANTITY_PLANS.forEach((quantity) => {
    const unitPrice = getUnitPrice(size, laminationCode, extraCode, quantity);
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
