<template>
    <div>
        <div>
            购物车列表
        </div>
        <div>
            <table border="1">
                <tr>
                    <th>
                        <el-checkbox v-model="check_all" @change="changeCheckAll()">全选</el-checkbox>
                    </th>
                    <th>
                        商品图片
                    </th>
                    <th>
                        商品名称
                    </th>
                    <th>
                        商品单价
                    </th>
                    <th>
                        商品数量
                    </th>
                    <th>
                        商品总价
                    </th>
                    <th>
                        商品规格
                    </th>
                    <th>
                        操作
                    </th>
                </tr>

                <tr v-for="item in cartlist" :key="item.id">
                    <td>
                        <el-checkbox v-model="item.is_check" @change="changeCheck(item.id)"></el-checkbox>
                    </td>
                    <td>
                        <img  alt="" :src="item.image" width="100px" height="100px">
                    </td>
                    <td>
                       {{item.name}}
                    </td>
                    <td>
                       {{item.price}}
                    </td>
                    <td>
                       <el-input-number min="1" :max="1000" v-model="item.count" @change="changeCount(item.id,item.count)"></el-input-number>
                    </td>
                    <td>
                       {{item.tprice}}
                    </td>
                    <td>
                        <el-select v-model="item.types" placeholder="请选择" @change="change(item.id,item.types)">
                            <el-option
                            v-for="item in item.pricelist"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id">
                            </el-option>
                        </el-select>
                      
                    </td>
                   
                    <td>
                        删除
                    </td>
                </tr>
            </table>
        </div>
        <div>
            总价：{{total}}
        </div>
        
    </div>

</template>
<script setup>
import { ref,onMounted } from 'vue'
import request from '@/utils/request'

const cartlist = ref([])
const total = ref(0)

const check_all = ref(false)

const getCartList =  () => {
   request.get('/cart/?userid=1').then(res => {
        cartlist.value = res.data.cart_list
        cartlist.value.forEach(item => {
            if(item.is_check == 1){
                 item.is_check = true
            }else{
                item.is_check = false
            }
        })
        total.value = res.data.total_price
        check_all.value = res.data.check_all
    })
}


const changeCount = (id,count) => {
    request.post('/changeCount/',{
        userid:1,
        id:id,
        count:count
    }).then(res => {
        getCartList()
    })
}

const change = (id,types) => {
    request.post('/changeTypes/',{
        userid:1,
        id:id,
        types:types
    }).then(res => {
        getCartList()
    })
}

const delall = (id,types) => {
    var del_list = []
    if(types == 1){
        //单个删除
        del_list.push(id)
    }else if(types == 2){
        //全选删除
        cartlist.value.forEach(item => {
            if(item.is_check == true){
                del_list.push(item.id)
            }
        })
    }
    request.post('/cartdel/',{
        userid:1,
        del_list:del_list
    }).then(res => {
        getCartList()
    })
}

const changeCheck = (id) => {
    request.post('/changeCheck/',{
        userid:1,
        id:id
    }).then(res => {
        getCartList()
    })
}

const changeCheckAll = () => {
    request.post('/changeCheckAll/',{
        userid:1,
        check_all:check_all.value
    }).then(res => {
        getCartList()
    })
}
onMounted(() => {
    getCartList()
})

</script>