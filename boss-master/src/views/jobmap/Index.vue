<script setup>
import { ref, onMounted, onUnmounted, shallowRef, nextTick, watch } from "vue";
import { useRouter } from "vue-router";
import { Search, ArrowDown } from "@element-plus/icons-vue";
import AMapLoader from "@amap/amap-jsapi-loader";
import CitySelector from "@/components/CitySelector.vue";
import { http } from "@/utils/request";

const router = useRouter();

// 当前城市
const currentCity = ref("北京");
const showCitySelector = ref(false);

// 搜索关键词
const searchKeyword = ref("");

// 分类标签
const categories = ref([
  { label: "全部", value: "all", active: true },
  { label: "推荐", value: "recommend", active: false },
  { label: "人事/财务/行政", value: "hr", active: false },
  { label: "供应链/物流", value: "logistics", active: false },
  { label: "展开", value: "expand", active: false },
]);

// 是否已登录
const isLoggedIn = ref(false);
// 是否隐藏登录提示
const hideLoginTip = ref(false);
// 地图加载错误
const mapError = ref(null);

// 地图相关 - 使用 shallowRef 存储地图实例
const map = shallowRef(null);
const mapContainer = ref(null); // 地图容器引用
const jobMarkers = ref([]); // 存储职位标记
const AMap = ref(null); // 存储 AMap 对象
const geocoder = ref(null); // 地理编码实例

// 职位数据
const jobList = ref([]);
const loadingJobs = ref(false);

// 选中的职位（用于显示详情浮层）
const selectedJob = ref(null);
const showJobDetail = ref(false);

// 生成模拟岗位数据（用于测试）
const generateMockJobs = () => {
  return [
    {
      id: 1001,
      title: "前端开发工程师(React方向)",
      money: "20-30K",
      salary: "20-30K",
      company_name: "北京科技有限公司",
      company: {
        name: "北京科技有限公司",
      },
      address: "海淀区中关村大街1号",
      full_location: "北京市海淀区中关村大街1号",
      city_name: "北京",
      city: {
        name: "北京",
      },
      experience: "5-10年",
      education: "本科",
      // 直接提供坐标（中关村附近）
      longitude: 116.316833,
      latitude: 39.983424,
      skills: ["React.js", "React", "前端开发经验", "英语六级"],
      tags: ["React.js", "React", "前端开发经验"],
      responsibilities: [
        "负责使用React.js开发高质量的前端应用",
        "与UI/UX设计师协作，实现优秀的用户界面",
        "优化应用性能，确保良好的用户体验",
        "使用Redux或Context API管理应用状态",
        "使用Webpack、Babel等工具构建和打包项目",
        "编写单元测试，使用Jest和React Testing Library",
        "与后端团队协作，集成RESTful API和GraphQL",
        "持续优化代码质量和开发流程",
      ],
      requirements: [
        "计算机科学或相关专业学历，3年以上React开发经验",
        "熟练掌握React.js核心概念，包括虚拟DOM、Hooks、生命周期方法",
      ],
    },
    {
      id: 1002,
      title: "Web前端开发工程师",
      money: "12-20K",
      salary: "12-20K",
      company_name: "创新互联网公司",
      company: {
        name: "创新互联网公司",
      },
      address: "朝阳区建国路88号",
      full_location: "北京市朝阳区建国路88号",
      city_name: "北京",
      city: {
        name: "北京",
      },
      experience: "3-5年",
      education: "本科",
      // 直接提供坐标（建国路附近）
      longitude: 116.461665,
      latitude: 39.90923,
      skills: ["Vue.js", "JavaScript", "TypeScript", "前端开发"],
      tags: ["Vue.js", "JavaScript", "TypeScript"],
      responsibilities: [
        "负责公司产品的前端开发工作",
        "使用Vue.js框架开发单页应用",
        "与后端API进行数据交互",
        "优化前端性能和用户体验",
        "参与技术方案设计和代码评审",
      ],
      requirements: [
        "3年以上前端开发经验，熟练掌握Vue.js",
        "熟悉JavaScript、TypeScript、HTML5、CSS3",
        "有良好的代码规范和团队协作能力",
      ],
    },
  ];
};

