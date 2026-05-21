<script setup>
import { ref, onMounted, watch } from "vue";
import { Search, Location } from "@element-plus/icons-vue";
import { http } from "@/utils/request.js";
import { ElMessage } from "element-plus";
import { useRouter } from "vue-router";

// 跳转到地图页面
const router = useRouter();
const handleMapClick = () => {
  router.push("/jobmap");
};

// 搜索相关
const jobType = ref("");
const searchKeyword = ref("");

// 热门职位标签
const defaultHotJobs = [
  "IT培训讲师",
  "前端开发工程师",
  "JavaScript",
  "嵌入式软件工程师",
  "单片机",
  "Java",
];
const hotJobs = ref([...defaultHotJobs]);

// 加载热门搜索关键词（使用 DSL 接口）
const loadHotKeywords = async (limit = 10) => {
  try {
    const response = await http.get("/search-dsl/hot_keywords/", { limit });
    console.log("热门关键词接口返回:", response);

    // 兼容多种返回格式
    const payload = response?.data ?? response ?? [];
    let keywords = [];

    if (Array.isArray(payload)) {
      keywords = payload;
    } else if (Array.isArray(payload.keywords)) {
      keywords = payload.keywords;
    } else if (Array.isArray(payload.data)) {
      keywords = payload.data;
    } else if (Array.isArray(payload.results)) {
      keywords = payload.results;
    }

    // 后端格式示例：{ code, message, data: [{ keyword, count }] }
    // 前端展示只需要关键词字符串数组
    const keywordList = (keywords || [])
      .map((item) => {
        if (typeof item === "string") return item;
        return item?.keyword || item?.name || item?.title || "";
      })
      .filter(Boolean);

    hotJobs.value = keywordList.length ? keywordList : defaultHotJobs;
  } catch (error) {
    console.error("加载热门关键词失败:", error);
    const errorMessage =
      error.response?.data?.message || error.message || "加载热门关键词失败";
    ElMessage.error(errorMessage);
    hotJobs.value = defaultHotJobs;
  }
};

// 职位分类数据
const jobCategories = ref([]);

// 加载分类数据
const loadCategories = async () => {
  try {
    const response = await http.get("/categories/list_all/");

    console.log("API 返回的原始数据:", response);

    // 后端返回的数据可能包装在 data 字段中，也可能直接是数组
    const categoriesData = response.data || response;

    console.log("处理后的分类数据:", categoriesData);

    // 确保 categoriesData 是数组
    if (!Array.isArray(categoriesData)) {
      console.error("返回的数据格式不正确，期望数组，实际:", categoriesData);
      ElMessage.error("数据格式错误，请检查后端接口");
      jobCategories.value = [];
      return;
    }

    // 将后端返回的数据转换为前端需要的格式
    const formattedCategories = categoriesData.map((category) => {
      // 获取所有二级分类的名称（用于显示前3个）
      const childrenNames = category.children
        ? category.children.map((child) => child.name)
        : [];

      // 将二级分类转换为 subCategories 格式
      const subCategories = category.children
        ? category.children.map((level2Category) => ({
            title: level2Category.name,
            items: level2Category.children
              ? level2Category.children.map(
                  (level3Category) => level3Category.name
                )
              : [],
          }))
        : [];

      return {
        id: category.id,
        name: category.name,
        children: childrenNames, // 二级分类名称数组（用于显示前3个）
        subCategories: subCategories, // 用于浮层显示
      };
    });

    jobCategories.value = formattedCategories;
  } catch (error) {
    console.error("加载分类数据失败:", error);
    console.error("错误详情:", error.response || error);
    const errorMessage =
      error.response?.data?.message ||
      error.message ||
      "加载分类数据失败，请稍后重试";
    ElMessage.error(errorMessage);
    // 如果加载失败，使用空数组，避免页面报错
    jobCategories.value = [];
  }
};

// 组件挂载时加载数据
onMounted(() => {
  loadCategories();
  loadJobList(1); // 加载初始职位列表
  loadRecommendation(); // 加载推荐信息
  loadHotKeywords(); // 加载热门搜索关键词
});

