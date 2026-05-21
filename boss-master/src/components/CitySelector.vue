<template>
  <!-- 遮罩层 -->
  <teleport to="body">
    <div
      v-if="visible"
      class="city-selector-overlay"
      @click="handleOverlayClick"
    >
      <!-- 弹窗容器 -->
      <div class="city-selector-modal" @click.stop>
        <!-- 顶部操作栏 -->
        <div class="modal-header">
          <div class="header-left">
            <button class="province-btn">按省份选择</button>
            <el-select
              v-model="selectedProvince"
              placeholder="省份"
              class="province-select"
              clearable
            >
              <el-option
                v-for="province in provinces"
                :key="province"
                :label="province"
                :value="province"
              />
            </el-select>
          </div>
          <div class="header-right">
            <div class="search-wrapper">
              <span class="search-label">直接搜索</span>
              <div class="search-input-wrapper">
                <svg
                  class="search-icon"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <circle cx="11" cy="11" r="8"></circle>
                  <path d="m21 21-4.35-4.35"></path>
                </svg>
                <input
                  v-model="searchKeyword"
                  type="text"
                  placeholder="城市名称"
                  class="search-input"
                  @input="handleSearch"
                />
              </div>
            </div>
          </div>
          <button class="close-btn" @click="handleClose">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <!-- 内容区域 -->
        <div class="modal-content">
          <!-- 热门城市 -->
          <div class="section">
            <h3 class="section-title">热门城市</h3>
            <div class="city-grid">
              <button
                v-for="city in hotCities"
                :key="city"
                class="city-btn"
                :class="{ active: selectedCity === city }"
                @click="selectCity(city)"
              >
                {{ city }}
              </button>
            </div>
          </div>

          <!-- 按字母选择 -->
          <div class="section">
            <h3 class="section-title">按字母选择:</h3>
            <!-- 字母导航栏 -->
            <div class="alphabet-nav">
              <span
                v-for="letter in alphabet"
                :key="letter"
                class="alphabet-item"
                :class="{ active: activeLetter === letter }"
                @click="scrollToLetter(letter)"
              >
                {{ letter }}
              </span>
            </div>

            <!-- 按字母分组的城市列表 -->
            <div class="city-by-letter">
              <div
                v-for="(cities, letter) in citiesByLetter"
                :key="letter"
                :id="`letter-${letter}`"
                class="letter-group"
              >
                <h4 class="letter-title">{{ letter }}</h4>
                <div class="city-list">
                  <button
                    v-for="city in cities.slice(0, showMoreCount[letter] || 10)"
                    :key="city"
                    class="city-item"
                    :class="{ active: selectedCity === city }"
                    @click="selectCity(city)"
                  >
                    {{ city }}
                  </button>
                  <button
                    v-if="cities.length > 10"
                    class="more-btn"
                    @click="toggleMore(letter)"
                  >
                    {{
                      showMoreCount[letter] >= cities.length ? "收起" : "更多"
                    }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { ref, computed, watch } from "vue";

const props = defineProps({
  visible: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["update:visible", "select"]);

// 选中的省份
const selectedProvince = ref("");

// 搜索关键词
const searchKeyword = ref("");

// 当前选中的城市
const selectedCity = ref("");

// 当前激活的字母
const activeLetter = ref("");

// 显示更多城市的数量
const showMoreCount = ref({});

// 热门城市
const hotCities = [
  "全国",
  "北京",
  "上海",
  "广州",
  "深圳",
  "杭州",
  "天津",
  "西安",
  "苏州",
  "武汉",
  "厦门",
  "长沙",
  "成都",
  "郑州",
  "重庆",
  "佛山",
  "合肥",
  "济南",
  "青岛",
  "南京",
  "东莞",
  "昆明",
  "南昌",
  "石家庄",
  "宁波",
  "福州",
];

// 省份列表
const provinces = [
  "北京",
  "上海",
  "天津",
  "重庆",
  "河北",
  "山西",
  "内蒙古",
  "辽宁",
  "吉林",
  "黑龙江",
  "江苏",
  "浙江",
  "安徽",
  "福建",
  "江西",
  "山东",
  "河南",
  "湖北",
  "湖南",
  "广东",
  "广西",
  "海南",
  "四川",
  "贵州",
  "云南",
  "西藏",
  "陕西",
  "甘肃",
  "青海",
  "宁夏",
  "新疆",
  "台湾",
  "香港",
  "澳门",
];

// 字母导航（缺少I和O）
const alphabet = [
  "A",
  "B",
  "C",
  "D",
  "E",
  "F",
  "G",
  "H",
  "J",
  "K",
  "L",
  "M",
  "N",
  "P",
  "Q",
  "R",
  "S",
  "T",
  "W",
  "X",
  "Y",
  "Z",
];

// 按字母分组的城市数据
const citiesByLetter = {
  A: [
    "鞍山",
    "阿拉善盟",
    "安康",
    "阿克苏地区",
    "阿勒泰地区",
    "阿拉尔",
    "阿里地区",
    "安阳",
    "安庆",
    "安顺",
  ],
  B: [
    "北京",
    "白城",
    "白山",
    "本溪",
    "包头",
    "巴彦淖尔",
    "保定",
    "宝鸡",
    "滨州",
    "巴音郭楞蒙古自治州",
  ],
  C: [
    "重庆",
    "长春",
    "朝阳",
    "赤峰",
    "承德",
    "沧州",
    "长治",
    "昌吉回族自治州",
    "昌都",
    "常州",
    "滁州",
    "池州",
    "长沙",
  ],
  D: [
    "大庆",
    "大兴安岭地区",
    "大连",
    "丹东",
    "大同",
    "德州",
    "东营",
    "定西",
    "达州",
    "德阳",
    "东莞",
    "东沙群岛",
  ],
  E: ["鄂尔多斯", "鄂州", "恩施土家族苗族自治州"],
  F: ["抚顺", "阜新", "阜阳", "福州", "抚州", "佛山", "防城港"],
  G: [
    "果洛藏族自治州",
    "甘南藏族自治州",
    "固原",
    "赣州",
    "贵阳",
    "广安",
    "广元",
    "甘孜藏族自治州",
    "广州",
    "桂林",
  ],
  H: [
    "哈尔滨",
    "鹤岗",
    "黑河",
    "呼伦贝尔",
    "葫芦岛",
    "衡水",
    "邯郸",
    "呼和浩特",
    "淮安",
    "杭州",
    "湖州",
    "合肥",
    "淮南",
    "淮北",
    "黄山",
    "菏泽",
    "鹤壁",
    "黄石",
    "黄冈",
    "怀化",
    "惠州",
    "河源",
    "贺州",
    "海口",
    "河池",
    "红河哈尼族彝族自治州",
    "汉中",
    "海东",
    "海北藏族自治州",
    "黄南藏族自治州",
    "海南藏族自治州",
    "海西蒙古族藏族自治州",
  ],
  J: [
    "鸡西",
    "佳木斯",
    "吉林",
    "锦州",
    "晋中",
    "晋城",
    "济南",
    "济宁",
    "焦作",
    "荆州",
    "荆门",
    "吉安",
    "景德镇",
    "九江",
    "江门",
    "揭阳",
    "金昌",
    "酒泉",
  ],
  K: ["昆明", "开封", "克拉玛依", "喀什地区", "克孜勒苏柯尔克孜自治州"],
  L: [
    "辽源",
    "辽阳",
    "廊坊",
    "临汾",
    "吕梁",
    "聊城",
    "洛阳",
    "漯河",
    "娄底",
    "六安",
    "六盘水",
    "乐山",
    "凉山彝族自治州",
    "丽江",
    "临沧",
    "拉萨",
    "林芝",
    "兰州",
    "陇南",
  ],
  M: ["牡丹江", "马鞍山", "茂名", "梅州", "绵阳", "眉山"],
  N: [
    "南京",
    "南通",
    "宁波",
    "南平",
    "宁德",
    "南昌",
    "南阳",
    "内江",
    "南充",
    "怒江傈僳族自治州",
    "那曲",
    "南宁",
    "内蒙",
  ],
  P: ["盘锦", "平顶山", "濮阳", "萍乡", "攀枝花", "普洱"],
  Q: ["齐齐哈尔", "七台河", "秦皇岛", "清远", "曲靖", "庆阳"],
  R: ["日照", "日喀则"],
  S: [
    "沈阳",
    "四平",
    "松原",
    "双鸭山",
    "绥化",
    "石家庄",
    "朔州",
    "上海",
    "宿迁",
    "苏州",
    "宿州",
    "三明",
    "上饶",
    "三门峡",
    "商丘",
    "十堰",
    "随州",
    "邵阳",
    "深圳",
    "韶关",
    "汕尾",
    "汕头",
    "三亚",
    "遂宁",
    "山南",
    "商洛",
    "石嘴山",
  ],
  T: [
    "通化",
    "通辽",
    "铁岭",
    "唐山",
    "太原",
    "泰安",
    "铜陵",
    "台州",
    "泰州",
    "铜仁",
    "天津",
    "天水",
    "吐鲁番",
    "塔城地区",
    "图木舒克",
  ],
  W: [
    "乌海",
    "乌兰察布",
    "无锡",
    "温州",
    "芜湖",
    "潍坊",
    "威海",
    "武汉",
    "梧州",
    "文山壮族苗族自治州",
    "渭南",
    "武威",
    "吴忠",
    "乌鲁木齐",
    "五家渠",
  ],
  X: [
    "兴安盟",
    "锡林郭勒盟",
    "徐州",
    "宣城",
    "新余",
    "信阳",
    "襄阳",
    "孝感",
    "湘潭",
    "湘西土家族苗族自治州",
    "西双版纳傣族自治州",
    "西安",
    "西宁",
    "新疆",
  ],
  Y: [
    "延边朝鲜族自治州",
    "营口",
    "阳泉",
    "运城",
    "盐城",
    "扬州",
    "宜春",
    "鹰潭",
    "烟台",
    "宜昌",
    "岳阳",
    "益阳",
    "永州",
    "阳江",
    "云浮",
    "玉林",
    "宜宾",
    "雅安",
    "玉溪",
    "银川",
    "伊犁哈萨克自治州",
  ],
  Z: [
    "张家口",
    "镇江",
    "舟山",
    "漳州",
    "淄博",
    "枣庄",
    "郑州",
    "驻马店",
    "株洲",
    "张家界",
    "珠海",
    "中山",
    "湛江",
    "肇庆",
    "自贡",
    "资阳",
    "遵义",
    "昭通",
    "中卫",
    "张掖",
  ],
};

// 过滤后的城市列表（根据搜索和省份）
const filteredCitiesByLetter = computed(() => {
  let result = { ...citiesByLetter };

  // 根据省份筛选
  if (selectedProvince.value) {
    // 这里可以根据省份筛选城市，简化处理
    // 实际应该根据省份-城市映射关系筛选
  }

  // 根据搜索关键词筛选
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase();
    const filtered = {};
    for (const [letter, cities] of Object.entries(result)) {
      const matched = cities.filter((city) =>
        city.toLowerCase().includes(keyword)
      );
      if (matched.length > 0) {
        filtered[letter] = matched;
      }
    }
    result = filtered;
  }

  return result;
});

// 切换显示更多
const toggleMore = (letter) => {
  const currentCount = showMoreCount.value[letter] || 10;
  const totalCount = citiesByLetter[letter]?.length || 0;
  showMoreCount.value[letter] = currentCount >= totalCount ? 10 : totalCount;
};

// 滚动到指定字母
const scrollToLetter = (letter) => {
  activeLetter.value = letter;
  const element = document.getElementById(`letter-${letter}`);
  if (element) {
    element.scrollIntoView({ behavior: "smooth", block: "start" });
  }
};

// 选择城市
const selectCity = (city) => {
  selectedCity.value = city;
  emit("select", city);
  handleClose();
};

// 搜索处理
const handleSearch = () => {
  // 搜索逻辑已在 computed 中处理
};

// 关闭弹窗
const handleClose = () => {
  emit("update:visible", false);
  // 重置状态
  searchKeyword.value = "";
  selectedProvince.value = "";
  selectedCity.value = "";
  activeLetter.value = "";
  showMoreCount.value = {};
};

// 点击遮罩层关闭
const handleOverlayClick = () => {
  handleClose();
};

// 监听 visible 变化
watch(
  () => props.visible,
  (newVal) => {
    if (newVal) {
      // 弹窗打开时，重置搜索和选择
      searchKeyword.value = "";
      selectedProvince.value = "";
    }
  }
);
</script>

<style scoped>
/* 遮罩层 */
.city-selector-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 弹窗容器 */
.city-selector-modal {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  position: relative;
}

/* 顶部操作栏 */
.modal-header {
  padding: 35px 25px;
  min-height: 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  background: linear-gradient(180deg, #4db8c4 0%, #5cc5d1 100%);
  border-radius: 8px 8px 0 0;
  position: relative;
  overflow: hidden;
}

.modal-header::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0,100 L20,80 L40,90 L60,70 L80,85 L100,75 L100,100 Z' fill='rgba(255,255,255,0.15)'/%3E%3C/svg%3E");
  background-size: 200px 100px;
  background-repeat: repeat-x;
  background-position: bottom;
  opacity: 0.4;
  pointer-events: none;
}

.modal-header::after {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  width: 40%;
  height: 100%;
  background-image: radial-gradient(
      circle at 80% 20%,
      rgba(255, 255, 255, 0.15) 0%,
      transparent 50%
    ),
    radial-gradient(
      circle at 85% 30%,
      rgba(255, 255, 255, 0.12) 0%,
      transparent 40%
    ),
    url("data:image/svg+xml,%3Csvg width='200' height='200' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M150,50 Q170,30 190,50 T230,50' stroke='rgba(255,255,255,0.1)' stroke-width='2' fill='none'/%3E%3Cpath d='M160,70 Q180,50 200,70 T240,70' stroke='rgba(255,255,255,0.08)' stroke-width='2' fill='none'/%3E%3Cpath d='M170,90 Q190,70 210,90 T250,90' stroke='rgba(255,255,255,0.06)' stroke-width='2' fill='none'/%3E%3C/svg%3E");
  background-size: 300px 300px, 250px 250px, 200px 200px;
  background-position: 80% 10%, 85% 25%, 90% 40%;
  background-repeat: no-repeat;
  opacity: 0.6;
  pointer-events: none;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
  z-index: 1;
}

.province-btn {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 4px;
  padding: 8px 16px;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  transition: all 0.3s;
}

.province-btn:hover {
  border-color: #00c2c2;
  color: #00c2c2;
}

.province-select {
  width: 150px;
}

.header-right {
  flex: 1;
  display: flex;
  justify-content: flex-end;
  position: relative;
  z-index: 1;
}

.search-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-label {
  font-size: 14px;
  color: #333;
  white-space: nowrap;
  font-weight: 500;
}

.search-input-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 4px;
  padding: 6px 12px;
  min-width: 200px;
}

