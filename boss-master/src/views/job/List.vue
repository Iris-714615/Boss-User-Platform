<template>
  <div class="job-list-page">
    <!-- 顶部头部区域 -->
    <div class="job-header">
      <div class="header-container">
        <!-- 左侧：推荐和添加期望 -->
        <div class="header-left">
          <span class="recommend-tab">推荐</span>
          <span class="divider"></span>
          <div class="add-expectation-btn" @click="handleAddExpectation">
            <div class="add-icon">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
              </svg>
            </div>
            <span class="add-text">添加求职期望</span>
          </div>
        </div>

        <!-- 右侧：搜索栏 -->
        <div class="header-right">
          <div class="search-bar-container">
            <div class="search-input-wrapper">
              <svg
                class="search-icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <circle cx="11" cy="11" r="8"></circle>
                <path d="m21 21-4.35-4.35"></path>
              </svg>
              <el-input
                v-model="searchKeyword"
                placeholder="搜索职位、公司"
                class="search-input-field"
                @keyup.enter="handleSearch"
              />
            </div>
            <div class="map-btn-wrapper" @click="handleMapClick">
              <svg
                class="map-icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                <circle cx="12" cy="10" r="3"></circle>
              </svg>
              <span class="map-text">地图</span>
            </div>
            <el-button class="search-btn" type="primary" @click="handleSearch">
              搜索
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <div class="filter-container">
        <!-- 城市选择按钮 -->
        <button class="city-filter-btn">
          <span class="location-dot">●</span>
          <span class="city-text">天津</span>
        </button>

        <!-- 筛选按钮组 -->
        <div class="filter-buttons">
          <!-- 求职类型 -->
          <div class="filter-btn-wrapper">
            <button
              class="filter-btn"
              :class="{ active: activeFilter === 'jobType' }"
              @click.stop="toggleFilter('jobType')"
            >
              <span>{{ selectedFilters.jobType || "求职类型" }}</span>
              <svg
                class="dropdown-arrow"
                :class="{ rotate: activeFilter === 'jobType' }"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </button>
            <div
              v-if="activeFilter === 'jobType'"
              class="filter-dropdown"
              @click.stop
            >
              <div
                v-for="item in filterData.jobType"
                :key="item"
                class="dropdown-item"
                :class="{ selected: selectedFilters.jobType === item }"
                @click="selectFilter('jobType', item)"
              >
                {{ item }}
              </div>
            </div>
          </div>

          <!-- 薪资待遇 -->
          <div class="filter-btn-wrapper">
            <button
              class="filter-btn"
              :class="{ active: activeFilter === 'salary' }"
              @click.stop="toggleFilter('salary')"
            >
              <span>{{ selectedFilters.salary || "薪资待遇" }}</span>
              <svg
                class="dropdown-arrow"
                :class="{ rotate: activeFilter === 'salary' }"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </button>
            <div
              v-if="activeFilter === 'salary'"
              class="filter-dropdown"
              @click.stop
            >
              <div
                v-for="item in filterData.salary"
                :key="item"
                class="dropdown-item"
                :class="{ selected: selectedFilters.salary === item }"
                @click="selectFilter('salary', item)"
              >
                {{ item }}
              </div>
            </div>
          </div>

          <!-- 工作经验 -->
          <div class="filter-btn-wrapper">
            <button
              class="filter-btn"
              :class="{ active: activeFilter === 'experience' }"
              @click.stop="toggleFilter('experience')"
            >
              <span>{{ selectedFilters.experience || "工作经验" }}</span>
              <svg
                class="dropdown-arrow"
                :class="{ rotate: activeFilter === 'experience' }"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </button>
            <div
              v-if="activeFilter === 'experience'"
              class="filter-dropdown"
              @click.stop
            >
              <div
                v-for="item in filterData.experience"
                :key="item"
                class="dropdown-item"
                :class="{ selected: selectedFilters.experience === item }"
                @click="selectFilter('experience', item)"
              >
                {{ item }}
              </div>
            </div>
          </div>

          <!-- 学历要求 -->
          <div class="filter-btn-wrapper">
            <button
              class="filter-btn"
              :class="{ active: activeFilter === 'education' }"
              @click.stop="toggleFilter('education')"
            >
              <span>{{ selectedFilters.education || "学历要求" }}</span>
              <svg
                class="dropdown-arrow"
                :class="{ rotate: activeFilter === 'education' }"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </button>
            <div
              v-if="activeFilter === 'education'"
              class="filter-dropdown"
              @click.stop
            >
              <div
                v-for="item in filterData.education"
                :key="item"
                class="dropdown-item"
                :class="{ selected: selectedFilters.education === item }"
                @click="selectFilter('education', item)"
              >
                {{ item }}
              </div>
            </div>
          </div>

          <!-- 公司行业 -->
          <div class="filter-btn-wrapper">
            <button
              class="filter-btn"
              :class="{ active: activeFilter === 'industry' }"
              @click.stop="toggleFilter('industry')"
            >
              <span>{{ selectedFilters.industry || "公司行业" }}</span>
              <svg
                class="dropdown-arrow"
                :class="{ rotate: activeFilter === 'industry' }"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </button>
            <div
              v-if="activeFilter === 'industry'"
              class="filter-dropdown filter-dropdown-large"
              @click.stop
            >
              <div
                v-for="(items, category) in filterData.industry"
                :key="category"
                class="industry-category"
              >
                <div class="category-title">{{ category }}</div>
                <div class="industry-items">
                  <div
                    v-for="item in items"
                    :key="item"
                    class="dropdown-item"
                    :class="{ selected: selectedFilters.industry === item }"
                    @click="selectFilter('industry', item)"
                  >
                    {{ item }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 公司规模 -->
          <div class="filter-btn-wrapper">
            <button
              class="filter-btn"
              :class="{ active: activeFilter === 'companySize' }"
              @click.stop="toggleFilter('companySize')"
            >
              <span>{{ selectedFilters.companySize || "公司规模" }}</span>
              <svg
                class="dropdown-arrow"
                :class="{ rotate: activeFilter === 'companySize' }"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </button>
            <div
              v-if="activeFilter === 'companySize'"
              class="filter-dropdown"
              @click.stop
            >
              <div
                v-for="item in filterData.companySize"
                :key="item"
                class="dropdown-item"
                :class="{ selected: selectedFilters.companySize === item }"
                @click="selectFilter('companySize', item)"
              >
                {{ item }}
              </div>
            </div>
          </div>
        </div>

        <!-- 清空按钮 -->
        <button class="clear-filter-btn" @click="clearFilters">清空</button>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="job-content">
      <div class="content-container">
        <!-- 左侧：职位列表 -->
        <div class="job-list-section" v-loading="loading">
          <!-- 空数据提示 -->
          <div v-if="!loading && jobList.length === 0" class="empty-state">
            <p>暂无职位数据</p>
          </div>
          <!-- 职位列表 -->
          <div
            v-for="job in jobList"
            :key="job.id"
            :class="['job-card', { active: selectedJobId === job.id }]"
            @click="selectJob(job.id)"
          >
            <div class="job-card-header">
              <h3 class="job-title">{{ job.title }}</h3>
              <span class="job-salary">{{ job.salary }}</span>
            </div>
            <div class="job-tags">
              <span class="tag" v-for="tag in job.tags" :key="tag">{{
                tag
              }}</span>
            </div>
            <div class="job-company">
              <span class="company-name">{{ job.company }}</span>
            </div>
            <div class="job-location">{{ job.location }}</div>
          </div>
          <!-- 分页组件 -->
          <div v-if="!loading && jobList.length > 0" class="pagination-wrapper">
            <el-pagination
              v-model:current-page="pagination.page"
              :page-size="pagination.page_size"
              :total="pagination.count"
              :page-sizes="[10, 20, 50, 100]"
              layout="total, prev, pager, next, jumper"
              @current-change="handlePageChange"
              @size-change="
                (size) => {
                  pagination.page_size = size;
                  pagination.page = 1;
                  loadJobList();
                }
              "
            />
          </div>
        </div>

        <!-- 右侧：职位详情 -->
        <div class="job-detail-section">
          <div v-if="selectedJob" class="job-detail-card">
            <div class="detail-header">
              <h2 class="detail-title">{{ selectedJob.title }}</h2>
              <span class="detail-salary">{{ selectedJob.salary }}</span>
            </div>
            <div class="detail-attributes">
              <div class="attribute-item">
                <svg
                  class="attr-icon"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"
                  ></path>
                  <circle cx="12" cy="10" r="3"></circle>
                </svg>
                <span>{{ selectedJob.location }}</span>
              </div>
              <div class="attribute-item">
                <svg
                  class="attr-icon"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                <span>{{ selectedJob.experience }}</span>
              </div>
              <div class="attribute-item">
                <svg
                  class="attr-icon"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                  <path
                    d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"
                  ></path>
                </svg>
                <span>{{ selectedJob.education }}</span>
              </div>
            </div>
            <div class="detail-actions">
              <button class="collect-btn">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"
                  ></path>
                </svg>
                收藏
              </button>
              <button class="communicate-btn">立即沟通</button>
            </div>
            <div class="detail-description">
              <h3 class="desc-title">职位描述</h3>
              <div class="desc-tags">
                <span
                  class="desc-tag"
                  v-for="tag in selectedJob.descTags"
                  :key="tag"
                  >{{ tag }}</span
                >
              </div>
              <div class="desc-content">
                <p
                  v-for="(item, index) in selectedJob.description"
                  :key="index"
                >
                  {{ item }}
                </p>
              </div>
            </div>
            <div class="detail-footer">
              <button class="share-btn">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path
                    d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z"
                  />
                </svg>
                微信扫码分享
              </button>
              <button class="report-btn">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"
                  ></path>
                  <line x1="12" y1="9" x2="12" y2="13"></line>
                  <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
                举报
              </button>
            </div>
          </div>
          <div v-else class="job-detail-empty">
            <p>请选择一个职位查看详情</p>
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
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import { http } from "@/utils/request";
import { ElMessage } from "element-plus";

// 搜索关键词
const searchKeyword = ref("");

// 选中的职位ID
const selectedJobId = ref(null);

// 加载状态
const loading = ref(false);

// 分页信息
const pagination = ref({
  page: 1,
  page_size: 20,
  total_pages: 1,
  count: 0,
  has_next: false,
  has_previous: false,
});

// 筛选数据
const filterData = {
  jobType: ["不限", "全职", "兼职"],
  salary: ["不限", "3K以下", "3-5K", "5-10K", "10-20K", "20-50K", "50K以上"],
  experience: [
    "不限",
    "在校生",
    "应届生",
    "经验不限",
    "1年以内",
    "1-3年",
    "3-5年",
    "5-10年",
    "10年以上",
  ],
  education: [
    "不限",
    "初中及以下",
    "中专/中技",
    "高中",
    "大专",
    "本科",
    "硕士",
    "博士",
  ],
  industry: {
    "互联网/AI": [
      "互联网",
      "生活服务(O2O)",
      "游戏",
      "云计算",
      "大数据",
      "新零售",
      "电子商务",
      "企业服务",
      "社交网络与媒体",
      "在线教育",
      "广告营销",
      "信息安全",
      "计算机软件",
      "医疗健康",
      "人工智能",
      "计算机服务",
      "物联网",
    ],
    "电子/通信/半导体": [
      "半导体/芯片",
      "智能硬件/消费电子",
      "电子/硬件开发",
      "运营商/增值服务",
      "通信/网络设备",
      "计算机硬件",
    ],
  },
  companySize: [
    "不限",
    "0-20人",
    "20-99人",
    "100-499人",
    "500-999人",
    "1000-9999人",
    "10000人以上",
  ],
};

// 当前打开的筛选菜单
const activeFilter = ref(null);

// 选中的筛选值
const selectedFilters = ref({
  jobType: null,
  salary: null,
  experience: null,
  education: null,
  industry: null,
  companySize: null,
});

// 切换筛选菜单
const toggleFilter = (filterType) => {
  if (activeFilter.value === filterType) {
    activeFilter.value = null;
  } else {
    activeFilter.value = filterType;
  }
};

// 选择筛选值
const selectFilter = (filterType, value) => {
  selectedFilters.value[filterType] = value;
  activeFilter.value = null;
  // 重置到第一页并重新加载数据
  pagination.value.page = 1;
  loadJobList();
};

// 清空筛选
const clearFilters = () => {
  selectedFilters.value = {
    jobType: null,
    salary: null,
    experience: null,
    education: null,
    industry: null,
    companySize: null,
  };
  activeFilter.value = null;
  // 重置到第一页并重新加载数据
  pagination.value.page = 1;
  loadJobList();
};

// 点击外部关闭下拉菜单
const handleClickOutside = (event) => {
  if (!event.target.closest(".filter-btn-wrapper")) {
    activeFilter.value = null;
  }
};

// 监听点击事件
onMounted(() => {
  document.addEventListener("click", handleClickOutside);
  // 初始化加载数据
  loadJobList();
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});

// 监听分页变化
const handlePageChange = (page) => {
  pagination.value.page = page;
  loadJobList();
  // 滚动到顶部
  window.scrollTo({ top: 0, behavior: "smooth" });
};

// 职位列表数据
const jobList = ref([]);

// 将后端数据映射到前端格式
const mapJobData = (backendJob) => {
  // 构建标签数组
  const tags = [];
  if (backendJob.type_display) tags.push(backendJob.type_display);
  if (backendJob.working_display) tags.push(backendJob.working_display);
  if (backendJob.education) tags.push(backendJob.education);
  if (backendJob.label) tags.push(backendJob.label);

  return {
    id: backendJob.id,
    title: backendJob.title || "",
    salary: backendJob.money || "",
    tags: tags,
    company: backendJob.company_name || "",
    location: backendJob.full_location || backendJob.city_name || "",
    experience: backendJob.working_display || "",
    education: backendJob.education || "",
    descTags: backendJob.label ? [backendJob.label] : [],
    description: backendJob.description
      ? backendJob.description.split("\n").filter((item) => item.trim())
      : [],
    // 保留后端原始数据，用于详情展示
    rawData: backendJob,
  };
};

// 加载职位列表
const loadJobList = async () => {
  try {
    loading.value = true;

    // 构建查询参数
    const params = {
      page: pagination.value.page,
      page_size: pagination.value.page_size,
    };

    // 添加搜索关键词
    if (searchKeyword.value) {
      params.query = searchKeyword.value;
    }

    // 添加筛选条件
    if (
      selectedFilters.value.jobType &&
      selectedFilters.value.jobType !== "不限"
    ) {
      // 将中文类型转换为数字：全职=1, 兼职=2
      if (selectedFilters.value.jobType === "全职") {
        params.type = 1;
      } else if (selectedFilters.value.jobType === "兼职") {
        params.type = 2;
      }
    }

    if (
      selectedFilters.value.salary &&
      selectedFilters.value.salary !== "不限"
    ) {
      params.salary = selectedFilters.value.salary;
    }

    if (
      selectedFilters.value.experience &&
      selectedFilters.value.experience !== "不限"
    ) {
      params.experience = selectedFilters.value.experience;
    }

    if (
      selectedFilters.value.education &&
      selectedFilters.value.education !== "不限"
    ) {
      params.education = selectedFilters.value.education;
    }

    if (
      selectedFilters.value.industry &&
      selectedFilters.value.industry !== "不限"
    ) {
      params.industry = selectedFilters.value.industry;
    }

    if (
      selectedFilters.value.companySize &&
      selectedFilters.value.companySize !== "不限"
    ) {
      params.company_size = selectedFilters.value.companySize;
    }

    // 调用接口
    const response = await http.get("/search-dsl/search/", params);

    if (response.code === 200) {
      // 映射数据
      jobList.value = response.data.map(mapJobData);

      // 更新分页信息
      if (response.pagination) {
        pagination.value = {
          page: response.pagination.page || 1,
          page_size: response.pagination.page_size || 20,
          total_pages: response.pagination.total_pages || 1,
          count: response.pagination.count || 0,
          has_next: response.pagination.has_next || false,
          has_previous: response.pagination.has_previous || false,
        };
      }

      // 自动选中第一个职位
      if (jobList.value.length > 0) {
        // 如果当前选中的职位不在新列表中，则选中第一个
        const currentJobExists = jobList.value.some(
          (job) => job.id === selectedJobId.value
        );
        if (!currentJobExists) {
          selectedJobId.value = jobList.value[0].id;
        }
      } else {
        // 如果没有数据，清空选中状态
        selectedJobId.value = null;
      }
    } else {
      ElMessage.error(response.message || "获取职位列表失败");
      jobList.value = [];
      selectedJobId.value = null;
    }
  } catch (error) {
    console.error("加载职位列表失败:", error);
    ElMessage.error("加载职位列表失败，请稍后重试");
    jobList.value = [];
    selectedJobId.value = null;
  } finally {
    loading.value = false;
  }
};

// 选中的职位详情
const selectedJob = computed(() => {
  return jobList.value.find((job) => job.id === selectedJobId.value);
});

// 选择职位
const selectJob = (jobId) => {
  selectedJobId.value = jobId;
};

// 搜索功能
const handleSearch = () => {
  // 重置到第一页并重新加载数据
  pagination.value.page = 1;
  loadJobList();
};

// 地图点击
const handleMapClick = () => {
  console.log("打开地图");
};

// 添加求职期望
const handleAddExpectation = () => {
  console.log("添加求职期望");
};
</script>

<style scoped>
.job-list-page {
  min-height: 100vh;
  background: #f5f5f5;
  margin: 0;
  padding: 0;
}

/* 头部区域 */
.job-header {
  background: linear-gradient(180deg, #1a4d5c 0%, #1e3a5f 100%);
  padding: 20px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 30px;
}

/* 左侧区域 */
.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-shrink: 0;
}

.recommend-tab {
  font-size: 16px;
  font-weight: 500;
  background: linear-gradient(135deg, #00c2c2 0%, #4dd0e1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  cursor: pointer;
  transition: opacity 0.3s;
}

.recommend-tab:hover {
  opacity: 0.8;
}

.divider {
  width: 1px;
  height: 20px;
  background: rgba(255, 255, 255, 0.3);
}

.add-expectation-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: opacity 0.3s;
  color: white;
}

.add-expectation-btn:hover {
  opacity: 0.8;
}

.add-icon {
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #333;
  flex-shrink: 0;
}

.add-icon svg {
  width: 14px;
  height: 14px;
}

.add-text {
  font-size: 14px;
  color: white;
  white-space: nowrap;
}

/* 右侧搜索区域 */
.header-right {
  flex: 1;
  max-width: 800px;
}

.search-bar-container {
  background: white;
  border: 1px solid #00c2c2;
  border-radius: 30px;
  padding: 0;
  display: flex;
  align-items: center;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 194, 194, 0.1);
}

