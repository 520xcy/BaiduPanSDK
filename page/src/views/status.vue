<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <el-icon><list /></el-icon> 正在下载
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
              icon="Delete"
              @click="handleDelete"
              style="width:100%"
              >删除
            </el-button>
          </el-col>
          <el-col :span="2">
            <el-button
              size="small"
              type="success"
              icon="Download"
              @click="handleDownload"
              style="width:100%"
              >下载
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
        row-key="localfile"
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
          prop="file"
          sortable
          fixed
        >
        </el-table-column>
        <el-table-column min-width="100px" label="大小" prop="size">
          <template #default="scope">
            {{ scope.row.size > 0 ? getfilesize(scope.row.size) : 0 }}
          </template>
        </el-table-column>
        <el-table-column width="100px" label="状态" prop="status">
        </el-table-column>
        <el-table-column min-width="600px" label="实际路径" prop="localfile">
        </el-table-column>
        <el-table-column
          min-width="150px"
          label="时间"
          prop="date"
        ></el-table-column>
        <el-table-column
          min-width="200px"
          label="备注"
          prop="connect"
        ></el-table-column>
        <el-table-column
          min-width="150px"
          label="文件id"
          prop="fsids"
        ></el-table-column>
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
  name: "status",
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
      noload_request({ url: apiUrl.getStatus, method: "get" }).then((res) => {
        console.log(res.data);
        tableData.data = res.data.data;
      });
    };
    getData();

    // 查询操作
    const handleDelete = () => {
      let keys = [];
      for (const key in multipleSelection.value) {
        keys.push(multipleSelection.value[key].localfile);
      }
      noload_request({
        url: apiUrl.delTask,
        method: "post",
        data: { key: keys },
      }).then((res) => {
        ElMessage.success("任务已删除");
      });
    };

    const handleDownload = () => {
      let fsids = [];
      for (const key in multipleSelection.value) {
        fsids.push(parseInt(multipleSelection.value[key].fsids));
      }
      noload_request({
        url: apiUrl.getFiles,
        method: "post",
        data: { fsids: fsids },
      }).then((res) => {
        ElMessage.success("任务开始下载");
      });
    };

    const filterTableData = computed(() =>
      tableData.data.filter(
        (data) =>
          !search.value ||
          data.file.toLowerCase().includes(search.value.toLowerCase())
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
      handleDelete,
      handleDownload,
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
