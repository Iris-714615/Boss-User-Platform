<template>
  <div class="company-list-page">
    <!-- 顶部搜索栏 -->
    <div class="search-header">
      <div class="search-container">
        <div class="search-bar-wrapper">
          <div class="search-input-area">
            <el-select
              v-model="jobType"
              placeholder="职位类型"
              class="job-type-select"
              clearable
            >
              <el-option label="全部" value="" />
              <el-option label="全职" value="fulltime" />
              <el-option label="兼职" value="parttime" />
            </el-select>
            <el-input
              v-model="searchKeyword"
              placeholder="搜索职位、公司"
              class="search-input"
              @keyup.enter="handleSearch"
            />
          </div>
          <el-button class="search-btn" type="primary" @click="handleSearch">
            搜索
          </el-button>
        </div>
      </div>
    </div>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <div class="filter-container">
        <!-- 公司地点 -->
        <div class="filter-group">
          <div class="filter-label">公司地点:</div>
          <div class="filter-options">
            <span
              v-for="city in filterData.locations"
              :key="city"
              :class="[
                'filter-option',
                { active: selectedFilters.location === city },
              ]"
              @click="selectFilter('location', city)"
            >
              {{ city }}
            </span>
          </div>
        </div>

        <!-- 行业类型 -->
        <div class="filter-group">
          <div class="filter-label">行业类型:</div>
          <div class="filter-options filter-options-multirow">
            <span
              v-for="industry in filterData.industries"
              :key="industry"
              :class="[
                'filter-option',
                { active: selectedFilters.industry === industry },
              ]"
              @click="selectFilter('industry', industry)"
            >
              {{ industry }}
            </span>
          </div>
        </div>

        <!-- 融资阶段 -->
        <div class="filter-group">
          <div class="filter-label">融资阶段:</div>
          <div class="filter-options">
            <span
              v-for="stage in filterData.fundingStages"
              :key="stage"
              :class="[
                'filter-option',
                { active: selectedFilters.fundingStage === stage },
              ]"
              @click="selectFilter('fundingStage', stage)"
            >
              {{ stage }}
            </span>
          </div>
        </div>

        <!-- 公司规模 -->
        <div class="filter-group">
          <div class="filter-label">公司规模:</div>
          <div class="filter-options">
            <span
              v-for="size in filterData.companySizes"
              :key="size"
              :class="[
                'filter-option',
                { active: selectedFilters.companySize === size },
              ]"
              @click="selectFilter('companySize', size)"
            >
              {{ size }}
            </span>
          </div>
        </div>
      </div>

      <!-- 清空筛选条件 -->
      <div class="clear-filters">
        <span class="clear-link" @click="clearFilters">清空筛选条件</span>
      </div>
    </div>

    <!-- 公司列表内容区域 -->
    <div class="company-content">
      <div class="content-container">
        <!-- 标签页 -->
        <div class="tabs-section">
          <div class="tabs">
            <span
              :class="['tab', { active: activeTab === 'default' }]"
              @click="activeTab = 'default'"
            >
              默认推荐
            </span>
            <span
              :class="['tab', { active: activeTab === 'expectation' }]"
              @click="activeTab = 'expectation'"
            >
              根据求职期望推荐
            </span>
          </div>
        </div>

        <!-- 公司卡片网格 -->
        <div class="company-grid">
          <div
            v-for="company in companyList"
            :key="company.id"
            class="company-card"
            @click="handleCompanyClick(company.id)"
          >
            <div class="company-header">
              <div class="company-logo">
                <div class="logo-placeholder">{{ company.logoText }}</div>
              </div>
              <div class="company-info">
                <h3 class="company-name">{{ company.name }}</h3>
                <div class="company-meta">
                  <span class="meta-item">{{ company.status }}</span>
                  <span class="meta-separator">·</span>
                  <span class="meta-item">{{ company.industry }}</span>
                </div>
              </div>
            </div>
            <div class="hot-job">
              <span class="hot-tag">热招</span>
              <span class="job-info"
                >| {{ company.hotJob.title }} {{ company.hotJob.salary }}</span
              >
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 浮动按钮 -->
    <div class="floating-buttons">
      <button class="float-btn">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="16" x2="12" y2="12"></line>
          <line x1="12" y1="8" x2="12.01" y2="8"></line>
        </svg>
      </button>
      <button class="float-btn">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
          ></path>
          <polyline points="14 2 14 8 20 8"></polyline>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

