<template> 
<div>
    <div>
    <h1>搜索功能</h1>
    <el-input v-model="name" placeholder="请输入内容" clearable></el-input>
    <el-input v-model="price" placeholder="请输入价格" clearable></el-input>
    <el-button type="primary" @click="search">搜索</el-button>
    <h1>分类列表</h1>
    <el-list>
        <el-list-item v-for="item in category_list" :key="item.id">
           <el-button type="primary" @click="changeCategory(item.id)">{{item.name}}</el-button>
        </el-list-item>
    </el-list>

    <h1>商品列表</h1>
    <el-list>
        <el-list-item v-for="item in product_list" :key="item.id">
            {{item.name}}  &nbsp;&nbsp;&nbsp;  {{ item.price }}  &nbsp;&nbsp;&nbsp; 
             <el-button type="primary" @click="addCart(item.id)">加入购物车</el-button>
            <br>
        </el-list-item>
    </el-list>
    </div>
    <div>
    <h1>分页</h1>

    <!-- <el-pagination
        layout="total, sizes, prev, pager, next, jumper"
        :total="100"
        :page-size="10"
        @current-change="handleCurrentChange"
    >
    </el-pagination> -->
    <div v-for = "i in tpages">
      <el-button type="primary" @click="changpage(i)">{{i}}</el-button>
    </div>

</div>

</div>
</template>
<script setup>
import { ref,onMounted } from 'vue'
import request from '@/utils/request'

const name = ref('')
const price = ref('')
const total = ref(0)
const pageSize = ref(2)
const currentPage = ref(1)
const categoryid = ref(0)
const tpages = ref(0)
const search = () => {
    currentPage.value = 1
    getProductList()
}
const category_list = ref([])
const product_list = ref([])

const handleCurrentChange = (val) => {
    console.log(`当前页: ${val}`)
}

const changpage = (i) => {
    currentPage.value = i
    getProductList()
}

const changeCategory = (id) => {
    categoryid.value = id
    currentPage.value = 1
    getProductList()
}

const getCategoryList =  () => {
    request.get('/category/').then(res => {
        category_list.value = res.data.category_list
    })
}

const getProductList =  () => {
   
   request.get('/product/',{
        params:{
            page:currentPage.value,
            page_size:pageSize.value,
            name:name.value,
            price:price.value,
            category_id:categoryid.value,
        }
    }).then(res => {
        product_list.value = res.data.product_list
        total.value = res.data.tcount
        tpages.value = Math.ceil(total.value/pageSize.value)
    })
}

const addCart = (id) => {
    // var token = localStorage.getItem('token')
    // if(!token){
    //     alert('请先登录')
    //     router.push('/login')
    // }
    request.post('/cart/',{
        product_id:id,
        userid:1,
    }).then(res => {
        if(res.data.code == 200){
            ElMessage.success('加入购物车成功')
        }
    })
}



onMounted(() => {
    getCategoryList()
    getProductList()
})

</script>