// 当前分类页
const categoryPage = ref(1);
const totalCategoryPages = ref(4);

// 当前选中的分类索引
const selectedCategoryIndex = ref(0);

// 鼠标悬停的分类索引
const hoveredCategoryIndex = ref(null);

// 搜索功能
const handleSearch = () => {
  console.log("搜索:", searchKeyword.value);
};

// 分类切换
const handleCategoryPageChange = (page) => {
  categoryPage.value = page;
};

// 鼠标进入分类项
const handleCategoryMouseEnter = (index) => {
  hoveredCategoryIndex.value = index;
};

// 鼠标离开分类项
const handleCategoryMouseLeave = () => {
  hoveredCategoryIndex.value = null;
};

// 职位列表相关
const activeTab = ref("featured"); // "featured" 或 "latest"
const jobList = ref([]);
const jobListLoading = ref(false);
const jobListPagination = ref({
  page: 1,
  page_size: 9,
  total_pages: 1,
  count: 0,
});

// 将后端职位数据转换为前端格式
const formatJobData = (job) => {
  return {
    id: job.id,
    title: job.title || job.job_title || "",
    salary: job.money || job.salary || "",
    education: job.education || "学历不限",
    company: job.company?.name || job.company_name || "",
    location: job.city?.name
      ? `${job.city.name}${job.district ? `·${job.district}` : ""}${
          job.address ? `·${job.address}` : ""
        }`
      : job.location || "",
    hasChat: job.has_chat !== false, // 默认显示聊天图标
    tag: job.tag || null,
  };
};

// 加载精选职位或最新职位
const loadJobList = async (page = 1) => {
  jobListLoading.value = true;
  try {
    let url = "";
    if (activeTab.value === "featured") {
      // 精选职位（热推职位）
      url = `/hot_jobs/hot_list/?page=${page}`;
    } else {
      // 最新职位
      url = `/hot_jobs/latest/?page=${page}`;
    }

    const response = await http.get(url);
    console.log("职位列表API返回:", response);

    // 处理响应数据：后端返回格式为 {code: 200, message: '...', data: [...], pagination: {...}}
    // 由于响应拦截器返回 response.data，所以 response 就是后端返回的完整对象
    const jobsData = response.data || [];
    const pagination = response.pagination || {};

    // 转换数据格式
    jobList.value = jobsData.map(formatJobData);

    // 更新分页信息
    jobListPagination.value = {
      page: pagination.page || page,
      page_size: pagination.page_size || 9,
      total_pages: pagination.total_pages || 1,
      count: pagination.count || 0,
    };
  } catch (error) {
    console.error("加载职位列表失败:", error);
    const errorMessage =
      error.response?.data?.message ||
      error.message ||
      "加载职位列表失败，请稍后重试";
    ElMessage.error(errorMessage);
    jobList.value = [];
  } finally {
    jobListLoading.value = false;
  }
};

// 监听标签切换
watch(activeTab, () => {
  loadJobList(1);
});

// 推荐信息
const recommendation = ref({
  location: "北京",
  position: "前端开发工程师",
  salary: "18-25K",
});

// 加载推荐职位信息（用于显示推荐横幅）
const loadRecommendation = async () => {
  try {
    // 从 localStorage 获取用户信息
    const userid = localStorage.getItem("userid");
    if (!userid) {
      // 如果没有用户信息，使用默认值
      return;
    }

    // 这里可以根据实际需求调用推荐接口或从用户期望中获取
    // 暂时使用默认值，后续可以根据实际API调整
    const cityId = localStorage.getItem("city_id") || "1";
    const categoryId = localStorage.getItem("category_id") || "10";
    const salaryMin = localStorage.getItem("salary_min") || "18";
    const salaryMax = localStorage.getItem("salary_max") || "25";

    const response = await http.get(
      `/hot_jobs/recommend/?city_id=${cityId}&category_id=${categoryId}&salary_min=${salaryMin}&salary_max=${salaryMax}&page=1`
    );

    // 处理响应数据：后端返回格式为 {code: 200, message: '...', data: [...], pagination: {...}}
    // 由于响应拦截器返回 response.data，所以 response 就是后端返回的完整对象
    if (response.data && response.data.length > 0) {
      const firstJob = response.data[0];
      recommendation.value = {
        location: firstJob.city?.name || "北京",
        position: firstJob.jobcate?.name || firstJob.title || "前端开发工程师",
        salary: firstJob.money || firstJob.salary || "18-25K",
      };
    }
  } catch (error) {
    console.error("加载推荐信息失败:", error);
    // 失败时使用默认值，不显示错误提示
  }
};