// 城市中心坐标映射（用于设置地图中心点）
const cityCenters = {
  北京: [116.397428, 39.90923],
  上海: [121.473701, 31.230416],
  广州: [113.264385, 23.129112],
  深圳: [114.057868, 22.543099],
  杭州: [120.153576, 30.287459],
  天津: [117.200983, 39.084158],
  西安: [108.940175, 34.341568],
  苏州: [120.585315, 31.298886],
  武汉: [114.3162, 30.581],
  厦门: [118.11087, 24.490474],
  长沙: [112.982279, 28.19409],
  成都: [104.066541, 30.572269],
  郑州: [113.665412, 34.757975],
  重庆: [106.551556, 29.562849],
  佛山: [113.121465, 23.021478],
  合肥: [117.283042, 31.86119],
  济南: [117.000923, 36.675807],
  青岛: [120.382639, 36.067082],
  南京: [118.796877, 32.060255],
  东莞: [113.746262, 23.046237],
  昆明: [102.712251, 25.040609],
  南昌: [115.892151, 28.676493],
  石家庄: [114.502461, 38.045474],
  宁波: [121.549792, 29.868388],
  福州: [119.306239, 26.075302],
  滨州: [118.016974, 37.383542],
};

// 初始化地图
const initMap = () => {
  if (!AMap.value) {
    console.error("高德地图 JS API 未加载");
    return;
  }

  // 检查地图容器是否存在
  if (!mapContainer.value) {
    console.error("地图容器不存在");
    return;
  }

  // 如果地图已经初始化，先销毁
  if (map.value) {
    map.value.destroy();
    map.value = null;
  }

  // 获取当前城市中心坐标
  const cityCenter = cityCenters[currentCity.value] || [117.2, 39.12];

  // 创建地图实例
  map.value = new AMap.value.Map(mapContainer.value, {
    zoom: 11, // 缩放级别
    center: cityCenter,
    mapStyle: "amap://styles/normal", // 地图样式
  });

  // 初始化地理编码服务
  geocoder.value = new AMap.value.Geocoder({
    city: currentCity.value, // 城市设为当前城市
  });

  // 添加地图控件
  try {
    // 添加比例尺控件
    const scale = new AMap.value.Scale({
      position: "LB", // 左下角
    });
    map.value.addControl(scale);
  } catch (error) {
    console.warn("比例尺控件加载失败:", error);
  }

  try {
    // 添加工具条控件
    const toolBar = new AMap.value.ToolBar({
      position: "RT", // 右上角
    });
    map.value.addControl(toolBar);
  } catch (error) {
    console.warn("工具条控件加载失败:", error);
  }

  // 等待地图完全加载后再加载职位数据
  setTimeout(() => {
    console.log("开始加载职位数据并标记在地图上");
    // 加载职位数据并标记在地图上（使用模拟数据）
    loadJobsAndMarkOnMap(true);
  }, 500);
};

// 加载高德地图
const loadAMap = async () => {
  try {
    const AMapInstance = await AMapLoader.load({
      key: "6135e881b5a30378a6c696316ddaab7c", // 申请好的Web端开发者Key
      version: "2.0", // 指定要加载的 JSAPI 的版本
      plugins: ["AMap.Scale", "AMap.ToolBar", "AMap.Geocoder"], // 需要使用的的插件列表
    });
    AMap.value = AMapInstance;
    mapError.value = null; // 清除错误
    return AMapInstance;
  } catch (error) {
    console.error("高德地图加载失败:", error);
    const errorMessage = error.message || String(error);

    // 检查是否是 key 错误
    if (
      errorMessage.includes("INVALID_USER_KEY") ||
      errorMessage.includes("INVALID")
    ) {
      mapError.value = {
        type: "INVALID_USER_KEY",
        message: "高德地图 API Key 配置错误",
        details:
          "请检查 API key 是否正确，或是否在高德开放平台配置了白名单（localhost、127.0.0.1）",
      };
    } else {
      mapError.value = {
        type: "LOAD_ERROR",
        message: "地图加载失败",
        details: errorMessage,
      };
    }
    throw error;
  }
};