.search-input-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
}

.search-icon {
  width: 20px;
  height: 20px;
  color: #999;
  flex-shrink: 0;
}

.search-input-field {
  flex: 1;
  border: none;
}

.search-input-field :deep(.el-input__wrapper) {
  box-shadow: none !important;
  border: none !important;
  background: transparent !important;
  padding: 0 !important;
}

.search-input-field :deep(.el-input__inner) {
  border: none !important;
  box-shadow: none !important;
  padding: 0 !important;
  font-size: 14px;
  color: #333;
}

.search-input-field :deep(.el-input__inner::placeholder) {
  color: #999;
}

.map-btn-wrapper {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 12px 16px;
  cursor: pointer;
  transition: background 0.3s;
  color: #666;
  border-left: 1px solid #f0f0f0;
}

.map-btn-wrapper:hover {
  background: #f5f5f5;
}

.map-icon {
  width: 18px;
  height: 18px;
  color: #999;
  flex-shrink: 0;
}

.map-text {
  font-size: 14px;
  color: #666;
  white-space: nowrap;
}

.search-btn {
  background: #00c2c2 !important;
  border: none !important;
  border-radius: 0 30px 30px 0 !important;
  padding: 12px 32px !important;
  font-size: 14px;
  font-weight: 500;
  color: white !important;
  height: 100%;
  transition: background 0.3s;
}