// 热招职位相关
// 从分类数据中获取一级分类作为热招职位分类
const hotJobCategories = ref([]);
const hotJobCategoryMap = ref({}); // 分类名称到ID的映射

const activeHotJobCategory = ref(null);
const hotJobList = ref([]);
const hotJobListLoading = ref(false);
const hotJobListPagination = ref({
  page: 1,
  page_size: 9,
  total_pages: 1,
  count: 0,
});

// 将后端热招职位数据转换为前端格式
const formatHotJobData = (job) => {
  return {
    id: job.id,
    title: job.title || job.job_title || "",
    salary: job.money || job.salary || "",
    location: job.city?.name || job.location || "",
    experience: job.experience || "经验不限",
    education: job.education || "学历不限",
    company: job.company?.name || job.company_name || "",
    industry: job.company?.industry || job.industry || "",
    funding: job.company?.funding || job.funding || "",
    logo: job.company?.logo || "🏢",
    skills: job.skills || job.tags || [],
  };
};

// 加载热招职位
const loadHotJobList = async (categoryName = null, page = 1) => {
  hotJobListLoading.value = true;
  try {
    let url = "";
    const categoryId = categoryName
      ? hotJobCategoryMap.value[categoryName]
      : null;

    if (categoryId) {
      // 根据一级分类获取热推职位
      url = `/hot_jobs/by_category/?category_id=${categoryId}&page=${page}`;
    } else {
      // 获取所有热推职位
      url = `/hot_jobs/hot_list/?page=${page}`;
    }

    const response = await http.get(url);
    console.log("热招职位API返回:", response);

    // 处理响应数据：后端返回格式为 {code: 200, message: '...', data: [...], pagination: {...}}
    // 由于响应拦截器返回 response.data，所以 response 就是后端返回的完整对象
    const jobsData = response.data || [];
    const pagination = response.pagination || {};

    // 转换数据格式
    hotJobList.value = jobsData.map(formatHotJobData);

    // 更新分页信息
    hotJobListPagination.value = {
      page: pagination.page || page,
      page_size: pagination.page_size || 9,
      total_pages: pagination.total_pages || 1,
      count: pagination.count || 0,
    };
  } catch (error) {
    console.error("加载热招职位失败:", error);
    const errorMessage =
      error.response?.data?.message ||
      error.message ||
      "加载热招职位失败，请稍后重试";
    ElMessage.error(errorMessage);
    hotJobList.value = [];
  } finally {
    hotJobListLoading.value = false;
  }
};

// 监听分类数据变化，初始化热招职位分类
watch(
  jobCategories,
  (categories) => {
    if (categories && categories.length > 0) {
      // 从分类数据中提取一级分类名称
      hotJobCategories.value = categories.map((cat) => cat.name);
      // 创建分类名称到ID的映射
      categories.forEach((cat) => {
        hotJobCategoryMap.value[cat.name] = cat.id;
      });
      // 设置默认选中的分类
      if (!activeHotJobCategory.value && hotJobCategories.value.length > 0) {
        activeHotJobCategory.value = hotJobCategories.value[0];
        loadHotJobList(activeHotJobCategory.value);
      }
    }
  },
  { immediate: true }
);

// 监听热招职位分类切换
watch(activeHotJobCategory, (newCategory) => {
  if (newCategory) {
    loadHotJobList(newCategory, 1);
  }
});
</script>

