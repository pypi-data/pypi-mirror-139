"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[8289],{49576:(e,t,a)=>{a.d(t,{Z:()=>g});var l=a(67294),i=a(51995),r=a(70163),n=a(11965);const o=i.iK.label`
  cursor: pointer;
  display: inline-block;
  margin-bottom: 0;
`,s=(0,i.iK)(r.Z.CheckboxHalf)`
  color: ${({theme:e})=>e.colors.primary.base};
  cursor: pointer;
`,d=(0,i.iK)(r.Z.CheckboxOff)`
  color: ${({theme:e})=>e.colors.grayscale.base};
  cursor: pointer;
`,c=(0,i.iK)(r.Z.CheckboxOn)`
  color: ${({theme:e})=>e.colors.primary.base};
  cursor: pointer;
`,u=i.iK.input`
  &[type='checkbox'] {
    cursor: pointer;
    opacity: 0;
    position: absolute;
    left: 3px;
    margin: 0;
    top: 4px;
  }
`,p=i.iK.div`
  cursor: pointer;
  display: inline-block;
  position: relative;
`,g=(0,l.forwardRef)((({indeterminate:e,id:t,checked:a,onChange:i,title:r="",labelText:g=""},h)=>{const m=(0,l.useRef)(),f=h||m;return(0,l.useEffect)((()=>{f.current.indeterminate=e}),[f,e]),(0,n.tZ)(l.Fragment,null,(0,n.tZ)(p,null,e&&(0,n.tZ)(s,null),!e&&a&&(0,n.tZ)(c,null),!e&&!a&&(0,n.tZ)(d,null),(0,n.tZ)(u,{name:t,id:t,type:"checkbox",ref:f,checked:a,onChange:i})),(0,n.tZ)(o,{title:r,htmlFor:t},g))}))},98289:(e,t,a)=>{a.d(t,{p:()=>re,Z:()=>ie});var l,i,r=a(5872),n=a.n(r),o=a(51995),s=a(61988),d=a(67294),c=a(82191),u=a(29487);function p(){return p=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var a=arguments[t];for(var l in a)Object.prototype.hasOwnProperty.call(a,l)&&(e[l]=a[l])}return e},p.apply(this,arguments)}const g=function(e){return d.createElement("svg",p({width:119,height:76,viewBox:"0 0 119 76",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),l||(l=d.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M83.195 1.366L103 24v38a4 4 0 01-4 4H20a4 4 0 01-4-4V24L35.805 1.366A4 4 0 0138.815 0h41.37a4 4 0 013.01 1.366zM101 26v36a2 2 0 01-2 2H20a2 2 0 01-2-2V26h17.25A4.75 4.75 0 0140 30.75a6.75 6.75 0 006.75 6.75h25.5A6.75 6.75 0 0079 30.75 4.75 4.75 0 0183.75 26H101zm-.658-2L81.69 2.683A2 2 0 0080.185 2h-41.37a2 2 0 00-1.505.683L18.657 24H35.25A6.75 6.75 0 0142 30.75a4.75 4.75 0 004.75 4.75h25.5A4.75 4.75 0 0077 30.75 6.75 6.75 0 0183.75 24h16.592z",fill:"#D1D1D1"})),i||(i=d.createElement("path",{d:"M16 53.29C6.074 55.7 0 58.94 0 62.5 0 69.956 26.64 76 59.5 76S119 69.956 119 62.5c0-3.56-6.074-6.799-16-9.21V62a4 4 0 01-4 4H20a4 4 0 01-4-4v-8.71z",fill:"#F2F2F2"})))};var h=a(94184),m=a.n(h),f=a(35932),b=a(70163),v=a(49576),x=a(64158),y=a(97754),w=a(11965);const Z=o.iK.div`
  ${({theme:e,showThumbnails:t})=>`\n    display: grid;\n    grid-gap: ${12*e.gridUnit}px ${4*e.gridUnit}px;\n    grid-template-columns: repeat(auto-fit, 300px);\n    margin-top: ${-6*e.gridUnit}px;\n    padding: ${t?`${8*e.gridUnit+3}px ${9*e.gridUnit}px`:`${8*e.gridUnit+1}px ${9*e.gridUnit}px`};\n  `}
`,S=o.iK.div`
  border: 2px solid transparent;
  &.card-selected {
    border: 2px solid ${({theme:e})=>e.colors.primary.base};
  }
  &.bulk-select {
    cursor: pointer;
  }
