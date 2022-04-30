<template>
  <el-row :gutter="20">
    <el-col :span="6">
      <p>扫二维码</p>
      <img :src="qrcode_url" alt="" />
    </el-col>
    <el-col :span="6">
      <p>或在下面输入:{{ user_code }}</p>
      <iframe
        :src="verification_url"
        width="500px"
        height="500px"
        frameborder="0"
        sandbox="allow-scripts allow-forms allow-same-origin"
      ></iframe>
    </el-col>
    <el-col :span="12" :offset="6"
      ><el-button
        style="width: 100%"
        size="large"
        type="primary"
        plain
        @click="getAccessToken()"
        >已完成授权</el-button
      >
    </el-col>
  </el-row>
</template>

<script>
import { ref } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { apiUrl } from "../api/index";
import request from "../utils/request";

export default {
  setup() {
    const router = useRouter();

    const user_code = ref("");
    const verification_url = ref("");
    const qrcode_url = ref("");
    const getCode = () => {
      request({ url: apiUrl.getCode, method: "get" }).then((res) => {
        user_code.value = res.data.data.user_code;
        verification_url.value = res.data.data.verification_url;
        qrcode_url.value = res.data.data.qrcode_url;
      });
    };
    getCode();

    const getAccessToken = () => {
      request({ url: apiUrl.getAccessToken, method: "get" }).then((res) => {
        if (res.data.code !== 200) {
          ElMessage.error("token获取失败,请刷新页面重新授权");
        } else {
          request({ url: apiUrl.getUserinfo, method: "get" }).then((res) => {
            ElMessage.success("授权成功");
            router.push("/");
          });
        }
      });
    };
    const store = useStore();
    store.commit("clearTags");

    return {
      user_code,
      verification_url,
      qrcode_url,
      getAccessToken,
    };
  },
};
</script>

<style scoped>
iframe {
  width: 1024px;
  height: 400px;
}

img {
  width: 300px;
  height: 300px;
}
</style>