<template>
  <div class="home-page">
    <!-- 顶部搜索区域 -->
    <div class="search-header">
      <div class="search-wrapper">
        <div class="search-container">
          <el-select
            v-model="jobType"
            placeholder="职位类型"
            class="job-type-select"
            clearable
          >
            <el-option label="全部" value="" />
            <el-option label="前端开发" value="frontend" />
            <el-option label="后端开发" value="backend" />
          </el-select>
          <el-input
            v-model="searchKeyword"
            placeholder="搜索职位、公司"
            class="search-input"
            @keyup.enter="handleSearch"
          />
          <el-button class="map-btn" :icon="Location" @click="handleMapClick"
            >地图</el-button
          >
          <el-button class="search-btn" :icon="Search" @click="handleSearch"
            >搜索</el-button
          >
        </div>
        <div class="hot-jobs">
          <span class="hot-jobs-label">热门职位:</span>
          <el-tag
            v-for="(job, index) in hotJobs"
            :key="index"
            class="hot-job-tag"
            effect="plain"
            @click="searchKeyword = job"
          >
            {{ job }}
          </el-tag>
        </div>
      </div>
    </div>

    <!-- 主体内容区域 -->
    <div class="main-content">
      <!-- 左侧分类栏 -->
      <div class="left-sidebar">
        <div class="category-list">
          <div
            v-for="(category, index) in jobCategories"
            :key="index"
            :class="[
              'category-item',
              { active: selectedCategoryIndex === index },
            ]"
            @click="selectedCategoryIndex = index"
            @mouseenter="handleCategoryMouseEnter(index)"
            @mouseleave="handleCategoryMouseLeave"
          >
            <span class="category-name">{{ category.name }}</span>
            <span
              v-for="(child, childIndex) in (category.children || []).slice(
                0,
                3
              )"
              :key="childIndex"
              class="category-child"
            >
              {{ child }}
            </span>
            <span class="arrow-icon">›</span>

            <!-- 三级分类浮层 -->
            <div
              v-if="hoveredCategoryIndex === index && category.subCategories"
              class="category-popup"
              @mouseenter="handleCategoryMouseEnter(index)"
              @mouseleave="handleCategoryMouseLeave"
            >
              <div class="popup-header">
                <h3 class="popup-title">{{ category.name }}</h3>
              </div>
              <div class="popup-content">
                <div
                  v-for="(subCategory, subIndex) in category.subCategories"
                  :key="subIndex"
                  class="popup-section"
                >
                  <h4 class="popup-section-title">{{ subCategory.title }}</h4>
                  <div class="popup-items">
                    <span
                      v-for="(item, itemIndex) in subCategory.items"
                      :key="itemIndex"
                      class="popup-item"
                    >
                      {{ item }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="category-pagination">
          <el-button
            :disabled="categoryPage === 1"
            @click="handleCategoryPageChange(categoryPage - 1)"
            circle
            size="small"
          >
            ‹
          </el-button>
          <span class="page-info"
            >{{ categoryPage }}/{{ totalCategoryPages }}</span
          >
          <el-button
            :disabled="categoryPage === totalCategoryPages"
            @click="handleCategoryPageChange(categoryPage + 1)"
            circle
            size="small"
          >
            ›
          </el-button>
        </div>
      </div>

      <!-- 右侧主内容区 -->
      <div class="right-content">
        <!-- 促销横幅区域 -->
        <div class="banner-grid">
          <!-- 第一个横幅：直聘简历 - 左上，可能更大 -->
          <div class="banner-item banner-1 banner-large">
            <div class="banner-label-pill">直聘简历</div>
            <div class="banner-content">
              <h3 class="banner-title">写好简历 找好工作</h3>
              <p class="banner-features-text">免费设计 | 海量模板 | 智能润色</p>
            </div>
            <div class="banner-icon">📄</div>
          </div>

          <!-- 第二个横幅：最前端有"钱"途 - 右上，较小 -->
          <div class="banner-item banner-2 banner-small">
            <div class="banner-badge">广告</div>
            <div class="banner-content">
              <h3 class="banner-title">最前端 有"钱"途</h3>
              <p class="banner-text">Web前端工程师岗位热推</p>
            </div>
            <div class="banner-icon">💰</div>
          </div>

          <!-- 第三个横幅：算法解决一切 - 左下，较小 -->
          <div class="banner-item banner-3 banner-small">
            <div class="banner-badge">广告</div>
            <div class="banner-content">
              <h3 class="banner-title">算法解决一切</h3>
              <p class="banner-text">算法工程师职位精选</p>
            </div>
            <div class="banner-icon">🧠</div>
          </div>

          <!-- 第四个横幅：挑战最高年薪 - 右下，较小 -->
          <div class="banner-item banner-4 banner-small">
            <div class="banner-badge">广告</div>
            <div class="banner-content">
              <h3 class="banner-title">挑战最高年薪</h3>
              <p class="banner-text">Java工程师职位精选</p>
            </div>
            <div class="banner-icon">☕</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 职位列表区域 -->
    <div class="job-list-section">
      <div class="job-list-container">
        <!-- 标题和标签区域 -->
        <div class="job-list-header">
          <div class="header-left">
            <h2 class="main-title">精选职位</h2>
            <div class="tabs">
              <span
                :class="['tab', { active: activeTab === 'featured' }]"
                @click="activeTab = 'featured'"
              >
                精选职位
              </span>
              <span
                :class="['tab', { active: activeTab === 'latest' }]"
                @click="activeTab = 'latest'"
              >
                最新职位
              </span>
            </div>
          </div>
          <div class="header-right">
            <div class="recommendation-banner">
              <el-avatar :size="24" class="avatar">用</el-avatar>
              <span class="recommendation-text">
                根据求职期望匹配: {{ recommendation.location }} |
                {{ recommendation.position }} | {{ recommendation.salary }}
              </span>
            </div>
          </div>
        </div>

        <!-- 职位列表网格 -->
        <div v-loading="jobListLoading" class="job-grid">
          <div
            v-if="jobList.length === 0 && !jobListLoading"
            class="empty-state"
          >
            暂无职位数据
          </div>
          <div v-for="job in jobList" :key="job.id" class="job-card">
            <div class="job-header">
              <h3 class="job-title">
                {{ job.title }}
                <span v-if="job.hasChat" class="chat-icon">💬</span>
              </h3>
              <span v-if="job.tag" class="job-tag">{{ job.tag }}</span>
            </div>
            <div class="job-salary">{{ job.salary }}</div>
            <div class="job-education">{{ job.education }}</div>
            <div class="job-company">
              <span class="company-logo">🏢</span>
              <span class="company-name">{{ job.company }}</span>
            </div>
            <div class="job-location">{{ job.location }}</div>
          </div>
        </div>

        <!-- 查看更多按钮 -->
        <div class="view-more-container">
          <el-button class="view-more-btn" type="primary" plain>
            查看更多
          </el-button>
        </div>
      </div>
    </div>

    <!-- 热招职位区域 -->
    <div class="hot-job-section">
      <div class="hot-job-container">
        <!-- 标题 -->
        <h2 class="hot-job-title">热招职位</h2>

        <!-- 分类导航 -->
        <div class="hot-job-nav">
          <span
            v-for="(category, index) in hotJobCategories"
            :key="index"
            :class="['nav-item', { active: activeHotJobCategory === category }]"
            @click="activeHotJobCategory = category"
          >
            {{ category }}
          </span>
        </div>

        <!-- 职位列表网格 -->
        <div v-loading="hotJobListLoading" class="hot-job-grid">
          <div
            v-if="hotJobList.length === 0 && !hotJobListLoading"
            class="empty-state"
          >
            暂无职位数据
          </div>
          <div v-for="job in hotJobList" :key="job.id" class="hot-job-card">
            <div class="hot-job-header">
              <h3 class="hot-job-title-text">{{ job.title }}</h3>
            </div>
            <div class="hot-job-salary">{{ job.salary }}</div>
            <div class="hot-job-details">
              <span class="detail-item">{{ job.location }}</span>
              <span class="detail-separator">·</span>
              <span class="detail-item">{{ job.experience }}</span>
              <span class="detail-separator">·</span>
              <span class="detail-item">{{ job.education }}</span>
            </div>
            <div v-if="job.skills && job.skills.length" class="hot-job-skills">
              <span
                v-for="(skill, skillIndex) in job.skills"
                :key="skillIndex"
                class="skill-tag"
              >
                {{ skill }}
              </span>
            </div>
            <div class="hot-job-company">
              <span class="company-logo-icon">{{ job.logo }}</span>
              <div class="company-info">
                <span class="company-name-text">{{ job.company }}</span>
                <div class="company-meta">
                  <span class="meta-item">{{ job.industry }}</span>
                  <span v-if="job.funding" class="meta-separator">·</span>
                  <span v-if="job.funding" class="meta-item">{{
                    job.funding
                  }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 查看更多按钮 -->
        <div class="view-more-container">
          <el-button class="view-more-btn" type="primary" plain>
            查看更多
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #e0f7f7 0%, #ffffff 100%);
  padding-bottom: 40px;
}

/* 顶部搜索区域 */
.search-header {
  padding: 30px 20px;
  display: flex;
  justify-content: center;
}

.search-wrapper {
  max-width: 900px;
  width: 100%;
  margin: 0 auto;
}

.search-container {
  background: white;
  border: 2px solid #00c2c2;
  border-radius: 12px;
  padding: 12px;
  display: flex;
  gap: 12px;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 194, 194, 0.1);
}