// 搜索相关
const jobType = ref("");
const searchKeyword = ref("");

// 标签页
const activeTab = ref("default");

// 公司列表数据
const companyList = ref([
  {
    id: 1,
    name: "凯莱英医药集团",
    logoText: "CASYMCHEM",
    status: "已上市",
    industry: "医疗健康",
    hotJob: {
      title: "机器学习研究员 (AI...",
      salary: "20-3...",
    },
  },
  {
    id: 2,
    name: "曼迪匹艾",
    logoText: "MDPI",
    status: "不需要融资",
    industry: "其他行业",
    hotJob: {
      title: "数学类英文学术期刊...",
      salary: "11-22K",
    },
  },
  {
    id: 3,
    name: "经纬恒润",
    logoText: "R",
    status: "已上市",
    industry: "电子/硬...",
    hotJob: {
      title: "自动驾驶系统工程师-...",
      salary: "15-3...",
    },
  },
  {
    id: 4,
    name: "京东世纪贸易有限公司",
    logoText: "京东",
    status: "已上市",
    industry: "互联网",
    hotJob: {
      title: "电商采销经理",
      salary: "20-25K·20薪",
    },
  },
  {
    id: 5,
    name: "融创服务",
    logoText: "sunac",
    status: "已上市",
    industry: "物业管理",
    hotJob: {
      title: "Android/IOS开发工...",
      salary: "15-25K",
    },
  },
  {
    id: 6,
    name: "京东集团",
    logoText: "京东",
    status: "已上市",
    industry: "电子商务",
    hotJob: {
      title: "测试开发高级工程师",
      salary: "25-45K...",
    },
  },
  {
    id: 7,
    name: "天地伟业",
    logoText: "Tiandy",
    status: "不需要融资",
    industry: "计算机软件",
    hotJob: {
      title: "嵌入式软件工程师",
      salary: "20-35K·1...",
    },
  },
  {
    id: 8,
    name: "中科曙光",
    logoText: "Sugon",
    status: "已上市",
    industry: "互联网",
    hotJob: {
      title: "C/C++",
      salary: "20-40K·14薪",
    },
  },
  {
    id: 9,
    name: "爱玛科技集团",
    logoText: "AIMA",
    status: "已上市",
    industry: "汽车研发/制造",
    hotJob: {
      title: "产品经理",
      salary: "15-25K",
    },
  },
  {
    id: 10,
    name: "京东科技集团",
    logoText: "JD",
    status: "已上市",
    industry: "互联网",
    hotJob: {
      title: "Java开发工程师",
      salary: "20-35K",
    },
  },
  {
    id: 11,
    name: "贝壳找房",
    logoText: "贝壳",
    status: "已上市",
    industry: "互联网",
    hotJob: {
      title: "前端开发工程师",
      salary: "18-30K",
    },
  },
  {
    id: 12,
    name: "诺禾致源",
    logoText: "Novogene",
    status: "已上市",
    industry: "医疗健康",
    hotJob: {
      title: "生物信息工程师",
      salary: "15-25K",
    },
  },
]);

