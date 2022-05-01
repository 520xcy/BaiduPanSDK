<template>
  <div class="header">
    <!-- 折叠按钮 -->
    <div class="collapse-btn" @click="collapseChage">
      <el-icon v-if="!collapse"><fold /></el-icon>
      <el-icon v-else><expand /></el-icon>
    </div>
    <div class="logo">度盘管理</div>
    <div class="header-right">
      <div class="header-user-con">
        <div class="diskuse">
          <el-progress :percentage="progress">
            <span style="color: #fff">{{ size }}</span>
          </el-progress>
        </div>

        <!-- 用户头像 -->
        <div class="user-avator">
          <img :src="avatar" />
        </div>
        <!-- 用户名下拉菜单 -->
        <el-dropdown class="user-name" trigger="click" @command="handleCommand">
          <span class="el-dropdown-link">
            {{ username }}
            <el-icon><caret-bottom /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="loginout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </div>
</template>
<script>
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { apiUrl } from "../api/index";
import noload_request from "../utils/noload_request";
import { getfilesize } from "../utils/tools";

export default {
  setup() {
    const size = ref("");

    const username = ref("");
    const avatar = ref("");
    const progress = ref(0);

    const getinfo = () => {
      noload_request({ url: apiUrl.getSize, method: "get" }).then((res) => {
        size.value =
          getfilesize(res.data.data.used) +
          "/" +
          getfilesize(res.data.data.total);
        progress.value = (res.data.data.used / res.data.data.total) * 100;
      });
      noload_request({ url: apiUrl.getUserinfo, method: "get" }).then((res) => {
        username.value = res.data.data.baidu_name;
        avatar.value = res.data.data.avatar_url;
      });
    };
    getinfo();

    const store = useStore();
    const collapse = computed(() => store.state.collapse);
    // 侧边栏折叠
    const collapseChage = () => {
      store.commit("handleCollapse", !collapse.value);
    };

    onMounted(() => {
      if (document.body.clientWidth < 1500) {
        collapseChage();
      }
    });

    // 用户名下拉菜单选择事件
    const router = useRouter();
    const handleCommand = (command) => {
      if (command == "loginout") {
        noload_request({ url: apiUrl.logOut, method: "get" }).then((res) => {
          router.push("/login");
        });
      }
    };

    return {
      progress,
      size,
      username,
      avatar,
      collapse,
      collapseChage,
      handleCommand,
    };
  },
};
</script>
<style scoped>
.header {
  position: relative;
  box-sizing: border-box;
  width: 100%;
  height: 70px;
  font-size: 22px;
  color: #fff;
}
.collapse-btn {
  float: left;
  padding: 0 21px;
  cursor: pointer;
  line-height: 70px;
}
.header .logo {
  float: left;
  width: 250px;
  line-height: 70px;
}
.header-right {
  float: right;
  padding-right: 50px;
}
.header-user-con {
  display: flex;
  height: 70px;
  align-items: center;
}
.btn-fullscreen {
  transform: rotate(45deg);
  margin-right: 5px;
  font-size: 24px;
}
.btn-bell,
.btn-fullscreen {
  position: relative;
  width: 30px;
  height: 30px;
  text-align: center;
  border-radius: 15px;
  cursor: pointer;
}
.btn-bell-badge {
  position: absolute;
  right: 0;
  top: -2px;
  width: 8px;
  height: 8px;
  border-radius: 4px;
  background: #f56c6c;
  color: #fff;
}
.btn-bell .el-icon-bell {
  color: #fff;
}
.user-name {
  margin-left: 10px;
}
.user-avator {
  margin-left: 20px;
}
.user-avator img {
  display: block;
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
.el-dropdown-link {
  color: #fff;
  cursor: pointer;
}
.el-dropdown-menu__item {
  text-align: center;
}
.diskuse {
  width: 400px;
}
</style>
