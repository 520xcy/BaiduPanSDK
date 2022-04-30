<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <el-icon><files /></el-icon> 全部文件
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="container">
      <div class="handle-box">
        <el-row :gutter="10">
          <el-col :span="2">
            <el-button
              size="small"
              type="success"
              icon="Download"
              @click="handleDownload"
              style="width: 100%"
              >下载
            </el-button>
          </el-col>
          <el-col :span="2">
            <el-button
              size="small"
              type="danger"
              icon="Delete"
              @click="handleDelete"
              style="width: 100%"
              >删除
            </el-button>
          </el-col>
          <el-col :span="6">
            <el-input
              v-model="search"
              size="small"
              placeholder="筛选文件名"
            ></el-input
          ></el-col>
          <el-col :span="5">
            <el-input
              size="small"
              v-model="query.start"
              placeholder="起始编号"
            ></el-input>
          </el-col>
          <el-col :span="5">
            <el-input
              size="small"
              v-model="query.limit"
              placeholder="每页显示"
            ></el-input>
          </el-col>
          <el-col :span="3">
            <el-button
              size="small"
              type="primary"
              icon="Search"
              @click="handleSearch"
              >搜索</el-button
            >
          </el-col>
        </el-row>
      </div>
      <el-table
        :data="filterTableData"
        height="800"
        stripe
        size="small"
        highlight-current-row
        class="table"
        ref="multipleTable"
        :default-sort="{ prop: 'server_mtime', order: 'descending' }"
        header-cell-class-name="table-header"
        lazy
        row-key="fs_id"
        :load="load"
        :tree-props="{ hasChildren: 'isdir' }"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column
          min-width="300px"
          label="文件名"
          prop="server_filename"
          sortable
        >
          <template #default="scope">
            <el-icon v-if="scope.row.isdir"><folder /></el-icon>
            {{ scope.row.server_filename }}
          </template>
        </el-table-column>
        <el-table-column width="100px" label="大小" prop="size" sortable>
          <template #default="scope">
            {{ scope.row.size > 0 ? getfilesize(scope.row.size) : "文件夹" }}
          </template>
        </el-table-column>
        <el-table-column
          min-width="150px"
          label="修改日期"
          prop="server_mtime"
          sortable
        >
          <template #default="scope">
            {{
              dayjs.unix(scope.row.server_mtime).format("YYYY-MM-DD HH:mm:ss")
            }}
          </template>
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
import dayjs from "dayjs";

export default {
  name: "filelist",
  setup() {
    const search = ref("");
    const multipleSelection = ref([]);
    const query = reactive({
      order: "",
      desc: "",
      start: 0,
      limit: 1000,
      ctime: 0,
      mtime: 0,
    });
    const tableData = reactive({
      data: [],
    });
    // 获取表格数据
    const getData = () => {
      noload_request({ url: apiUrl.getList, method: "get", params: query }).then(
        (res) => {
          console.log(res.data);
          tableData.data = res.data.data.list;
        }
      );
    };
    getData();
    // 查询操作
    const handleSearch = () => {
      query.start = 0;
      getData();
    };

    const filterTableData = computed(() =>
      tableData.data.filter(
        (data) =>
          !search.value ||
          data.server_filename
            .toLowerCase()
            .includes(search.value.toLowerCase())
      )
    );

    const load = (row, treeNode, resolve) => {
      noload_request({
        url: apiUrl.getList,
        method: "get",
        params: { dir: row.path, limit: query.limit },
      }).then((res) => {
        resolve(res.data.data.list);
      });
    };

    const handleDetail = (index, row) => {
      console.log(index, row);
    };

    const handleDownload = () => {
      let fsids = [];
      for (const key in multipleSelection.value) {
        fsids.push(multipleSelection.value[key].fs_id);
      }
      noload_request({
        url: apiUrl.getFiles,
        method: "post",
        data: { fsids: fsids },
      }).then((res) => {
        ElMessage.success("任务开始下载");
      });
    };

    const handleDelete = () => {
      ElMessageBox.confirm("确定要删除吗？", "提示", {
        type: "warning",
      }).then(() => {
        let files = [];
        for (const key in multipleSelection.value) {
          files.push(multipleSelection.value[key].path);
        }
        noload_request({
          url: apiUrl.delFiles,
          method: "post",
          data: { files: files },
        }).then((res) => {
          ElMessage.success("删除成功");
          for (var i = tableData.data.length - 1; i != -1; i--) {
            if (files.includes(tableData.data[i].path))
              tableData.data.splice(i, 1);
          }
        });
      });
    };

    const handleSelectionChange = (val) => {
      multipleSelection.value = val;
    };
    return {
      getfilesize,
      load,
      dayjs,
      query,
      search,
      filterTableData,
      handleDelete,
      handleSearch,
      handleDownload,
      handleDetail,
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