// 筛选数据
const filterData = {
  locations: [
    "不限",
    "全国",
    "北京",
    "上海",
    "广州",
    "深圳",
    "杭州",
    "西安",
    "苏州",
    "武汉",
    "厦门",
    "长沙",
    "成都",
    "郑州",
    "重庆",
    "全部城市",
  ],
  industries: [
    "不限",
    "电子商务",
    "游戏",
    "社交网络与媒体",
    "广告营销",
    "大数据",
    "医疗健康",
    "生活服务(O2O)",
    "O2O",
    "旅游",
    "分类信息",
    "音乐/视频/阅读",
    "在线教育",
    "社交网络",
    "人力资源服务",
    "企业服务",
    "信息安全",
    "智能硬件",
    "移动互联网",
    "互联网",
    "计算机软件",
    "通信/网络设备",
    "广告/公关/会展",
    "互联网金融",
    "物流/仓储",
    "进出口贸易",
    "咨询",
    "工程施工",
    "汽车研发/制造",
    "其他行业",
  ],
  fundingStages: [
    "不限",
    "未融资",
    "天使轮",
    "A轮",
    "B轮",
    "C轮",
    "D轮及以上",
    "已上市",
    "不需要融资",
  ],
  companySizes: [
    "不限",
    "0-20人",
    "20-99人",
    "100-499人",
    "500-999人",
    "1000-9999人",
    "10000人以上",
  ],
};

// 选中的筛选条件
const selectedFilters = ref({
  location: "不限",
  industry: "不限",
  fundingStage: "不限",
  companySize: "不限",
});

// 选择筛选条件
const selectFilter = (type, value) => {
  selectedFilters.value[type] = value;
  console.log("筛选条件:", selectedFilters.value);
};

// 清空筛选条件
const clearFilters = () => {
  selectedFilters.value = {
    location: "不限",
    industry: "不限",
    fundingStage: "不限",
    companySize: "不限",
  };
};

// 搜索功能
const handleSearch = () => {
  console.log("搜索:", searchKeyword.value, "职位类型:", jobType.value);
};

// 点击公司卡片
const handleCompanyClick = (companyId) => {
  console.log("点击公司:", companyId);
  // 这里可以跳转到公司详情页
};
</script>

<style scoped>
.company-list-page {
  min-height: 100vh;
  background: #f5f5f5;
}

/* 顶部搜索栏 */
.search-header {
  background: white;
  padding: 20px 40px;
  border-bottom: 1px solid #e0e0e0;
}

.search-container {
  max-width: 1000px;
  margin: 0 auto;
}

.search-bar-wrapper {
  background: white;
  border: 2px solid #00c2c2;
  border-radius: 30px;
  display: flex;
  align-items: center;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 194, 194, 0.1);
  height: 48px;
}

.search-input-area {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0;
  padding: 12px 16px;
}

.job-type-select {
  width: 140px;
  border: none;
  margin-right: 12px;
  padding-right: 12px;
  border-right: 1px solid #e0e0e0;
}

.job-type-select :deep(.el-input__wrapper) {
  box-shadow: none !important;
  border: none !important;
  background: transparent !important;
}

.job-type-select :deep(.el-input__wrapper.is-focus) {
  box-shadow: none !important;
  border: none !important;
}

.job-type-select :deep(.el-input__wrapper:hover) {
  box-shadow: none !important;
  border: none !important;
}

.job-type-select :deep(.el-input__wrapper.is-hover) {
  box-shadow: none !important;
  border: none !important;
}

.job-type-select :deep(.el-input__inner) {
  border: none !important;
  box-shadow: none !important;
  color: #333;
}

.job-type-select :deep(.el-input) {
  border: none !important;
}

.job-type-select :deep(.el-select__wrapper) {
  box-shadow: none !important;
  border: none !important;
}

.search-input {
  flex: 1;
  border: none;
}

.search-input :deep(.el-input__wrapper) {
  box-shadow: none !important;
  border: none !important;
  background: transparent !important;
}

.search-input :deep(.el-input__inner) {
  border: none !important;
  box-shadow: none !important;
  padding: 0 !important;
}

.search-input :deep(.el-input__inner::placeholder) {
  color: #999;
}

