import{a as I,k as L,l as M,i as U,m as Y,n as j,o as F,p as H,q as O,r as V,s as R}from"./_element-plus.6fe2094f.js";import{_ as W,g as X,s as b,a as v}from"./index.53b3ddbb.js";import{q as A}from"./__vendor.a475fe49.js";import{g as x,r as E,f as G,al as S,o as B,c as J,a as D,a1 as e,X as o,$ as c,W as K,_ as P,a0 as k}from"./_@vue.454cd839.js";import"./_@element-plus.19db05d5.js";const Q={name:"filelist",setup(){const _=x(""),n=x([]),m=E({order:"",desc:"",start:0,limit:1e3,ctime:0,mtime:0}),l=E({data:[]}),u={},y=()=>{b({url:v.getList,method:"get",params:m}).then(a=>{console.log(a.data),l.data=a.data.data.list})};y();const w=()=>{m.start=0,y()},p=G(()=>l.data.filter(a=>!_.value||a.server_filename.toLowerCase().includes(_.value.toLowerCase()))),f=(a,s,d)=>{u[a.path]={row:a,treeNode:s,resolve:d},b({url:v.getList,method:"get",params:{dir:a.path,limit:m.limit}}).then(r=>{d(r.data.data.list)})};return{getfilesize:X,load:f,dayjs:A,query:m,search:_,filterTableData:p,handleDelete:()=>{R.confirm("\u786E\u5B9A\u8981\u5220\u9664\u5417\uFF1F","\u63D0\u793A",{type:"warning"}).then(()=>{let a=[],s=[];for(const r in n.value)a.push(n.value[r].path),s.push(n.value[r].f_dir);let d=[];s=s.filter(r=>Object.keys(u).includes(r)&&!a.includes(r)&&!d.includes(r)&&d.push(r)),b({url:v.delFiles,method:"post",data:{files:a}}).then(r=>{for(var t=l.data.length-1;t!=-1;t--)a.includes(l.data[t].path)&&l.data.splice(t,1);setTimeout(()=>{for(let C=0;C<d.length;C++){const{row:T,treeNode:q,resolve:N}=u[d[C]];f(T,q,N)}},2e3),V.success("\u5220\u9664\u6210\u529F")})})},handleSearch:w,handleDownload:()=>{let a=[];for(const s in n.value)a.push(n.value[s].fs_id);b({url:v.getFiles,method:"post",data:{fsids:a}}).then(s=>{V.success("\u4EFB\u52A1\u5F00\u59CB\u4E0B\u8F7D")})},handleDetail:(a,s)=>{console.log(a,s)},handleSelectionChange:a=>{n.value=a}}}},Z={class:"crumbs"},$={class:"container"},ee={class:"handle-box"};function ae(_,n,m,l,u,y){const w=S("files",!0),p=I,f=L,z=M,h=U,i=Y,g=j,a=F,s=H,d=S("folder"),r=O;return B(),J("div",null,[D("div",Z,[e(z,{separator:"/"},{default:o(()=>[e(f,null,{default:o(()=>[e(p,null,{default:o(()=>[e(w)]),_:1}),c(" \u5168\u90E8\u6587\u4EF6 ")]),_:1})]),_:1})]),D("div",$,[D("div",ee,[e(a,{gutter:10},{default:o(()=>[e(i,{span:2},{default:o(()=>[e(h,{size:"small",type:"success",icon:"Download",onClick:l.handleDownload,style:{width:"100%"}},{default:o(()=>[c("\u4E0B\u8F7D ")]),_:1},8,["onClick"])]),_:1}),e(i,{span:2},{default:o(()=>[e(h,{size:"small",type:"danger",icon:"Delete",onClick:l.handleDelete,style:{width:"100%"}},{default:o(()=>[c("\u5220\u9664 ")]),_:1},8,["onClick"])]),_:1}),e(i,{span:6},{default:o(()=>[e(g,{modelValue:l.search,"onUpdate:modelValue":n[0]||(n[0]=t=>l.search=t),size:"small",placeholder:"\u7B5B\u9009\u6587\u4EF6\u540D"},null,8,["modelValue"])]),_:1}),e(i,{span:5},{default:o(()=>[e(g,{size:"small",modelValue:l.query.start,"onUpdate:modelValue":n[1]||(n[1]=t=>l.query.start=t),placeholder:"\u8D77\u59CB\u7F16\u53F7"},null,8,["modelValue"])]),_:1}),e(i,{span:5},{default:o(()=>[e(g,{size:"small",modelValue:l.query.limit,"onUpdate:modelValue":n[2]||(n[2]=t=>l.query.limit=t),placeholder:"\u6BCF\u9875\u663E\u793A"},null,8,["modelValue"])]),_:1}),e(i,{span:3},{default:o(()=>[e(h,{size:"small",type:"primary",icon:"Search",onClick:l.handleSearch},{default:o(()=>[c("\u641C\u7D22")]),_:1},8,["onClick"])]),_:1})]),_:1})]),e(r,{data:l.filterTableData,height:"800",stripe:"",size:"small","highlight-current-row":"",class:"table",ref:"multipleTable","default-sort":{prop:"server_mtime",order:"descending"},"header-cell-class-name":"table-header",lazy:"","row-key":"fs_id",load:l.load,"tree-props":{hasChildren:"isdir"},onSelectionChange:l.handleSelectionChange},{default:o(()=>[e(s,{type:"selection",width:"55"}),e(s,{"min-width":"300px",label:"\u6587\u4EF6\u540D",prop:"server_filename",sortable:""},{default:o(t=>[t.row.isdir?(B(),K(p,{key:0},{default:o(()=>[e(d)]),_:1})):P("",!0),c(" "+k(t.row.server_filename),1)]),_:1}),e(s,{width:"100px",label:"\u5927\u5C0F",prop:"size",sortable:""},{default:o(t=>[c(k(t.row.size>0?l.getfilesize(t.row.size):"\u6587\u4EF6\u5939"),1)]),_:1}),e(s,{"min-width":"150px",label:"\u4FEE\u6539\u65E5\u671F",prop:"server_mtime",sortable:""},{default:o(t=>[c(k(l.dayjs.unix(t.row.server_mtime).format("YYYY-MM-DD HH:mm:ss")),1)]),_:1})]),_:1},8,["data","load","onSelectionChange"])])])}var re=W(Q,[["render",ae],["__scopeId","data-v-cb45f2aa"]]);export{re as default};