`;function C({bulkSelectEnabled:e,loading:t,prepareRow:a,renderCard:l,rows:i,showThumbnails:r}){return l?(0,w.tZ)(Z,{showThumbnails:r},t&&0===i.length&&[...new Array(25)].map(((e,a)=>(0,w.tZ)("div",{key:a},l({loading:t})))),i.length>0&&i.map((i=>l?(a(i),(0,w.tZ)(S,{className:m()({"card-selected":e&&i.isSelected,"bulk-select":e}),key:i.id,onClick:t=>{return a=t,l=i.toggleRowSelected,void(e&&(a.preventDefault(),a.stopPropagation(),l()));var a,l},role:"none"},l({...i.original,loading:t}))):null))):null}var $=a(68135),k=a(18446),F=a.n(k),P=a(79521),I=a(35755),T=a(15926),M=a.n(T);const U={encode:e=>void 0===e?void 0:M().encode(e).replace(/%/g,"%25").replace(/&/g,"%26").replace(/\+/g,"%2B").replace(/#/g,"%23"),decode:e=>void 0===e||Array.isArray(e)?void 0:M().decode(e)};class R extends Error{constructor(...e){super(...e),this.name="ListViewError"}}function A(e,t){return e.map((({id:e,urlDisplay:a,operator:l})=>({id:e,urlDisplay:a,operator:l,value:t[a||e]})))}function _(e,t){const a=[],l={};return Object.keys(e).forEach((t=>{const i={id:t,value:e[t]};l[t]=i,a.push(i)})),t.forEach((e=>{const t=e.urlDisplay||e.id,a=l[t];a&&(a.operator=e.operator,a.id=e.id)})),a}var V=a(49238);const z=o.iK.div`
  width: ${200}px;
`,B=(0,o.iK)(b.Z.Search)`
  color: ${({theme:e})=>e.colors.grayscale.light1};
`,E=(0,o.iK)(c.oc)`
  border-radius: ${({theme:e})=>e.gridUnit}px;
`;function K({Header:e,name:t,initialValue:a,onSubmit:l}){const[i,r]=(0,d.useState)(a||""),n=()=>{i&&l(i.trim())};return(0,w.tZ)(z,null,(0,w.tZ)(V.lX,null,e),(0,w.tZ)(E,{allowClear:!0,placeholder:(0,s.t)("Type a value"),name:t,value:i,onChange:e=>{r(e.currentTarget.value),""===e.currentTarget.value&&l("")},onPressEnter:n,onBlur:n,prefix:(0,w.tZ)(B,{iconSize:"l"})}))}var O=a(4715);const N=o.iK.div`
  display: inline-flex;
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  align-items: center;
  width: ${200}px;
`,H=function({Header:e,name:t,fetchSelects:a,initialValue:l,onSelect:i,selects:r=[]}){const[n,o]=(0,d.useState)(l),c=(0,d.useMemo)((()=>async(e,t,l)=>{if(a){const i=await a(e,t,l);return{data:i.data,totalCount:i.totalCount}}return{data:[],totalCount:0}}),[a]);return(0,w.tZ)(N,null,(0,w.tZ)(O.P,{allowClear:!0,ariaLabel:"string"==typeof e?e:t||(0,s.t)("Filter"),labelInValue:!0,header:(0,w.tZ)(V.lX,null,e),onChange:e=>{i(e?{label:e.label,value:e.value}:void 0),o(e)},onClear:()=>{i(void 0),o(void 0)},options:a?c:r,placeholder:(0,s.t)("Select or type a value"),showSearch:!0,value:n}))};var D=a(30381),L=a.n(D),j=a(62276);const q=o.iK.div`
  display: inline-flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  width: 360px;
`;function G({Header:e,initialValue:t,onSubmit:a}){const[l,i]=(0,d.useState)(null!=t?t:null),r=(0,d.useMemo)((()=>!l||Array.isArray(l)&&!l.length?null:[L()(l[0]),L()(l[1])]),[l]);return(0,w.tZ)(q,null,(0,w.tZ)(V.lX,null,e),(0,w.tZ)(j.S,{showTime:!0,value:r,onChange:e=>{var t,l,r,n;if(!e)return i(null),void a([]);const o=[null!=(t=null==(l=e[0])?void 0:l.valueOf())?t:0,null!=(r=null==(n=e[1])?void 0:n.valueOf())?r:0];i(o),a(o)}}))}const W=(0,$.b)((function({filters:e,internalFilters:t=[],updateFilterValue:a}){return(0,w.tZ)(d.Fragment,null,e.map((({Header:e,fetchSelects:l,id:i,input:r,paginate:n,selects:o},s)=>{const d=t[s]&&t[s].value;return"select"===r?(0,w.tZ)(H,{Header:e,fetchSelects:l,initialValue:d,key:i,name:i,onSelect:e=>a(s,e),paginate:n,selects:o}):"search"===r&&"string"==typeof e?(0,w.tZ)(K,{Header:e,initialValue:d,key:i,name:i,onSubmit:e=>a(s,e)}):"datetime_range"===r?(0,w.tZ)(G,{Header:e,initialValue:d,key:i,name:i,onSubmit:e=>a(s,e)}):null})))})),X=o.iK.div`
  display: inline-flex;
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  align-items: center;
  text-align: left;
  width: ${200}px;