.search-btn {
  background: #00c2c2 !important;
  border: none !important;
  border-radius: 0 30px 30px 0 !important;
  padding: 12px 40px !important;
  font-size: 14px;
  font-weight: 600;
  color: white !important;
  height: 48px;
  transition: background 0.3s;
  box-shadow: none !important;
  outline: none !important;
  margin: 0 !important;
  line-height: 1;
}

.search-btn :deep(.el-button__inner) {
  color: white !important;
}

.search-btn :deep(.el-button) {
  border: none !important;
  box-shadow: none !important;
}

.search-btn:hover {
  background: #00a8a8 !important;
  border: none !important;
  box-shadow: none !important;
}

.search-btn:hover :deep(.el-button) {
  border: none !important;
  box-shadow: none !important;
}

.search-btn:focus {
  box-shadow: none !important;
  outline: none !important;
  border: none !important;
}

.search-btn:focus :deep(.el-button) {
  border: none !important;
  box-shadow: none !important;
}

.search-btn:active {
  box-shadow: none !important;
  border: none !important;
}

/* 筛选区域 */
.filter-section {
  background: white;
  padding: 16px 40px;
  margin-bottom: 20px;
  position: relative;
}

.filter-container {
  max-width: 1400px;
  margin: 0 auto;
}

.filter-group {
  margin-bottom: 16px;
  display: flex;
  align-items: flex-start;
}

.filter-group:last-child {
  margin-bottom: 0;
}

.filter-label {
  width: 90px;
  flex-shrink: 0;
  font-size: 14px;
  color: #333;
  font-weight: 500;
  padding-top: 6px;
}

.filter-options {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}

.filter-options-multirow {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-option {
  display: inline-block;
  padding: 5px 14px;
  font-size: 14px;
  color: #666;
  background: #f5f5f5;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.filter-option:hover {
  background: #e8f5f5;
  color: #00c2c2;
}

.filter-option.active {
  background: #00c2c2;
  color: white;
}

/* 清空筛选条件 */
.clear-filters {
  position: absolute;
  bottom: 16px;
  right: 40px;
}

.clear-link {
  font-size: 14px;
  color: #00c2c2;
  cursor: pointer;
  text-decoration: none;
  transition: color 0.3s;
}

.clear-link:hover {
  color: #00a8a8;
  text-decoration: underline;
}

/* 内容区域 */
.company-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px 40px;
}

.content-container {
  background: transparent;
  padding: 0;
}

/* 标签页 */
.tabs-section {
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e0e0e0;
}

.tabs {
  display: flex;
  gap: 32px;
}

.tab {
  font-size: 16px;
  color: #666;
  cursor: pointer;
  padding-bottom: 8px;
  transition: all 0.3s;
  position: relative;
}

.tab:hover {
  color: #00c2c2;
}

.tab.active {
  color: #00c2c2;
  font-weight: 500;
}

.tab.active::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: #00c2c2;
}

/* 公司卡片网格 */
.company-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.company-card {
  background: white;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.company-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.company-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 16px;
}

.company-logo {
  width: 60px;
  height: 60px;
  flex-shrink: 0;
  background: #f5f5f5;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e0e0e0;
}

.logo-placeholder {
  font-size: 12px;
  color: #666;
  font-weight: 500;
  text-align: center;
  line-height: 1.2;
}

.company-info {
  flex: 1;
  min-width: 0;
}

.company-name {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.company-meta {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #999;
}

.meta-item {
  white-space: nowrap;
}

.meta-separator {
  color: #ccc;
}

.hot-job {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #333;
}

.hot-tag {
  background: #fff4e6;
  color: #ff9800;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 2px;
  font-weight: 500;
}

.job-info {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 浮动按钮 */
.floating-buttons {
  position: fixed;
  right: 20px;
  bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  z-index: 100;
}

.float-btn {
  width: 48px;
  height: 48px;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.float-btn svg {
  width: 20px;
  height: 20px;
  color: #666;
}

.float-btn:hover {
  background: #f5f5f5;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
</style>