.search-icon {
  width: 16px;
  height: 16px;
  color: #999;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
  color: #333;
}

.search-input::placeholder {
  color: #999;
}

.close-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #333;
  transition: color 0.3s;
  flex-shrink: 0;
  position: relative;
  z-index: 1;
}

.close-btn svg {
  width: 20px;
  height: 20px;
}

.close-btn:hover {
  color: #333;
}

/* 内容区域 */
.modal-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.section {
  margin-bottom: 30px;
}

.section:last-child {
  margin-bottom: 0;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 16px 0;
}

/* 热门城市网格 */
.city-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
}

.city-btn {
  background: #f5f5f5;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 10px 16px;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  transition: all 0.3s;
  text-align: center;
}

.city-btn:hover {
  border-color: #00c2c2;
  color: #00c2c2;
}

.city-btn.active {
  background: #00c2c2;
  border-color: #00c2c2;
  color: white;
}

/* 字母导航栏 */
.alphabet-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #d0e0e5;
}

.alphabet-item {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 1px solid #d0d0d0;
  border-radius: 4px;
  font-size: 14px;
  color: #999;
  cursor: pointer;
  transition: all 0.3s;
  opacity: 0.6;
}

.alphabet-item:hover {
  border-color: #00c2c2;
  color: #00c2c2;
  opacity: 1;
}

.alphabet-item.active {
  background: #00c2c2;
  border-color: #00c2c2;
  color: white;
  opacity: 1;
}

/* 按字母分组的城市列表 */
.city-by-letter {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.letter-group {
  background: transparent;
  border-radius: 4px;
  padding: 16px 0;
}

.letter-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 12px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}

.city-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.city-item {
  background: #f5f5f5;
  border: 1px solid transparent;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
}

.city-item:hover {
  background: #e8f5f5;
  color: #00c2c2;
}

.city-item.active {
  background: #00c2c2;
  color: white;
}

.more-btn {
  background: white;
  border: 1px solid #d0d0d0;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
}

.more-btn:hover {
  border-color: #00c2c2;
  color: #00c2c2;
}
</style>
