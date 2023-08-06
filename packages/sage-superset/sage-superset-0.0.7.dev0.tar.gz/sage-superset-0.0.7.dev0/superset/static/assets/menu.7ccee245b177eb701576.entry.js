(()=>{"use strict";var e,t,a,r,n,d,i,o={53894:(e,t,a)=>{function r(e){return function(t){var a=t.dispatch,r=t.getState;return function(t){return function(n){return"function"==typeof n?n(a,r,e):t(n)}}}}a.d(t,{Z:()=>d});var n=r();n.withExtraArgument=r;const d=n},56481:(e,t,a)=>{var r=a(67294),n=a(90731),d=a(68135),i=a(23882),o=a(5872),c=a.n(o),l=a(23279),f=a.n(l),b=a(51995),s=a(11965),u=a(23525),m=a(82191),p=a(58593),h=a(73727),g=a(70163),v=a(29147),y=a(27600),Z=a(61988),x=a(70695),w=a(37703);const{SubMenu:$}=m.$t,_=b.iK.div`
  display: flex;
  align-items: center;

  & i {
    margin-right: ${({theme:e})=>2*e.gridUnit}px;
  }

  & a {
    display: block;
    width: 150px;
    word-wrap: break-word;
    text-decoration: none;
  }
`,k=b.iK.i`
  margin-top: 2px;
`;function S(e){const{locale:t,languages:a,...r}=e;return(0,s.tZ)($,c()({"aria-label":"Languages",title:(0,s.tZ)("div",{className:"f16"},(0,s.tZ)(k,{className:`flag ${a[t].flag}`})),icon:(0,s.tZ)(g.Z.TriangleDown,null)},r),Object.keys(a).map((e=>(0,s.tZ)(m.$t.Item,{key:e,style:{whiteSpace:"normal",height:"auto"}},(0,s.tZ)(_,{className:"f16"},(0,s.tZ)("i",{className:`flag ${a[e].flag}`}),(0,s.tZ)("a",{href:a[e].url},a[e].name))))))}const U=[{label:(0,Z.t)("Data"),icon:"fa-database",childs:[{icon:"fa-upload",label:(0,Z.t)("Upload a CSV"),name:"Upload a CSV",url:"/csvtodatabaseview/form"},{icon:"fa-upload",label:(0,Z.t)("Upload a Columnar File"),name:"Upload a Columnar file",url:"/columnartodatabaseview/form"},{icon:"fa-upload",label:(0,Z.t)("Upload Excel"),name:"Upload Excel",url:"/exceltodatabaseview/form"}]},{label:(0,Z.t)("SQL query"),url:"/superset/sqllab?new=true",icon:"fa-fw fa-search",perm:"can_sqllab",view:"Superset"},{label:(0,Z.t)("Chart"),url:"/chart/add",icon:"fa-fw fa-bar-chart",perm:"can_write",view:"Chart"},{label:(0,Z.t)("Dashboard"),url:"/dashboard/new",icon:"fa-fw fa-dashboard",perm:"can_write",view:"Dashboard"}],E=e=>s.iv`
  padding: ${1.5*e.gridUnit}px ${4*e.gridUnit}px
    ${4*e.gridUnit}px ${7*e.gridUnit}px;
  color: ${e.colors.grayscale.base};
  font-size: ${e.typography.sizes.xs}px;
  white-space: nowrap;
`,O=b.iK.div`
  color: ${({theme:e})=>e.colors.primary.dark1};
`,N=b.iK.div`
  display: flex;
  flex-direction: row;
  justify-content: ${({align:e})=>e};
  align-items: center;
  margin-right: ${({theme:e})=>e.gridUnit}px;
  .ant-menu-submenu-title > svg {
    top: ${({theme:e})=>5.25*e.gridUnit}px;
  }
`,j=b.iK.a`
  padding-right: ${({theme:e})=>e.gridUnit}px;
  padding-left: ${({theme:e})=>e.gridUnit}px;
`,{SubMenu:C}=m.$t,I=({align:e,settings:t,navbarRight:a,isFrontendRoute:n})=>{const{roles:d}=(0,w.v9)((e=>e.user)),{CSV_EXTENSIONS:i,COLUMNAR_EXTENSIONS:o,EXCEL_EXTENSIONS:c}=(0,w.v9)((e=>e.common.conf)),l={"Upload a CSV":i,"Upload a Columnar file":o,"Upload Excel":c},f=(0,x.Z)("can_sqllab","Superset",d),b=(0,x.Z)("can_write","Dashboard",d),u=(0,x.Z)("can_write","Chart",d),p=f||u||b,v=e=>(0,s.tZ)(r.Fragment,null,(0,s.tZ)("i",{className:`fa ${e.icon}`}),e.label);return(0,s.tZ)(N,{align:e},(0,s.tZ)(m.$t,{mode:"horizontal"},!a.user_is_anonymous&&p&&(0,s.tZ)(C,{title:(0,s.tZ)(O,{className:"fa fa-plus"}),icon:(0,s.tZ)(g.Z.TriangleDown,null)},U.map((e=>e.childs?(0,s.tZ)(C,{key:"sub2",className:"data-menu",title:v(e)},e.childs.map((e=>"string"!=typeof e&&e.name&&!0===l[e.name]?(0,s.tZ)(m.$t.Item,{key:e.name},(0,s.tZ)("a",{href:e.url}," ",e.label," ")):null))):(0,x.Z)(e.perm,e.view,d)&&(0,s.tZ)(m.$t.Item,{key:e.label},(0,s.tZ)("a",{href:e.url},(0,s.tZ)("i",{className:`fa ${e.icon}`})," ",e.label))))),(0,s.tZ)(C,{title:(0,Z.t)("Settings"),icon:(0,s.tZ)(g.Z.TriangleDown,{iconSize:"xl"})},t.map(((e,a)=>{var r;return[(0,s.tZ)(m.$t.ItemGroup,{key:`${e.label}`,title:e.label},null==(r=e.childs)?void 0:r.map((e=>"string"!=typeof e?(0,s.tZ)(m.$t.Item,{key:`${e.label}`},n(e.url)?(0,s.tZ)(h.rU,{to:e.url||""},e.label):(0,s.tZ)("a",{href:e.url},e.label)):null))),a<t.length-1&&(0,s.tZ)(m.$t.Divider,null)]})),!a.user_is_anonymous&&[(0,s.tZ)(m.$t.Divider,{key:"user-divider"}),(0,s.tZ)(m.$t.ItemGroup,{key:"user-section",title:(0,Z.t)("User")},a.user_profile_url&&(0,s.tZ)(m.$t.Item,{key:"profile"},(0,s.tZ)("a",{href:a.user_profile_url},(0,Z.t)("Profile"))),a.user_info_url&&(0,s.tZ)(m.$t.Item,{key:"info"},(0,s.tZ)("a",{href:a.user_info_url},(0,Z.t)("Info"))),(0,s.tZ)(m.$t.Item,{key:"logout"},(0,s.tZ)("a",{href:a.user_logout_url},(0,Z.t)("Logout"))))],(a.version_string||a.version_sha)&&[(0,s.tZ)(m.$t.Divider,{key:"version-info-divider"}),(0,s.tZ)(m.$t.ItemGroup,{key:"about-section",title:(0,Z.t)("About")},(0,s.tZ)("div",{className:"about-section"},a.show_watermark&&(0,s.tZ)("div",{css:E},(0,Z.t)("Powered by Apache Superset")),a.version_string&&(0,s.tZ)("div",{css:E},"Version: ",a.version_string),a.version_sha&&(0,s.tZ)("div",{css:E},"SHA: ",a.version_sha),a.build_number&&(0,s.tZ)("div",{css:E},"Build: ",a.build_number)))]),a.show_language_picker&&(0,s.tZ)(S,{locale:a.locale,languages:a.languages})),a.documentation_url&&(0,s.tZ)(j,{href:a.documentation_url,target:"_blank",rel:"noreferrer",title:(0,Z.t)("Documentation")},(0,s.tZ)("i",{className:"fa fa-question"})," "),a.bug_report_url&&(0,s.tZ)(j,{href:a.bug_report_url,target:"_blank",rel:"noreferrer",title:(0,Z.t)("Report a bug")},(0,s.tZ)("i",{className:"fa fa-bug"})),a.user_is_anonymous&&(0,s.tZ)(j,{href:a.user_login_url},(0,s.tZ)("i",{className:"fa fa-fw fa-sign-in"}),(0,Z.t)("Login")))},T=b.iK.header`
  background-color: white;
  margin-bottom: 2px;
  &:nth-last-of-type(2) nav {
    margin-bottom: 2px;
  }

  .caret {
    display: none;
  }
  .navbar-brand {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .navbar-brand-text {
    border-left: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-right: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    height: 100%;
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    padding-left: ${({theme:e})=>4*e.gridUnit}px;
    padding-right: ${({theme:e})=>4*e.gridUnit}px;
    margin-right: ${({theme:e})=>6*e.gridUnit}px;
    font-size: ${({theme:e})=>4*e.gridUnit}px;
    float: left;
    display: flex;
    flex-direction: column;
    justify-content: center;

    span {
      max-width: ${({theme:e})=>58*e.gridUnit}px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    @media (max-width: 1127px) {
      display: none;
    }
  }
  .main-nav .ant-menu-submenu-title > svg {
    top: ${({theme:e})=>5.25*e.gridUnit}px;
  }
  @media (max-width: 767px) {
    .navbar-brand {
      float: none;
    }
  }
  .ant-menu-horizontal .ant-menu-item {
    height: 100%;
    line-height: inherit;
  }
  .ant-menu > .ant-menu-item > a {
    padding: ${({theme:e})=>4*e.gridUnit}px;
  }
  @media (max-width: 767px) {
    .ant-menu-item {
      padding: 0 ${({theme:e})=>6*e.gridUnit}px 0
        ${({theme:e})=>3*e.gridUnit}px !important;
    }
    .ant-menu > .ant-menu-item > a {
      padding: 0px;
    }
    .main-nav .ant-menu-submenu-title > svg:nth-child(1) {
      display: none;
    }
    .ant-menu-item-active > a {
      &:hover {
        color: ${({theme:e})=>e.colors.primary.base} !important;
        background-color: transparent !important;
      }
    }
  }

  .ant-menu-item a {
    &:hover {
      color: ${({theme:e})=>e.colors.grayscale.dark1};
      background-color: ${({theme:e})=>e.colors.primary.light5};
      border-bottom: none;
      margin: 0;
      &:after {
        opacity: 1;
        width: 100%;
      }
    }
  }
`,D=e=>s.iv`
  .ant-menu-submenu.ant-menu-submenu-popup.ant-menu.ant-menu-light.ant-menu-submenu-placement-bottomLeft {
    border-radius: 0px;
  }
  .ant-menu-submenu.ant-menu-submenu-popup.ant-menu.ant-menu-light {
    border-radius: 0px;
  }
  .ant-menu-vertical > .ant-menu-submenu.data-menu > .ant-menu-submenu-title {
    height: 28px;
    i {
      padding-right: ${2*e.gridUnit}px;
      margin-left: ${1.75*e.gridUnit}px;
    }
  }
`,{SubMenu:A}=m.$t,{useBreakpoint:F}=m.rj;function L({data:{menu:e,brand:t,navbar_right:a,settings:n},isFrontendRoute:d=(()=>!1)}){const[i,o]=(0,r.useState)("horizontal"),c=F(),l=(0,v.fG)(),Z=(0,b.Fg)();return(0,r.useEffect)((()=>{function e(){window.innerWidth<=767?o("inline"):o("horizontal")}e();const t=f()((()=>e()),10);return window.addEventListener("resize",t),()=>window.removeEventListener("resize",t)}),[]),(0,u.e)(y.KD.standalone)||l.hideNav?(0,s.tZ)(r.Fragment,null):(0,s.tZ)(T,{className:"top",id:"main-menu",role:"navigation"},(0,s.tZ)(s.xB,{styles:D(Z)}),(0,s.tZ)(m.X2,null,(0,s.tZ)(m.JX,{md:16,xs:24},(0,s.tZ)(p.u,{id:"brand-tooltip",placement:"bottomLeft",title:t.tooltip,arrowPointAtCenter:!0},(0,s.tZ)("a",{className:"navbar-brand",href:t.path},(0,s.tZ)("img",{width:t.width,src:t.icon,alt:t.alt}))),t.text&&(0,s.tZ)("div",{className:"navbar-brand-text"},(0,s.tZ)("span",null,t.text)),(0,s.tZ)(m.$t,{mode:i,className:"main-nav"},e.map((e=>{var t;return(({label:e,childs:t,url:a,index:n,isFrontendRoute:d})=>a&&d?(0,s.tZ)(m.$t.Item,{key:e,role:"presentation"},(0,s.tZ)(h.rU,{role:"button",to:a},e)):a?(0,s.tZ)(m.$t.Item,{key:e},(0,s.tZ)("a",{href:a},e)):(0,s.tZ)(A,{key:n,title:e,icon:"inline"===i?(0,s.tZ)(r.Fragment,null):(0,s.tZ)(g.Z.TriangleDown,null)},null==t?void 0:t.map(((e,t)=>"string"==typeof e&&"-"===e?(0,s.tZ)(m.$t.Divider,{key:`$${t}`}):"string"!=typeof e?(0,s.tZ)(m.$t.Item,{key:`${e.label}`},e.isFrontendRoute?(0,s.tZ)(h.rU,{to:e.url||""},e.label):(0,s.tZ)("a",{href:e.url},e.label)):null))))({...e,isFrontendRoute:d(e.url),childs:null==(t=e.childs)?void 0:t.map((e=>"string"==typeof e?e:{...e,isFrontendRoute:d(e.url)}))})})))),(0,s.tZ)(m.JX,{md:8,xs:24},(0,s.tZ)(I,{align:c.md?"flex-end":"flex-start",settings:n,navbarRight:a,isFrontendRoute:d}))))}var P,z=a(85156),M=a(89474);const R=document.getElementById("app"),B=null!=(P=null==R?void 0:R.getAttribute("data-bootstrap"))?P:"{}",K={...JSON.parse(B).common.menu_data},q=(0,i.Z)({key:"menu"}),X=(0,s.tZ)(d.C,{value:q},(0,s.tZ)(d.a,{theme:z.r},(0,s.tZ)(w.zt,{store:M.h},(0,s.tZ)((function({data:e,...t}){const a={...e},r={Security:!0,Manage:!0},n=[],d=[];return a.menu.forEach((e=>{if(!e)return;const t=[],a={...e};e.childs&&(e.childs.forEach((e=>{("string"==typeof e||e.label)&&t.push(e)})),a.childs=t),r.hasOwnProperty(e.name)?d.push(a):n.push(a)})),a.menu=n,a.settings=d,(0,s.tZ)(L,c()({data:a},t))}),{data:K}))));n.render(X,document.getElementById("app-menu"))}},c={};function l(e){var t=c[e];if(void 0!==t)return t.exports;var a=c[e]={id:e,loaded:!1,exports:{}};return o[e].call(a.exports,a,a.exports,l),a.loaded=!0,a.exports}l.m=o,l.amdD=function(){throw new Error("define cannot be used indirect")},l.amdO={},e=[],l.O=(t,a,r,n)=>{if(!a){var d=1/0;for(f=0;f<e.length;f++){for(var[a,r,n]=e[f],i=!0,o=0;o<a.length;o++)(!1&n||d>=n)&&Object.keys(l.O).every((e=>l.O[e](a[o])))?a.splice(o--,1):(i=!1,n<d&&(d=n));if(i){e.splice(f--,1);var c=r();void 0!==c&&(t=c)}}return t}n=n||0;for(var f=e.length;f>0&&e[f-1][2]>n;f--)e[f]=e[f-1];e[f]=[a,r,n]},l.n=e=>{var t=e&&e.__esModule?()=>e.default:()=>e;return l.d(t,{a:t}),t},a=Object.getPrototypeOf?e=>Object.getPrototypeOf(e):e=>e.__proto__,l.t=function(e,r){if(1&r&&(e=this(e)),8&r)return e;if("object"==typeof e&&e){if(4&r&&e.__esModule)return e;if(16&r&&"function"==typeof e.then)return e}var n=Object.create(null);l.r(n);var d={};t=t||[null,a({}),a([]),a(a)];for(var i=2&r&&e;"object"==typeof i&&!~t.indexOf(i);i=a(i))Object.getOwnPropertyNames(i).forEach((t=>d[t]=()=>e[t]));return d.default=()=>e,l.d(n,d),n},l.d=(e,t)=>{for(var a in t)l.o(t,a)&&!l.o(e,a)&&Object.defineProperty(e,a,{enumerable:!0,get:t[a]})},l.f={},l.e=e=>Promise.all(Object.keys(l.f).reduce(((t,a)=>(l.f[a](e,t),t)),[])),l.u=e=>2087===e?"2087.c57929e84c0056c13f96.entry.js":674===e?"674.20f750c92a3b868845b5.entry.js":2671===e?"2671.6ce397f443a3ef54b565.entry.js":{57:"3eef258f00447ab2ba56",112:"881dd2510f19ed31e172",158:"488593bc94ab7caa58e0",177:"4b03c272091be7836683",183:"3f0101a74920ebdf5721",215:"abe0f2a4a3f69594f00c",310:"77d6d4c65a4250a67f54",312:"ba5d653bdbc1bcc11798",336:"f4bdd4f606d6d7592f7e",363:"210381fc4c2bbae6d099",435:"d7a82346f632ffe4f5d6",440:"515662946aea2cdc4413",597:"20b87c137727ff9aaf87",600:"044558ce92babe1fa2db",826:"0e2f19bbb57b5a8aff83",992:"d71578d87db841083c93",999:"ce189cf323818358d600",1075:"2572ea51a4adfc4ff9a4",1174:"1033573182d374214540",1185:"63e33afadbeb6e51d8dd",1256:"035f322d4ce964f73de1",1258:"6381160c0229525565fd",1263:"cfe95e8e20298feb874e",1293:"14b3a7ee4cc17de5c441",1351:"2eb1a9ba1648eb7a8193",1398:"0c371615e0996614785c",1493:"0c0664678b66d74ba38f",1568:"b2bb81324e29ed5bce61",1605:"d6a140bf5e3bef201212",1899:"e1eb313fc03e90fa0d70",2079:"579cd7268aa39862c290",2089:"13db7039a066b543f45a",2105:"02df5ff9f97c181f9de4",2264:"5a90b87bf6c82cddd60f",2267:"58a5465f711b4c6b0f0c",2403:"ff967bce10197be4d6e0",2439:"92ff10820007284a3594",2646:"3dcaf7b2edc6b26550ba",2651:"ca3e1b94c1afcbd6c921",2698:"e7b7a6eeb3966de7d0c1",2713:"a68c27cd1e12e64ffed4",2797:"5db241c8af5a71f0f30d",2983:"8afbd45ac5fc6d8b4b6d",3141:"494a0ca0a1bb39f625bd",3240:"e7218edd46dedf7e1dda",3265:"1671e36958a7bf6f4cfc",3325:"9295baeedc623870f610",3544:"0fb4e4d961165cd76e18",3558:"e2f6e711a397fa768c21",3567:"d77d0432d12254aeeded",3606:"0b65905a659b39cd6909",3749:"9d45482bb7e08b4be181",3871:"b94982d813b3a1874fe0",3955:"afc2c2846692569a5718",3985:"f293395f2172b1317b51",4139:"285945130a72bfc46e1d",4266:"5b30930400b0988390e0",4273:"7ddbd55189a7899df93c",4458:"4309988c3c4fa37de107",4474:"b598fc6c061ecd9e6b0d",4579:"16ca3c26d224ec2bea51",4625:"51252df40a568e9858e9",4662:"b32dd6447e5fae270c83",4667:"48c3843ffce6d71edad4",4732:"40416b4ab4e61de326ae",4757:"93d740911bd493adf140",4758:"139bfe0e5a3d55b967f5",4794:"604a01412367c61f28d1",4797:"ec310aed295dd6ac6d3e",4810:"c9e88f8bb26309aea9a3",4817:"c6d5f79ba80cd01dc865",4832:"ef14aea5648058059b49",4851:"ddfa921c0ae9aa3cc18b",4972:"c5b4433dc989f0536983",4981:"a591e398113e3a68af10",5094:"d5af7ef50f8a584f4a24",5201:"3ec18a3a291224aa9108",5224:"c47e9d538010833596c1",5226:"6827078f00442327de34",5249:"666b274dce41432ba44f",5281:"bee09c165592668d3f89",5330:"599272faeb108b72e7f9",5335:"8aa0878ebf5d4ad6ce59",5350:"074a558227a6662abcb5",5359:"2b8c50de5d5c4b38aca0",5367:"21ae5e3e001039f857b3",5507:"f70d497b4e7632b6cc22",5580:"24915749e40e9d761a9c",5592:"e87311d9b096af643f33",5641:"38809faee0024a508b21",5707:"147d8ca4332836cd578d",5771:"1052f585ff4ae106bee8",5777:"554d568382eb31588d65",5802:"6cc12bb8302843f1d8f2",5816:"280673beea0b5f2fd1e1",5832:"0c735281dd62de64b370",5838:"dbba442e12c14d0a2a2e",5962:"72dc9794359fb77a60d2",5972:"19c7fc52abf01d211d54",5998:"1ee3b4651923335492d5",6061:"55bf4311a87981b3e733",6126:"91fa0738674c868ec8cc",6150:"dc68c567fc3c38729c6e",6167:"d6258818427262c45fa8",6207:"6910f3c4f0be2cfcd7f9",6254:"fb638befd53ef04822fc",6303:"ad52f9efd303183abf5e",6371:"83c9e45ceb3fbb5ac155",6377:"0cf4434a790b254858ca",6420:"c893ff2534f9ec304fc8",6447:"ae65f54f868cf08677c1",6486:"40ed2ed019bff637c535",6507:"45af87d3e964f08e8a6b",6668:"55647a5d1bc9e3c671d6",6682:"9becee958a13c31f4d51",6758:"6fcf8c53e0a66334e5b5",6819:"e5d97b6c04bdd4635620",6883:"520bd0ef8bbe299a89fd",6977:"d2b3c9ce6ad0030f20e0",6981:"a398d4d79a48e5730885",7183:"5a6c8f84f8386ea3c3ed",7249:"4073992e83966234ebec",7405:"108895750399ba59f40d",7460:"6a739700fefd3a4fbac2",7584:"f1a7f6c3be667fceb4de",7610:"fe88065240ff7a6e5504",7654:"1cc0055d2d390c30d171",7716:"26ccebd94ddb1fb178f8",7760:"df6139586bc8db9f4686",7803:"fa5606e48db6b49a7a94",7832:"741031b8b31f62237cd5",7850:"daed96c9f6d33ebc1f7c",7922:"5d8ea477355f17a5b790",8312:"65a7d4d9a4760d7a5210",8349:"7aa90fbe18ad73a1b95a",8398:"602f4d50559d187c1db8",8425:"d4ab2b8d82b74d62566e",8463:"44ea1565bba7d3f2c8f7",8616:"dee76665d36ed3374636",8682:"689daa7df9dd2c6fa4fd",8695:"01d9bc6edddbf539b1b7",8750:"dc92e0e945b83ec1e05f",8883:"a09378804d20733f3763",8970:"cc02d84919fe9ecd9cde",9013:"a4b833b1258c7c9a94fd",9052:"02f43b9abb68bfc5f39c",9109:"276f36aed8996da1df63",9305:"34d5c67b5c79995f8a60",9325:"1defe50332e08632f07f",9393:"442f478da05ba19070c4",9510:"c5c3e89e58541aa7825b",9558:"d2eaa19757d176a93ab7",9767:"ad438ca70361b5e69126",9794:"c13a738c3f6b2ba76ca9",9811:"21a7c18f6923c4c737b9"}[e]+".chunk.js",l.miniCssF=e=>e+".ca3e1b94c1afcbd6c921.chunk.css",l.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),l.hmd=e=>((e=Object.create(e)).children||(e.children=[]),Object.defineProperty(e,"exports",{enumerable:!0,set:()=>{throw new Error("ES Modules may not assign module.exports or exports.*, Use ESM export syntax, instead: "+e.id)}}),e),l.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),r={},n="superset:",l.l=(e,t,a,d)=>{if(r[e])r[e].push(t);else{var i,o;if(void 0!==a)for(var c=document.getElementsByTagName("script"),f=0;f<c.length;f++){var b=c[f];if(b.getAttribute("src")==e||b.getAttribute("data-webpack")==n+a){i=b;break}}i||(o=!0,(i=document.createElement("script")).charset="utf-8",i.timeout=120,l.nc&&i.setAttribute("nonce",l.nc),i.setAttribute("data-webpack",n+a),i.src=e),r[e]=[t];var s=(t,a)=>{i.onerror=i.onload=null,clearTimeout(u);var n=r[e];if(delete r[e],i.parentNode&&i.parentNode.removeChild(i),n&&n.forEach((e=>e(a))),t)return t(a)},u=setTimeout(s.bind(null,void 0,{type:"timeout",target:i}),12e4);i.onerror=s.bind(null,i.onerror),i.onload=s.bind(null,i.onload),o&&document.head.appendChild(i)}},l.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},l.nmd=e=>(e.paths=[],e.children||(e.children=[]),e),l.p="/static/assets/",d=e=>new Promise(((t,a)=>{var r=l.miniCssF(e),n=l.p+r;if(((e,t)=>{for(var a=document.getElementsByTagName("link"),r=0;r<a.length;r++){var n=(i=a[r]).getAttribute("data-href")||i.getAttribute("href");if("stylesheet"===i.rel&&(n===e||n===t))return i}var d=document.getElementsByTagName("style");for(r=0;r<d.length;r++){var i;if((n=(i=d[r]).getAttribute("data-href"))===e||n===t)return i}})(r,n))return t();((e,t,a,r)=>{var n=document.createElement("link");n.rel="stylesheet",n.type="text/css",n.onerror=n.onload=d=>{if(n.onerror=n.onload=null,"load"===d.type)a();else{var i=d&&("load"===d.type?"missing":d.type),o=d&&d.target&&d.target.href||t,c=new Error("Loading CSS chunk "+e+" failed.\n("+o+")");c.code="CSS_CHUNK_LOAD_FAILED",c.type=i,c.request=o,n.parentNode.removeChild(n),r(c)}},n.href=t,document.head.appendChild(n)})(e,n,t,a)})),i={8860:0,9783:0},l.f.miniCss=(e,t)=>{i[e]?t.push(i[e]):0!==i[e]&&{2651:1}[e]&&t.push(i[e]=d(e).then((()=>{i[e]=0}),(t=>{throw delete i[e],t})))},(()=>{var e={8860:0,9783:0};l.f.j=(t,a)=>{var r=l.o(e,t)?e[t]:void 0;if(0!==r)if(r)a.push(r[2]);else{var n=new Promise(((a,n)=>r=e[t]=[a,n]));a.push(r[2]=n);var d=l.p+l.u(t),i=new Error;l.l(d,(a=>{if(l.o(e,t)&&(0!==(r=e[t])&&(e[t]=void 0),r)){var n=a&&("load"===a.type?"missing":a.type),d=a&&a.target&&a.target.src;i.message="Loading chunk "+t+" failed.\n("+n+": "+d+")",i.name="ChunkLoadError",i.type=n,i.request=d,r[1](i)}}),"chunk-"+t,t)}},l.O.j=t=>0===e[t];var t=(t,a)=>{var r,n,[d,i,o]=a,c=0;if(d.some((t=>0!==e[t]))){for(r in i)l.o(i,r)&&(l.m[r]=i[r]);if(o)var f=o(l)}for(t&&t(a);c<d.length;c++)n=d[c],l.o(e,n)&&e[n]&&e[n][0](),e[d[c]]=0;return l.O(f)},a=globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[];a.forEach(t.bind(null,0)),a.push=t.bind(null,a.push.bind(a))})(),l.O(void 0,[1216,7550,4998,1514,8075,2357,9356,2717,741,5473,571,9525,6962,9083,7843,2619,2825,3375,3389,7620,9152],(()=>l(85156)));var f=l.O(void 0,[1216,7550,4998,1514,8075,2357,9356,2717,741,5473,571,9525,6962,9083,7843,2619,2825,3375,3389,7620,9152],(()=>l(56481)));f=l.O(f)})();