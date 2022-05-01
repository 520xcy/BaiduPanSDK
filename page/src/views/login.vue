<template>
  <div class="login-wrap">
    <div class="ms-login">
      <div class="ms-title">管理登录</div>
      <el-form
        :model="param"
        :rules="rules"
        ref="login"
        label-width="0px"
        class="ms-content"
      >
        <el-form-item prop="user">
          <el-input v-model="param.user" placeholder="用户名">
            <template #prepend>
              <el-button icon="user"></el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            type="password"
            placeholder="密码"
            v-model="param.password"
            @keyup.enter="submitForm()"
          >
            <template #prepend>
              <el-button icon="lock"></el-button>
            </template>
          </el-input>
        </el-form-item>
        <div class="login-btn">
          <el-button type="primary" @click="submitForm()">登录</el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { apiUrl } from "../api/index";
import request from "../utils/request";

export default {
  setup() {
    const router = useRouter();
    const param = reactive({
      user: "",
      password: "",
    });
  
    const rules = {
      user: [
        {
          required: true,
          message: "请输入用户名",
          trigger: "blur",
        },
      ],
      password: [{ required: true, message: "请输入密码", trigger: "blur" }],
    };
    const login = ref(null);
    const submitForm = () => {
      login.value.validate((valid) => {
        if (valid) {
          request({ url: apiUrl.getLogin, method: "post", data: param }).then(
            (res) => {
              ElMessage.success("登录成功");
              // request({ url: apiUrl.me, method: "get" }).then((res) => {
              //   if (Object.hasOwnProperty.call(res.data, 'get_departments') && Object.hasOwnProperty.call(res.data.get_departments, 'name')) {
              //   }
              //   username.value = res.data.data.name;
              // });
            
              localStorage.setItem("baidusdk", res.data.token);

              router.push('/');
            }
          );
        } else {
          ElMessage.error("登录失败");
          return false;
        }
      });
    };

    const store = useStore();
    store.commit("clearTags");

    return {
      param,
      rules,
      login,
      submitForm,
    };
  },
};
</script>

<style scoped>
.login-wrap {
  position: relative;
  width: 100%;
  height: 100%;
  background-image: url(../assets/img/login-bg.jpg);
  background-size: 100%;
}
.ms-title {
  width: 100%;
  line-height: 50px;
  text-align: center;
  font-size: 20px;
  color: #fff;
  border-bottom: 1px solid #ddd;
}
.ms-login {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 350px;
  margin: -190px 0 0 -175px;
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.3);
  overflow: hidden;
}
.ms-content {
  padding: 30px 30px;
}
.login-btn {
  text-align: center;
}
.login-btn button {
  width: 100%;
  height: 36px;
  margin-bottom: 10px;
}
.login-tips a {
  font-size: 12px;
  line-height: 30px;
  color: #409eff;
}
</style>