.job-type-select {
  width: 140px;
}

.job-type-select :deep(.el-input__wrapper) {
  box-shadow: none !important;
  border: none !important;
  background: transparent !important;
  padding: 0 !important;
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
  padding: 0 !important;
}

.job-type-select :deep(.el-input) {
  border: none !important;
}

.job-type-select :deep(.el-select__wrapper) {
  box-shadow: none !important;
  border: none !important;
}

.job-type-select :deep(.el-select__caret) {
  color: #999;
}

.job-type-select :deep(.el-input__suffix) {
  border: none !important;
}

.search-input {
  flex: 1;
}

.search-input :deep(.el-input__wrapper) {
  box-shadow: none;
  border: none;
}

.map-btn {
  border: none;
  background: transparent;
  color: #666;
  padding: 0 12px;
}

.map-btn:hover {
  background: transparent;
  color: #00c2c2;
}

.search-btn {
  background: #00c2c2;
  border-color: #00c2c2;
  color: white;
  padding: 10px 24px;
  font-weight: 500;
}

.search-btn:hover {
  background: #00a8a8;
  border-color: #00a8a8;
}

.hot-jobs {
  margin-top: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.hot-jobs-label {
  color: #666;
  font-size: 13px;
}

.hot-job-tag {
  cursor: pointer;
  transition: all 0.3s;
  background: #fafafa;
  border: none;
  color: #00c2c2;
  border-radius: 5px;
  padding: 6px 14px;
  font-size: 12px;
}

.hot-job-tag:hover {
  background: #f0f0f0;
  color: #00a8a8;
}

/* 主体内容区域 */
.main-content {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
  display: flex;
  gap: 20px;
  align-items: stretch;
  position: relative;
  overflow: visible;
}

/* 左侧分类栏 */
.left-sidebar {
  width: 320px;
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  height: 100%;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: visible;
}

.category-list {
  margin-bottom: 12px;
  flex: 1;
  overflow: visible;
}

.category-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 8px;
  border: 1px solid transparent;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 4px;
  position: relative;
}