.search-btn:hover {
  background: #00a8a8 !important;
}

/* 筛选区域 */
.filter-section {
  background: #e0f2f7;
  padding: 16px 0;
}

.filter-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

/* 城市选择按钮 */
.city-filter-btn {
  background: #b3e5fc;
  border: none;
  border-radius: 6px;
  padding: 8px 16px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: background 0.3s;
  font-size: 14px;
}

.city-filter-btn:hover {
  background: #81d4fa;
}

.location-dot {
  color: #00c2c2;
  font-size: 16px;
  line-height: 1;
}

.city-text {
  color: #00c2c2;
  font-weight: 500;
}

/* 筛选按钮组 */
.filter-buttons {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  flex-wrap: wrap;
}

.filter-btn-wrapper {
  position: relative;
}

.filter-btn {
  background: white;
  border: none;
  border-radius: 6px;
  padding: 8px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
  color: #666;
}

.filter-btn:hover {
  background: #f5f5f5;
}

.filter-btn.active {
  background: #b3e5fc;
  color: #00c2c2;
}

.filter-btn span {
  white-space: nowrap;
}

.dropdown-arrow {
  width: 12px;
  height: 12px;
  color: #999;
  flex-shrink: 0;
  transition: transform 0.3s;
}

.dropdown-arrow.rotate {
  transform: rotate(180deg);
  color: #00c2c2;
}