`,Y=({initialSort:e,onChange:t,options:a,pageIndex:l,pageSize:i})=>{const r=e&&a.find((({id:t})=>t===e[0].id))||a[0],[n,o]=(0,d.useState)({label:r.label,value:r.value}),c=(0,d.useMemo)((()=>a.map((e=>({label:e.label,value:e.value})))),[a]);return(0,w.tZ)(X,null,(0,w.tZ)(O.P,{ariaLabel:(0,s.t)("Sort"),header:(0,w.tZ)(V.lX,null,(0,s.t)("Sort")),labelInValue:!0,onChange:e=>(e=>{o(e);const r=a.find((({value:t})=>t===e.value));if(r){const e=[{id:r.id,desc:r.desc}];t({pageIndex:l,pageSize:i,sortBy:e,filters:[]})}})(e),options:c,showSearch:!0,value:n}))},J=o.iK.div`
  text-align: center;

  .superset-list-view {
    text-align: left;
    border-radius: 4px 0;
    margin: 0 ${({theme:e})=>4*e.gridUnit}px;

    .header {
      display: flex;
      padding-bottom: ${({theme:e})=>4*e.gridUnit}px;

      & .controls {
        display: flex;
        flex-wrap: wrap;
        column-gap: ${({theme:e})=>6*e.gridUnit}px;
        row-gap: ${({theme:e})=>4*e.gridUnit}px;
      }
    }

    .body.empty table {
      margin-bottom: 0;
    }

    .body {
      overflow-x: auto;
    }

    .ant-empty {
      .ant-empty-image {
        height: auto;
      }
    }
  }

  .pagination-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-bottom: ${({theme:e})=>4*e.gridUnit}px;
  }

  .row-count-container {
    margin-top: ${({theme:e})=>2*e.gridUnit}px;
    color: ${({theme:e})=>e.colors.grayscale.base};
  }
`,Q=(0,o.iK)(u.Z)`
  border-radius: 0;
  margin-bottom: 0;
  color: #3d3d3d;
  background-color: ${({theme:e})=>e.colors.primary.light4};

  .selectedCopy {
    display: inline-block;
    padding: ${({theme:e})=>2*e.gridUnit}px 0;
  }

  .deselect-all {
    color: #1985a0;
    margin-left: ${({theme:e})=>4*e.gridUnit}px;
  }

  .divider {
    margin: ${({theme:{gridUnit:e}})=>`${2*-e}px 0 ${2*-e}px ${4*e}px`};
    width: 1px;
    height: ${({theme:e})=>8*e.gridUnit}px;
    box-shadow: inset -1px 0px 0px #dadada;
    display: inline-flex;
    vertical-align: middle;
    position: relative;
  }

  .ant-alert-close-icon {
    margin-top: ${({theme:e})=>1.5*e.gridUnit}px;
  }
`,ee={Cell:({row:e})=>(0,w.tZ)(v.Z,n()({},e.getToggleRowSelectedProps(),{id:e.id})),Header:({getToggleAllRowsSelectedProps:e})=>(0,w.tZ)(v.Z,n()({},e(),{id:"header-toggle-all"})),id:"selection",size:"sm"},te=o.iK.div`
  padding-right: ${({theme:e})=>4*e.gridUnit}px;
  margin-top: ${({theme:e})=>5*e.gridUnit+1}px;
  white-space: nowrap;
  display: inline-block;

  .toggle-button {
    display: inline-block;
    border-radius: ${({theme:e})=>e.gridUnit/2}px;
    padding: ${({theme:e})=>e.gridUnit}px;
    padding-bottom: ${({theme:e})=>.5*e.gridUnit}px;

    &:first-of-type {
      margin-right: ${({theme:e})=>2*e.gridUnit}px;
    }
  }

  .active {
    background-color: ${({theme:e})=>e.colors.grayscale.base};
    svg {
      color: ${({theme:e})=>e.colors.grayscale.light5};
    }
  }