// 组件挂载
onMounted(async () => {
  // 检查登录状态
  const token = localStorage.getItem("token");
  isLoggedIn.value = !!token;

  // 检查是否已隐藏登录提示
  const hideTip = localStorage.getItem("hideMapLoginTip");
  hideLoginTip.value = hideTip === "true";

  // 加载地图
  try {
    // 先等待 DOM 渲染完成
    await nextTick();

    // 检查容器是否存在
    if (!mapContainer.value) {
      console.error("地图容器 ref 未找到，等待 DOM 更新...");
      await nextTick();
      await new Promise((resolve) => setTimeout(resolve, 100));
    }

    // 加载高德地图 API
    console.log("开始加载高德地图 API...");
    await loadAMap();
    console.log("高德地图 API 加载完成");

    // 再次等待确保容器已渲染
    await nextTick();

    // 额外等待一小段时间确保容器完全准备好
    await new Promise((resolve) => setTimeout(resolve, 300));

    // 初始化地图
    console.log("开始初始化地图...");
    initMap();
    console.log("地图初始化完成");
  } catch (error) {
    console.error("地图初始化失败:", error);
    // 显示用户友好的错误提示
    const errorMessage = error.message || String(error);
    if (errorMessage.includes("INVALID_USER_KEY")) {
      console.error(
        "❌ 高德地图 API Key 配置错误！\n" +
          "地图无法显示，请检查 API key 配置。"
      );
    } else {
      console.error("地图加载失败，错误信息:", errorMessage);
    }
  }
});

// 组件卸载
onUnmounted(() => {
  // 清除所有标记
  clearJobMarkers();

  if (map.value) {
    map.value.destroy();
    map.value = null;
  }
  geocoder.value = null;
  AMap.value = null;
});

// 清除地图上的所有职位标记
const clearJobMarkers = () => {
  jobMarkers.value.forEach((marker) => {
    if (marker) {
      marker.setMap(null);
      marker = null;
    }
  });
  jobMarkers.value = [];
};

// 根据地址获取坐标
const getLocationByAddress = (address, city) => {
  return new Promise((resolve, reject) => {
    if (!geocoder.value) {
      reject(new Error("地理编码服务未初始化"));
      return;
    }

    // 构建完整地址
    let fullAddress = address;
    if (city && city !== "全国") {
      // 如果地址不包含城市名称，则添加
      if (!address.includes(city)) {
        fullAddress = `${city}${address}`;
      } else {
        fullAddress = address;
      }
    }

    geocoder.value.getLocation(fullAddress, (status, result) => {
      if (
        status === "complete" &&
        result.geocodes &&
        result.geocodes.length > 0
      ) {
        const location = result.geocodes[0].location;
        if (location && location.lng && location.lat) {
          resolve([location.lng, location.lat]);
        } else {
          reject(new Error("坐标数据无效"));
        }
      } else {
        reject(new Error(`地址解析失败: ${status}`));
      }
    });
  });
};

