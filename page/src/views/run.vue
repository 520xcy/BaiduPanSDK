<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <el-icon><video-play /></el-icon> 正在下载
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="container">
      <div class="handle-box">
        <el-row :gutter="10">
          <el-col :span="2">
            <el-button
              size="small"
              type="danger"
              icon="Close"
              @click="handleStop"
              style="width: 100%"
              >停止
            </el-button>
          </el-col>
          <el-col :span="6">
            <el-input
              v-model="search"
              size="small"
              placeholder="筛选文件名"
            ></el-input
          ></el-col>
        </el-row>
      </div>
      <el-table
        :data="filterTableData"
        height="800"
        stripe
        size="small"
        highlight-current-row
        class="table"
        row-key="local_filename"
        ref="multipleTable"
        header-cell-class-name="table-header"
        @selection-change="handleSelectionChange"
      >
        <el-table-column
          type="selection"
          width="55"
          :reserve-selection="true"
        ></el-table-column>
        <el-table-column
          min-width="300px"
          label="文件名"
          prop="filename"
          sortable
          fixed
        >
        </el-table-column>
        <el-table-column min-width="300px" label="下载进度">
          <template #default="scope">
            <el-progress :percentage="(scope.row.size / scope.row.total) * 100">
              {{ ((scope.row.size / scope.row.total) * 100).toFixed(2) }}%&nbsp;{{ getfilesize(scope.row.speed) }}/s
            </el-progress>
          </template>
        </el-table-column>
        <el-table-column width="100px" label="总文件大小" prop="total">
          <template #default="scope">
            {{ scope.row.total > 0 ? getfilesize(scope.row.total) : "文件夹" }}
          </template>
        </el-table-column>
        <el-table-column
          min-width="600px"
          label="实际路径"
          prop="local_filename"
        >
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { apiUrl } from "../api/index";
import noload_request from "../utils/noload_request";
import { getfilesize } from "../utils/tools";

export default {
  name: "run",
  beforeRouteLeave(to, from, next) {
    window.clearInterval(this.timer);
    next();
  },
  setup() {
    const search = ref("");
    const multipleSelection = ref([]);
    const tableData = reactive({
      data: [],
    });
    const timer = window.setInterval(() => {
      window.setTimeout(getData(), 0);
    }, 2000);
    // 获取表格数据
    const getData = () => {
      noload_request({ url: apiUrl.getRun, method: "get" }).then((res) => {
        console.log(res.data);
        tableData.data = res.data.data;
      });
    };
    getData();

    // 查询操作
    const handleStop = () => {
      let fsids = [];
      for (const key in multipleSelection.value) {
        fsids.push(parseInt(multipleSelection.value[key].fs_id));
      }
      noload_request({
        url: apiUrl.getStop,
        method: "post",
        data: { fsids: fsids },
      }).then((res) => {
        ElMessage.success("任务已停止");
      });
    };

    const filterTableData = computed(() =>
      tableData.data.filter(
        (data) =>
          !search.value ||
          data.filename.toLowerCase().includes(search.value.toLowerCase())
      )
    );

    const handleSelectionChange = (val) => {
      multipleSelection.value = val;
    };
    return {
      timer,
      getfilesize,
      search,
      filterTableData,
      handleStop,
      handleSelectionChange,
    };
  },
};
</script>

<style scoped>
.handle-box {
  margin-bottom: 20px;
}

.handle-select {
  width: 120px;
}

.handle-input {
  width: 200px;
  display: inline-block;
}
.table {
  width: 100%;
  font-size: 9px;
}
.red {
  color: #ff0000;
}
.mr10 {
  margin-right: 10px;
}
.mr1 {
  margin-right: 1px;
}
.table-td-thumb {
  display: block;
  margin: auto;
  width: 40px;
  height: 40px;
}
</style>
