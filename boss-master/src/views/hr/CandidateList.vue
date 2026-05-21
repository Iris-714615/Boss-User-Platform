<template>
  <div class="candidate-list-page">
    <header class="page-header">
      <div>
        <h2>候选人管理</h2>
        <p class="sub">管理候选人信息，跟踪招聘进度</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="handleImport">
          <el-icon><Upload /></el-icon>
          导入候选人
        </el-button>
        <el-button @click="handleExport">
          <el-icon><Download /></el-icon>
          导出列表
        </el-button>
      </div>
    </header>

    <!-- 搜索筛选区域 -->
    <section class="card filter-section">
      <div class="filter-row">
        <el-input
          v-model="filters.keyword"
          placeholder="搜索姓名、职位、公司"
          clearable
          style="width: 300px"
          @keyup.enter="loadData"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>

        <el-select
          v-model="filters.stage"
          placeholder="招聘阶段"
          clearable
          style="width: 150px"
        >
          <el-option label="全部" value="" />
          <el-option label="待筛选" value="待筛选" />
          <el-option label="面试中" value="面试中" />
          <el-option label="已通过" value="已通过" />
          <el-option label="已拒绝" value="已拒绝" />
        </el-select>

        <el-input
          v-model="filters.position"
          placeholder="期望职位"
          clearable
          style="width: 200px"
        />

        <el-button type="primary" @click="loadData">
          <el-icon><Search /></el-icon>
          搜索
        </el-button>
        <el-button @click="handleResetFilter">重置</el-button>
      </div>
    </section>

    <!-- 候选人列表 -->
    <section class="card table-section">
      <el-table
        v-loading="loading"
        :data="candidateList"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="desiredPosition" label="期望职位" width="180" />
        <el-table-column prop="stage" label="招聘阶段" width="120">
          <template #default="{ row }">
            <el-tag
              :type="getStageType(row.stage)"
              size="small"
            >
              {{ row.stage }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="experience" label="工作经验" width="120" />
        <el-table-column prop="education" label="学历" width="100" />
        <el-table-column prop="phone" label="联系电话" width="150" />
        <el-table-column prop="updateTime" label="更新时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              link
              type="primary"
              size="small"
              @click="handleView(row)"
            >
              查看
            </el-button>
            <el-button
              link
              type="primary"
              size="small"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              link
              type="danger"
              size="small"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper" v-if="pagination.total > 0">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadData"
          @current-change="loadData"
        />
      </div>

      <!-- 空状态 -->
      <div v-if="!loading && candidateList.length === 0" class="empty-state">
        <el-empty description="暂无候选人数据" />
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { Search, Upload, Download } from "@element-plus/icons-vue";
import { http } from "@/utils/request";

const loading = ref(false);
const candidateList = ref([]);

const filters = reactive({
  keyword: "",
  stage: "",
  position: "",
});

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
});

// 获取阶段标签类型
const getStageType = (stage) => {
  const typeMap = {
    待筛选: "info",
    面试中: "warning",
    已通过: "success",
    已拒绝: "danger",
  };
  return typeMap[stage] || "info";
};

// 加载数据
const loadData = async () => {
  loading.value = true;
  try {
    // TODO: 调用获取候选人列表接口
    // const response = await http.get("/hr/candidates/", {
    //   params: {
    //     page: pagination.page,
    //     page_size: pagination.pageSize,
    //     ...filters,
    //   },
    // });

    // 模拟数据
    await new Promise((resolve) => setTimeout(resolve, 500));
    
    candidateList.value = [
      {
        id: 1,
        name: "张三",
        desiredPosition: "前端开发工程师",
        stage: "面试中",
        experience: "3-5年",
        education: "本科",
        phone: "138****8888",
        updateTime: "2024-01-15 10:30",
      },
      {
        id: 2,
        name: "李四",
        desiredPosition: "Java开发工程师",
        stage: "待筛选",
        experience: "5-10年",
        education: "本科",
        phone: "139****9999",
        updateTime: "2024-01-14 15:20",
      },
      {
        id: 3,
        name: "王五",
        desiredPosition: "产品经理",
        stage: "已通过",
        experience: "3-5年",
        education: "硕士",
        phone: "137****7777",
        updateTime: "2024-01-13 09:15",
      },
    ];
    
    pagination.total = 3;
  } catch (error) {
    console.error("加载候选人列表失败:", error);
    ElMessage.error("加载候选人列表失败，请稍后重试");
  } finally {
    loading.value = false;
  }
};

// 重置筛选
const handleResetFilter = () => {
  filters.keyword = "";
  filters.stage = "";
  filters.position = "";
  pagination.page = 1;
  loadData();
};

// 查看候选人
const handleView = (row) => {
  ElMessage.info(`查看候选人：${row.name}`);
  // TODO: 打开候选人详情弹窗
};

// 编辑候选人
const handleEdit = (row) => {
  ElMessage.info(`编辑候选人：${row.name}`);
  // TODO: 打开编辑弹窗
};

// 删除候选人
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除候选人"${row.name}"吗？`,
      "确认删除",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }
    );

    // TODO: 调用删除接口
    // await http.delete(`/hr/candidates/${row.id}/`);
    
    ElMessage.success("删除成功");
    loadData();
  } catch (error) {
    if (error !== "cancel") {
      console.error("删除失败:", error);
      ElMessage.error("删除失败，请稍后重试");
    }
  }
};

// 导入候选人
const handleImport = () => {
  ElMessage.info("导入候选人功能开发中");
  // TODO: 实现导入功能
};

// 导出列表
const handleExport = () => {
  ElMessage.info("导出列表功能开发中");
  // TODO: 实现导出功能
};

onMounted(() => {
  loadData();
});
</script>

<style scoped>
.candidate-list-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-header {
  background: #fff;
  border-radius: 12px;
  padding: 20px 24px;
  border: 1px solid #eef0f4;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header h2 {
  font-size: 24px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 8px 0;
}

.page-header .sub {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #eef0f4;
}

.filter-section {
  margin-bottom: 0;
}

.filter-row {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.table-section {
  min-height: 400px;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.empty-state {
  padding: 60px 0;
  text-align: center;
}

:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-table th) {
  background: #f9fafb;
  font-weight: 600;
  color: #374151;
}
</style>