// 在地图上标记职位
const markJobsOnMap = async (jobs) => {
  if (!map.value || !AMap.value) {
    console.error("地图未初始化");
    return;
  }

  // 先清除旧的标记
  clearJobMarkers();

  // 批量处理职位标记（限制数量避免过多标记）
  const jobsToMark = jobs.slice(0, 50); // 最多标记50个职位，避免过多请求
  let successCount = 0;

  // 使用 Promise.all 并发处理，但限制并发数量
  const batchSize = 5; // 每批处理5个
  for (let i = 0; i < jobsToMark.length; i += batchSize) {
    const batch = jobsToMark.slice(i, i + batchSize);

    await Promise.all(
      batch.map(async (job) => {
        try {
          let location = null;

          // 如果职位数据中直接包含坐标，优先使用
          if (job.longitude && job.latitude) {
            location = [job.longitude, job.latitude];
          } else {
            // 否则通过地理编码获取坐标
            let address = job.address || job.full_location || "";

            // 如果地址包含城市名称，去掉城市名称（地理编码时已经指定了城市）
            if (
              address &&
              currentCity.value &&
              address.includes(currentCity.value)
            ) {
              address = address.replace(currentCity.value, "").trim();
            }

            if (!address) {
              console.warn("职位缺少地址信息:", job.title);
              return;
            }

            // 获取坐标
            location = await getLocationByAddress(address, currentCity.value);
          }

          if (!location || !Array.isArray(location) || location.length !== 2) {
            console.warn("无法获取职位坐标:", job.title);
            return;
          }

          // 创建标记内容
          const jobTitle = (job.title || "职位").substring(0, 10); // 限制标题长度
          const jobSalary = job.money || job.salary || "";
          const companyName = (
            job.company_name ||
            job.company?.name ||
            ""
          ).substring(0, 12); // 限制公司名长度

          const markerContent = `
            <div style="
              background: #4db8c4;
              color: white;
              padding: 6px 10px;
              border-radius: 6px;
              font-size: 12px;
              white-space: nowrap;
              box-shadow: 0 2px 8px rgba(0,0,0,0.2);
              cursor: pointer;
              max-width: 200px;
            ">
              <div style="font-weight: 500; margin-bottom: 2px;">${jobTitle}</div>
              <div style="font-size: 11px; opacity: 0.9;">${jobSalary}</div>
              <div style="font-size: 10px; opacity: 0.8; margin-top: 2px;">${companyName}</div>
            </div>
          `;

          // 创建标记
          const marker = new AMap.value.Marker({
            position: location,
            content: markerContent,
            offset: new AMap.value.Pixel(-100, -50),
            zIndex: 100,
          });

          // 添加点击事件
          marker.on("click", () => {
            // 显示职位详情浮层
            selectedJob.value = job;
            showJobDetail.value = true;
            console.log("点击职位:", job);
          });

          marker.setMap(map.value);
          jobMarkers.value.push(marker);
          successCount++;

          console.log(
            `成功标记职位: ${jobTitle} at [${location[0]}, ${location[1]}]`
          );
        } catch (error) {
          console.warn("标记职位失败:", job.title || job.id, error.message);
        }
      })
    );

    // 每批之间稍作延迟，避免请求过快
    if (i + batchSize < jobsToMark.length) {
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
  }

  console.log(`成功标记 ${successCount} 个职位`);
};

// 获取职位数据
const loadJobs = async () => {
  if (loadingJobs.value) return [];

  loadingJobs.value = true;
  try {
    const params = {
      page: 1,
      page_size: 50, // 获取50条数据用于地图标记
    };

    // 如果当前城市不是"全国"，添加城市筛选
    if (currentCity.value && currentCity.value !== "全国") {
      // 尝试使用城市名称作为查询参数
      params.query = currentCity.value;
    }

    const response = await http.get("/search-dsl/search/", params);

    if (
      response.code === 200 &&
      response.data &&
      Array.isArray(response.data)
    ) {
      // 如果返回的数据中包含城市信息，可以进一步筛选
      let filteredJobs = response.data;

      // 如果当前城市不是"全国"，进一步筛选匹配城市的职位
      if (currentCity.value && currentCity.value !== "全国") {
        filteredJobs = response.data.filter((job) => {
          const jobCity = job.city_name || job.city?.name || "";
          return (
            jobCity.includes(currentCity.value) ||
            currentCity.value.includes(jobCity)
          );
        });
      }

      jobList.value = filteredJobs;
      return filteredJobs;
    } else {
      console.error("获取职位数据失败:", response.message || "数据格式错误");
      jobList.value = [];
      return [];
    }
  } catch (error) {
    console.error("加载职位数据失败:", error);
    jobList.value = [];
    return [];
  } finally {
    loadingJobs.value = false;
  }
};

// 加载职位数据并标记在地图上
const loadJobsAndMarkOnMap = async (useMockData = false) => {
  let jobs = [];

  if (useMockData) {
    // 使用模拟数据
    jobs = generateMockJobs();
    jobList.value = jobs;
    console.log("使用模拟数据:", jobs);
  } else {
    // 从API获取数据
    jobs = await loadJobs();
  }

  if (jobs.length > 0) {
    await markJobsOnMap(jobs);
  }
};

// 城市选择
const handleCitySelect = (city) => {
  currentCity.value = city;
  showCitySelector.value = false;

  // 更新地图中心点
  if (map.value && cityCenters[city]) {
    map.value.setCenter(cityCenters[city]);
    map.value.setZoom(11);
  }

  // 更新地理编码服务的城市
  if (geocoder.value) {
    geocoder.value.setCity(city);
  }

  // 重新加载职位数据并标记（切换城市时使用真实API数据）
  loadJobsAndMarkOnMap(false);
};

// 分类切换
const handleCategoryClick = (category) => {
  if (category.value === "expand") {
    // 展开更多分类
    return;
  }
  categories.value.forEach((cat) => {
    cat.active = cat.value === category.value;
  });
};

// 搜索
const handleSearch = () => {
  console.log("搜索:", searchKeyword.value);
  // 实现搜索逻辑
};

// 登录跳转
const handleLogin = () => {
  router.push("/login");
};

// 关闭登录提示
const closeLoginTip = () => {
  // 设置一个标记，不再显示
  localStorage.setItem("hideMapLoginTip", "true");
  hideLoginTip.value = true;
};

// 关闭职位详情浮层
const closeJobDetail = () => {
  showJobDetail.value = false;
  selectedJob.value = null;
};

// 重试加载地图
const retryLoadMap = async () => {
  mapError.value = null;
  // 清理旧地图
  clearJobMarkers();

  if (map.value) {
    map.value.destroy();
    map.value = null;
  }
  geocoder.value = null;
  AMap.value = null;

  // 重新加载
  try {
    await nextTick();
    if (!mapContainer.value) {
      await nextTick();
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
    await loadAMap();
    await nextTick();
    await new Promise((resolve) => setTimeout(resolve, 300));
    initMap();
  } catch (error) {
    console.error("重试加载地图失败:", error);
  }
};
</script>

<template>
  <div class="job-map-page">
    <!-- 顶部导航栏 -->
    <div class="map-header">
      <div class="header-content">
        <!-- 左侧：城市选择 -->
        <div class="city-selector-wrapper">
          <button class="city-btn" @click="showCitySelector = true">
            <span class="city-name">{{ currentCity }}</span>
            <el-icon class="arrow-icon"><ArrowDown /></el-icon>
          </button>
        </div>

        <!-- 中间：搜索框 -->
        <div class="search-wrapper">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索职位、公司"
            class="search-input"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>

        <!-- 右侧：分类标签 -->
        <div class="category-tabs">
          <button
            v-for="category in categories"
            :key="category.value"
            :class="['category-tab', { active: category.active }]"
            @click="handleCategoryClick(category)"
          >
            {{ category.label }}
            <el-icon v-if="category.value === 'expand'" class="expand-icon">
              <ArrowDown />
            </el-icon>
          </button>
        </div>
      </div>
    </div>

    <!-- 地图容器 -->
    <div ref="mapContainer" id="map-container" class="map-container">
      <!-- 错误提示 -->
      <div v-if="mapError" class="map-error-overlay">
        <div class="error-card">
          <div class="error-icon">⚠️</div>
          <h3 class="error-title">{{ mapError.message }}</h3>
          <p class="error-details">{{ mapError.details }}</p>
          <div v-if="mapError.type === 'INVALID_USER_KEY'" class="error-steps">
            <p class="steps-title">解决步骤：</p>
            <ol>
              <li>
                登录
                <a href="https://console.amap.com/" target="_blank"
                  >高德开放平台</a
                >
              </li>
              <li>进入"应用管理"，找到你的 key</li>
              <li>在"服务平台"中勾选"Web服务"和"Web端(JS API)"</li>
              <li>在"安全设置"中添加白名单：localhost、127.0.0.1</li>
            </ol>
          </div>
          <el-button type="primary" @click="retryLoadMap">重试</el-button>
        </div>
      </div>
    </div>

    <!-- 登录提示浮层 -->
    <div v-if="!isLoggedIn && !hideLoginTip" class="login-overlay">
      <div class="login-tip-card">
        <div class="tip-header">
          <svg
            class="map-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
            <circle cx="12" cy="10" r="3"></circle>
          </svg>
          <span class="tip-title">登录使用地图找工作</span>
        </div>
        <p class="tip-description">随意拖动缩放地图,附近工作即刻呈现</p>
        <el-button type="primary" class="login-btn" @click="handleLogin">
          立即登录
        </el-button>
        <button class="close-btn" @click="closeLoginTip">×</button>
      </div>
    </div>

    <!-- 城市选择器 -->
    <CitySelector
      v-model:visible="showCitySelector"
      @select="handleCitySelect"
    />

    <!-- 职位详情浮层 -->
    <div v-if="showJobDetail && selectedJob" class="job-detail-overlay">
      <div class="job-detail-card">
        <!-- 关闭按钮 -->
        <button class="job-detail-close" @click="closeJobDetail">×</button>

        <!-- 职位标题 -->
        <div class="job-detail-header">
          <h2 class="job-title">
            {{ selectedJob.title || "职位名称" }}
            <span
              class="job-salary"
              v-if="selectedJob.money || selectedJob.salary"
            >
              {{ selectedJob.money || selectedJob.salary }}
            </span>
          </h2>
          <div class="job-meta">
            <span v-if="selectedJob.city_name || selectedJob.city?.name">
              {{ selectedJob.city_name || selectedJob.city?.name }}
            </span>
            <span v-if="selectedJob.experience">
              | {{ selectedJob.experience }}</span
            >
            <span v-if="selectedJob.education">
              | {{ selectedJob.education }}</span
            >
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="job-detail-actions">
          <el-button type="primary" class="chat-btn">立即沟通</el-button>
          <el-button class="interest-btn">
            <span>感兴趣</span>
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"
              ></path>
            </svg>
          </el-button>
        </div>

        <!-- 职位描述 -->
        <div class="job-detail-content">
          <h3 class="content-title">职位描述:</h3>

          <!-- 标签 -->
          <div class="job-tags" v-if="selectedJob.skills || selectedJob.tags">
            <span
              v-for="(tag, index) in selectedJob.skills ||
              selectedJob.tags ||
              []"
              :key="index"
              class="job-tag"
            >
              {{ tag }}
            </span>
          </div>

          <!-- 职责 -->
          <div class="job-section" v-if="selectedJob.responsibilities">
            <h4 class="section-title">职责</h4>
            <ul class="section-list">
              <li
                v-for="(item, index) in selectedJob.responsibilities"
                :key="index"
              >
                {{ item }}
              </li>
            </ul>
          </div>

          <!-- 需求 -->
          <div class="job-section" v-if="selectedJob.requirements">
            <h4 class="section-title">需求</h4>
            <ul class="section-list">
              <li
                v-for="(item, index) in selectedJob.requirements"
                :key="index"
              >
                {{ item }}
              </li>
            </ul>
          </div>

          <!-- 公司信息 -->
          <div
            class="job-company"
            v-if="selectedJob.company_name || selectedJob.company?.name"
          >
            <h4 class="section-title">公司信息</h4>
            <p class="company-name">
              {{ selectedJob.company_name || selectedJob.company?.name }}
            </p>
            <p
              v-if="selectedJob.address || selectedJob.full_location"
              class="company-address"
            >
              {{ selectedJob.address || selectedJob.full_location }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.job-map-page {
  width: 100%;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

/* 顶部导航栏 */
.map-header {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 12px 20px;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 20px;
}

/* 城市选择 */
.city-selector-wrapper {
  flex-shrink: 0;
}

.city-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #333;
  padding: 8px 12px;
  border-radius: 6px;
  transition: background 0.3s;
}

.city-btn:hover {
  background: rgba(0, 0, 0, 0.05);
}

.city-name {
  font-weight: 500;
}

.arrow-icon {
  font-size: 12px;
  color: #999;
}

/* 搜索框 */
.search-wrapper {
  flex: 1;
  max-width: 400px;
}

.search-input {
  width: 100%;
}

:deep(.el-input__wrapper) {
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 分类标签 */
.category-tabs {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.category-tab {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 16px;
  background: none;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  transition: all 0.3s;
  white-space: nowrap;
}

.category-tab:hover {
  background: rgba(0, 0, 0, 0.05);
  color: #333;
}

.category-tab.active {
  background: #4db8c4;
  color: white;
}

.expand-icon {
  font-size: 12px;
}

/* 地图容器 */
.map-container {
  width: 100%;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

/* 错误提示覆盖层 */
.map-error-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.95);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
}

.error-card {
  background: white;
  border-radius: 12px;
  padding: 30px;
  max-width: 500px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  text-align: center;
}

.error-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.error-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0 0 12px 0;
}

.error-details {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
}

.error-steps {
  text-align: left;
  background: #f5f7fa;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.steps-title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin: 0 0 12px 0;
}

.error-steps ol {
  margin: 0;
  padding-left: 20px;
  color: #666;
  font-size: 14px;
  line-height: 1.8;
}

.error-steps li {
  margin-bottom: 8px;
}

.error-steps a {
  color: #4db8c4;
  text-decoration: none;
}

.error-steps a:hover {
  text-decoration: underline;
}

/* 登录提示浮层 */
.login-overlay {
  position: absolute;
  top: 80px;
  right: 20px;
  z-index: 2000;
  pointer-events: none;
}

.login-tip-card {
  position: relative;
  width: 280px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  padding: 20px;
  pointer-events: auto;
}

.tip-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #eee;
}

.map-icon {
  width: 20px;
  height: 20px;
  color: #4db8c4;
  flex-shrink: 0;
}

.tip-title {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.tip-description {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 16px;
}

.login-btn {
  width: 100%;
  height: 40px;
  background: #4db8c4;
  border: none;
  border-radius: 20px;
  font-size: 16px;
  font-weight: 500;
}

.login-btn:hover {
  background: #3da8b4;
}

.close-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 24px;
  height: 24px;
  background: rgba(0, 0, 0, 0.05);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 18px;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.close-btn:hover {
  background: rgba(0, 0, 0, 0.1);
  color: #333;
}

/* 职位详情浮层 */
.job-detail-overlay {
  position: absolute;
  left: 20px;
  top: 80px;
  bottom: 20px;
  z-index: 2000;
  pointer-events: none;
}

.job-detail-card {
  position: relative;
  width: 400px;
  max-height: calc(100vh - 100px);
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  padding: 24px;
  pointer-events: auto;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.job-detail-close {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 32px;
  height: 32px;
  background: rgba(0, 0, 0, 0.05);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 20px;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  z-index: 10;
}

.job-detail-close:hover {
  background: rgba(0, 0, 0, 0.1);
  color: #333;
}

.job-detail-header {
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
}

.job-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0 0 12px 0;
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.job-salary {
  font-size: 18px;
  font-weight: 600;
  color: #ff4757;
}

.job-meta {
  font-size: 14px;
  color: #666;
  display: flex;
  align-items: center;
  gap: 4px;
}

.job-detail-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.chat-btn {
  flex: 1;
  height: 44px;
  background: #4db8c4;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
}

.chat-btn:hover {
  background: #3da8b4;
}

.interest-btn {
  flex: 0 0 auto;
  height: 44px;
  padding: 0 20px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  color: #666;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.interest-btn:hover {
  border-color: #4db8c4;
  color: #4db8c4;
}

.interest-btn svg {
  width: 16px;
  height: 16px;
  stroke: currentColor;
  fill: none;
}

.job-detail-content {
  flex: 1;
  overflow-y: auto;
}

.content-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 16px 0;
}

.job-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 24px;
}

.job-tag {
  padding: 4px 12px;
  background: #f5f7fa;
  border-radius: 16px;
  font-size: 12px;
  color: #666;
  border: 1px solid #e0e0e0;
}

.job-section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin: 0 0 12px 0;
}

.section-list {
  margin: 0;
  padding-left: 20px;
  color: #666;
  font-size: 14px;
  line-height: 1.8;
}

.section-list li {
  margin-bottom: 8px;
}

.job-company {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #eee;
}

.company-name {
  font-size: 15px;
  font-weight: 500;
  color: #333;
  margin: 0 0 8px 0;
}

.company-address {
  font-size: 14px;
  color: #666;
  margin: 0;
  line-height: 1.6;
}

/* 滚动条样式 */
.job-detail-card::-webkit-scrollbar {
  width: 6px;
}

.job-detail-card::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.job-detail-card::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 3px;
}

.job-detail-card::-webkit-scrollbar-thumb:hover {
  background: #999;
}
</style>