.category-item:last-child {
  margin-bottom: 0;
}

.category-item:hover {
  background: #f9f9f9;
}

.category-item.active {
  border-color: #ff4d4f;
  background: #fff5f5;
}

.category-name {
  font-size: 13px;
  font-weight: 500;
  color: #333;
  white-space: nowrap;
  min-width: 80px;
}

.category-child {
  font-size: 12px;
  color: #666;
  cursor: pointer;
  padding: 2px 4px;
  transition: color 0.3s;
  white-space: nowrap;
}

.category-child:hover {
  color: #00c2c2;
}

.arrow-icon {
  color: #999;
  font-size: 14px;
  margin-left: auto;
}

/* 三级分类浮层 */
.category-popup {
  position: absolute;
  left: calc(100% + 8px);
  top: -20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  z-index: 10000;
  width: 650px;
  max-height: 600px;
  min-height: 400px;
  overflow-y: auto;
  padding: 20px;
  animation: fadeIn 0.2s ease-in-out;
  box-sizing: border-box;
  white-space: normal;
}

/* 浮层滚动条样式 */
.category-popup::-webkit-scrollbar {
  width: 6px;
}

.category-popup::-webkit-scrollbar-track {
  background: #f5f5f5;
  border-radius: 3px;
}

.category-popup::-webkit-scrollbar-thumb {
  background: #ddd;
  border-radius: 3px;
}

