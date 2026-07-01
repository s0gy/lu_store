const productConfigElement = document.getElementById("productConfig");
const productConfig = productConfigElement ? JSON.parse(productConfigElement.textContent) : null;

const productType = document.getElementById("productType");
const sizeInput = document.getElementById("sizeInput");
const quantityBase = document.getElementById("quantityBase");
const styleCount = document.getElementById("styleCount");
const resultText = document.getElementById("resultText");
const calcButton = document.getElementById("calcButton");
const resetButton = document.getElementById("resetButton");
const copyButton = document.getElementById("copyButton");
const chips = Array.from(document.querySelectorAll(".chip"));
const extraFields = Array.from(document.querySelectorAll(".extra-field"));

function getSelectedValues(groupName) {
  return chips
    .filter((chip) => chip.dataset.group === groupName && chip.classList.contains("active"))
    .map((chip) => chip.dataset.value);
}

function parseSize(raw) {
  const normalized = raw.replace(/[xX＊]/g, "*").trim();
  const parts = normalized.split("*").map((item) => Number(item.trim()));
  if (parts.length !== 2 || parts.some((item) => Number.isNaN(item) || item <= 0)) {
    return null;
  }
  return { width: parts[0], height: parts[1] };
}

function getAreaFee(area) {
  return productConfig.pricing.area_steps.find((item) => area <= item.max).fee;
}

function getQuantityUnit() {
  const match = productConfig.quantity_label.match(/[（(]([^()（）]+)[)）]/);
  return match ? match[1] : "个";
}

function formatQuantity(qty) {
  return `${qty}${getQuantityUnit()}`;
}

function buildUnitPrice(type, area, crafts, qty) {
  const basePrice = productConfig.pricing.base_price[type] || 0;
  const areaFee = getAreaFee(area);
  const quantityFee = productConfig.pricing.quantity_fee[qty] || 0;
  const craftFee = crafts.reduce((sum, craft) => sum + (productConfig.pricing.craft_fee[craft] || 0), 0);
  return basePrice + areaFee + quantityFee + craftFee;
}

function generateText() {
  const size = parseSize(sizeInput.value);
  if (!size) {
    resultText.value = "请输入正确尺寸，格式例如 5*5";
    return;
  }

  const selectedType = productType.value;
  const selectedQty = Number(quantityBase.value);
  const count = Math.max(1, Number(styleCount.value) || 1);
  const craftValues = productConfig.craft_groups.flatMap((group) => getSelectedValues(group.key));
  const area = size.width * size.height;
  const unitPrice = buildUnitPrice(selectedType, area, craftValues, selectedQty);
  const totalPrice = unitPrice * count;
  const titleCraft = craftValues.join("-");
  const lines = [];

  lines.push(`${selectedType} - ${size.width}*${size.height} - ${titleCraft || "基础工艺"}`);
  extraFields.forEach((field) => {
    if (field.value.trim()) {
      lines.push(`${field.dataset.label}：${field.value.trim()}`);
    }
  });
  lines.push(`${count}款 ${formatQuantity(selectedQty)}，参考报价 ${totalPrice}元`);
  lines.push(`单款参考 ${unitPrice}元，已包含基础排版与 demo 工艺费`);

  productConfig.quantity_options.forEach((qty) => {
    const demoTotal = buildUnitPrice(selectedType, area, craftValues, qty) * count;
    lines.push(`${formatQuantity(qty)}：${demoTotal}元${qty === selectedQty ? "  <- 当前选择" : ""}`);
  });

  productConfig.result_lines.forEach((line) => {
    lines.push(line);
  });

  resultText.value = lines.join("\n");
}

function resetForm() {
  productType.value = productConfig.default_type;
  sizeInput.value = productConfig.default_size;
  quantityBase.value = String(productConfig.default_quantity);
  styleCount.value = String(productConfig.default_style_count);
  extraFields.forEach((field) => {
    const config = (productConfig.extra_fields || []).find((item) => item.key === field.id);
    if (config) {
      field.value = config.default;
    }
  });

  productConfig.craft_groups.forEach((group) => {
    const defaultOptions = group.default_options || [];
    const groupChips = chips.filter((chip) => chip.dataset.group === group.key);
    groupChips.forEach((chip) => {
      chip.classList.toggle("active", defaultOptions.includes(chip.dataset.value));
    });
  });

  generateText();
}

chips.forEach((chip) => {
  chip.addEventListener("click", () => {
    const { group, multi } = chip.dataset;
    if (multi === "true") {
      chip.classList.toggle("active");
    } else {
      chips
        .filter((item) => item.dataset.group === group)
        .forEach((item) => item.classList.remove("active"));
      chip.classList.add("active");
    }
    generateText();
  });
});

[productType, sizeInput, quantityBase, styleCount, ...extraFields].forEach((element) => {
  element.addEventListener("input", generateText);
  element.addEventListener("change", generateText);
});

calcButton.addEventListener("click", generateText);
resetButton.addEventListener("click", resetForm);
copyButton.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(resultText.value);
    copyButton.textContent = "已复制";
    window.setTimeout(() => {
      copyButton.textContent = "点击复制";
    }, 1500);
  } catch (_error) {
    copyButton.textContent = "复制失败";
    window.setTimeout(() => {
      copyButton.textContent = "点击复制";
    }, 1500);
  }
});

if (productConfig) {
  generateText();
}
