<template>
  <div class="hr-home-page">
    <!-- 概览统计 -->
    <section class="stats">
      <div class="stat-card">
        <div class="stat-title">今日新增简历</div>
        <div class="stat-value">12</div>
        <div class="stat-desc up">↑ 较昨日 +3</div>
      </div>
      <div class="stat-card">
        <div class="stat-title">待处理面试</div>
        <div class="stat-value">8</div>
        <div class="stat-desc">待安排</div>
      </div>
      <div class="stat-card">
        <div class="stat-title">活跃职位</div>
        <div class="stat-value">24</div>
        <div class="stat-desc up">↑ 较上周 +5</div>
      </div>
      <div class="stat-card">
        <div class="stat-title">候选人总数</div>
        <div class="stat-value">156</div>
        <div class="stat-desc">人才库</div>
      </div>
    </section>

    <!-- 功能卡片 -->
    <section class="grid">
      <div class="feature-card">
        <div class="card-head">
          <div class="icon-wrap">📢</div>
          <div>
            <div class="card-title">职位发布</div>
            <div class="card-sub">快速发布招聘职位</div>
          </div>
        </div>
        <ul class="card-list">
          <li>• 一键发布职位信息</li>
          <li>• 智能职位推荐</li>
          <li>• 职位数据分析</li>
        </ul>
        <div class="card-actions">
          <router-link to="/hr/post" class="primary-btn">创建职位</router-link>
        </div>
      </div>

      <div class="feature-card">
        <div class="card-head">
          <div class="icon-wrap">👥</div>
          <div>
            <div class="card-title">候选人管理</div>
            <div class="card-sub">高效管理人才库</div>
          </div>
        </div>
        <ul class="card-list">
          <li>• 简历筛选与分类</li>
          <li>• 候选人跟进记录</li>
          <li>• 批量操作功能</li>
        </ul>
        <div class="card-actions">
          <router-link to="/hr/candidates" class="primary-btn">进入人才库</router-link>
          <button class="ghost-btn">批量导入</button>
        </div>
      </div>

      <div class="feature-card">
        <div class="card-head">
          <div class="icon-wrap">🤖</div>
          <div>
            <div class="card-title">智能招聘助手</div>
            <div class="card-sub">AI驱动的招聘工具</div>
          </div>
        </div>
        <ul class="card-list">
          <li>• 智能简历匹配</li>
          <li>• 自动筛选候选人</li>
          <li>• 招聘数据分析</li>
        </ul>
        <div class="card-actions">
          <router-link to="/hr/agent" class="primary-btn">打开助手</router-link>
          <button class="ghost-btn">查看推荐</button>
        </div>
      </div>

      <div class="feature-card">
        <div class="card-head">
          <div class="icon-wrap">🎓</div>
          <div>
            <div class="card-title">学历验证</div>
            <div class="card-sub">快速验证候选人学历</div>
          </div>
        </div>
        <ul class="card-list">
          <li>• 在线学历验证</li>
          <li>• 验证记录查询</li>
          <li>• 批量验证功能</li>
        </ul>
        <div class="card-actions">
          <router-link to="/hr/degree" class="primary-btn">发起验证</router-link>
          <button class="ghost-btn">查看记录</button>
        </div>
      </div>

      <div class="feature-card">
        <div class="card-head">
          <div class="icon-wrap">🧾</div>
          <div>
            <div class="card-title">人事助手</div>
            <div class="card-sub">HR专业问答助手</div>
          </div>
        </div>
        <ul class="card-list">
          <li>• 人事政策咨询</li>
          <li>• 招聘流程指导</li>
          <li>• 法律法规查询</li>
        </ul>
        <div class="card-actions">
          <router-link to="/hr/assistant" class="primary-btn">点击使用</router-link>
          <button class="ghost-btn">配置提醒</button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
// HR首页组件
</script>

<style scoped>
.hr-home-page {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 14px;
  border: 1px solid #eef0f4;
  box-shadow: 0 4px 8px rgba(17, 24, 39, 0.03);
}

.stat-title {
  color: #6b7280;
  font-size: 13px;
}

.stat-value {
  font-size: 26px;
  font-weight: 700;
  color: #0f172a;
  margin: 6px 0;
}

.stat-desc {
  font-size: 12px;
  color: #6b7280;
}

.stat-desc.up {
  color: #0ea5e9;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 14px;
}

.feature-card {
  background: #fff;
  border-radius: 14px;
  padding: 16px;
  border: 1px solid #eef0f4;
  box-shadow: 0 8px 16px rgba(17, 24, 39, 0.04);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.card-head {
  display: flex;
  gap: 12px;
  align-items: center;
}

.icon-wrap {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: #f0f9ff;
  display: grid;
  place-items: center;
  font-size: 18px;
}

.card-title {
  font-size: 16px;
  font-weight: 700;
  color: #0f172a;
}

.card-sub {
  font-size: 13px;
  color: #6b7280;
}

.card-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: #374151;
  font-size: 13px;
}

.card-actions {
  display: flex;
  gap: 10px;
}

.primary-btn {
  background: #3b82f6;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: background 0.2s;
}

.primary-btn:hover {
  background: #2563eb;
}

.ghost-btn {
  background: transparent;
  color: #6b7280;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.ghost-btn:hover {
  background: #f9fafb;
  color: #374151;
}
</style>