`,ae=o.iK.div`
  padding: ${({theme:e})=>40*e.gridUnit}px 0;

  &.table {
    background: ${({theme:e})=>e.colors.grayscale.light5};
  }
`,le=({mode:e,setMode:t})=>(0,w.tZ)(te,null,(0,w.tZ)("div",{role:"button",tabIndex:0,onClick:e=>{e.currentTarget.blur(),t("card")},className:m()("toggle-button",{active:"card"===e})},(0,w.tZ)(b.Z.CardView,null)),(0,w.tZ)("div",{role:"button",tabIndex:0,onClick:e=>{e.currentTarget.blur(),t("table")},className:m()("toggle-button",{active:"table"===e})},(0,w.tZ)(b.Z.ListView,null))),ie=function({columns:e,data:t,count:a,pageSize:l,fetchData:i,loading:r,initialSort:n=[],className:o="",filters:u=[],bulkActions:p=[],bulkSelectEnabled:h=!1,disableBulkSelect:m=(()=>{}),renderBulkSelectCopy:b=(e=>(0,s.t)("%s Selected",e.length)),renderCard:v,showThumbnails:Z,cardSortSelectOptions:S,defaultViewMode:$="card",highlightRowId:k,emptyState:T={}}){const{getTableProps:M,getTableBodyProps:V,headerGroups:z,rows:B,prepareRow:E,pageCount:K=1,gotoPage:O,applyFilterValue:N,selectedFlatRows:H,toggleAllRowsSelected:D,setViewMode:L,state:{pageIndex:j,pageSize:q,internalFilters:G,viewMode:X}}=function({fetchData:e,columns:t,data:a,count:l,initialPageSize:i,initialFilters:r=[],initialSort:n=[],bulkSelectMode:o=!1,bulkSelectColumnConfig:s,renderCard:c=!1,defaultViewMode:u="card"}){const[p,g]=(0,I.Kx)({filters:U,pageIndex:I.yz,sortColumn:I.Zp,sortOrder:I.Zp,viewMode:I.Zp}),h=(0,d.useMemo)((()=>p.sortColumn&&p.sortOrder?[{id:p.sortColumn,desc:"desc"===p.sortOrder}]:n),[p.sortColumn,p.sortOrder]),m={filters:p.filters?_(p.filters,r):[],pageIndex:p.pageIndex||0,pageSize:i,sortBy:h},[f,b]=(0,d.useState)(p.viewMode||(c?u:"table")),v=(0,d.useMemo)((()=>{const e=t.map((e=>({...e,filter:"exact"})));return o?[s,...e]:e}),[o,t]),{getTableProps:x,getTableBodyProps:y,headerGroups:w,rows:Z,prepareRow:S,canPreviousPage:C,canNextPage:$,pageCount:k,gotoPage:T,setAllFilters:M,selectedFlatRows:R,toggleAllRowsSelected:V,state:{pageIndex:z,pageSize:B,sortBy:E,filters:K}}=(0,P.useTable)({columns:v,count:l,data:a,disableFilters:!0,disableSortRemove:!0,initialState:m,manualFilters:!0,manualPagination:!0,manualSortBy:!0,autoResetFilters:!1,pageCount:Math.ceil(l/i)},P.useFilters,P.useSortBy,P.usePagination,P.useRowState,P.useRowSelect),[O,N]=(0,d.useState)(p.filters&&r.length?A(r,p.filters):[]);return(0,d.useEffect)((()=>{r.length&&N(A(r,p.filters?p.filters:{}))}),[r]),(0,d.useEffect)((()=>{const t={};O.forEach((e=>{if(void 0!==e.value&&("string"!=typeof e.value||e.value.length>0)){const a=e.urlDisplay||e.id;t[a]=e.value}}));const a={filters:Object.keys(t).length?t:void 0,pageIndex:z};E[0]&&(a.sortColumn=E[0].id,a.sortOrder=E[0].desc?"desc":"asc"),c&&(a.viewMode=f);const l=void 0!==p.pageIndex&&a.pageIndex!==p.pageIndex?"push":"replace";g(a,l),e({pageIndex:z,pageSize:B,sortBy:E,filters:K})}),[e,z,B,E,K]),(0,d.useEffect)((()=>{F()(m.pageIndex,z)||T(m.pageIndex)}),[p]),{canNextPage:$,canPreviousPage:C,getTableBodyProps:y,getTableProps:x,gotoPage:T,headerGroups:w,pageCount:k,prepareRow:S,rows:Z,selectedFlatRows:R,setAllFilters:M,state:{pageIndex:z,pageSize:B,sortBy:E,filters:K,internalFilters:O,viewMode:f},toggleAllRowsSelected:V,applyFilterValue:(e,t)=>{N((a=>{if(a[e].value===t)return a;const l={...a[e],value:t},i=function(e,t,a){const l=e.find(((e,a)=>t===a));return[...e.slice(0,t),{...l,...a},...e.slice(t+1)]}(a,e,l);return M(i.filter((e=>!(void 0===e.value||Array.isArray(e.value)&&!e.value.length))).map((({value:e,operator:t,id:a})=>"between"===t&&Array.isArray(e)?[{value:e[0],operator:"gt",id:a},{value:e[1],operator:"lt",id:a}]:{value:e,operator:t,id:a})).flat()),T(0),i}))},setViewMode:b}}({bulkSelectColumnConfig:ee,bulkSelectMode:h&&Boolean(p.length),columns:e,count:a,data:t,fetchData:i,initialPageSize:l,initialSort:n,initialFilters:u,renderCard:Boolean(v),defaultViewMode:$}),te=Boolean(u.length);if(te){const t=e.reduce(((e,t)=>({...e,[t.id||t.accessor]:!0})),{});u.forEach((e=>{if(!t[e.id])throw new R(`Invalid filter config, ${e.id} is not present in columns`)}))}const ie=Boolean(v);return(0,d.useEffect)((()=>{h||D(!1)}),[h,D]),(0,w.tZ)(J,null,(0,w.tZ)("div",{className:`superset-list-view ${o}`},(0,w.tZ)("div",{className:"header"},ie&&(0,w.tZ)(le,{mode:X,setMode:L}),(0,w.tZ)("div",{className:"controls"},te&&(0,w.tZ)(W,{filters:u,internalFilters:G,updateFilterValue:N}),"card"===X&&S&&(0,w.tZ)(Y,{initialSort:n,onChange:i,options:S,pageIndex:j,pageSize:q}))),(0,w.tZ)("div",{className:"body "+(0===B.length?"empty":"")},h&&(0,w.tZ)(Q,{type:"info",closable:!0,showIcon:!1,onClose:m,message:(0,w.tZ)(d.Fragment,null,(0,w.tZ)("div",{className:"selectedCopy"},b(H)),Boolean(H.length)&&(0,w.tZ)(d.Fragment,null,(0,w.tZ)("span",{role:"button",tabIndex:0,className:"deselect-all",onClick:()=>D(!1)},(0,s.t)("Deselect all")),(0,w.tZ)("div",{className:"divider"}),p.map((e=>(0,w.tZ)(f.Z,{key:e.key,buttonStyle:e.type,cta:!0,onClick:()=>e.onSelect(H.map((e=>e.original)))},e.name)))))}),"card"===X&&(0,w.tZ)(C,{bulkSelectEnabled:h,prepareRow:E,renderCard:v,rows:B,loading:r,showThumbnails:Z}),"table"===X&&(0,w.tZ)(y.Z,{getTableProps:M,getTableBodyProps:V,prepareRow:E,headerGroups:z,rows:B,columns:e,loading:r,highlightRowId:k}),!r&&0===B.length&&(0,w.tZ)(ae,{className:X},(0,w.tZ)(c.HY,{image:(0,w.tZ)(g,null),description:T.message||(0,s.t)("No Data")},T.slot||null)))),B.length>0&&(0,w.tZ)("div",{className:"pagination-container"},(0,w.tZ)(x.Z,{totalPages:K||0,currentPage:K?j+1:0,onChange:e=>O(e-1),hideFirstAndLastPageLinks:!0}),(0,w.tZ)("div",{className:"row-count-container"},!r&&(0,s.t)("%s-%s of %s",q*j+(B.length&&1),q*j+B.length,a))))};var re;!function(e){e.startsWith="sw",e.endsWith="ew",e.contains="ct",e.equals="eq",e.notStartsWith="nsw",e.notEndsWith="new",e.notContains="nct",e.notEquals="neq",e.greaterThan="gt",e.lessThan="lt",e.relationManyMany="rel_m_m",e.relationOneMany="rel_o_m",e.titleOrSlug="title_or_slug",e.nameOrDescription="name_or_description",e.allText="all_text",e.chartAllText="chart_all_text",e.datasetIsNullOrEmpty="dataset_is_null_or_empty",e.between="between",e.dashboardIsFav="dashboard_is_favorite",e.chartIsFav="chart_is_favorite",e.chartIsCertified="chart_is_certified",e.dashboardIsCertified="dashboard_is_certified"}(re||(re={}))}}]);