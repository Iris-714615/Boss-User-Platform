<template>
    <div>
        <h1>Test Chat</h1>
        <div>
            <div v-for="i in messages">{{i.user}} {{i.content}}</div>
        </div>
        <input type="text" v-model="textmes" placeholder="请输入消息">
        <button @click="sendMessage">发送</button>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import request from '@/utils/request'
const messages = ref([{"id":1,"user":"AI","content":"请问你有什么问题？"}])
const textmes = ref('')
const sseEvent = ref(null)

const flag = ref(false)
const number = ref(0)
const flagnumber = ref(1)


const initsse = (message) => {
    // 关闭旧的 SSE 连接（避免多个流同时跑）
    if (sseEvent.value) {
        sseEvent.value.close()
    }
    number.value = 0
    var url = "http://localhost:8000/chatai/chat_stream?message="+message
    sseEvent.value = new EventSource(url)
    flagnumber.value += 1
    sseEvent.value.onmessage = (event) => {
        // 先判断是不是结束标记，是就直接返回，不追加到内容
        if(event.data.includes("[DONE]")){
            closeSse()
            flag.value = false
            return
        }

        number.value += 1
        if (number.value == 1){
           messages.value.push({"id":flagnumber.value, "user": "AI说", content: event.data.replace(/\n\n$/, '') })
        }else{
            // messages.value.push({ id: flagnumber.value, user: '', content: event.data.replace(/\n\n$/, '') })
            messages.value.forEach(item => {
                if (item.id == flagnumber.value){
                    item.content = item.content +event.data.replace(/\n\n$/, '')
                }
            })
        }
    }
        
}


const closeSse = () => {
    sseEvent.value.close()
    sseEvent.value = null
}

const sendMessage = () => {
    flagnumber.value += 1
    messages.value.push({ id: flagnumber.value, user: '用户', content: textmes.value })
    initsse(textmes.value)
    // request.get('/chat_many?message=' + textmes.value).then(res => {
    //     messages.value.push({ user: 'AI', content: res.message })
    //     textmes.value = ''
    // })
}
</script>