/* 下拉菜单 */
.filter-dropdown {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  background: white;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  min-width: 120px;
  max-height: 300px;
  overflow-y: auto;
  padding: 8px 0;
}

.filter-dropdown-large {
  min-width: 600px;
  max-height: 400px;
  padding: 16px;
}

.dropdown-item {
  padding: 10px 16px;
  cursor: pointer;
  font-size: 14px;
  color: #333;
  transition: background 0.2s;
}

.dropdown-item:hover {
  background: #f5f5f5;
}

.dropdown-item.selected {
  background: #e0f7f7;
  color: #00c2c2;
}

/* 公司行业分类样式 */
.industry-category {
  margin-bottom: 16px;
}

.industry-category:last-child {
  margin-bottom: 0;
}

.category-title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}

.industry-items {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

/* 清空按钮 */
.clear-filter-btn {
  background: none;
  border: none;
  color: #666;
  font-size: 14px;
  cursor: pointer;
  padding: 8px 0;
  transition: color 0.3s;
  white-space: nowrap;
}

.clear-filter-btn:hover {
  color: #333;
}

/* 内容区域 */
.job-content {
  background: #f5f5f5;
  min-height: calc(100vh - 200px);
  padding: 20px 0;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

/* 左侧职位列表 */
.job-list-section {
  flex: 0 0 420px;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.job-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.job-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.job-card.active {
  border-color: #00c2c2;
  box-shadow: 0 2px 8px rgba(0, 194, 194, 0.2);
}

.job-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.job-title {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin: 0;
  flex: 1;
}

.job-salary {
  font-size: 18px;
  font-weight: 600;
  color: #ff4d4f;
  margin-left: 12px;
}

.job-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.tag {
  background: #f0f0f0;
  color: #666;
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
}

.job-company {
  margin-bottom: 8px;
}

.company-name {
  font-size: 14px;
  color: #666;
}

.job-location {
  font-size: 12px;
  color: #999;
}

/* 右侧职位详情 */
.job-detail-section {
  flex: 1;
  min-width: 0;
  position: sticky;
  top: 20px;
}

.job-detail-card {
  background: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.job-detail-empty {
  background: white;
  border-radius: 8px;
  padding: 60px 24px;
  text-align: center;
  color: #999;
}

.detail-header {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.detail-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0 0 12px 0;
}

.detail-salary {
  font-size: 24px;
  font-weight: 600;
  color: #ff4d4f;
}

.detail-attributes {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.attribute-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  font-size: 14px;
}

.attr-icon {
  width: 16px;
  height: 16px;
  color: #999;
  flex-shrink: 0;
}

.detail-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.collect-btn {
  flex: 1;
  background: white;
  border: 1px solid #00c2c2;
  color: #00c2c2;
  border-radius: 6px;
  padding: 12px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all 0.3s;
}

.collect-btn svg {
  width: 16px;
  height: 16px;
}

.collect-btn:hover {
  background: #f0f7f7;
}

.communicate-btn {
  flex: 2;
  background: #00c2c2;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 12px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.3s;
}

.communicate-btn:hover {
  background: #00a8a8;
}

.detail-description {
  margin-bottom: 24px;
}

.desc-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 16px 0;
}

.desc-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.desc-tag {
  background: #e0f7f7;
  color: #00c2c2;
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
}

.desc-content {
  color: #666;
  font-size: 14px;
  line-height: 1.8;
}

.desc-content p {
  margin: 8px 0;
}

.detail-footer {
  display: flex;
  justify-content: space-between;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.share-btn,
.report-btn {
  background: none;
  border: none;
  color: #999;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0;
  transition: color 0.3s;
}

.share-btn svg,
.report-btn svg {
  width: 14px;
  height: 14px;
}

.share-btn:hover,
.report-btn:hover {
  color: #666;
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

/* 空数据状态 */
.empty-state {
  background: white;
  border-radius: 8px;
  padding: 60px 24px;
  text-align: center;
  color: #999;
  font-size: 14px;
}

/* 分页组件 */
.pagination-wrapper {
  margin-top: 20px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  display: flex;
  justify-content: center;
}
</style>
