const pricingConfig = {
  basePrice: {
    "铜板纸不干胶": 50,
    "透明不干胶": 62,
    "书写纸不干胶": 56
  },
  areaFee: [
    { max: 25, fee: 0 },
    { max: 64, fee: 8 },
    { max: 120, fee: 18 },
    { max: Infinity, fee: 32 }
  ],
  quantityFee: {
    500: 19,
    1000: 31,
    2000: 60
  },
  craftFee: {
    "模切": 0,
    "裁切": 3,
    "覆亮膜": 0,
    "覆哑膜": 4,
    "不覆膜": -2,
    "配刮刮膜": 9,
    "粘钻刮刮膜": 15,
    "烫金": 18
  }
};

const quantityPlans = [500, 1000, 2000];

const productType = document.getElementById("productType");
const sizeInput = document.getElementById("sizeInput");
const quantityBase = document.getElementById("quantityBase");
const styleCount = document.getElementById("styleCount");
const customerName = document.getElementById("customerName");
const resultText = document.getElementById("resultText");
const calcButton = document.getElementById("calcButton");
const resetButton = document.getElementById("resetButton");
const copyButton = document.getElementById("copyButton");
const chips = Array.from(document.querySelectorAll(".chip"));

function getActiveValue(groupName) {
  const active = document.querySelector(`.chip.active[data-group="${groupName}"]`);
  return active ? active.dataset.value : "";
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
  return pricingConfig.areaFee.find((item) => area <= item.max).fee;
}

function buildPrice(product, area, crafts, qty, count) {
  const productFee = pricingConfig.basePrice[product] || 0;
  const areaFee = getAreaFee(area);
  const quantityFee = pricingConfig.quantityFee[qty] || 0;
  const craftTotal = crafts.reduce((sum, craft) => sum + (pricingConfig.craftFee[craft] || 0), 0);
  return (productFee + areaFee + quantityFee + craftTotal) * count;
}

function generateText() {
  const size = parseSize(sizeInput.value);
  if (!size) {
    resultText.value = "请输入正确尺寸，格式例如 5*5";
    return;
  }

  const product = productType.value;
  const count = Math.max(1, Number(styleCount.value) || 1);
  const cut = getActiveValue("cut");
  const lamination = getActiveValue("lamination");
  const extra = getActiveValue("extra");
  const crafts = [cut, lamination, extra].filter(Boolean);
  const area = size.width * size.height;
  const selectedQty = Number(quantityBase.value);

  const lines = [];
  const titleCraft = [cut, lamination].filter(Boolean).join("-");
  const header = `${product} - ${size.width}*${size.height}厘米 - ${titleCraft}${extra ? `-${extra}` : ""}--`;
  lines.push(header);

  quantityPlans.forEach((qty) => {
    const price = buildPrice(product, area, crafts, qty, count);
    lines.push(`${count}款 ${qty}个，共${price}元${qty === selectedQty ? "  <- 当前选择" : ""}`);
  });

  lines.push("包邮，免费设计呢~（偏远地区需补邮费）");
  lines.push("");
  lines.push("亲 现在下单可以参加活动折扣哦！");

  if (customerName.value.trim()) {
    lines.push(`客户旺旺：${customerName.value.trim()}`);
  }

  resultText.value = lines.join("\n");
}

function resetForm() {
  productType.value = "铜板纸不干胶";
  sizeInput.value = "5*5";
  quantityBase.value = "500";
  styleCount.value = "1";
  customerName.value = "";

  chips.forEach((chip) => {
    chip.classList.remove("active");
  });

  document.querySelector('.chip[data-group="cut"][data-value="模切"]').classList.add("active");
  document.querySelector('.chip[data-group="lamination"][data-value="覆亮膜"]').classList.add("active");
  generateText();
}

chips.forEach((chip) => {
  chip.addEventListener("click", () => {
    const { group } = chip.dataset;
    if (group === "extra") {
      chip.classList.toggle("active");
    } else {
      document.querySelectorAll(`.chip[data-group="${group}"]`).forEach((item) => {
        item.classList.remove("active");
      });
      chip.classList.add("active");
    }
    generateText();
  });
});

[productType, sizeInput, quantityBase, styleCount, customerName].forEach((element) => {
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
  } catch (error) {
    copyButton.textContent = "复制失败";
    window.setTimeout(() => {
      copyButton.textContent = "点击复制";
    }, 1500);
  }
});

generateText();