.category-popup::-webkit-scrollbar-thumb:hover {
  background: #bbb;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.popup-header {
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.popup-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.popup-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.popup-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.popup-section-title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.popup-items {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.popup-item {
  font-size: 13px;
  color: #666;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  background: #f9f9f9;
  border: 1px solid transparent;
}

.popup-item:hover {
  background: #f0f7f7;
  border-color: #00c2c2;
  color: #00c2c2;
}

.category-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.page-info {
  font-size: 13px;
  color: #666;
}

/* 右侧主内容区 */
.right-content {
  flex: 1;
  display: flex;
  align-items: stretch;
  min-width: 0;
}

/* 促销横幅区域 */
.banner-grid {
  display: grid;
  grid-template-columns: 1.3fr 0.8fr;
  grid-template-rows: 1.5fr 0.8fr;
  gap: 26px;
  width: 100%;
  height: 95%;
}

.banner-item {
  border-radius: 16px;
  padding: 20px;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  width: 100%;
  height: 90%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.banner-large {
  grid-column: 1;
  grid-row: 1;
  padding: 24px;
}

.banner-2 {
  grid-column: 2;
  grid-row: 1;
}

.banner-3 {
  grid-column: 1;
  grid-row: 2;
}

.banner-4 {
  grid-column: 2;
  grid-row: 2;
}

.banner-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.banner-1 {
  background: linear-gradient(180deg, #a78bfa 0%, #8b5cf6 100%);
  color: white;
}

.banner-2 {
  background: linear-gradient(180deg, #60a5fa 0%, #3b82f6 100%);
  color: white;
}

.banner-3 {
  background: linear-gradient(180deg, #f472b6 0%, #ec4899 100%);
  color: white;
}

.banner-4 {
  background: linear-gradient(180deg, #34d399 0%, #10b981 100%);
  color: white;
}

.banner-label-pill {
  position: absolute;
  top: 16px;
  left: 16px;
  background: rgba(255, 255, 255, 0.25);
  color: white;
  padding: 5px 12px;
  border-radius: 16px;
  font-size: 11px;
  font-weight: 500;
  backdrop-filter: blur(6px);
  z-index: 2;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.banner-badge {
  position: absolute;
  bottom: 12px;
  right: 12px;
  background: rgba(255, 255, 255, 0.25);
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 11px;
  color: white;
  backdrop-filter: blur(4px);
}

.banner-content {
  flex: 1;
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding-top: 12px;
}

.banner-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 8px 0;
  line-height: 1.4;
  color: white;
}

.banner-text {
  font-size: 13px;
  margin: 0;
  opacity: 0.9;
  line-height: 1.5;
  color: white;
}

.banner-features-text {
  font-size: 12px;
  margin: 0;
  opacity: 0.9;
  line-height: 1.6;
  color: white;
}

.banner-icon {
  position: absolute;
  bottom: 16px;
  right: 16px;
  font-size: 48px;
  opacity: 0.3;
  line-height: 1;
  z-index: 0;
}

.banner-large .banner-icon {
  font-size: 64px;
  bottom: 20px;
  right: 20px;
}

/* 响应式设计 */
/* 职位列表区域 */
.job-list-section {
  max-width: 1200px;
  margin: 40px auto;
  padding: 0 20px;
}

.job-list-container {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.job-list-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.main-title {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.tabs {
  display: flex;
  gap: 24px;
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

.header-right {
  display: flex;
  align-items: center;
}

.recommendation-banner {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #f9f9f9;
  border-radius: 20px;
}

.recommendation-banner .avatar {
  background: #00c2c2;
  color: white;
  font-size: 12px;
}

.recommendation-text {
  font-size: 13px;
  color: #666;
}

/* 职位网格 */
.job-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.job-card {
  background: #fafafa;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s;
  cursor: pointer;
}

.job-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.job-header {
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
  line-height: 1.4;
  display: flex;
  align-items: center;
  gap: 6px;
}

.chat-icon {
  font-size: 14px;
  opacity: 0.6;
}

.job-tag {
  font-size: 12px;
  color: #00c2c2;
  background: #e0f7f7;
  padding: 2px 8px;
  border-radius: 4px;
  white-space: nowrap;
}

.job-salary {
  font-size: 18px;
  font-weight: 600;
  color: #ff4d4f;
  margin-bottom: 8px;
}

.job-education {
  font-size: 13px;
  color: #999;
  margin-bottom: 12px;
}

.job-company {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
}

.company-logo {
  font-size: 16px;
}

.company-name {
  font-size: 14px;
  color: #666;
}

.job-location {
  font-size: 13px;
  color: #999;
}

/* 查看更多按钮 */
.view-more-container {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

.view-more-btn {
  padding: 12px 40px;
  font-size: 14px;
  border-radius: 20px;
  background: #e0f2f4 !important;
  border-color: #2e8b99 !important;
  color: #2e8b99 !important;
}

.view-more-btn:hover {
  background: #d0e8ea !important;
  border-color: #2e8b99 !important;
  color: #2e8b99 !important;
}

/* 热招职位区域 */
.hot-job-section {
  max-width: 1200px;
  margin: 40px auto;
  padding: 0 20px;
}

.hot-job-container {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.hot-job-title {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin: 0 0 24px 0;
  text-align: center;
}

.hot-job-nav {
  display: flex;
  gap: 24px;
  margin-bottom: 30px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
  flex-wrap: wrap;
}

.nav-item {
  font-size: 15px;
  color: #666;
  cursor: pointer;
  padding-bottom: 8px;
  transition: all 0.3s;
  position: relative;
  white-space: nowrap;
}

.nav-item:hover {
  color: #00c2c2;
}

.nav-item.active {
  color: #00c2c2;
  font-weight: 500;
}

.nav-item.active::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: #00c2c2;
}

/* 热招职位网格 */
.hot-job-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.hot-job-card {
  background: #fafafa;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s;
  cursor: pointer;
}

.hot-job-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.hot-job-header {
  margin-bottom: 12px;
}

.hot-job-title-text {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin: 0;
  line-height: 1.4;
}

.hot-job-salary {
  font-size: 18px;
  font-weight: 600;
  color: #ff4d4f;
  margin-bottom: 12px;
}

.hot-job-details {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 12px;
  font-size: 13px;
  color: #999;
}

.detail-item {
  color: #999;
}

.detail-separator {
  color: #ddd;
}

.hot-job-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.skill-tag {
  font-size: 12px;
  color: #666;
  background: #f0f0f0;
  padding: 4px 10px;
  border-radius: 4px;
}

.hot-job-company {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.company-logo-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.company-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.company-name-text {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.company-meta {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #999;
}

.meta-item {
  color: #999;
}

.meta-separator {
  color: #ddd;
}

@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
    height: auto;
  }

  .left-sidebar {
    width: 100%;
    max-height: 200px;
  }

  .banner-grid {
    grid-template-columns: 1fr;
  }

  .search-container {
    flex-wrap: wrap;
  }

  .job-type-select {
    width: 100%;
  }

  .job-list-header {
    flex-direction: column;
    gap: 16px;
  }

  .header-right {
    width: 100%;
  }

  .recommendation-banner {
    width: 100%;
    justify-content: flex-start;
  }

  .job-grid {
    grid-template-columns: 1fr;
  }

  .hot-job-nav {
    gap: 16px;
  }

  .hot-job-grid {
    grid-template-columns: 1fr;
  }
}

/* 空状态样式 */
.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px 20px;
  color: #999;
  font-size: 16px;
}
</style>
